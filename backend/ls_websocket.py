"""
LS증권 WebSocket API 연결 모듈
참고: websocket_sample/data_worker.py의 WebSocketWorker 로직 이식
"""
import json
import requests
import websockets
import asyncio
import datetime
import traceback
import os
from typing import Callable, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

# ============================================================================
# [설정] API KEY 및 서버 정보
# ============================================================================
APP_KEY = os.getenv("LS_APP_KEY", "")
APP_SECRET = os.getenv("LS_APP_SECRET", "")

# 모의투자 전용 설정
REST_URL = "https://openapi.ls-sec.co.kr:8080"
WS_URL = "wss://openapi.ls-sec.co.kr:29443/websocket"


class LSWebSocketClient:
    """
    LS증권 WebSocket 클라이언트
    실시간 체결 데이터 수신 및 처리
    """

    def __init__(
        self,
        target_code: str = "005930",
        on_data: Optional[Callable] = None,
        on_log: Optional[Callable] = None
    ):
        self.target_code = target_code
        self.on_data = on_data  # 데이터 수신 콜백
        self.on_log = on_log or print  # 로그 콜백
        self.websocket = None
        self.file = None
        self.running = False

    def log(self, message: str):
        """로그 출력"""
        self.on_log(message)

    def get_access_token(self) -> Optional[str]:
        """LS증권 API 접근 토큰 발급"""
        self.log(f">>> [토큰 요청] {REST_URL}")

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
                self.log(f">>> [토큰 성공] {token[:15]}...")
                return token
            else:
                self.log(f"!!! 토큰 실패: {resp.text}")
                return None
        except Exception as e:
            self.log(f"!!! 연결 오류: {e}")
            return None

    async def connect_and_subscribe(self):
        """웹소켓 연결 및 구독"""
        token = self.get_access_token()
        if not token:
            return

        self.log(f">>> [WS 연결] {WS_URL}")

        # 파일 저장 준비
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"raw_data_{self.target_code}_{today_str}.txt"
        self.log(f">>> [파일 저장] {filename}")

        self.running = True

        try:
            with open(filename, "a", encoding="utf-8") as f:
                self.file = f
                async with websockets.connect(WS_URL) as websocket:
                    self.websocket = websocket
                    self.log(">>> [연결 성공] 서버 접속 완료!")

                    # 구독 요청 (US3: 통합 체결)
                    subscribe_packet = {
                        "header": {"token": token, "tr_type": "3"},
                        "body": {"tr_cd": "US3", "tr_key": f"U{self.target_code}   "}
                    }
                    await websocket.send(json.dumps(subscribe_packet))
                    self.log(f">>> [구독 전송] {self.target_code}")

                    while self.running:
                        try:
                            message = await asyncio.wait_for(
                                websocket.recv(),
                                timeout=1.0
                            )
                        except asyncio.TimeoutError:
                            continue

                        try:
                            data = json.loads(message)
                        except json.JSONDecodeError:
                            continue

                        # PING 처리
                        if data.get("header", {}).get("tr_id") == "PING":
                            await websocket.send(json.dumps({"header": {"tr_id": "PONG"}}))
                            continue

                        # 데이터 전송 (US3: 통합 체결)
                        if data.get("header", {}).get("tr_cd") == "US3":
                            body = data.get("body")
                            if body and isinstance(body, dict):
                                # 필요한 데이터만 추출하여 저장 (NDJSON 형식)
                                tick_data = {
                                    "chetime": body.get("chetime", ""),
                                    "price": body.get("price", ""),
                                    "cvolume": body.get("cvolume", ""),
                                    "cgubun": body.get("cgubun", "")
                                }
                                f.write(json.dumps(tick_data, ensure_ascii=False) + "\n")
                                f.flush()

                                # Frontend로 데이터 전달
                                if self.on_data:
                                    self.on_data(body)

        except Exception as e:
            self.log(f"!!! 에러 발생: {e}")
            traceback.print_exc()
        finally:
            self.running = False
            if self.file:
                self.file.close()

    def stop(self):
        """웹소켓 연결 종료"""
        self.running = False
        self.log(">>> [연결 종료 요청]")
