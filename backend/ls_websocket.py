"""
LS증권 WebSocket API 연결 모듈 (Multi-Stock Support + Auto Reconnect)
여러 종목을 하나의 연결로 구독하고, 연결 끊김 시 자동 재연결
"""
import json
import requests
import websockets
import asyncio
import datetime
import traceback
import os
from typing import Callable, Optional, List, Dict
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
    LS증권 WebSocket 클라이언트 (Multi-Stock Support)
    실시간 체결 데이터 수신 및 처리
    """

    def __init__(
        self,
        target_codes: List[str],
        on_data: Optional[Callable] = None,
        on_log: Optional[Callable] = None
    ):
        self.target_codes = target_codes  # 구독할 종목 리스트
        self.on_data = on_data  # 데이터 수신 콜백 (code, body를 인자로 받음)
        self.on_log = on_log or print  # 로그 콜백
        self.websocket = None
        self.file_handles: Dict[str, any] = {}  # {code: file_handle}
        self.running = False
        self.current_token = None  # 현재 사용 중인 토큰 저장

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

    async def add_subscription(self, code: str):
        """
        실행 중인 WebSocket에 새로운 종목 구독 추가

        Args:
            code: 추가할 종목 코드 (예: "035720")

        Returns:
            bool: 성공 여부
        """
        if not self.running or not self.websocket:
            self.log(f"!!! WebSocket이 실행 중이 아닙니다.")
            return False

        if code in self.target_codes:
            self.log(f">>> [이미 구독 중] {code}")
            return True

        try:
            # 1. target_codes에 추가
            self.target_codes.append(code)
            self.log(f">>> [동적 구독] {code} 추가 중...")

            # 2. 파일 핸들 생성
            today_str = datetime.datetime.now().strftime("%Y%m%d")
            filename = f"raw_data_{code}_{today_str}.txt"
            self.file_handles[code] = open(filename, "a", encoding="utf-8")
            self.log(f">>> [파일 생성] {filename}")

            # 3. LS증권에 구독 요청 전송
            if self.current_token:
                subscribe_packet = {
                    "header": {"token": self.current_token, "tr_type": "3"},
                    "body": {"tr_cd": "US3", "tr_key": f"U{code}   "}
                }
                await self.websocket.send(json.dumps(subscribe_packet))
                self.log(f">>> [구독 전송 완료] {code}")
                return True
            else:
                self.log(f"!!! 토큰이 없어 구독 실패: {code}")
                return False

        except Exception as e:
            self.log(f"!!! 동적 구독 실패: {code}, 에러: {e}")
            return False

    async def connect_and_subscribe(self):
        """웹소켓 연결 및 구독 (Auto Reconnect 포함)"""
        reconnect_delay = 5  # 재연결 대기 시간 (초)

        while self.running:
            try:
                token = self.get_access_token()
                if not token:
                    self.log(f"!!! 토큰 발급 실패, {reconnect_delay}초 후 재시도...")
                    await asyncio.sleep(reconnect_delay)
                    continue

                # 토큰 저장 (동적 구독에 사용)
                self.current_token = token
                self.log(f">>> [WS 연결] {WS_URL}")

                # 파일 저장 준비 (종목별)
                today_str = datetime.datetime.now().strftime("%Y%m%d")
                for code in self.target_codes:
                    filename = f"raw_data_{code}_{today_str}.txt"
                    self.file_handles[code] = open(filename, "a", encoding="utf-8")
                    self.log(f">>> [파일 열림] {filename}")

                async with websockets.connect(WS_URL) as websocket:
                    self.websocket = websocket
                    self.log(">>> [연결 성공] 서버 접속 완료!")

                    # 각 종목에 대해 개별 구독 요청 (US3: 통합 체결)
                    for code in self.target_codes:
                        subscribe_packet = {
                            "header": {"token": token, "tr_type": "3"},
                            "body": {"tr_cd": "US3", "tr_key": f"U{code}   "}
                        }
                        await websocket.send(json.dumps(subscribe_packet))
                        self.log(f">>> [구독 전송] {code}")
                        await asyncio.sleep(0.1)  # 요청 간 짧은 대기

                    # 메시지 수신 루프
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
                                # tr_key에서 종목코드 추출 (예: "U005930   " → "005930")
                                tr_key = data.get("header", {}).get("tr_key", "")
                                code = tr_key[1:7].strip() if len(tr_key) >= 7 else ""

                                if code and code in self.file_handles:
                                    # 필요한 데이터만 추출하여 저장 (NDJSON 형식)
                                    tick_data = {
                                        "chetime": body.get("chetime", ""),
                                        "price": body.get("price", ""),
                                        "cvolume": body.get("cvolume", ""),
                                        "cgubun": body.get("cgubun", "")
                                    }

                                    file_handle = self.file_handles[code]
                                    file_handle.write(json.dumps(tick_data, ensure_ascii=False) + "\n")
                                    file_handle.flush()

                                    # Frontend로 데이터 전달 (종목코드 포함)
                                    if self.on_data:
                                        body_with_code = {**body, "code": code}
                                        await self.on_data(code, body_with_code)

            except websockets.exceptions.ConnectionClosed as e:
                self.log(f"!!! 연결 종료됨: {e}, {reconnect_delay}초 후 재연결...")
            except Exception as e:
                self.log(f"!!! 에러 발생: {e}")
                traceback.print_exc()
            finally:
                # 파일 핸들 정리
                for code, fh in self.file_handles.items():
                    if fh and not fh.closed:
                        fh.close()
                        self.log(f">>> [파일 닫힘] raw_data_{code}_{today_str}.txt")
                self.file_handles.clear()

            # 재연결 대기 (running이 True인 경우에만)
            if self.running:
                self.log(f">>> [{reconnect_delay}초 후 재연결 시도...]")
                await asyncio.sleep(reconnect_delay)

        self.log(">>> [종료] WebSocket 클라이언트 정지됨")

    def start(self):
        """WebSocket 연결 시작"""
        self.running = True
        self.log(">>> [시작] WebSocket 클라이언트 실행")

    def stop(self):
        """웹소켓 연결 종료"""
        self.running = False
        self.log(">>> [연결 종료 요청]")

        # 파일 핸들 정리
        for code, fh in self.file_handles.items():
            if fh and not fh.closed:
                fh.close()
        self.file_handles.clear()
