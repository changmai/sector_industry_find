"""
Sector Theme Analyzer V3 - 메인 실행 모듈

과거 날짜 기준으로 업종 + 테마 동시 연속 상승 종목 분석
사용법:
    python main.py --base-date 20251101 --days 5
"""
import sys
import os
import io
import argparse
import json
from datetime import datetime

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from config import AnalysisConfig, OUTPUT_DIR
from ls_api_client import LSApiClient
from sector_analyzer import SectorAnalyzer
from theme_analyzer import ThemeAnalyzer
from stock_matcher import StockMatcher


def parse_args():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="업종 + 테마 동시 연속 상승 종목 분석 (V3)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python main.py --base-date 20251101 --days 5
    python main.py --base-date 20251115 --days 3 --ratio 0.7
    python main.py --base-date 20251201 --sector-only
    python main.py --base-date 20251201 --theme-only
        """
    )

    parser.add_argument(
        "--base-date",
        type=str,
        required=True,
        help="기준 날짜 (YYYYMMDD 형식)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="연속 상승 일수 (기본값: 5)"
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.6,
        help="테마 상승 판정 비율 (기본값: 0.6 = 60%%)"
    )
    parser.add_argument(
        "--sector-only",
        action="store_true",
        help="업종 분석만 실행"
    )
    parser.add_argument(
        "--theme-only",
        action="store_true",
        help="테마 분석만 실행"
    )
    parser.add_argument(
        "--detail",
        action="store_true",
        help="상세 결과 출력"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="결과 저장 파일 경로 (JSON)"
    )

    return parser.parse_args()


def validate_date(date_str: str) -> bool:
    """날짜 형식 검증"""
    try:
        datetime.strptime(date_str, "%Y%m%d")
        return True
    except ValueError:
        return False


def save_results(results: dict, output_path: str):
    """결과를 JSON 파일로 저장"""
    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n   [SAVE] 결과 저장 완료: {output_path}")


def main():
    """메인 실행 함수"""
    args = parse_args()

    # 날짜 검증
    if not validate_date(args.base_date):
        print(f"   [ERROR] 잘못된 날짜 형식: {args.base_date}")
        print("   YYYYMMDD 형식으로 입력하세요 (예: 20251101)")
        sys.exit(1)

    # 설정 생성
    config = AnalysisConfig(
        base_date=args.base_date,
        consecutive_days=args.days,
        theme_rise_ratio=args.ratio
    )

    print("\n" + "=" * 60)
    print("   SECTOR THEME ANALYZER V3")
    print("   과거 날짜 기준 업종 + 테마 동시 상승 종목 분석")
    print("=" * 60)
    print(f"   기준일: {args.base_date}")
    print(f"   연속 상승 일수: {args.days}일")
    print(f"   테마 상승 비율: {args.ratio * 100:.0f}%")
    print("=" * 60)

    # API 클라이언트 초기화
    api = LSApiClient(config)

    # 결과 저장용
    results = {
        "base_date": args.base_date,
        "days": args.days,
        "theme_rise_ratio": args.ratio,
        "rising_sectors": [],
        "rising_themes": [],
        "matched_stocks": []
    }

    # 업종 분석
    rising_sector_codes = set()
    rising_sectors = []

    if not args.theme_only:
        sector_analyzer = SectorAnalyzer(api, config)
        rising_sectors = sector_analyzer.find_rising_sectors(args.base_date, args.days)
        rising_sector_codes = sector_analyzer.get_rising_sector_codes()
        sector_analyzer.print_results()
        results["rising_sectors"] = rising_sectors
        results["actual_sector_base_date"] = sector_analyzer.actual_base_date

    # 테마 분석
    rising_theme_codes = set()
    rising_themes = []
    stock_chart_cache = {}

    if not args.sector_only:
        theme_analyzer = ThemeAnalyzer(api, config)
        rising_themes = theme_analyzer.find_rising_themes(args.base_date, args.days)
        rising_theme_codes = theme_analyzer.get_rising_theme_codes()
        stock_chart_cache = theme_analyzer.stock_chart_cache
        theme_analyzer.print_results()
        results["rising_themes"] = rising_themes
        results["actual_theme_base_date"] = theme_analyzer.actual_base_date

    # 종목 매칭 (둘 다 분석한 경우)
    if not args.sector_only and not args.theme_only:
        if rising_sector_codes and rising_theme_codes:
            matcher = StockMatcher(config)
            matched_stocks = matcher.find_matching_stocks(
                rising_sector_codes,
                rising_theme_codes,
                rising_sectors,
                rising_themes,
                stock_chart_cache
            )
            matcher.print_results(show_detail=args.detail)
            results["matched_stocks"] = matched_stocks
        else:
            print("\n   [INFO] 상승 업종 또는 테마가 없어 매칭할 수 없습니다.")

    # API 호출 통계
    print("\n" + "=" * 60)
    print(f"   [STAT] 총 API 호출 횟수: {api.get_api_call_count()}회")
    print("=" * 60)

    # 결과 저장
    if args.output:
        output_path = args.output
    else:
        # 기본 출력 경로
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"result_{args.base_date}_{args.days}d.json")

    save_results(results, output_path)

    print("\n   분석 완료!\n")


if __name__ == "__main__":
    main()
