import json
import requests
import websockets
import asyncio
import datetime
import traceback
from PyQt6.QtCore import QThread, pyqtSignal

# ============================================================================
# [설정] API KEY 및 서버 정보
# ============================================================================
APP_KEY = "PS6lqhn4yWxmGvFaaxcewYhO4mwGKCjiqcdl"
APP_SECRET = "zW3QvuUIT8uHnfxcpmIg49dvXCxXkqyn"

TARGET_CODE = "005930"  # 삼성전자

# 모의투자 전용 설정
REST_URL = "https://openapi.ls-sec.co.kr:8080"
WS_URL = "wss://openapi.ls-sec.co.kr:29443/websocket"


# ============================================================================

class WebSocketWorker(QThread):
    """
    서버 통신 및 데이터 수집을 전담하는 워커
    UI와 독립적으로 백그라운드에서 동작함
    """
    data_signal = pyqtSignal(dict)  # 정제된 데이터를 UI로 보냄
    log_signal = pyqtSignal(str)  # 로그 메시지

    def run(self):
        asyncio.run(self.connect_and_subscribe())

    def get_access_token(self):
        self.log_signal.emit(f">>> [토큰 요청] {REST_URL}")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials", "appkey": APP_KEY, "appsecretkey": APP_SECRET, "scope": "oob"}

        try:
            resp = requests.post(f"{REST_URL}/oauth2/token", headers=headers, data=data)
            if resp.status_code == 200:
                token = resp.json().get("access_token")
                self.log_signal.emit(f">>> [토큰 성공] {token[:15]}...")
                return token
            else:
                self.log_signal.emit(f"!!! 토큰 실패: {resp.text}")
                return None
        except Exception as e:
            self.log_signal.emit(f"!!! 연결 오류: {e}")
            return None

    async def connect_and_subscribe(self):
        token = self.get_access_token()
        if not token: return

        self.log_signal.emit(f">>> [WS 연결] {WS_URL}")

        # 파일 저장 준비
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        filename = f"raw_data_{TARGET_CODE}_{today_str}.txt"
        self.log_signal.emit(f">>> [파일 저장] {filename}")

        try:
            with open(filename, "a", encoding="utf-8") as f:
                async with websockets.connect(WS_URL) as websocket:
                    self.log_signal.emit(">>> [연결 성공] 서버 접속 완료!")

                    # 구독 요청 (US3: 통합 체결)
                    subscribe_packet = {
                        "header": {"token": token, "tr_type": "3"},
                        "body": {"tr_cd": "US3", "tr_key": f"U{TARGET_CODE}   "}
                    }
                    await websocket.send(json.dumps(subscribe_packet))
                    self.log_signal.emit(f">>> [구독 전송] {TARGET_CODE}")

                    while True:
                        message = await websocket.recv()
                        f.write(message + "\n")  # 원본 저장
                        f.flush()

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
                                self.data_signal.emit(body)

        except Exception as e:
            self.log_signal.emit(f"!!! 에러 발생: {e}")
            traceback.print_exc()