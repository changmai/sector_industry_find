"""
FastAPI 백엔드 서버
LS증권 WebSocket 데이터를 Frontend로 중계
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from ls_websocket import LSWebSocketClient

app = FastAPI(title="Footprint Chart Backend")

# CORS 설정 (React 앱과 통신)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 현재 연결된 WebSocket 클라이언트들
connected_clients = set()

# LS증권 WebSocket 클라이언트 (전역)
ls_client = None
current_target_code = "005930"  # 기본 종목: 삼성전자


@app.get("/")
async def root():
    """헬스 체크"""
    return {
        "status": "running",
        "target_code": current_target_code,
        "connected_clients": len(connected_clients)
    }


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

    # 기존 연결 종료
    if ls_client:
        ls_client.stop()
        await asyncio.sleep(1)

    current_target_code = new_code
    ls_client = None  # 다음 연결 시 새 코드로 재연결


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
