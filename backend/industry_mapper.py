"""
Industry & Sector Mapper (업종/섹터 코드 매퍼)

LS증권 Open API를 활용하여 종목별 업종코드 및 섹터(테마) 정보를 매핑하는 모듈.

[업종 매핑]
- t8424: 전체 업종 코드 조회
- t1516: 업종별 종목 시세 조회
- Reverse Mapping 방식으로 전체 업종 데이터를 수집하여 종목코드 -> 업종코드 매핑

[섹터(테마) 매핑]
- t1532: 종목별 테마 조회 (종목코드 -> 테마코드/테마명 직접 조회)
- 각 종목별로 API 호출하여 테마 정보 수집
"""

import requests
import json
import time
import os
from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IndustryInfo:
    """업종 정보"""
    upcode: str       # 업종코드
    hname: str        # 업종명
    market_type: str  # 시장구분 (KOSPI/KOSDAQ)


@dataclass
class SectorInfo:
    """섹터(테마) 정보"""
    tmcode: str       # 테마코드
    tmname: str       # 테마명


class IndustryMapper:
    """
    종목별 업종코드 및 섹터(테마) 매핑 클래스

    LS증권 API를 통해 전체 업종 데이터를 수집하고,
    종목코드 -> 업종코드/섹터코드 매핑 테이블을 구축합니다.
    """

    BASE_URL = "https://openapi.ls-sec.co.kr:8080"
    INDUSTRY_ENDPOINT = "/indtp/market-data"
    SECTOR_ENDPOINT = "/stock/sector"  # 섹터(테마) API 엔드포인트

    # Rate Limiting 설정 (LS증권 API 제한: 초당 1건)
    BASE_DELAY = 1.0        # 기본 딜레이 (초) - 초당 1건 제한
    EXTRA_DELAY = 2.0       # 5회마다 추가 딜레이 (초)
    EXTRA_DELAY_INTERVAL = 5  # 추가 딜레이 적용 간격

    def __init__(self, app_key: str = "", app_secret: str = ""):
        """
        Args:
            app_key: LS증권 API App Key
            app_secret: LS증권 API App Secret
        """
        self.app_key = app_key or os.getenv("LS_APP_KEY", "")
        self.app_secret = app_secret or os.getenv("LS_APP_SECRET", "")

        # 매핑 테이블: 종목코드 -> 업종코드 리스트 (복수 업종 지원)
        self.stock_to_industry: dict[str, list[str]] = {}

        # 업종 정보: 업종코드 -> IndustryInfo
        self.industry_info: dict[str, IndustryInfo] = {}

        # 섹터(테마) 매핑 테이블: 종목코드 -> 섹터 리스트 (복수 섹터 지원)
        self.stock_to_sector: dict[str, list[SectorInfo]] = {}

        # API 호출 카운터 (Rate Limiting)
        self._api_call_count = 0

        # 캐시된 토큰
        self._access_token: Optional[str] = None

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
                f"{self.BASE_URL}/oauth2/token",
                headers=headers,
                data=data,
                timeout=10
            )
            if resp.status_code == 200:
                self._access_token = resp.json().get("access_token")
                return self._access_token
            else:
                raise Exception(f"Token fetch failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            raise Exception(f"Token fetch error: {e}")

    def _rate_limit_delay(self):
        """Rate Limiting 딜레이 적용"""
        self._api_call_count += 1

        # 기본 딜레이
        time.sleep(self.BASE_DELAY)

        # 10회마다 추가 딜레이
        if self._api_call_count % self.EXTRA_DELAY_INTERVAL == 0:
            print(f"   ⏳ Rate limit: {self._api_call_count}번째 요청, {self.EXTRA_DELAY}초 추가 대기...")
            time.sleep(self.EXTRA_DELAY)

    def _make_request(self, tr_cd: str, body: dict, tr_cont: str = "N", tr_cont_key: str = "", retry_count: int = 0) -> dict:
        """
        LS증권 API 요청

        Args:
            tr_cd: 거래코드 (예: "t8424", "t1516")
            body: 요청 바디
            tr_cont: 연속 거래 여부 ("Y" 또는 "N")
            tr_cont_key: 연속 거래 키
            retry_count: 재시도 횟수

        Returns:
            dict: API 응답 JSON
        """
        MAX_RETRIES = 3
        RATE_LIMIT_WAIT = 60  # API 호출 제한 시 대기 시간 (초)

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
                f"{self.BASE_URL}{self.INDUSTRY_ENDPOINT}",
                headers=headers,
                json=body,
                timeout=30
            )

            # Rate Limiting 적용
            self._rate_limit_delay()

            if resp.status_code == 200:
                result = resp.json()

                # API 호출 제한 에러 체크 (IGW00201)
                if result.get("rsp_cd") == "IGW00201":
                    if retry_count < MAX_RETRIES:
                        print(f"   ⏳ API 호출 제한! {RATE_LIMIT_WAIT}초 대기 후 재시도... ({retry_count + 1}/{MAX_RETRIES})")
                        time.sleep(RATE_LIMIT_WAIT)
                        return self._make_request(tr_cd, body, tr_cont, tr_cont_key, retry_count + 1)
                    else:
                        print(f"   ❌ 최대 재시도 횟수 초과")
                        return {}

                return result
            else:
                raise Exception(f"API error: {resp.status_code} - {resp.text}")

        except requests.Timeout:
            print(f"   ⚠️ Timeout for {tr_cd}")
            return {}
        except Exception as e:
            print(f"   ❌ Request error for {tr_cd}: {e}")
            return {}

    def fetch_all_industries(self, market_type: str = "") -> list[IndustryInfo]:
        """
        전체 업종 코드 조회 (t8424)

        Args:
            market_type: 시장 구분 ("1": 코스피, "2": 코스닥, "": 전체)

        Returns:
            list[IndustryInfo]: 업종 정보 리스트
        """
        print(f"\n📊 전체 업종 코드 조회 중... (gubun1={market_type or '전체'})")

        body = {
            "t8424InBlock": {
                "gubun1": market_type
            }
        }

        result = self._make_request("t8424", body)

        if result.get("rsp_cd") != "00000":
            print(f"   ❌ 업종 조회 실패: {result.get('rsp_msg', 'Unknown error')}")
            return []

        industries = []
        for item in result.get("t8424OutBlock", []):
            upcode = item.get("upcode", "")
            hname = item.get("hname", "").strip()

            if upcode:
                info = IndustryInfo(
                    upcode=upcode,
                    hname=hname,
                    market_type="KOSPI" if market_type == "1" else "KOSDAQ" if market_type == "2" else "ALL"
                )
                industries.append(info)
                self.industry_info[upcode] = info

        print(f"   ✅ {len(industries)}개 업종 조회 완료")
        return industries

    def fetch_stocks_by_industry(self, upcode: str, gubun: str = "1") -> list[str]:
        """
        업종별 종목 리스트 조회 (t1516)

        Args:
            upcode: 업종코드
            gubun: 구분 (1: 코스피, 2: 코스닥, 3: 섹터지수)

        Returns:
            list[str]: 종목코드 리스트
        """
        all_stocks = []
        shcode = ""  # 연속조회용 종목코드
        tr_cont = "N"

        while True:
            body = {
                "t1516InBlock": {
                    "upcode": upcode,
                    "gubun": gubun,
                    "shcode": shcode
                }
            }

            result = self._make_request("t1516", body, tr_cont=tr_cont)

            if result.get("rsp_cd") != "00000":
                # 일부 업종은 해당 시장에 없을 수 있음 (에러 무시)
                break

            # 종목 리스트 추출
            stocks = result.get("t1516OutBlock1", [])
            for stock in stocks:
                stock_code = stock.get("shcode", "")
                if stock_code:
                    all_stocks.append(stock_code)
                    # 매핑 테이블에 추가 (복수 업종 지원)
                    if stock_code not in self.stock_to_industry:
                        self.stock_to_industry[stock_code] = []
                    if upcode not in self.stock_to_industry[stock_code]:
                        self.stock_to_industry[stock_code].append(upcode)

            # 연속조회 확인
            out_block = result.get("t1516OutBlock", {})
            next_shcode = out_block.get("shcode", "")

            if not next_shcode or next_shcode == shcode or len(stocks) == 0:
                break

            shcode = next_shcode
            tr_cont = "Y"

        return all_stocks

    def build_mapping_table(self, include_kospi: bool = True, include_kosdaq: bool = True) -> dict[str, str]:
        """
        전체 업종을 순회하며 종목 -> 업종 매핑 테이블 구축

        Args:
            include_kospi: 코스피 업종 포함 여부
            include_kosdaq: 코스닥 업종 포함 여부

        Returns:
            dict[str, str]: 종목코드 -> 업종코드 매핑 딕셔너리
        """
        print("\n" + "="*60)
        print("🏗️  업종코드 매핑 테이블 구축 시작")
        print("="*60)

        start_time = time.time()
        self._api_call_count = 0

        # 1. 전체 업종 코드 조회
        all_industries = []

        if include_kospi:
            kospi_industries = self.fetch_all_industries("1")
            all_industries.extend(kospi_industries)

        if include_kosdaq:
            kosdaq_industries = self.fetch_all_industries("2")
            all_industries.extend(kosdaq_industries)

        if not all_industries:
            print("❌ 업종 정보를 가져올 수 없습니다.")
            return {}

        # 2. 각 업종별 종목 조회
        total = len(all_industries)
        print(f"\n📋 총 {total}개 업종의 종목 조회 시작...")

        for i, industry in enumerate(all_industries, 1):
            gubun = "1" if industry.market_type == "KOSPI" else "2"

            print(f"   [{i}/{total}] {industry.upcode} {industry.hname} ({industry.market_type})")

            try:
                stocks = self.fetch_stocks_by_industry(industry.upcode, gubun)
                print(f"      → {len(stocks)}개 종목")
            except Exception as e:
                print(f"      ⚠️ 조회 실패: {e}")
                continue

        elapsed = time.time() - start_time

        print("\n" + "="*60)
        print(f"✅ 매핑 테이블 구축 완료!")
        print(f"   - 총 종목 수: {len(self.stock_to_industry):,}개")
        print(f"   - 총 업종 수: {len(self.industry_info):,}개")
        print(f"   - API 호출 수: {self._api_call_count}회")
        print(f"   - 소요 시간: {elapsed:.1f}초")
        print("="*60)

        return self.stock_to_industry

    # ========================================================================
    # 섹터(테마) 매핑 관련 메서드
    # ========================================================================

    def _make_sector_request(self, tr_cd: str, body: dict, retry_count: int = 0) -> dict:
        """
        LS증권 섹터(테마) API 요청

        Args:
            tr_cd: 거래코드 (예: "t1532")
            body: 요청 바디
            retry_count: 재시도 횟수

        Returns:
            dict: API 응답 JSON
        """
        MAX_RETRIES = 3
        RATE_LIMIT_WAIT = 60

        token = self._get_access_token()

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": f"Bearer {token}",
            "tr_cd": tr_cd,
            "tr_cont": "N",
            "tr_cont_key": "",
            "mac_address": ""
        }

        try:
            resp = requests.post(
                f"{self.BASE_URL}{self.SECTOR_ENDPOINT}",
                headers=headers,
                json=body,
                timeout=30
            )

            # Rate Limiting 적용
            self._rate_limit_delay()

            if resp.status_code == 200:
                result = resp.json()

                # API 호출 제한 에러 체크 (IGW00201)
                if result.get("rsp_cd") == "IGW00201":
                    if retry_count < MAX_RETRIES:
                        print(f"   ⏳ API 호출 제한! {RATE_LIMIT_WAIT}초 대기 후 재시도... ({retry_count + 1}/{MAX_RETRIES})")
                        time.sleep(RATE_LIMIT_WAIT)
                        return self._make_sector_request(tr_cd, body, retry_count + 1)
                    else:
                        print(f"   ❌ 최대 재시도 횟수 초과")
                        return {}

                return result
            else:
                raise Exception(f"API error: {resp.status_code} - {resp.text}")

        except requests.Timeout:
            print(f"   ⚠️ Timeout for {tr_cd}")
            return {}
        except Exception as e:
            print(f"   ❌ Request error for {tr_cd}: {e}")
            return {}

    def fetch_sector_for_stock(self, stock_code: str) -> list[SectorInfo]:
        """
        종목별 테마(섹터) 조회 (t1532)

        Args:
            stock_code: 종목코드 (6자리)

        Returns:
            list[SectorInfo]: 해당 종목의 섹터 정보 리스트
        """
        body = {
            "t1532InBlock": {
                "shcode": stock_code
            }
        }

        result = self._make_sector_request("t1532", body)

        if result.get("rsp_cd") != "00000":
            # 테마가 없는 종목도 있을 수 있음
            return []

        sectors = []
        for item in result.get("t1532OutBlock", []):
            tmcode = item.get("tmcode", "")
            tmname = item.get("tmname", "").strip()

            if tmcode:
                sector = SectorInfo(tmcode=tmcode, tmname=tmname)
                sectors.append(sector)

        return sectors

    def build_sector_mapping(self, stock_codes: list[str] = None) -> dict[str, list[SectorInfo]]:
        """
        종목별 섹터(테마) 매핑 테이블 구축

        Args:
            stock_codes: 조회할 종목코드 리스트 (None이면 업종 매핑된 종목 사용)

        Returns:
            dict[str, list[SectorInfo]]: 종목코드 -> 섹터 리스트 매핑
        """
        print("\n" + "="*60)
        print("🏷️  섹터(테마) 매핑 테이블 구축 시작")
        print("="*60)

        start_time = time.time()
        sector_api_start_count = self._api_call_count

        # 조회할 종목 리스트 결정
        if stock_codes is None:
            stock_codes = list(self.stock_to_industry.keys())

        if not stock_codes:
            print("❌ 조회할 종목이 없습니다.")
            return {}

        total = len(stock_codes)
        print(f"\n📋 총 {total:,}개 종목의 섹터 조회 시작...")
        print(f"   ⏱️  예상 소요 시간: 약 {total * 1.5 / 60:.0f}분")

        success_count = 0
        no_sector_count = 0

        for i, code in enumerate(stock_codes, 1):
            # 진행 상황 출력 (100개마다)
            if i % 100 == 0 or i == 1:
                elapsed = time.time() - start_time
                remaining = (elapsed / i) * (total - i) if i > 0 else 0
                print(f"   [{i:,}/{total:,}] 진행 중... (경과: {elapsed/60:.1f}분, 남은 시간: {remaining/60:.1f}분)")

            try:
                sectors = self.fetch_sector_for_stock(code)
                if sectors:
                    self.stock_to_sector[code] = sectors
                    success_count += 1
                else:
                    self.stock_to_sector[code] = []
                    no_sector_count += 1
            except Exception as e:
                print(f"   ⚠️ {code} 조회 실패: {e}")
                self.stock_to_sector[code] = []
                no_sector_count += 1

        elapsed = time.time() - start_time
        sector_api_calls = self._api_call_count - sector_api_start_count

        print("\n" + "="*60)
        print(f"✅ 섹터 매핑 테이블 구축 완료!")
        print(f"   - 조회 종목 수: {total:,}개")
        print(f"   - 섹터 있음: {success_count:,}개")
        print(f"   - 섹터 없음: {no_sector_count:,}개")
        print(f"   - API 호출 수: {sector_api_calls}회")
        print(f"   - 소요 시간: {elapsed/60:.1f}분")
        print("="*60)

        return self.stock_to_sector

    def get_sector_codes(self, stock_code: str) -> Optional[list[str]]:
        """
        종목코드로 섹터코드 리스트 조회

        Args:
            stock_code: 종목코드 (6자리)

        Returns:
            list[str] | None: 섹터코드 리스트 (없으면 None)
        """
        sectors = self.stock_to_sector.get(stock_code)
        if sectors:
            return [s.tmcode for s in sectors]
        return None

    def get_sector_names(self, stock_code: str) -> Optional[list[str]]:
        """
        종목코드로 섹터명 리스트 조회

        Args:
            stock_code: 종목코드 (6자리)

        Returns:
            list[str] | None: 섹터명 리스트 (없으면 None)
        """
        sectors = self.stock_to_sector.get(stock_code)
        if sectors:
            return [s.tmname for s in sectors]
        return None

    def get_industry_code(self, stock_code: str) -> Optional[list[str]]:
        """
        종목코드로 업종코드 리스트 조회

        Args:
            stock_code: 종목코드 (6자리)

        Returns:
            list[str] | None: 업종코드 리스트 (없으면 None)
        """
        return self.stock_to_industry.get(stock_code)

    def get_industry_names(self, upcodes: list[str]) -> list[str]:
        """
        업종코드 리스트로 업종명 리스트 조회

        Args:
            upcodes: 업종코드 리스트

        Returns:
            list[str]: 업종명 리스트
        """
        names = []
        for upcode in upcodes:
            info = self.industry_info.get(upcode)
            if info:
                names.append(info.hname)
            else:
                names.append("")
        return names

    def get_industry_name(self, upcode: str) -> str:
        """
        업종코드로 업종명 조회

        Args:
            upcode: 업종코드

        Returns:
            str: 업종명 (없으면 빈 문자열)
        """
        info = self.industry_info.get(upcode)
        return info.hname if info else ""

    def update_stock_list_file(
        self,
        input_path: str = "ls_stock_list_final.json",
        output_path: str = "ls_stock_list_final.json",
        include_sector: bool = True
    ) -> int:
        """
        ls_stock_list_final.json 파일에 업종코드 및 섹터코드 추가 (복수 지원)

        Args:
            input_path: 입력 파일 경로
            output_path: 출력 파일 경로
            include_sector: 섹터 정보 포함 여부

        Returns:
            int: 업데이트된 종목 수
        """
        print(f"\n📂 파일 업데이트: {input_path} -> {output_path}")

        # 파일 로드
        try:
            with open(input_path, "r", encoding="utf-8") as f:
                stock_list = json.load(f)
        except FileNotFoundError:
            print(f"   ❌ 파일을 찾을 수 없습니다: {input_path}")
            return 0
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON 파싱 실패: {e}")
            return 0

        # 업종코드 및 섹터코드 추가
        industry_updated = 0
        sector_updated = 0
        multi_industry_count = 0
        multi_sector_count = 0

        for stock in stock_list:
            code = stock.get("단축코드", "")
            if code:
                # 업종 정보 추가
                upcodes = self.stock_to_industry.get(code)
                if upcodes and len(upcodes) > 0:
                    stock["업종코드"] = upcodes
                    stock["업종명"] = self.get_industry_names(upcodes)
                    industry_updated += 1
                    if len(upcodes) > 1:
                        multi_industry_count += 1
                else:
                    stock["업종코드"] = None
                    stock["업종명"] = None

                # 섹터 정보 추가
                if include_sector:
                    sectors = self.stock_to_sector.get(code, [])
                    if sectors:
                        stock["섹터코드"] = [s.tmcode for s in sectors]
                        stock["섹터명"] = [s.tmname for s in sectors]
                        sector_updated += 1
                        if len(sectors) > 1:
                            multi_sector_count += 1
                    else:
                        stock["섹터코드"] = None
                        stock["섹터명"] = None

        # 결과 저장
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(stock_list, f, ensure_ascii=False, indent=2)
            print(f"   ✅ 저장 완료: {output_path}")
            print(f"   - 전체 종목: {len(stock_list):,}개")
            print(f"   [업종]")
            print(f"   - 매핑 성공: {industry_updated:,}개")
            print(f"   - 복수 업종: {multi_industry_count:,}개")
            if include_sector:
                print(f"   [섹터]")
                print(f"   - 매핑 성공: {sector_updated:,}개")
                print(f"   - 복수 섹터: {multi_sector_count:,}개")
        except Exception as e:
            print(f"   ❌ 저장 실패: {e}")
            return 0

        return industry_updated

    def save_mapping_cache(self, cache_path: str = "industry_mapping_cache.json"):
        """
        매핑 테이블을 캐시 파일로 저장 (업종 + 섹터)

        Args:
            cache_path: 캐시 파일 경로
        """
        cache_data = {
            "created_at": datetime.now().isoformat(),
            "stock_to_industry": self.stock_to_industry,
            "industry_info": {
                upcode: {
                    "upcode": info.upcode,
                    "hname": info.hname,
                    "market_type": info.market_type
                }
                for upcode, info in self.industry_info.items()
            },
            # 섹터 정보 추가
            "stock_to_sector": {
                code: [{"tmcode": s.tmcode, "tmname": s.tmname} for s in sectors]
                for code, sectors in self.stock_to_sector.items()
            }
        }

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            print(f"   💾 캐시 저장: {cache_path}")
            print(f"      - 업종 매핑: {len(self.stock_to_industry):,}개")
            print(f"      - 섹터 매핑: {len(self.stock_to_sector):,}개")
        except Exception as e:
            print(f"   ⚠️ 캐시 저장 실패: {e}")

    def load_mapping_cache(self, cache_path: str = "industry_mapping_cache.json") -> bool:
        """
        캐시 파일에서 매핑 테이블 로드 (업종 + 섹터)

        Args:
            cache_path: 캐시 파일 경로

        Returns:
            bool: 로드 성공 여부
        """
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            self.stock_to_industry = cache_data.get("stock_to_industry", {})

            industry_info_raw = cache_data.get("industry_info", {})
            self.industry_info = {
                upcode: IndustryInfo(
                    upcode=info["upcode"],
                    hname=info["hname"],
                    market_type=info["market_type"]
                )
                for upcode, info in industry_info_raw.items()
            }

            # 섹터 정보 로드
            sector_raw = cache_data.get("stock_to_sector", {})
            self.stock_to_sector = {
                code: [SectorInfo(tmcode=s["tmcode"], tmname=s["tmname"]) for s in sectors]
                for code, sectors in sector_raw.items()
            }

            created_at = cache_data.get("created_at", "Unknown")
            print(f"   📂 캐시 로드: {cache_path} (생성일: {created_at})")
            print(f"   - 업종 매핑 종목: {len(self.stock_to_industry):,}개")
            print(f"   - 업종 수: {len(self.industry_info):,}개")
            print(f"   - 섹터 매핑 종목: {len(self.stock_to_sector):,}개")

            return True

        except FileNotFoundError:
            print(f"   ⚠️ 캐시 파일 없음: {cache_path}")
            return False
        except Exception as e:
            print(f"   ❌ 캐시 로드 실패: {e}")
            return False


def run_industry_mapping(
    input_file: str = "ls_stock_list_final.json",
    output_file: str = "ls_stock_list_final.json",
    cache_file: str = "industry_mapping_cache.json",
    use_cache: bool = True,
    include_sector: bool = True,
    sector_only: bool = False
):
    """
    업종코드 및 섹터(테마) 매핑 실행 함수

    Args:
        input_file: 입력 파일 경로
        output_file: 출력 파일 경로
        cache_file: 캐시 파일 경로
        use_cache: 캐시 사용 여부 (True면 캐시 우선 로드)
        include_sector: 섹터(테마) 정보 포함 여부
        sector_only: 섹터 매핑만 실행 (업종 매핑 스킵)
    """
    from dotenv import load_dotenv
    load_dotenv()

    mapper = IndustryMapper()

    # 캐시 로드 시도
    cache_loaded = False
    if use_cache:
        cache_loaded = mapper.load_mapping_cache(cache_file)

    # 업종 매핑 (sector_only가 아닌 경우)
    if not sector_only:
        if not cache_loaded or not mapper.stock_to_industry:
            print("\n🔄 API를 통해 업종 매핑 테이블 구축...")
            mapper.build_mapping_table(include_kospi=True, include_kosdaq=True)

    # 섹터(테마) 매핑
    if include_sector:
        # 캐시에 섹터 정보가 없거나 비어있으면 API 호출
        if not mapper.stock_to_sector:
            print("\n🔄 API를 통해 섹터 매핑 테이블 구축...")

            # 종목 리스트 결정
            if mapper.stock_to_industry:
                stock_codes = list(mapper.stock_to_industry.keys())
            else:
                # 입력 파일에서 종목 리스트 로드
                try:
                    with open(input_file, "r", encoding="utf-8") as f:
                        stock_list = json.load(f)
                    stock_codes = [s.get("단축코드", "") for s in stock_list if s.get("단축코드")]
                    print(f"   📂 {input_file}에서 {len(stock_codes):,}개 종목 로드")
                except Exception as e:
                    print(f"   ❌ 종목 리스트 로드 실패: {e}")
                    stock_codes = []

            if stock_codes:
                mapper.build_sector_mapping(stock_codes)

    # 캐시 저장 (업종 또는 섹터 정보가 있으면)
    if mapper.stock_to_industry or mapper.stock_to_sector:
        mapper.save_mapping_cache(cache_file)

    # 파일 업데이트
    mapper.update_stock_list_file(input_file, output_file, include_sector=include_sector)


# CLI 실행
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LS증권 업종/섹터 코드 매퍼")
    parser.add_argument("-i", "--input", default="ls_stock_list_final.json", help="입력 파일")
    parser.add_argument("-o", "--output", default="ls_stock_list_final.json", help="출력 파일")
    parser.add_argument("-c", "--cache", default="industry_mapping_cache.json", help="캐시 파일")
    parser.add_argument("--no-cache", action="store_true", help="캐시 사용 안 함")
    parser.add_argument("--no-sector", action="store_true", help="섹터(테마) 매핑 제외")
    parser.add_argument("--sector-only", action="store_true", help="섹터 매핑만 실행 (업종 매핑 스킵)")

    args = parser.parse_args()

    print("\n" + "="*60)
    print("🚀 LS증권 업종/섹터 코드 매퍼 실행")
    print("="*60)
    print(f"   입력 파일: {args.input}")
    print(f"   출력 파일: {args.output}")
    print(f"   캐시 파일: {args.cache}")
    print(f"   캐시 사용: {'아니오' if args.no_cache else '예'}")
    print(f"   섹터 매핑: {'아니오' if args.no_sector else '예'}")
    print(f"   섹터만 실행: {'예' if args.sector_only else '아니오'}")
    print("="*60)

    run_industry_mapping(
        input_file=args.input,
        output_file=args.output,
        cache_file=args.cache,
        use_cache=not args.no_cache,
        include_sector=not args.no_sector,
        sector_only=args.sector_only
    )
