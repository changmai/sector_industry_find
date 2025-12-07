"""
종목 매칭 모듈

연속 상승 테마(섹터)와 업종 조건을 동시에 만족하는 종목을 찾습니다.
"""
import json
import os
from typing import Optional
from config import STOCK_LIST_PATH


class StockMatcher:
    """
    조건 동시 만족 종목 매칭기

    연속 상승 테마코드와 업종코드를 받아,
    두 조건을 모두 만족하는 종목을 종목 리스트에서 찾습니다.
    """

    def __init__(self, stock_list_path: str = STOCK_LIST_PATH):
        """
        Args:
            stock_list_path: 종목 리스트 JSON 파일 경로
        """
        self.stock_list_path = stock_list_path
        self.stock_list: list[dict] = []
        self.theme_info: dict[str, str] = {}  # {tmcode: tmname}
        self.sector_info: dict[str, str] = {}  # {upcode: hname}

    def load_stock_list(self) -> list[dict]:
        """종목 리스트 로드"""
        try:
            # 절대 경로 확인
            path = self.stock_list_path
            if not os.path.isabs(path):
                path = os.path.join(os.path.dirname(__file__), path)

            # 경로가 존재하지 않으면 대체 경로 시도
            if not os.path.exists(path):
                alt_paths = [
                    os.path.join(os.path.dirname(__file__), '..', 'backend', 'ls_stock_list_final.json'),
                    os.path.join(os.path.dirname(__file__), 'ls_stock_list_final.json'),
                    'backend/ls_stock_list_final.json',
                    'ls_stock_list_final.json'
                ]
                for alt in alt_paths:
                    if os.path.exists(alt):
                        path = alt
                        break

            with open(path, 'r', encoding='utf-8') as f:
                self.stock_list = json.load(f)
            print(f"   -> 종목 리스트 로드 완료: {len(self.stock_list)}개 종목")
            return self.stock_list

        except FileNotFoundError:
            print(f"   [ERROR] 종목 리스트 파일을 찾을 수 없습니다: {self.stock_list_path}")
            return []
        except json.JSONDecodeError as e:
            print(f"   [ERROR] JSON 파싱 실패: {e}")
            return []

    def set_theme_info(self, rising_themes: list[dict]):
        """연속 상승 테마 정보 설정"""
        for theme in rising_themes:
            tmcode = theme.get("tmcode", "")
            tmname = theme.get("tmname", "")
            if tmcode:
                self.theme_info[tmcode] = tmname

    def set_sector_info(self, rising_sectors: list[dict]):
        """연속 상승 업종 정보 설정"""
        for sector in rising_sectors:
            upcode = sector.get("upcode", "")
            hname = sector.get("hname", "")
            if upcode:
                self.sector_info[upcode] = hname

    def find_matching_stocks(
        self,
        rising_theme_codes: set,
        rising_sector_codes: set,
        rising_themes: list[dict] = None,
        rising_sectors: list[dict] = None
    ) -> list[dict]:
        """
        조건 동시 만족 종목 찾기

        Args:
            rising_theme_codes: 연속 상승 테마코드 집합
            rising_sector_codes: 연속 상승 업종코드 집합
            rising_themes: 연속 상승 테마 정보 리스트 (선택)
            rising_sectors: 연속 상승 업종 정보 리스트 (선택)

        Returns:
            list[dict]: 조건 만족 종목 리스트
        """
        print("\n" + "="*60)
        print("   [MATCH] 조건 동시 만족 종목 매칭")
        print("="*60)

        # 테마/업종 정보 설정
        if rising_themes:
            self.set_theme_info(rising_themes)
        if rising_sectors:
            self.set_sector_info(rising_sectors)

        # 종목 리스트 로드
        if not self.stock_list:
            self.load_stock_list()

        if not self.stock_list:
            print("   [ERROR] 종목 리스트가 비어있습니다.")
            return []

        print(f"\n   연속 상승 테마: {len(rising_theme_codes)}개")
        print(f"   연속 상승 업종: {len(rising_sector_codes)}개")
        print(f"   총 종목 수: {len(self.stock_list)}개")

        # 매칭
        matched_stocks = []
        theme_only_count = 0
        sector_only_count = 0

        for stock in self.stock_list:
            stock_code = stock.get("단축코드", "")
            stock_name = stock.get("종목명", "")

            # 섹터코드(테마코드)와 업종코드 추출
            sector_codes = stock.get("섹터코드") or []  # None 처리
            industry_codes = stock.get("업종코드") or []  # None 처리

            # 집합으로 변환
            stock_sector_codes = set(sector_codes) if sector_codes else set()
            stock_industry_codes = set(industry_codes) if industry_codes else set()

            # 조건 확인
            theme_match = bool(stock_sector_codes & rising_theme_codes)
            sector_match = bool(stock_industry_codes & rising_sector_codes)

            if theme_match and not sector_match:
                theme_only_count += 1
            elif sector_match and not theme_match:
                sector_only_count += 1

            # 두 조건 모두 만족
            if theme_match and sector_match:
                # 매칭된 테마/업종 정보 추출
                matched_themes = stock_sector_codes & rising_theme_codes
                matched_sectors = stock_industry_codes & rising_sector_codes

                matched_theme_names = [
                    self.theme_info.get(code, code) for code in matched_themes
                ]
                matched_sector_names = [
                    self.sector_info.get(code, code) for code in matched_sectors
                ]

                matched_stocks.append({
                    "종목코드": stock_code,
                    "종목명": stock_name,
                    "시장구분": stock.get("시장구분명", ""),
                    "매칭테마코드": list(matched_themes),
                    "매칭테마명": matched_theme_names,
                    "매칭업종코드": list(matched_sectors),
                    "매칭업종명": matched_sector_names,
                    "전체섹터코드": sector_codes,
                    "전체섹터명": stock.get("섹터명") or [],
                    "전체업종코드": industry_codes,
                    "전체업종명": stock.get("업종명") or []
                })

        print(f"\n   테마만 매칭: {theme_only_count}개")
        print(f"   업종만 매칭: {sector_only_count}개")
        print(f"   [RESULT] 동시 만족: {len(matched_stocks)}개")

        # 종목명 기준 정렬
        matched_stocks.sort(key=lambda x: x.get("종목명", ""))

        return matched_stocks

    def print_results(self, matched_stocks: list[dict], max_display: int = 50):
        """결과 출력"""
        if not matched_stocks:
            print("\n   조건을 동시에 만족하는 종목이 없습니다.")
            return

        print("\n" + "-"*80)
        print(f"   {'종목코드':<8} {'종목명':<15} {'시장':<6} {'매칭테마':<20} {'매칭업종':<15}")
        print("-"*80)

        display_count = min(len(matched_stocks), max_display)
        for stock in matched_stocks[:display_count]:
            code = stock.get("종목코드", "")
            name = stock.get("종목명", "")[:12]
            market = stock.get("시장구분", "")[:5]
            themes = ", ".join(stock.get("매칭테마명", []))[:18]
            sectors = ", ".join(stock.get("매칭업종명", []))[:13]
            print(f"   {code:<8} {name:<15} {market:<6} {themes:<20} {sectors:<15}")

        if len(matched_stocks) > max_display:
            print(f"\n   ... 외 {len(matched_stocks) - max_display}개 종목")

        print("-"*80)


if __name__ == "__main__":
    # 테스트
    matcher = StockMatcher()
    matcher.load_stock_list()

    # 테스트용 더미 데이터
    test_theme_codes = {"0172", "0266"}  # 제약업체, 겨울
    test_sector_codes = {"009", "027"}   # 의약품, 제조업

    matched = matcher.find_matching_stocks(test_theme_codes, test_sector_codes)
    matcher.print_results(matched)
