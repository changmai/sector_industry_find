"""
테마 연속 상승 분석 모듈 (V3)

JSON 기반 테마 그룹핑 + t8410 API로 종목별 일봉 조회
- 테마별 종목을 JSON의 섹터코드로 그룹핑
- 각 종목의 N일 일봉 데이터로 상승 여부 판단
- 테마 상승 판정: 평균 등락률 양수 AND 60% 이상 종목 상승
"""
import json
from collections import defaultdict
from typing import Optional
from ls_api_client import LSApiClient
from config import AnalysisConfig, DEFAULT_CONFIG, STOCK_LIST_PATH


class ThemeAnalyzer:
    """
    테마 연속 상승 분석기 (V3)

    JSON에서 테마별 종목을 그룹핑하고,
    t8410 API로 각 종목의 일봉을 조회하여
    테마별 상승 여부를 판단합니다.
    """

    def __init__(self, api_client: LSApiClient, config: AnalysisConfig = None):
        """
        Args:
            api_client: LS증권 API 클라이언트
            config: 분석 설정
        """
        self.api = api_client
        self.config = config or DEFAULT_CONFIG
        self.stock_list: list[dict] = []
        self.theme_stocks: dict[str, list[dict]] = defaultdict(list)
        self.theme_names: dict[str, str] = {}
        self.rising_themes: list[dict] = []
        self.stock_chart_cache: dict[str, list[dict]] = {}
        self.actual_base_date: str = ""

    def load_stock_list(self, file_path: str = None) -> list[dict]:
        """종목 리스트 JSON 로드 (섹터코드 있는 종목만)"""
        path = file_path or STOCK_LIST_PATH
        print(f"\n   [JSON] 종목 리스트 로드 중...")

        try:
            with open(path, "r", encoding="utf-8") as f:
                all_stocks = json.load(f)

            # 섹터코드가 있는 종목만 필터링
            self.stock_list = [
                s for s in all_stocks
                if s.get("섹터코드") and len(s.get("섹터코드")) > 0
            ]
            print(f"   -> {len(self.stock_list)}개 종목 로드 완료 (섹터 있는 종목만, 전체 {len(all_stocks)}개)")
            return self.stock_list
        except FileNotFoundError:
            print(f"   [ERROR] 파일을 찾을 수 없습니다: {path}")
            return []
        except json.JSONDecodeError as e:
            print(f"   [ERROR] JSON 파싱 오류: {e}")
            return []

    def group_stocks_by_theme(self) -> dict[str, list[dict]]:
        """
        테마(섹터)별 종목 그룹핑

        JSON의 섹터코드를 기준으로 종목을 테마별로 분류합니다.
        """
        print(f"\n   [GROUP] 테마별 종목 그룹핑 중...")
        self.theme_stocks = defaultdict(list)
        self.theme_names = {}

        for stock in self.stock_list:
            sector_codes = stock.get("섹터코드") or []
            sector_names = stock.get("섹터명") or []

            for i, tmcode in enumerate(sector_codes):
                if tmcode:
                    self.theme_stocks[tmcode].append(stock)
                    # 테마명 저장
                    if tmcode not in self.theme_names and i < len(sector_names):
                        self.theme_names[tmcode] = sector_names[i]

        print(f"   -> {len(self.theme_stocks)}개 테마로 그룹핑 완료")
        return self.theme_stocks

    def _is_stock_rising(self, chart_data: list[dict], days: int) -> bool:
        """
        종목 상승 여부 판단 (X일 평균 등락률 양수)

        Args:
            chart_data: 종목 일봉 데이터
            days: 기준 일수

        Returns:
            bool: 평균 등락률이 양수인지 여부
        """
        if len(chart_data) < days:
            return False

        # X일 평균 등락률 계산
        avg_change = self._calculate_stock_change(chart_data, days) / days
        return avg_change > 0

    def _calculate_stock_change(self, chart_data: list[dict], days: int) -> float:
        """종목 총 등락률 계산"""
        if len(chart_data) < days:
            return 0.0

        sorted_data = sorted(chart_data, key=lambda x: x.get("date", ""))
        recent_data = sorted_data[-days:]

        total = 0.0
        for data in recent_data:
            try:
                # t8410은 rate 필드로 등락률 제공
                rate = float(data.get("rate", "0") or "0")
                total += rate
            except (ValueError, TypeError):
                pass

        return total

    def _analyze_theme(
        self, tmcode: str, stocks: list[dict], base_date: str, days: int
    ) -> Optional[dict]:
        """
        단일 테마 분석

        Args:
            tmcode: 테마 코드
            stocks: 테마에 속한 종목 리스트
            base_date: 기준일
            days: 연속 상승 판단 기준 일수

        Returns:
            dict: 상승 테마 정보 (조건 미충족시 None)
        """
        rising_count = 0
        total_change = 0.0
        analyzed_count = 0
        rising_stocks = []

        for stock in stocks:
            shcode = stock.get("단축코드", "")
            if not shcode:
                continue

            # 캐시 확인
            if shcode in self.stock_chart_cache:
                chart_data = self.stock_chart_cache[shcode]
            else:
                # API 호출
                chart_data = self.api.get_stock_chart(shcode, base_date, cnt=days + 2)
                self.stock_chart_cache[shcode] = chart_data

                # 실제 기준일 저장
                if not self.actual_base_date and chart_data:
                    sorted_data = sorted(chart_data, key=lambda x: x.get("date", ""), reverse=True)
                    self.actual_base_date = sorted_data[0].get("date", "") if sorted_data else ""

            if not chart_data or len(chart_data) < days:
                continue

            analyzed_count += 1
            stock_change = self._calculate_stock_change(chart_data, days)
            total_change += stock_change

            if self._is_stock_rising(chart_data, days):
                rising_count += 1
                rising_stocks.append({
                    "shcode": shcode,
                    "name": stock.get("종목명", ""),
                    "change": round(stock_change, 2)
                })

        if analyzed_count == 0:
            return None

        # 상승 비율 계산
        rise_ratio = rising_count / analyzed_count
        avg_change = total_change / analyzed_count

        # 상승 테마 판정: 60% 이상 상승 AND 평균 등락률 양수
        if rise_ratio >= self.config.theme_rise_ratio and avg_change > 0:
            return {
                "tmcode": tmcode,
                "tmname": self.theme_names.get(tmcode, ""),
                "total_stocks": len(stocks),
                "analyzed_stocks": analyzed_count,
                "rising_stocks": rising_count,
                "rise_ratio": round(rise_ratio * 100, 1),
                "avg_change": round(avg_change, 2),
                "top_stocks": sorted(rising_stocks, key=lambda x: x["change"], reverse=True)[:5]
            }

        return None

    def find_rising_themes(self, base_date: str, days: int = 5) -> list[dict]:
        """
        N거래일 연속 상승 테마 탐색

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 연속 상승 판단 기준 일수

        Returns:
            list[dict]: 연속 상승 테마 정보 리스트
        """
        print("\n" + "=" * 60)
        print(f"   [THEME] 테마 {days}거래일 평균 상승 탐색 (V3)")
        print(f"   [BASE DATE] 기준일: {base_date}")
        print("=" * 60)

        # 1. 종목 리스트 로드
        if not self.stock_list:
            self.load_stock_list()

        # 2. 테마별 종목 그룹핑
        if not self.theme_stocks:
            self.group_stocks_by_theme()

        # 3. 각 테마별 분석
        print(f"\n   [t8410] 테마별 종목 차트 분석 중...")
        self.rising_themes = []
        total_themes = len(self.theme_stocks)

        for i, (tmcode, stocks) in enumerate(self.theme_stocks.items(), 1):
            # 진행 상황
            if i % 20 == 0 or i == 1:
                print(f"   -> 분석 중... {i}/{total_themes} 테마", flush=True)

            # 최소 종목 수 체크 (너무 적은 테마 제외)
            if len(stocks) < 3:
                continue

            result = self._analyze_theme(tmcode, stocks, base_date, days)
            if result:
                self.rising_themes.append(result)

        # 실제 기준일 출력
        if self.actual_base_date and self.actual_base_date != base_date:
            print(f"   [INFO] 실제 조회 기준일: {self.actual_base_date} (요청: {base_date})")

        print(f"\n   [RESULT] {days}거래일 평균 상승 테마: {len(self.rising_themes)}개")

        # 상승 비율 기준 정렬
        self.rising_themes.sort(key=lambda x: x.get("rise_ratio", 0), reverse=True)

        # 디버깅: 상위 테마 통계 출력
        self._print_debug_stats(days)

        # 캐시 데이터 저장
        self._save_cache(base_date, days)

        return self.rising_themes

    def _save_cache(self, base_date: str, days: int):
        """캐시 데이터를 JSON으로 저장 (시뮬레이션용)"""
        import os
        from config import OUTPUT_DIR

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        cache_path = os.path.join(OUTPUT_DIR, f"cache_{base_date}_{days}d.json")

        cache_data = {
            "base_date": base_date,
            "days": days,
            "actual_base_date": self.actual_base_date,
            "theme_names": self.theme_names,
            "theme_stocks": {
                tmcode: [{"단축코드": s.get("단축코드", ""), "종목명": s.get("종목명", "")} for s in stocks]
                for tmcode, stocks in self.theme_stocks.items()
            },
            "stock_chart_cache": self.stock_chart_cache
        }

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

        print(f"\n   [CACHE] 캐시 저장 완료: {cache_path}")

    def _print_debug_stats(self, days: int):
        """디버깅용 테마 통계 출력"""
        if not self.theme_stocks:
            return

        print(f"\n   [DEBUG] 테마별 상승 비율 통계 (상위 10개):")
        print("-" * 70)
        print(f"   {'테마코드':<6} {'테마명':<18} {'상승비율':>8} {'평균등락':>10} {'상승/분석':>12}")
        print("-" * 70)

        # 모든 테마 분석 결과 수집
        theme_stats = []
        for tmcode, stocks in self.theme_stocks.items():
            if len(stocks) < 3:
                continue

            rising_count = 0
            total_change = 0.0
            analyzed_count = 0

            for stock in stocks:
                shcode = stock.get("단축코드", "")
                if shcode in self.stock_chart_cache:
                    chart_data = self.stock_chart_cache[shcode]
                    if chart_data and len(chart_data) >= days:
                        analyzed_count += 1
                        stock_change = self._calculate_stock_change(chart_data, days)
                        total_change += stock_change
                        if self._is_stock_rising(chart_data, days):
                            rising_count += 1

            if analyzed_count > 0:
                rise_ratio = rising_count / analyzed_count * 100
                avg_change = total_change / analyzed_count
                theme_stats.append({
                    "tmcode": tmcode,
                    "tmname": self.theme_names.get(tmcode, "")[:16],
                    "rise_ratio": rise_ratio,
                    "avg_change": avg_change,
                    "rising": rising_count,
                    "analyzed": analyzed_count
                })

        # 상승 비율 기준 정렬
        theme_stats.sort(key=lambda x: x["rise_ratio"], reverse=True)

        # 상위 10개 출력
        for t in theme_stats[:10]:
            status = "O" if t["rise_ratio"] >= self.config.theme_rise_ratio * 100 and t["avg_change"] > 0 else "X"
            print(f"   {t['tmcode']:<6} {t['tmname']:<18} {t['rise_ratio']:>7.1f}% {t['avg_change']:>+9.2f}% {t['rising']:>4}/{t['analyzed']:<4} [{status}]")

        print("-" * 70)
        print(f"   * 조건: 상승비율 >= {self.config.theme_rise_ratio * 100:.0f}% AND 평균등락 > 0%")
        print(f"   * [O]=조건충족, [X]=미충족")

    def get_rising_theme_codes(self) -> set:
        """연속 상승 테마 코드 집합 반환"""
        return {t.get("tmcode", "") for t in self.rising_themes}

    def print_results(self):
        """결과 출력"""
        if not self.rising_themes:
            print("\n   연속 상승 테마가 없습니다.")
            return

        print("\n" + "-" * 80)
        print(f"   {'테마코드':<6} {'테마명':<20} {'상승비율':>8} {'평균등락':>8} {'상승/분석':>10}")
        print("-" * 80)

        for theme in self.rising_themes:
            tmcode = theme.get("tmcode", "")
            tmname = theme.get("tmname", "")[:18]
            rise_ratio = theme.get("rise_ratio", 0)
            avg_change = theme.get("avg_change", 0)
            rising = theme.get("rising_stocks", 0)
            analyzed = theme.get("analyzed_stocks", 0)

            print(f"   {tmcode:<6} {tmname:<20} {rise_ratio:>7.1f}% {avg_change:>+7.2f}% {rising:>4}/{analyzed:<4}")

        print("-" * 80)


if __name__ == "__main__":
    # 테스트 실행
    config = AnalysisConfig(base_date="20251201")
    api = LSApiClient(config)
    analyzer = ThemeAnalyzer(api, config)

    rising_themes = analyzer.find_rising_themes("20251201", 5)
    analyzer.print_results()
