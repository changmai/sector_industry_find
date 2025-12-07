"""
테마(섹터) 연속 상승 탐색 모듈

t8425: 전체 테마 목록 조회
t1533: 테마 N일 대비 등락 조회 (gubun=7, chgdate=1~5)
"""
from typing import Optional
from ls_api_client import LSApiClient
from config import DEFAULT_CONSECUTIVE_DAYS


class ThemeFinder:
    """
    테마(섹터) 연속 상승 탐색기

    t1533 API의 chgdate 파라미터를 1~5로 호출하여
    각 날짜별 상승 테마를 추출하고, 교집합으로 연속 상승 테마를 찾습니다.
    """

    def __init__(self, api_client: Optional[LSApiClient] = None):
        """
        Args:
            api_client: LS증권 API 클라이언트 (없으면 새로 생성)
        """
        self.api = api_client or LSApiClient()
        self.all_themes: list[dict] = []
        self.daily_rising_themes: dict[int, set] = {}  # {day: set of tmcode}
        self.theme_info: dict[str, dict] = {}  # {tmcode: {tmname, avgdiff, ...}}

    def fetch_all_themes(self) -> list[dict]:
        """전체 테마 목록 조회"""
        print("\n   [t8425] 전체 테마 목록 조회 중...")
        self.all_themes = self.api.get_all_themes()
        print(f"   -> {len(self.all_themes)}개 테마 조회 완료")

        # 테마 정보 저장
        for theme in self.all_themes:
            tmcode = theme.get("tmcode", "")
            if tmcode:
                self.theme_info[tmcode] = {
                    "tmname": theme.get("tmname", ""),
                    "tmcode": tmcode
                }

        return self.all_themes

    def fetch_daily_rising_themes(self, chgdate: int) -> set:
        """
        특정 날짜 대비 상승 테마 조회

        Args:
            chgdate: 대비 일자 (1~5)

        Returns:
            set: 상승 테마 코드 집합
        """
        themes = self.api.get_theme_change(chgdate)
        rising_codes = set()

        for theme in themes:
            tmcode = theme.get("tmcode", "")
            try:
                chgdiff = float(theme.get("chgdiff", "0"))
            except (ValueError, TypeError):
                chgdiff = 0

            # 상승 테마 (등락율 > 0)
            if chgdiff > 0 and tmcode:
                rising_codes.add(tmcode)

                # 테마 정보 업데이트
                if tmcode not in self.theme_info:
                    self.theme_info[tmcode] = {}
                self.theme_info[tmcode].update({
                    "tmname": theme.get("tmname", ""),
                    "tmcode": tmcode,
                    f"chgdiff_day{chgdate}": chgdiff,
                    "avgdiff": theme.get("avgdiff", "")
                })

        return rising_codes

    def find_rising_themes(self, days: int = DEFAULT_CONSECUTIVE_DAYS) -> list[dict]:
        """
        N거래일 연속 상승 테마 탐색

        Args:
            days: 연속 상승 판단 기준 일수 (기본 5일)

        Returns:
            list[dict]: 연속 상승 테마 정보 리스트
        """
        print("\n" + "="*60)
        print(f"   [THEME] 테마(섹터) {days}거래일 연속 상승 탐색")
        print("="*60)

        # 1. 전체 테마 목록 조회 (참조용)
        self.fetch_all_themes()

        # 2. 각 날짜별 상승 테마 조회
        print(f"\n   [t1533] 날짜별 상승 테마 조회 중...")
        for day in range(1, days + 1):
            rising_codes = self.fetch_daily_rising_themes(day)
            self.daily_rising_themes[day] = rising_codes
            print(f"   -> {day}일 대비 상승 테마: {len(rising_codes)}개")

        # 3. 교집합으로 연속 상승 테마 추출
        if not self.daily_rising_themes:
            return []

        consecutive_rising = self.daily_rising_themes[1].copy()
        for day in range(2, days + 1):
            consecutive_rising &= self.daily_rising_themes.get(day, set())

        print(f"\n   [RESULT] {days}거래일 연속 상승 테마: {len(consecutive_rising)}개")

        # 4. 결과 정리
        result = []
        for tmcode in consecutive_rising:
            info = self.theme_info.get(tmcode, {})
            result.append({
                "tmcode": tmcode,
                "tmname": info.get("tmname", ""),
                "avgdiff": info.get("avgdiff", ""),
                "daily_changes": {
                    f"day{d}": info.get(f"chgdiff_day{d}", 0)
                    for d in range(1, days + 1)
                }
            })

        # 평균 등락율 기준 정렬
        result.sort(key=lambda x: float(x.get("avgdiff", "0") or "0"), reverse=True)

        return result

    def get_rising_theme_codes(self) -> set:
        """연속 상승 테마 코드 집합 반환"""
        if not self.daily_rising_themes:
            return set()

        result = None
        for day_codes in self.daily_rising_themes.values():
            if result is None:
                result = day_codes.copy()
            else:
                result &= day_codes

        return result or set()

    def print_results(self, themes: list[dict]):
        """결과 출력"""
        if not themes:
            print("\n   연속 상승 테마가 없습니다.")
            return

        print("\n" + "-"*60)
        print(f"   {'테마코드':<8} {'테마명':<25} {'평균등락율':>10}")
        print("-"*60)

        for theme in themes:
            tmcode = theme.get("tmcode", "")
            tmname = theme.get("tmname", "")[:20]
            avgdiff = theme.get("avgdiff", "")
            print(f"   {tmcode:<8} {tmname:<25} {avgdiff:>10}%")

        print("-"*60)


if __name__ == "__main__":
    # 테스트 실행
    finder = ThemeFinder()
    rising_themes = finder.find_rising_themes(5)
    finder.print_results(rising_themes)
