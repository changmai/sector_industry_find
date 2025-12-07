"""
5거래일 연속 상승 테마/업종 및 조건 동시 만족 종목 탐색

메인 실행 파일
"""
import sys
import io
import json
import os
import argparse
import re
from datetime import datetime

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from config import DEFAULT_CONSECUTIVE_DAYS, OUTPUT_DIR
from ls_api_client import LSApiClient
from theme_finder import ThemeFinder
from sector_finder import SectorFinder
from stock_matcher import StockMatcher


def validate_date(date_str: str) -> bool:
    """날짜 형식 유효성 검사 (YYYYMMDD)"""
    if not date_str:
        return True
    if not re.match(r'^\d{8}$', date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False


class ConsecutiveRiseFinder:
    """
    연속 상승 탐색기

    테마(섹터)와 업종의 연속 상승을 탐색하고,
    두 조건을 동시에 만족하는 종목을 찾습니다.
    """

    def __init__(self, days: int = DEFAULT_CONSECUTIVE_DAYS, base_date: str = ""):
        """
        Args:
            days: 연속 상승 판단 기준 일수 (기본 5일)
            base_date: 기준일 (YYYYMMDD 형식, 빈 문자열이면 오늘 기준)
        """
        self.days = days
        self.base_date = base_date
        self.api = LSApiClient()
        self.theme_finder = ThemeFinder(self.api)
        self.sector_finder = SectorFinder(self.api)
        self.stock_matcher = StockMatcher()

        self.rising_themes: list[dict] = []
        self.rising_sectors: list[dict] = []
        self.matched_stocks: list[dict] = []
        self.execution_time: str = ""

    def run(self) -> dict:
        """
        전체 탐색 실행

        Returns:
            dict: 탐색 결과
        """
        self.execution_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_date_display = self.base_date if self.base_date else "오늘"

        print("\n" + "="*70)
        print(f"   [SEARCH] {self.days}거래일 연속 상승 테마/업종 및 종목 탐색")
        print(f"   [TIME] 실행 시간: {self.execution_time}")
        if self.base_date:
            print(f"   [BASE DATE] 기준일: {self.base_date}")
            print(f"   [NOTE] 테마(t1533)는 기준일 미지원 - 오늘 기준으로 조회됩니다")
        print("="*70)

        # 1. 테마(섹터) 연속 상승 탐색 (항상 오늘 기준)
        print("\n" + "="*70)
        print(f"   [THEME] 조건1: 테마(섹터) {self.days}거래일 연속 상승 탐색")
        if self.base_date:
            print(f"   [NOTE] 테마 API는 기준일 미지원 - 오늘 기준")
        print("="*70)
        self.rising_themes = self.theme_finder.find_rising_themes(self.days)
        self.theme_finder.print_results(self.rising_themes)

        # 2. 업종 연속 상승 탐색 (base_date 전달)
        print("\n" + "="*70)
        print(f"   [SECTOR] 조건2: 업종 {self.days}거래일 연속 상승 탐색")
        print("="*70)
        self.rising_sectors = self.sector_finder.find_rising_sectors(self.days, base_date=self.base_date)
        self.sector_finder.print_results(self.rising_sectors)

        # 3. 조건 동시 만족 종목 매칭
        print("\n" + "="*70)
        print("   [MATCH] 조건1+2: 동시 만족 종목 탐색")
        print("="*70)

        rising_theme_codes = self.theme_finder.get_rising_theme_codes()
        rising_sector_codes = {s.get("upcode", "") for s in self.rising_sectors}

        self.matched_stocks = self.stock_matcher.find_matching_stocks(
            rising_theme_codes,
            rising_sector_codes,
            self.rising_themes,
            self.rising_sectors
        )
        self.stock_matcher.print_results(self.matched_stocks)

        # 4. 요약 출력
        self._print_summary()

        # 5. 결과 반환
        return self._build_result()

    def _print_summary(self):
        """최종 요약 출력"""
        print("\n" + "="*70)
        print("   [SUMMARY] 최종 요약")
        print("="*70)
        print(f"   실행 시간: {self.execution_time}")
        print(f"   연속 상승 기준: {self.days}거래일")
        if self.base_date:
            actual_date = self.sector_finder.actual_base_date or self.base_date
            print(f"   기준일: {actual_date} (요청: {self.base_date})")
            print(f"   [NOTE] 테마는 오늘 기준, 업종만 기준일 적용")
        print(f"   API 호출 횟수: {self.api.get_api_call_count()}회")
        print("-"*70)
        print(f"   [THEME] 연속 상승 테마: {len(self.rising_themes)}개")
        print(f"   [SECTOR] 연속 상승 업종: {len(self.rising_sectors)}개")
        print(f"   [RESULT] 동시 만족 종목: {len(self.matched_stocks)}개")
        print("="*70)

    def _build_result(self) -> dict:
        """결과 딕셔너리 생성"""
        result = {
            "execution_time": self.execution_time,
            "consecutive_days": self.days,
            "api_call_count": self.api.get_api_call_count(),
            "summary": {
                "rising_themes_count": len(self.rising_themes),
                "rising_sectors_count": len(self.rising_sectors),
                "matched_stocks_count": len(self.matched_stocks)
            },
            "rising_themes": self.rising_themes,
            "rising_sectors": self.rising_sectors,
            "matched_stocks": self.matched_stocks
        }

        # 기준일 정보 추가
        if self.base_date:
            result["base_date"] = {
                "requested": self.base_date,
                "actual_sector": self.sector_finder.actual_base_date or self.base_date,
                "theme": "today (not supported)"
            }

        return result

    def save_result(self, result: dict = None, output_dir: str = OUTPUT_DIR) -> str:
        """
        결과 저장

        Args:
            result: 저장할 결과 (없으면 자동 생성)
            output_dir: 출력 디렉토리

        Returns:
            str: 저장된 파일 경로
        """
        if result is None:
            result = self._build_result()

        # 출력 디렉토리 생성
        os.makedirs(output_dir, exist_ok=True)

        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"consecutive_rise_{self.days}days_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)

        # JSON 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n   [SAVE] 결과 저장: {filepath}")
        return filepath


def main():
    """메인 실행 함수"""
    parser = argparse.ArgumentParser(
        description="N거래일 연속 상승 테마/업종 및 조건 동시 만족 종목 탐색"
    )
    parser.add_argument(
        "-d", "--days",
        type=int,
        default=DEFAULT_CONSECUTIVE_DAYS,
        help=f"연속 상승 판단 기준 일수 (기본: {DEFAULT_CONSECUTIVE_DAYS}일)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=OUTPUT_DIR,
        help=f"결과 저장 디렉토리 (기본: {OUTPUT_DIR})"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="결과를 파일로 저장하지 않음"
    )
    parser.add_argument(
        "--theme-only",
        action="store_true",
        help="테마(섹터) 연속 상승만 탐색"
    )
    parser.add_argument(
        "--sector-only",
        action="store_true",
        help="업종 연속 상승만 탐색"
    )
    parser.add_argument(
        "-b", "--base-date",
        type=str,
        default="",
        help="기준일 (YYYYMMDD 형식, 기본: 오늘). 업종만 지원, 테마는 항상 오늘 기준"
    )

    args = parser.parse_args()

    # 날짜 형식 유효성 검사
    if args.base_date and not validate_date(args.base_date):
        print(f"   [ERROR] 잘못된 날짜 형식: {args.base_date}")
        print("   날짜는 YYYYMMDD 형식으로 입력하세요. (예: 20251201)")
        sys.exit(1)

    # 개별 모드 실행
    if args.theme_only:
        if args.base_date:
            print("\n   [WARNING] 테마(t1533) API는 기준일을 지원하지 않습니다.")
            print("   --base-date 옵션은 무시되고 오늘 기준으로 조회됩니다.\n")
        print("\n" + "="*70)
        print(f"   [THEME] 테마(섹터) {args.days}거래일 연속 상승 탐색 (단독)")
        print("="*70)
        finder = ThemeFinder()
        themes = finder.find_rising_themes(args.days)
        finder.print_results(themes)
        return

    if args.sector_only:
        print("\n" + "="*70)
        print(f"   [SECTOR] 업종 {args.days}거래일 연속 상승 탐색 (단독)")
        if args.base_date:
            print(f"   [BASE DATE] 기준일: {args.base_date}")
        print("="*70)
        finder = SectorFinder()
        sectors = finder.find_rising_sectors(args.days, base_date=args.base_date)
        finder.print_results(sectors)

        # 실제 조회된 기준일 출력
        if finder.actual_base_date:
            print(f"\n   [INFO] 실제 조회 기준일: {finder.actual_base_date}")
        return

    # 전체 탐색 실행
    finder = ConsecutiveRiseFinder(days=args.days, base_date=args.base_date)
    result = finder.run()

    # 결과 저장
    if not args.no_save:
        finder.save_result(result, args.output)


if __name__ == "__main__":
    main()
