"""
LS증권 Open API 클라이언트

업종 및 종목 차트 관련 API 호출을 담당합니다.
- t8424: 전체 업종 목록
- t1514: 업종 기간별 추이
- t8410: 종목 일봉 차트
"""
import requests
import time
from datetime import datetime, timedelta
from typing import Optional
from config import (
    LS_APP_KEY, LS_APP_SECRET, LS_REST_URL,
    INDUSTRY_ENDPOINT, CHART_ENDPOINT, AnalysisConfig, DEFAULT_CONFIG
)


class LSApiClient:
    """LS증권 API 클라이언트"""

    def __init__(self, config: AnalysisConfig = None):
        """
        Args:
            config: 분석 설정 (없으면 기본 설정 사용)
        """
        self.config = config or DEFAULT_CONFIG
        self.app_key = LS_APP_KEY
        self.app_secret = LS_APP_SECRET
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
        time.sleep(self.config.api_delay)

        # N회마다 추가 딜레이
        if self._api_call_count % self.config.extra_delay_interval == 0:
            print(f"   ... {self._api_call_count}회 API 호출 완료", flush=True)
            time.sleep(self.config.extra_delay)

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
            endpoint: API 엔드포인트
            tr_cd: 거래코드
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

            result = resp.json() if resp.text else {}

            # API 호출 제한 에러 체크 (200 또는 500으로 올 수 있음)
            if result.get("rsp_cd") == "IGW00201":
                if retry_count < self.config.max_retries:
                    print(f"   [RATE LIMIT] API 호출 제한! {self.config.rate_limit_wait}초 대기...")
                    time.sleep(self.config.rate_limit_wait)
                    return self._make_request(endpoint, tr_cd, body, tr_cont, tr_cont_key, retry_count + 1)
                else:
                    print(f"   [ERROR] 최대 재시도 횟수 초과")
                    return {}

            # 토큰 만료 에러 체크 - 토큰 재발급 후 재시도
            if result.get("rsp_cd") == "IGW00121":
                if retry_count < self.config.max_retries:
                    print(f"   [TOKEN EXPIRED] 토큰 만료! 재발급 중...")
                    self._access_token = None  # 토큰 초기화
                    time.sleep(1)
                    return self._make_request(endpoint, tr_cd, body, tr_cont, tr_cont_key, retry_count + 1)
                else:
                    print(f"   [ERROR] 토큰 재발급 최대 재시도 횟수 초과")
                    return {}

            if resp.status_code == 200:
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

    def get_sector_period(self, upcode: str, base_date: str, cnt: int = 5) -> list[dict]:
        """
        업종 기간별 추이 조회 (t1514)

        Args:
            upcode: 업종코드
            base_date: 기준일 (YYYYMMDD)
            cnt: 조회 건수

        Returns:
            list[dict]: 업종 추이 정보 [{date, sign, diff, jisu, ...}, ...]
        """
        body = {
            "t1514InBlock": {
                "upcode": upcode,
                "gubun1": " ",      # 미사용
                "gubun2": "1",      # 일
                "cts_date": base_date,
                "cnt": cnt,
                "rate_gbn": "1"     # 거래량 비중
            }
        }

        result = self._make_request(INDUSTRY_ENDPOINT, "t1514", body)

        if result.get("rsp_cd") != "00000":
            return []

        period_data = result.get("t1514OutBlock1", [])
        return period_data

    # ========================================================================
    # 종목 차트 API
    # ========================================================================

    def get_stock_chart(self, shcode: str, base_date: str, cnt: int = 5) -> list[dict]:
        """
        종목 일봉 차트 조회 (t8410)

        Args:
            shcode: 종목코드 (6자리)
            base_date: 기준일 (YYYYMMDD) - 이 날짜 포함 이전 데이터
            cnt: 조회 건수

        Returns:
            list[dict]: 일봉 데이터 [{date, open, high, low, close, sign, ...}, ...]
        """
        body = {
            "t8410InBlock": {
                "shcode": shcode,
                "gubun": "2",       # 일봉
                "qrycnt": cnt,
                "sdate": "",        # 시작일 (빈값: edate 기준)
                "edate": base_date, # 종료일 (기준일)
                "cts_date": "",
                "comp_yn": "N",     # 비압축
                "sujung": "Y"       # 수정주가 적용
            }
        }

        result = self._make_request(CHART_ENDPOINT, "t8410", body)

        if result.get("rsp_cd") != "00000":
            return []

        chart_data = result.get("t8410OutBlock1", [])
        return chart_data

    def get_stock_chart_range(self, shcode: str, start_date: str, end_date: str) -> list[dict]:
        """
        종목 일봉 차트 조회 (기간 범위 지정)

        Args:
            shcode: 종목코드 (6자리)
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)

        Returns:
            list[dict]: 일봉 데이터 [{date, open, high, low, close, ...}, ...]
        """
        body = {
            "t8410InBlock": {
                "shcode": shcode,
                "gubun": "2",       # 일봉
                "qrycnt": 500,      # 최대 500건
                "sdate": start_date,
                "edate": end_date,
                "cts_date": "",
                "comp_yn": "N",     # 비압축
                "sujung": "Y"       # 수정주가 적용
            }
        }

        result = self._make_request(CHART_ENDPOINT, "t8410", body)

        if result.get("rsp_cd") != "00000":
            return []

        chart_data = result.get("t8410OutBlock1", [])
        return chart_data

    def get_stock_minute_chart(self, shcode: str, start_date: str, end_date: str, ncnt: int = 30) -> list[dict]:
        """
        종목 분봉 차트 조회 (기간 범위 지정, 6개월 단위 분할 조회)

        Args:
            shcode: 종목코드 (6자리)
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)
            ncnt: 분 단위 (1, 3, 5, 10, 15, 30, 60)

        Returns:
            list[dict]: 분봉 데이터 [{date, time, open, high, low, close, ...}, ...]
        """
        # 기간을 6개월 단위로 분할
        date_ranges = self._split_date_range(start_date, end_date, months=6)

        all_data = []
        for range_start, range_end in date_ranges:
            chunk_data = self._get_minute_chart_chunk(shcode, range_start, range_end, ncnt)
            all_data.extend(chunk_data)

        # 날짜/시간 기준 정렬 및 중복 제거
        all_data = self._deduplicate_and_sort(all_data)

        return all_data

    def _split_date_range(self, start_date: str, end_date: str, months: int = 6) -> list[tuple[str, str]]:
        """
        기간을 N개월 단위로 분할

        Args:
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)
            months: 분할 단위 (개월)

        Returns:
            list[tuple]: [(시작일, 종료일), ...] 리스트
        """
        from dateutil.relativedelta import relativedelta

        start = datetime.strptime(start_date, "%Y%m%d")
        end = datetime.strptime(end_date, "%Y%m%d")

        ranges = []
        current_start = start

        while current_start <= end:
            current_end = current_start + relativedelta(months=months) - timedelta(days=1)
            if current_end > end:
                current_end = end

            ranges.append((
                current_start.strftime("%Y%m%d"),
                current_end.strftime("%Y%m%d")
            ))

            current_start = current_end + timedelta(days=1)

        return ranges

    def _get_minute_chart_chunk(self, shcode: str, start_date: str, end_date: str, ncnt: int) -> list[dict]:
        """
        단일 기간 분봉 차트 조회 (연속 조회 포함)
        """
        all_data = []
        cts_date = ""
        cts_time = ""

        while True:
            body = {
                "t8412InBlock": {
                    "shcode": shcode,
                    "ncnt": ncnt,
                    "qrycnt": 500,
                    "nday": "0",
                    "sdate": start_date,
                    "stime": "",
                    "edate": end_date,
                    "etime": "",
                    "cts_date": cts_date,
                    "cts_time": cts_time,
                    "comp_yn": "N"
                }
            }

            tr_cont = "Y" if cts_date else "N"
            result = self._make_request(CHART_ENDPOINT, "t8412", body, tr_cont=tr_cont)

            if result.get("rsp_cd") != "00000":
                break

            chart_data = result.get("t8412OutBlock1", [])
            if not chart_data:
                break

            all_data.extend(chart_data)

            # 연속 조회 키 확인
            out_block = result.get("t8412OutBlock", {})
            new_cts_date = out_block.get("cts_date", "")
            new_cts_time = out_block.get("cts_time", "")

            # 더 이상 데이터가 없으면 종료
            if not new_cts_date or (new_cts_date == cts_date and new_cts_time == cts_time):
                break

            # start_date보다 이전 데이터가 나오면 종료
            if new_cts_date < start_date:
                break

            cts_date = new_cts_date
            cts_time = new_cts_time

        return all_data

    def _deduplicate_and_sort(self, data: list[dict]) -> list[dict]:
        """중복 제거 및 정렬"""
        seen = set()
        unique_data = []

        for item in data:
            key = (item.get("date", ""), item.get("time", ""))
            if key not in seen:
                seen.add(key)
                unique_data.append(item)

        # 날짜/시간 기준 정렬
        unique_data.sort(key=lambda x: (x.get("date", ""), x.get("time", "")))

        return unique_data

    def get_api_call_count(self) -> int:
        """API 호출 횟수 반환"""
        return self._api_call_count

    def reset_token(self):
        """토큰 초기화 (재발급 필요시)"""
        self._access_token = None
