"""
FastAPI 백엔드 서버
LS증권 WebSocket 데이터를 Frontend로 중계
Server-Driven 아키텍처: 서버 시작 시 자동으로 관심종목 데이터 수집

[v2.0] 프로그램 매매 연구 도구 통합
- UPH(통합프로그램매매종목별) 구독
- 비차익 매수 급증 이벤트 감지
- 가격 추적 및 수익률 분석
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
import asyncio
import json
import requests
import os
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from ls_websocket import LSWebSocketClient

# 연구 모듈 임포트
from research.research_db import ResearchDB, ProgramEvent
from research.event_detector import EventDetector, THRESHOLD_VALUE
from research.price_tracker import PriceTracker
from research.report_generator import ReportGenerator
from research.backtester import Backtester, create_backtester

# 환경변수 로드
load_dotenv()

# LS증권 API 설정
APP_KEY = os.getenv("LS_APP_KEY", "")
APP_SECRET = os.getenv("LS_APP_SECRET", "")
REST_URL = "https://openapi.ls-sec.co.kr:8080"

# 전역 변수
ls_client: LSWebSocketClient = None
connected_clients = set()
watchlist_codes = []

# 연구 도구 전역 변수
research_db: ResearchDB = None
event_detector: EventDetector = None
price_tracker: PriceTracker = None
report_generator: ReportGenerator = None
backtester: Backtester = None  # 백테스터
stock_names_cache: dict = {}  # 종목명 캐시


def load_stock_names_from_file() -> dict:
    """ls_stock_list.json 파일에서 종목명 로드 (API 호출 없이 즉시 조회 가능)"""
    possible_paths = [
        "ls_stock_list.json",
        "backend/ls_stock_list.json",
        os.path.join(os.path.dirname(__file__), "ls_stock_list.json")
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    stock_list = json.load(f)
                    # 단축코드 -> 종목명 매핑
                    stock_names = {}
                    for stock in stock_list:
                        code = stock.get("단축코드", "")
                        name = stock.get("종목명", "")
                        if code and name:
                            stock_names[code] = name
                    print(f"✅ 종목명 로드 완료: {len(stock_names)}개 종목 (from {path})")
                    return stock_names
            except Exception as e:
                print(f"⚠️ 종목명 파일 로드 실패 ({path}): {e}")

    print("⚠️ ls_stock_list.json 파일을 찾을 수 없습니다. API 호출로 대체됩니다.")
    return {}


def load_watchlist() -> list:
    """watchlist.json 파일에서 관심종목 리스트 로드"""
    # 여러 경로 시도
    possible_paths = [
        "watchlist.json",           # 현재 디렉토리 (backend 폴더에서 실행 시)
        "backend/watchlist.json",   # 프로젝트 루트에서 실행 시
        os.path.join(os.path.dirname(__file__), "watchlist.json")  # main.py 기준 상대 경로
    ]

    for path in possible_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                codes = data.get("codes", [])
                print(f"[WATCHLIST] Loaded {len(codes)} stocks from '{path}': {codes}")
                return codes
        except FileNotFoundError:
            continue
        except Exception as e:
            print(f"[ERROR] Failed to load watchlist from '{path}': {e}")
            continue

    print("[WARN] watchlist.json not found in any location, using default")
    return ["005930"]  # 기본값: 삼성전자


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan Event: 서버 시작/종료 시 실행"""
    global ls_client, watchlist_codes, stock_names_cache
    global research_db, event_detector, price_tracker, report_generator, backtester

    # ========== STARTUP ==========
    print("\n" + "="*60)
    print("🚀 SERVER STARTUP - Initializing LS WebSocket...")
    print("="*60)

    # 0. 종목명 파일에서 로드 (API 호출 절약)
    stock_names_cache = load_stock_names_from_file()

    # 1. 관심종목 로드
    watchlist_codes = load_watchlist()

    # 2. 연구 도구 초기화
    print("\n📊 Initializing Research Tools...")
    research_db = ResearchDB()
    await research_db.init_tables()
    # 마이그레이션: 추세/다이버전스 컬럼 추가
    await research_db.migrate_add_trend_columns()

    event_detector = EventDetector(threshold_value=THRESHOLD_VALUE)
    price_tracker = PriceTracker(db=research_db)

    # 종목명 조회 함수 설정
    def get_stock_name(code: str) -> str:
        return stock_names_cache.get(code, code)

    report_generator = ReportGenerator(db=research_db, stock_name_getter=get_stock_name)

    # 백테스터 초기화
    backtester = create_backtester(uph_data_dir="uph_raw_data")
    print("✅ Research Tools initialized (including Backtester)")

    # 3. LS증권 WebSocket 클라이언트 생성
    async def on_data(code: str, body: dict):
        """LS증권 체결 데이터를 모든 Frontend 클라이언트로 전송"""
        # 디버깅: 데이터 수신 확인 (너무 많아서 주석 처리)
        # price = body.get("price", "?")
        # volume = body.get("cvolume", "?")
        # print(f"[DATA] {code} | Price: {price} | Volume: {volume} | Clients: {len(connected_clients)}")

        # price_tracker 및 event_detector에 가격 업데이트
        try:
            price = int(body.get("price", 0))
            if price > 0:
                price_tracker.update_price(code, price)
                # 이벤트 감지기에도 가격 히스토리 전달 (다이버전스 분석용)
                event_detector.update_price(code, price)
        except (ValueError, TypeError):
            pass

        disconnected = set()
        for client in list(connected_clients):
            try:
                await client.send_json(body)  # body에 이미 "code" 필드 포함됨
            except Exception as e:
                print(f"[ERROR] Failed to send to client: {e}")
                disconnected.add(client)

        # 연결 해제된 클라이언트 제거
        for client in disconnected:
            connected_clients.discard(client)

    async def on_program_data(code: str, body: dict):
        """UPH 프로그램 매매 데이터 처리 - 이벤트 감지 및 기록 (v2.0)"""
        # 이벤트 감지
        result = event_detector.detect(code, body)

        if result.is_event:
            # 이벤트 발생!
            event_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 추세 정보 및 다이버전스 추출
            trend_info = result.details.get('trend_info', {})
            divergence_type = result.details.get('divergence_type')

            # v2.0 추가 정보 추출
            time_session = result.details.get('time_session', '정규')
            is_noisy_time = result.details.get('is_noisy_time', False)
            threshold_used = result.details.get('threshold_value', 0)
            threshold_type = result.details.get('threshold_type', 'fixed')
            order_book = result.details.get('order_book', {})

            # 종목명 조회
            stock_name = stock_names_cache.get(code, code)

            # 이벤트 유형 아이콘
            event_icon = "🟢" if result.event_type == 'buy_surge' else "🔴"
            event_label = "매수급증" if result.event_type == 'buy_surge' else "매도급증"

            # 로그 출력 (v2.0 상세 정보 포함)
            print(f"\n{'='*60}")
            print(f"{event_icon} [EVENT] {event_time} | {code} {stock_name} | {event_label}")
            print(f"   💰 Delta: {result.delta_vol:,}주 | Value: {result.estimated_value:,.0f}원 | Price: {result.current_price:,}원")
            print(f"   ⚙️  임계값: {threshold_used:,}원 ({threshold_type}) | 시간대: {time_session}{'⚠️' if is_noisy_time else ''}")

            # 다이버전스 정보
            if divergence_type and divergence_type != 'none':
                trend_5m = trend_info.get('price_trend_5m', '?')
                change_5m = trend_info.get('price_change_5m')
                change_str = f"{change_5m:+.2f}%" if change_5m else "?"
                div_icon = "📈" if divergence_type == 'bullish' else "📉"
                print(f"   {div_icon} 다이버전스: {divergence_type} (5분 추세: {trend_5m}, {change_str})")

            # 호가잔량 신호
            order_signal = order_book.get('signal_description', '없음')
            if order_signal and order_signal != '없음':
                print(f"   📊 호가잔량: {order_signal}")

            # 체결강도
            buy_intensity = order_book.get('buy_intensity')
            sell_intensity = order_book.get('sell_intensity')
            if buy_intensity or sell_intensity:
                intensity_str = []
                if buy_intensity:
                    intensity_str.append(f"매수강도:{buy_intensity:.2f}")
                if sell_intensity:
                    intensity_str.append(f"매도강도:{sell_intensity:.2f}")
                print(f"   📈 체결강도: {' | '.join(intensity_str)}")

            print(f"{'='*60}")

            # DB에 이벤트 기록 (v2.0 정보 포함)
            event = ProgramEvent(
                event_time=event_time,
                code=code,
                event_type=result.event_type,
                trigger_value=result.estimated_value,
                price_at_event=result.current_price,
                bshrem=result.details.get('bshrem', 0),
                bdhrem=result.details.get('bdhrem', 0),
                bshvolume=result.details.get('curr_bshvolume', 0),
                bdhvolume=result.details.get('bdhvolume', 0),
                tval=result.details.get('tval', 0),
                delta_vol=result.delta_vol,
                # 추세 정보 (다이버전스 분석용)
                price_1m_ago=trend_info.get('price_1m_ago'),
                price_3m_ago=trend_info.get('price_3m_ago'),
                price_5m_ago=trend_info.get('price_5m_ago'),
                price_change_1m=trend_info.get('price_change_1m'),
                price_change_3m=trend_info.get('price_change_3m'),
                price_change_5m=trend_info.get('price_change_5m'),
                price_trend_5m=trend_info.get('price_trend_5m'),
                price_high_5m=trend_info.get('price_high_5m'),
                price_low_5m=trend_info.get('price_low_5m'),
                divergence_type=divergence_type,
                # v2.0 추가 필드
                time_session=time_session,
                is_noisy_time=is_noisy_time,
                threshold_used=threshold_used,
                threshold_type=threshold_type,
                buy_intensity=buy_intensity,
                sell_intensity=sell_intensity,
                order_book_signal=order_signal
            )

            try:
                event_id = await research_db.insert_event(event)
                print(f"   📝 Event #{event_id} saved to database")

                # 가격 추적 시작
                await price_tracker.add_tracking_event(
                    event_id=event_id,
                    code=code,
                    price_at_event=result.current_price
                )
            except Exception as e:
                print(f"   ❌ Failed to save event: {e}")

    def on_log(msg: str):
        print(f"[LS] {msg}")

    ls_client = LSWebSocketClient(
        target_codes=watchlist_codes,
        on_data=on_data,
        on_log=on_log,
        on_program_data=on_program_data,  # UPH 콜백 추가
        enable_uph=True  # UPH 구독 활성화
    )

    # 4. 백그라운드에서 LS증권 연결 시작
    ls_client.start()
    asyncio.create_task(ls_client.connect_and_subscribe())

    # 5. 가격 추적 루프 시작
    price_tracker.start()

    print("✅ LS WebSocket client started in background")
    print("="*60 + "\n")

    yield  # 서버 실행 중...

    # ========== SHUTDOWN ==========
    print("\n" + "="*60)
    print("🛑 SERVER SHUTDOWN - Closing LS WebSocket...")
    print("="*60)

    if price_tracker:
        price_tracker.stop()

    if ls_client:
        ls_client.stop()

    if research_db:
        research_db.close()

    print("✅ LS WebSocket client stopped")
    print("✅ Research tools stopped")
    print("="*60 + "\n")


# FastAPI 앱 생성 (lifespan 적용)
app = FastAPI(title="Footprint Chart Backend", lifespan=lifespan)

# CORS 설정 (React 앱과 통신)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://192.168.50.75:3000",
        "http://192.168.50.75:3001"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_access_token() -> str:
    """LS증권 API 접근 토큰 발급"""
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "appkey": APP_KEY,
        "appsecretkey": APP_SECRET,
        "scope": "oob"
    }

    try:
        resp = requests.post(f"{REST_URL}/oauth2/token", headers=headers, data=data)
        if resp.status_code == 200:
            token = resp.json().get("access_token")
            return token
        else:
            raise Exception(f"Token fetch failed: {resp.text}")
    except Exception as e:
        raise Exception(f"Token fetch error: {e}")


@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "status": "running",
        "watchlist": watchlist_codes,
        "connected_clients": len(connected_clients),
        "ls_client_running": ls_client.running if ls_client else False
    }


@app.get("/api/history")
async def get_history(code: str, date: str = None):
    """
    과거 틱 데이터 조회

    Args:
        code: 종목코드 (예: "005930")
        date: 날짜 (YYYYMMDD, default=오늘)

    Returns:
        List[dict]: 틱 데이터 배열 (NDJSON 파싱 결과)
    """
    import datetime

    # 날짜 기본값 설정
    if not date:
        date = datetime.datetime.now().strftime("%Y%m%d")

    # 파일 경로 생성 (여러 경로 시도)
    possible_paths = [
        f"raw_data_{code}_{date}.txt",  # 현재 디렉토리
        f"backend/raw_data_{code}_{date}.txt",  # 프로젝트 루트에서 실행 시
        os.path.join(os.path.dirname(__file__), f"raw_data_{code}_{date}.txt")  # main.py 기준
    ]

    filename = None
    for path in possible_paths:
        if os.path.exists(path):
            filename = path
            break

    if not filename:
        print(f"[API] History file not found. Tried: {possible_paths}")
        return []

    # 파일 읽기 및 파싱
    try:
        ticks = []
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    tick = json.loads(line)
                    ticks.append(tick)

        print(f"[API] Loaded {len(ticks)} ticks from {filename}")
        return ticks

    except Exception as e:
        print(f"[ERROR] Failed to read history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/subscribe/{code}")
async def subscribe_to_stock(code: str):
    """
    새로운 종목을 동적으로 구독 (실시간 구독 추가, 서버 재시작 불필요)
    """
    global ls_client, watchlist_codes

    # 이미 구독 중인 종목인지 확인
    if code in watchlist_codes:
        return {
            "status": "already_subscribed",
            "code": code,
            "message": f"{code} is already being tracked"
        }

    # watchlist에 추가 (메모리)
    watchlist_codes.append(code)

    # LS증권 WebSocket에 실시간 구독 추가
    if ls_client and ls_client.running:
        success = await ls_client.add_subscription(code)

        if success:
            print(f"[SUBSCRIBE] ✅ Successfully added {code} to live subscription")

            # watchlist.json 파일에 저장 (영구 보존)
            try:
                # 파일 경로 찾기
                possible_paths = [
                    "watchlist.json",
                    "backend/watchlist.json",
                    os.path.join(os.path.dirname(__file__), "watchlist.json")
                ]

                watchlist_path = None
                for path in possible_paths:
                    if os.path.exists(path):
                        watchlist_path = path
                        break

                # 없으면 기본 경로에 생성
                if not watchlist_path:
                    watchlist_path = os.path.join(os.path.dirname(__file__), "watchlist.json")

                # 파일 저장
                with open(watchlist_path, "w", encoding="utf-8") as f:
                    json.dump({
                        "codes": watchlist_codes,
                        "description": "관심종목 리스트 - 서버 시작 시 자동으로 모든 종목 데이터 수집"
                    }, f, ensure_ascii=False, indent=2)

                print(f"[SUBSCRIBE] 💾 Saved to {watchlist_path}")

                return {
                    "status": "success",
                    "code": code,
                    "message": f"{code} added to watchlist and live subscription started",
                    "watchlist": watchlist_codes
                }

            except Exception as e:
                print(f"[ERROR] Failed to save watchlist: {e}")
                return {
                    "status": "partial_success",
                    "code": code,
                    "message": f"{code} subscribed live but failed to save to file",
                    "watchlist": watchlist_codes
                }
        else:
            print(f"[SUBSCRIBE] ❌ Failed to add {code} to live subscription")
            # 실패 시 메모리에서도 제거
            watchlist_codes.remove(code)
            return {
                "status": "error",
                "code": code,
                "message": f"Failed to subscribe to {code}"
            }
    else:
        print(f"[SUBSCRIBE] ⚠️ LS client not running, cannot subscribe")
        # 메모리에서 제거
        watchlist_codes.remove(code)
        return {
            "status": "error",
            "code": code,
            "message": "LS WebSocket client is not running"
        }


@app.get("/api/watchlist")
async def get_watchlist_with_names():
    """
    구독 중인 종목 목록과 종목명 반환
    ls_stock_list.json에서 로드된 캐시 사용 (API 호출 없음)
    """
    items = []
    for code in watchlist_codes:
        items.append({
            "code": code,
            "name": stock_names_cache.get(code, code)  # 캐시에 없으면 코드 반환
        })
    return {
        "status": "success",
        "count": len(items),
        "items": items
    }


@app.get("/api/stock/{code}")
async def get_stock_info(code: str):
    """
    LS증권 t1102 TR을 사용하여 종목 정보 조회
    """
    try:
        # 캐시에 있으면 바로 반환 (API 호출 절약)
        if code in stock_names_cache:
            return {
                "code": code,
                "name": stock_names_cache[code],
                "status": "cached"
            }

        # 토큰 발급
        token = get_access_token()

        # t1102 종목 정보 조회 API 호출
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "tr_cd": "t1102",
            "tr_cont": "N",
            "tr_cont_key": "",
            "mac_address": ""
        }

        # 요청 데이터 (종목코드)
        data = {
            "t1102InBlock": {
                "shcode": code  # 종목코드
            }
        }

        resp = requests.post(
            f"{REST_URL}/stock/market-data",
            headers=headers,
            json=data
        )

        # Rate Limit 헤더 확인 (있는 경우 로깅)
        rate_limit_headers = {k: v for k, v in resp.headers.items() if 'limit' in k.lower() or 'rate' in k.lower() or 'retry' in k.lower()}
        if rate_limit_headers:
            print(f"[RATE-LIMIT] {code}: {rate_limit_headers}")

        if resp.status_code == 200:
            result = resp.json()
            # t1102 응답에서 종목명 추출
            if "t1102OutBlock" in result:
                stock_name = result["t1102OutBlock"].get("hname", "").strip()
                # 캐시에 저장
                if stock_name:
                    stock_names_cache[code] = stock_name
                return {
                    "code": code,
                    "name": stock_name,
                    "status": "success"
                }
            else:
                raise HTTPException(status_code=404, detail="Stock not found")
        else:
            # 에러 시 상세 정보 로깅
            print(f"[ERROR] API failed for {code}: status={resp.status_code}, headers={dict(resp.headers)}, body={resp.text[:500]}")
            raise HTTPException(status_code=resp.status_code, detail=f"API error: {resp.text}")

    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Stock info fetch failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    Frontend와 WebSocket 연결
    LS증권에서 받은 데이터를 실시간으로 전달
    """
    print("[DEBUG] ============================================")
    print("[DEBUG] WebSocket endpoint called")
    print(f"[DEBUG] Client info: {websocket.client}")

    try:
        await websocket.accept()
        print("[DEBUG] ✅ WebSocket accepted successfully")
    except Exception as e:
        print(f"[ERROR] ❌ Failed to accept WebSocket: {e}")
        return

    connected_clients.add(websocket)
    print(f"[OK] 🎉 Frontend connected (total clients: {len(connected_clients)})")
    print("[DEBUG] ============================================")

    try:
        # Frontend로 연결 성공 메시지 전송
        await websocket.send_json({
            "type": "status",
            "message": f"LS증권 연결됨 (구독 중: {len(watchlist_codes)}개 종목)",
            "watchlist": watchlist_codes
        })

        # 연결 유지 (Frontend에서 연결 해제 시까지)
        while True:
            try:
                # Frontend에서 메시지 수신 (Ping 등)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message = json.loads(data)

                # Pong 응답
                if message.get("type") == "ping":
                    await websocket.send_json({"type": "pong"})

            except asyncio.TimeoutError:
                # Ping/Pong (연결 유지)
                try:
                    await websocket.send_json({"type": "ping"})
                except Exception:
                    break
            except json.JSONDecodeError:
                continue

    except WebSocketDisconnect:
        print(f"[DISCONNECT] Frontend disconnected")
    except Exception as e:
        print(f"[ERROR] WebSocket error: {e}")
    finally:
        connected_clients.discard(websocket)
        print(f"[INFO] Remaining clients: {len(connected_clients)}")
        # 주의: LS증권 연결은 절대 끊지 않음 (서버가 계속 데이터 수집)


# ============================================================================
# 연구 도구 API 엔드포인트
# ============================================================================

@app.get("/api/research/events")
async def get_research_events(
    date: Optional[str] = Query(None, description="날짜 (YYYY-MM-DD)"),
    limit: int = Query(50, description="최대 결과 수")
):
    """
    프로그램 매매 이벤트 목록 조회

    Args:
        date: 날짜 (YYYY-MM-DD, 기본값: 오늘)
        limit: 최대 결과 수 (기본값: 50)
    """
    if not research_db:
        raise HTTPException(status_code=503, detail="Research database not initialized")

    try:
        if date:
            events = await research_db.get_events_by_date(date)
        else:
            events = await research_db.get_recent_events(limit)

        return {
            "status": "success",
            "count": len(events),
            "events": [
                {
                    "id": e.id,
                    "event_time": e.event_time,
                    "code": e.code,
                    "event_type": e.event_type,
                    "trigger_value": e.trigger_value,
                    "price_at_event": e.price_at_event,
                    "delta_vol": e.delta_vol,
                    "stock_name": stock_names_cache.get(e.code, e.code)
                }
                for e in events
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/events/{event_id}")
async def get_research_event_detail(event_id: int):
    """
    이벤트 상세 조회 (가격 추적 포함)
    """
    if not research_db:
        raise HTTPException(status_code=503, detail="Research database not initialized")

    try:
        event = await research_db.get_event_by_id(event_id)
        if not event:
            raise HTTPException(status_code=404, detail=f"Event #{event_id} not found")

        trackings = await research_db.get_price_tracking_for_event(event_id)

        return {
            "status": "success",
            "event": {
                "id": event.id,
                "event_time": event.event_time,
                "code": event.code,
                "stock_name": stock_names_cache.get(event.code, event.code),
                "event_type": event.event_type,
                "trigger_value": event.trigger_value,
                "price_at_event": event.price_at_event,
                "delta_vol": event.delta_vol,
                "bshrem": event.bshrem,
                "bdhrem": event.bdhrem,
                "bshvolume": event.bshvolume,
                "bdhvolume": event.bdhvolume,
                "tval": event.tval
            },
            "price_tracking": [
                {
                    "minutes_after": t.minutes_after,
                    "price": t.price,
                    "price_change_pct": t.price_change_pct,
                    "tracking_time": t.tracking_time
                }
                for t in trackings
            ]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/summary/{date}")
async def get_research_summary(date: str):
    """
    일간 요약 조회 (JSON)
    """
    if not report_generator:
        raise HTTPException(status_code=503, detail="Report generator not initialized")

    try:
        summary = await report_generator.generate_summary_json(date)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/report/{date}", response_class=PlainTextResponse)
async def get_research_report(date: str):
    """
    일간 리포트 조회 (텍스트)
    """
    if not report_generator:
        raise HTTPException(status_code=503, detail="Report generator not initialized")

    try:
        report = await report_generator.generate_daily_report(date)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/report", response_class=PlainTextResponse)
async def get_today_research_report():
    """
    오늘 일간 리포트 조회 (텍스트)
    """
    if not report_generator:
        raise HTTPException(status_code=503, detail="Report generator not initialized")

    try:
        today = datetime.now().strftime('%Y-%m-%d')
        report = await report_generator.generate_daily_report(today)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/research/config")
async def update_research_config(threshold_value: int = Query(..., description="이벤트 감지 최소 금액 (원)")):
    """
    이벤트 감지 설정 변경
    """
    if not event_detector:
        raise HTTPException(status_code=503, detail="Event detector not initialized")

    try:
        old_value = event_detector.threshold_value
        event_detector.update_threshold(threshold_value)

        return {
            "status": "success",
            "old_threshold": old_value,
            "new_threshold": threshold_value,
            "message": f"Threshold updated: {old_value:,}원 -> {threshold_value:,}원"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/status")
async def get_research_status():
    """
    연구 도구 상태 조회
    """
    # 백테스팅 가능한 파일 수
    backtest_files = backtester.list_available_files() if backtester else []

    return {
        "status": "running",
        "event_detector": {
            "threshold_value": event_detector.threshold_value if event_detector else None,
            "tracked_stocks": len(event_detector._prev_data) if event_detector else 0
        },
        "price_tracker": {
            "pending_tasks": price_tracker.get_pending_count() if price_tracker else 0,
            "tasks": price_tracker.get_pending_tasks() if price_tracker else []
        },
        "database": {
            "path": research_db.db_path if research_db else None
        },
        "backtester": {
            "available_files": len(backtest_files),
            "uph_data_dir": backtester.uph_data_dir if backtester else None
        }
    }


# ============================================================================
# 백테스팅 API 엔드포인트
# ============================================================================

@app.get("/api/backtest/files")
async def get_backtest_files():
    """
    백테스팅 가능한 UPH 데이터 파일 목록 조회

    Returns:
        List[Dict]: 파일 정보 목록
    """
    if not backtester:
        raise HTTPException(status_code=503, detail="Backtester not initialized")

    try:
        files = backtester.list_available_files()
        return {
            "status": "success",
            "count": len(files),
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/backtest/run/{code}/{date}")
async def run_backtest(
    code: str,
    date: str,
    threshold: int = Query(THRESHOLD_VALUE, description="이벤트 감지 임계값 (원)")
):
    """
    단일 종목/날짜 백테스트 실행

    Args:
        code: 종목코드 (예: 005930)
        date: 날짜 (YYYYMMDD)
        threshold: 이벤트 감지 임계값 (기본: 3천만원)

    Returns:
        Dict: 백테스트 결과
    """
    if not backtester:
        raise HTTPException(status_code=503, detail="Backtester not initialized")

    try:
        result = backtester.run_backtest(
            code=code,
            date=date,
            threshold_value=threshold
        )

        return {
            "status": "success",
            "result": backtester._result_to_dict(result)
        }
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/backtest/run/{code}/{date}/report", response_class=PlainTextResponse)
async def get_backtest_report(
    code: str,
    date: str,
    threshold: int = Query(THRESHOLD_VALUE, description="이벤트 감지 임계값 (원)")
):
    """
    백테스트 리포트 조회 (텍스트)

    Args:
        code: 종목코드
        date: 날짜 (YYYYMMDD)
        threshold: 이벤트 감지 임계값

    Returns:
        str: 텍스트 리포트
    """
    if not backtester:
        raise HTTPException(status_code=503, detail="Backtester not initialized")

    try:
        result = backtester.run_backtest(
            code=code,
            date=date,
            threshold_value=threshold
        )
        report = backtester.generate_backtest_report(result)
        return report
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 연구 대시보드 API 엔드포인트 (v2.1)
# ============================================================================

async def fetch_stock_name(code: str) -> str:
    """종목명 조회 (캐시 우선, 없으면 API 호출)"""
    if code in stock_names_cache:
        return stock_names_cache[code]

    try:
        token = get_access_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "tr_cd": "t1102",
            "tr_cont": "N",
            "tr_cont_key": "",
            "mac_address": ""
        }
        data = {"t1102InBlock": {"shcode": code}}

        resp = requests.post(
            f"{REST_URL}/stock/market-data",
            headers=headers,
            json=data,
            timeout=5
        )

        if resp.status_code == 200:
            result = resp.json()
            if "t1102OutBlock" in result:
                stock_name = result["t1102OutBlock"].get("hname", "").strip()
                if stock_name:
                    stock_names_cache[code] = stock_name
                    return stock_name
    except Exception as e:
        print(f"[WARN] Failed to fetch stock name for {code}: {e}")

    return code  # 실패시 코드 반환


@app.get("/api/research/live")
async def get_research_live():
    """
    실시간 연구 대시보드 데이터
    - 전체 요약 통계
    - 최근 이벤트 목록 (수익률 포함)
    - 종목별 요약
    """
    if not research_db:
        raise HTTPException(status_code=503, detail="Research database not initialized")

    try:
        # 병렬로 데이터 조회
        summary_task = research_db.get_live_summary()
        events_task = research_db.get_recent_events_with_returns(limit=20)
        stocks_task = research_db.get_stock_summary()

        summary, events, by_stock = await asyncio.gather(
            summary_task, events_task, stocks_task
        )

        # 고유 종목코드 수집
        unique_codes = set()
        for event in events:
            unique_codes.add(event['code'])
        for stock in by_stock:
            unique_codes.add(stock['code'])

        # 캐시에 없는 종목명 조회
        for code in unique_codes:
            if code not in stock_names_cache:
                await fetch_stock_name(code)

        # 종목명 추가
        for event in events:
            event['stock_name'] = stock_names_cache.get(event['code'], event['code'])

        for stock in by_stock:
            stock['stock_name'] = stock_names_cache.get(stock['code'], stock['code'])

        return {
            "status": "success",
            "summary": summary,
            "recent_events": events,
            "by_stock": by_stock
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/stock/{code}/detail")
async def get_research_stock_detail(code: str):
    """
    특정 종목의 상세 통계
    - 종목별 요약
    - 이벤트 목록 (수익률 포함)
    - 시간대별 통계
    - Delta 범위별 통계
    """
    if not research_db:
        raise HTTPException(status_code=503, detail="Research database not initialized")

    try:
        detail = await research_db.get_stock_detail(code)

        return {
            "status": "success",
            "code": code,
            "stock_name": stock_names_cache.get(code, code),
            "summary": detail['summary'],
            "events": detail['events'],
            "by_hour": detail['by_hour'],
            "by_delta": detail['by_delta']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/event/{event_id}/detail")
async def get_research_event_detail_v2(event_id: int):
    """
    이벤트 상세 정보 (가격 추적 차트용)
    """
    if not research_db:
        raise HTTPException(status_code=503, detail="Research database not initialized")

    try:
        event = await research_db.get_event_detail(event_id)
        if not event:
            raise HTTPException(status_code=404, detail=f"Event #{event_id} not found")

        # 종목명 추가
        event['stock_name'] = stock_names_cache.get(event['code'], event['code'])

        return {
            "status": "success",
            "event": event
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/research/divergence")
async def get_divergence_analysis(date: Optional[str] = Query(None, description="날짜 (YYYY-MM-DD)")):
    """
    다이버전스 패턴별 수익률 분석

    Returns:
        - by_divergence: 다이버전스 유형별 통계 (bullish, bearish, none)
        - by_trend: 가격 추세별 이벤트 수익률
    """
    if not research_db:
        raise HTTPException(status_code=503, detail="Research database not initialized")

    try:
        # 병렬로 분석 데이터 조회
        divergence_task = research_db.get_divergence_analysis(date)
        trend_task = research_db.get_trend_based_analysis(date)

        by_divergence, by_trend = await asyncio.gather(divergence_task, trend_task)

        return {
            "status": "success",
            "date": date,
            "by_divergence": by_divergence,
            "by_trend": by_trend
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# 백테스팅 API 엔드포인트
# ============================================================================

@app.post("/api/backtest/multi")
async def run_multi_backtest(
    codes: Optional[list] = Query(None, description="종목코드 리스트"),
    dates: Optional[list] = Query(None, description="날짜 리스트 (YYYYMMDD)"),
    threshold: int = Query(THRESHOLD_VALUE, description="이벤트 감지 임계값 (원)")
):
    """
    여러 종목/날짜에 대한 백테스트 실행

    Args:
        codes: 종목코드 리스트 (None이면 전체)
        dates: 날짜 리스트 (None이면 전체)
        threshold: 이벤트 감지 임계값

    Returns:
        Dict: 종합 백테스트 결과
    """
    if not backtester:
        raise HTTPException(status_code=503, detail="Backtester not initialized")

    try:
        result = backtester.run_multi_backtest(
            codes=codes,
            dates=dates,
            threshold_value=threshold
        )
        return {
            "status": "success",
            **result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
