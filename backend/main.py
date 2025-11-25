"""
FastAPI 백엔드 서버
LS증권 WebSocket 데이터를 Frontend로 중계
Server-Driven 아키텍처: 서버 시작 시 자동으로 관심종목 데이터 수집
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
import requests
import os
from dotenv import load_dotenv
from ls_websocket import LSWebSocketClient

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
    global ls_client, watchlist_codes

    # ========== STARTUP ==========
    print("\n" + "="*60)
    print("🚀 SERVER STARTUP - Initializing LS WebSocket...")
    print("="*60)

    # 1. 관심종목 로드
    watchlist_codes = load_watchlist()

    # 2. LS증권 WebSocket 클라이언트 생성
    async def on_data(code: str, body: dict):
        """LS증권 데이터를 모든 Frontend 클라이언트로 전송"""
        # 디버깅: 데이터 수신 확인
        price = body.get("price", "?")
        volume = body.get("cvolume", "?")
        print(f"[DATA] {code} | Price: {price} | Volume: {volume} | Clients: {len(connected_clients)}")

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

    def on_log(msg: str):
        print(f"[LS] {msg}")

    ls_client = LSWebSocketClient(
        target_codes=watchlist_codes,
        on_data=on_data,
        on_log=on_log
    )

    # 3. 백그라운드에서 LS증권 연결 시작
    ls_client.start()
    asyncio.create_task(ls_client.connect_and_subscribe())

    print("✅ LS WebSocket client started in background")
    print("="*60 + "\n")

    yield  # 서버 실행 중...

    # ========== SHUTDOWN ==========
    print("\n" + "="*60)
    print("🛑 SERVER SHUTDOWN - Closing LS WebSocket...")
    print("="*60)

    if ls_client:
        ls_client.stop()

    print("✅ LS WebSocket client stopped")
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


@app.get("/api/stock/{code}")
async def get_stock_info(code: str):
    """
    LS증권 t1102 TR을 사용하여 종목 정보 조회
    """
    try:
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

        if resp.status_code == 200:
            result = resp.json()
            # t1102 응답에서 종목명 추출
            if "t1102OutBlock" in result:
                stock_name = result["t1102OutBlock"].get("hname", "").strip()
                return {
                    "code": code,
                    "name": stock_name,
                    "status": "success"
                }
            else:
                raise HTTPException(status_code=404, detail="Stock not found")
        else:
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
