"""
종목 매칭 모듈

업종 + 테마 동시 연속 상승 종목을 찾습니다.
- 종목의 업종코드가 상승 업종에 포함
- 종목의 섹터코드가 상승 테마에 포함
"""
import json
from typing import Optional
from config import AnalysisConfig, DEFAULT_CONFIG, STOCK_LIST_PATH


class StockMatcher:
    """
    종목 매칭기

    연속 상승 업종과 테마에 동시에 속하는 종목을 찾습니다.
    """

    def __init__(self, config: AnalysisConfig = None):
        """
        Args:
            config: 분석 설정
        """
        self.config = config or DEFAULT_CONFIG
        self.stock_list: list[dict] = []
        self.matched_stocks: list[dict] = []

    def load_stock_list(self, file_path: str = None) -> list[dict]:
        """종목 리스트 JSON 로드"""
        path = file_path or STOCK_LIST_PATH

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.stock_list = json.load(f)
            return self.stock_list
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def find_matching_stocks(
        self,
        rising_sector_codes: set,
        rising_theme_codes: set,
        rising_sectors: list[dict] = None,
        rising_themes: list[dict] = None,
        stock_chart_cache: dict = None
    ) -> list[dict]:
        """
        업종 + 테마 동시 상승 종목 찾기

        Args:
            rising_sector_codes: 연속 상승 업종 코드 집합
            rising_theme_codes: 연속 상승 테마 코드 집합
            rising_sectors: 상승 업종 상세 정보 (선택)
            rising_themes: 상승 테마 상세 정보 (선택)
            stock_chart_cache: 종목 차트 캐시 (선택)

        Returns:
            list[dict]: 매칭된 종목 리스트
        """
        print("\n" + "=" * 60)
        print("   [MATCH] 업종 + 테마 동시 상승 종목 탐색")
        print("=" * 60)

        # 종목 리스트 로드
        if not self.stock_list:
            self.load_stock_list()
            print(f"   -> {len(self.stock_list)}개 종목 로드")

        print(f"   -> 상승 업종: {len(rising_sector_codes)}개")
        print(f"   -> 상승 테마: {len(rising_theme_codes)}개")

        # 업종/테마 정보 딕셔너리 생성
        sector_info = {}
        if rising_sectors:
            for s in rising_sectors:
                sector_info[s.get("upcode", "")] = s

        theme_info = {}
        if rising_themes:
            for t in rising_themes:
                theme_info[t.get("tmcode", "")] = t

        # 종목 매칭
        self.matched_stocks = []

        for stock in self.stock_list:
            shcode = stock.get("단축코드", "")
            name = stock.get("종목명", "")
            upcode_list = stock.get("업종코드") or []
            tmcode_list = stock.get("섹터코드") or []

            # 업종 매칭
            matched_sectors = set(upcode_list) & rising_sector_codes
            if not matched_sectors:
                continue

            # 테마 매칭
            matched_themes = set(tmcode_list) & rising_theme_codes
            if not matched_themes:
                continue

            # 종목 차트 정보 (캐시에서)
            stock_change = 0.0
            if stock_chart_cache and shcode in stock_chart_cache:
                chart_data = stock_chart_cache[shcode]
                if chart_data:
                    sorted_data = sorted(chart_data, key=lambda x: x.get("date", ""))
                    days = self.config.consecutive_days
                    recent_data = sorted_data[-days:] if len(sorted_data) >= days else sorted_data
                    for d in recent_data:
                        try:
                            rate = float(d.get("rate", "0") or "0")
                            stock_change += rate
                        except (ValueError, TypeError):
                            pass

            # 매칭된 업종/테마 정보
            matched_sector_info = []
            for upcode in matched_sectors:
                if upcode in sector_info:
                    s = sector_info[upcode]
                    matched_sector_info.append({
                        "upcode": upcode,
                        "hname": s.get("hname", ""),
                        "total_change": s.get("total_change", 0)
                    })

            matched_theme_info = []
            for tmcode in matched_themes:
                if tmcode in theme_info:
                    t = theme_info[tmcode]
                    matched_theme_info.append({
                        "tmcode": tmcode,
                        "tmname": t.get("tmname", ""),
                        "rise_ratio": t.get("rise_ratio", 0),
                        "avg_change": t.get("avg_change", 0)
                    })

            self.matched_stocks.append({
                "shcode": shcode,
                "name": name,
                "stock_change": round(stock_change, 2),
                "matched_sectors": list(matched_sectors),
                "matched_themes": list(matched_themes),
                "sector_info": matched_sector_info,
                "theme_info": matched_theme_info
            })

        # 등락률 기준 정렬
        self.matched_stocks.sort(key=lambda x: x.get("stock_change", 0), reverse=True)

        print(f"\n   [RESULT] 업종+테마 동시 상승 종목: {len(self.matched_stocks)}개")

        return self.matched_stocks

    def print_results(self, show_detail: bool = False):
        """결과 출력"""
        if not self.matched_stocks:
            print("\n   매칭된 종목이 없습니다.")
            return

        print("\n" + "-" * 80)
        print(f"   {'종목코드':<8} {'종목명':<16} {'등락률':>8} {'업종수':>6} {'테마수':>6}")
        print("-" * 80)

        for stock in self.matched_stocks:
            shcode = stock.get("shcode", "")
            name = stock.get("name", "")[:14]
            change = stock.get("stock_change", 0)
            sector_cnt = len(stock.get("matched_sectors", []))
            theme_cnt = len(stock.get("matched_themes", []))

            print(f"   {shcode:<8} {name:<16} {change:>+7.2f}% {sector_cnt:>6} {theme_cnt:>6}")

            if show_detail:
                # 업종 상세
                for s in stock.get("sector_info", []):
                    print(f"      -> 업종: {s.get('hname', '')} ({s.get('upcode', '')}) {s.get('total_change', 0):+.2f}%")
                # 테마 상세
                for t in stock.get("theme_info", []):
                    print(f"      -> 테마: {t.get('tmname', '')} ({t.get('tmcode', '')}) {t.get('rise_ratio', 0):.1f}%")

        print("-" * 80)
        print(f"   총 {len(self.matched_stocks)}개 종목")

    def get_matched_stock_codes(self) -> list[str]:
        """매칭된 종목 코드 리스트 반환"""
        return [s.get("shcode", "") for s in self.matched_stocks]


if __name__ == "__main__":
    # 테스트
    matcher = StockMatcher()
    matcher.load_stock_list()
    print(f"종목 수: {len(matcher.stock_list)}")

    # 샘플 테스트 (실제로는 분석 결과 사용)
    test_sectors = {"009", "012"}
    test_themes = {"0172", "0389"}
    results = matcher.find_matching_stocks(test_sectors, test_themes)
    matcher.print_results()
