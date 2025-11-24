"""
FastAPI 백엔드 서버
LS증권 WebSocket 데이터를 Frontend로 중계
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

app = FastAPI(title="Footprint Chart Backend")

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

# 현재 연결된 WebSocket 클라이언트들
connected_clients = set()

# LS증권 WebSocket 클라이언트 (전역)
ls_client = None
current_target_code = "005930"  # 기본 종목: 삼성전자


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
        "target_code": current_target_code,
        "connected_clients": len(connected_clients)
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
    global ls_client

    print("[DEBUG] WebSocket endpoint called")
    await websocket.accept()
    print("[DEBUG] WebSocket accepted")
    connected_clients.add(websocket)
    print(f"[OK] Frontend connected (total: {len(connected_clients)})")

    try:
        # LS증권 WebSocket 시작 (아직 연결되지 않은 경우)
        if ls_client is None or not ls_client.running:
            # 데이터 수신 콜백: Frontend로 브로드캐스트
            async def on_data(body: dict):
                """LS증권 데이터를 모든 Frontend 클라이언트로 전송"""
                disconnected = set()
                # Set을 list로 복사해서 iteration 중 size 변경 문제 방지
                for client in list(connected_clients):
                    try:
                        await client.send_json(body)
                    except Exception:
                        disconnected.add(client)

                # 연결 해제된 클라이언트 제거
                for client in disconnected:
                    connected_clients.discard(client)

            # 로그 콜백
            def on_log(msg: str):
                print(f"[LS] {msg}")

            ls_client = LSWebSocketClient(
                target_code=current_target_code,
                on_data=lambda body: asyncio.create_task(on_data(body)),
                on_log=on_log
            )

            # 백그라운드에서 LS증권 연결 시작
            print("[INFO] Starting LS WebSocket connection...")
            asyncio.create_task(ls_client.connect_and_subscribe())
            await asyncio.sleep(3)  # 연결 대기 (3초로 증가)
            print("[INFO] LS WebSocket task started")

        # Frontend로 연결 성공 메시지 전송
        await websocket.send_json({
            "type": "status",
            "message": f"LS증권 연결됨 ({current_target_code})",
            "target_code": current_target_code
        })

        # 연결 유지 (Frontend에서 연결 해제 시까지)
        while True:
            try:
                # Frontend에서 메시지 수신 (Ping 등)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                message = json.loads(data)

                # 종목 코드 변경 요청 처리
                if message.get("type") == "change_code":
                    new_code = message.get("code")
                    if new_code:
                        await change_target_code(new_code)
                        await websocket.send_json({
                            "type": "status",
                            "message": f"종목 변경: {new_code}"
                        })

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

        # 모든 클라이언트 연결 해제 시 LS증권 연결 종료
        if len(connected_clients) == 0 and ls_client:
            ls_client.stop()
            ls_client = None
            print("[STOP] LS WebSocket connection closed")


async def change_target_code(new_code: str):
    """종목 코드 변경"""
    global ls_client, current_target_code

    print(f"[INFO] Changing target code to: {new_code}")

    # 종목 정보 가져오기
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
        data = {
            "t1102InBlock": {
                "shcode": new_code
            }
        }

        resp = requests.post(
            f"{REST_URL}/stock/market-data",
            headers=headers,
            json=data
        )

        stock_name = new_code  # 기본값
        if resp.status_code == 200:
            result = resp.json()
            if "t1102OutBlock" in result:
                stock_name = result["t1102OutBlock"].get("hname", "").strip()
    except Exception as e:
        print(f"[WARN] Failed to fetch stock name: {e}")
        stock_name = new_code  # 실패 시 코드를 이름으로 사용

    # 기존 연결 종료
    if ls_client:
        ls_client.stop()
        await asyncio.sleep(1)

    current_target_code = new_code
    ls_client = None  # 다음 연결 시 새 코드로 재연결

    # 모든 클라이언트에게 종목 변경 알림
    disconnected = set()
    for client in list(connected_clients):
        try:
            await client.send_json({
                "type": "code_changed",
                "code": new_code,
                "name": stock_name,
                "message": f"종목 변경: {new_code} - {stock_name}"
            })
        except Exception:
            disconnected.add(client)

    # 연결 해제된 클라이언트 제거
    for client in disconnected:
        connected_clients.discard(client)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
