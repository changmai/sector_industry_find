"""
LS증권 Open API 클라이언트

테마(섹터) 및 업종 관련 API 호출을 담당하는 클래스
"""
import requests
import time
from typing import Optional
from config import (
    LS_APP_KEY, LS_APP_SECRET, LS_REST_URL,
    SECTOR_ENDPOINT, INDUSTRY_ENDPOINT,
    BASE_DELAY, EXTRA_DELAY, EXTRA_DELAY_INTERVAL,
    MAX_RETRIES, RATE_LIMIT_WAIT
)


class LSApiClient:
    """
    LS증권 API 클라이언트

    테마(섹터) 및 업종 관련 API를 호출합니다.
    """

    def __init__(self, app_key: str = "", app_secret: str = ""):
        """
        Args:
            app_key: LS증권 API App Key (없으면 환경변수 사용)
            app_secret: LS증권 API App Secret (없으면 환경변수 사용)
        """
        self.app_key = app_key or LS_APP_KEY
        self.app_secret = app_secret or LS_APP_SECRET
        self.base_url = LS_REST_URL

        self._access_token: Optional[str] = None
        self._api_call_count = 0

    def _get_access_token(self) -> str:
        """LS증권 API 접근 토큰 발급"""
        if self._access_token:
            return self._access_token

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecretkey": self.app_secret,
            "scope": "oob"
        }

        try:
            resp = requests.post(
                f"{self.base_url}/oauth2/token",
                headers=headers,
                data=data,
                timeout=10
            )
            if resp.status_code == 200:
                self._access_token = resp.json().get("access_token")
                print(f"   [TOKEN] 토큰 발급 성공")
                return self._access_token
            else:
                raise Exception(f"Token fetch failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            raise Exception(f"Token fetch error: {e}")

    def _rate_limit_delay(self):
        """Rate Limiting 딜레이 적용"""
        self._api_call_count += 1

        # 기본 딜레이
        time.sleep(BASE_DELAY)

        # N회마다 추가 딜레이
        if self._api_call_count % EXTRA_DELAY_INTERVAL == 0:
            print(f"   ... {self._api_call_count}회 API 호출 완료", flush=True)
            time.sleep(EXTRA_DELAY)

    def _make_request(
        self,
        endpoint: str,
        tr_cd: str,
        body: dict,
        tr_cont: str = "N",
        tr_cont_key: str = "",
        retry_count: int = 0
    ) -> dict:
        """
        LS증권 API 요청

        Args:
            endpoint: API 엔드포인트 (SECTOR_ENDPOINT 또는 INDUSTRY_ENDPOINT)
            tr_cd: 거래코드 (예: "t8425", "t1533")
            body: 요청 바디
            tr_cont: 연속 거래 여부
            tr_cont_key: 연속 거래 키
            retry_count: 재시도 횟수

        Returns:
            dict: API 응답 JSON
        """
        token = self._get_access_token()

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {token}",
            "tr_cd": tr_cd,
            "tr_cont": tr_cont,
            "tr_cont_key": tr_cont_key,
            "mac_address": ""
        }

        try:
            resp = requests.post(
                f"{self.base_url}{endpoint}",
                headers=headers,
                json=body,
                timeout=30
            )

            # Rate Limiting 적용
            self._rate_limit_delay()

            if resp.status_code == 200:
                result = resp.json()

                # API 호출 제한 에러 체크
                if result.get("rsp_cd") == "IGW00201":
                    if retry_count < MAX_RETRIES:
                        print(f"   [RATE LIMIT] API 호출 제한! {RATE_LIMIT_WAIT}초 대기...")
                        time.sleep(RATE_LIMIT_WAIT)
                        return self._make_request(endpoint, tr_cd, body, tr_cont, tr_cont_key, retry_count + 1)
                    else:
                        print(f"   [ERROR] 최대 재시도 횟수 초과")
                        return {}

                return result
            else:
                print(f"   [ERROR] API error: {resp.status_code} - {resp.text[:200]}")
                return {}

        except requests.Timeout:
            print(f"   [TIMEOUT] {tr_cd} 요청 타임아웃")
            return {}
        except Exception as e:
            print(f"   [ERROR] {tr_cd} 요청 실패: {e}")
            return {}

    # ========================================================================
    # 테마(섹터) 관련 API
    # ========================================================================

    def get_all_themes(self) -> list[dict]:
        """
        전체 테마 목록 조회 (t8425)

        Returns:
            list[dict]: 테마 목록 [{tmname, tmcode}, ...]
        """
        body = {
            "t8425InBlock": {
                "dummy": ""
            }
        }

        result = self._make_request(SECTOR_ENDPOINT, "t8425", body)

        if result.get("rsp_cd") != "00000":
            print(f"   [ERROR] 테마 목록 조회 실패: {result.get('rsp_msg', 'Unknown error')}")
            return []

        themes = result.get("t8425OutBlock", [])
        return themes

    def get_theme_change(self, chgdate: int) -> list[dict]:
        """
        테마 N일 대비 등락 조회 (t1533)

        gubun="7"(기준대비 상승율 상위)으로 조회하면 chgdiff 값을 얻을 수 있음

        Args:
            chgdate: 대비 일자 (1~5)

        Returns:
            list[dict]: 테마 등락 정보 [{tmcode, tmname, avgdiff, chgdiff, ...}, ...]
        """
        body = {
            "t1533InBlock": {
                "gubun": "7",  # 기준대비 상승율 상위
                "chgdate": chgdate
            }
        }

        result = self._make_request(SECTOR_ENDPOINT, "t1533", body)

        if result.get("rsp_cd") != "00000":
            print(f"   [ERROR] 테마 등락 조회 실패 (chgdate={chgdate}): {result.get('rsp_msg', 'Unknown error')}")
            return []

        themes = result.get("t1533OutBlock1", [])
        return themes

    def get_theme_stocks(self, tmcode: str) -> list[dict]:
        """
        테마별 종목 시세 조회 (t1537)

        Args:
            tmcode: 테마코드

        Returns:
            list[dict]: 테마 종목 정보 [{shcode, hname, price, ...}, ...]
        """
        body = {
            "t1537InBlock": {
                "tmcode": tmcode
            }
        }

        result = self._make_request(SECTOR_ENDPOINT, "t1537", body)

        if result.get("rsp_cd") != "00000":
            return []

        return result.get("t1537OutBlock1", [])

    # ========================================================================
    # 업종 관련 API
    # ========================================================================

    def get_all_sectors(self, gubun1: str = "") -> list[dict]:
        """
        전체 업종 목록 조회 (t8424)

        Args:
            gubun1: 구분 ("": 전체, "1": 코스피, "2": 코스닥)

        Returns:
            list[dict]: 업종 목록 [{upcode, hname}, ...]
        """
        body = {
            "t8424InBlock": {
                "gubun1": gubun1
            }
        }

        result = self._make_request(INDUSTRY_ENDPOINT, "t8424", body)

        if result.get("rsp_cd") != "00000":
            print(f"   [ERROR] 업종 목록 조회 실패: {result.get('rsp_msg', 'Unknown error')}")
            return []

        sectors = result.get("t8424OutBlock", [])
        return sectors

    def get_sector_period(self, upcode: str, cnt: int = 5, gubun2: str = "1", cts_date: str = " ") -> list[dict]:
        """
        업종 기간별 추이 조회 (t1514)

        Args:
            upcode: 업종코드
            cnt: 조회 건수 (기본 5일)
            gubun2: 구분 ("1": 일, "2": 주, "3": 월)
            cts_date: 기준일자 (YYYYMMDD 형식, 기본 " "은 오늘 기준)

        Returns:
            list[dict]: 업종 추이 정보 [{date, sign, diff, jisu, ...}, ...]
        """
        body = {
            "t1514InBlock": {
                "upcode": upcode,
                "gubun1": " ",      # 미사용
                "gubun2": gubun2,   # 일/주/월
                "cts_date": cts_date,  # 기준일 (YYYYMMDD 또는 " ")
                "cnt": cnt,
                "rate_gbn": "1"     # 거래량 비중
            }
        }

        result = self._make_request(INDUSTRY_ENDPOINT, "t1514", body)

        if result.get("rsp_cd") != "00000":
            return []

        period_data = result.get("t1514OutBlock1", [])
        return period_data

    def get_sector_current(self, upcode: str) -> dict:
        """
        업종 현재가 조회 (t1511)

        Args:
            upcode: 업종코드

        Returns:
            dict: 업종 현재가 정보
        """
        body = {
            "t1511InBlock": {
                "upcode": upcode
            }
        }

        result = self._make_request(INDUSTRY_ENDPOINT, "t1511", body)

        if result.get("rsp_cd") != "00000":
            return {}

        return result.get("t1511OutBlock", {})

    def get_api_call_count(self) -> int:
        """API 호출 횟수 반환"""
        return self._api_call_count

    def reset_token(self):
        """토큰 초기화 (재발급 필요시)"""
        self._access_token = None
