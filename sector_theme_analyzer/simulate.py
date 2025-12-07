"""
테마 상승 비율 시뮬레이션 스크립트

캐시 데이터를 로드하여 다양한 상승 비율로 시뮬레이션합니다.
API 호출 없이 즉시 결과를 확인할 수 있습니다.

사용법:
    python simulate.py cache_20251104_3d.json
    python simulate.py cache_20251104_3d.json --ratio 0.5
    python simulate.py cache_20251104_3d.json --ratio 0.3 0.4 0.5 0.6 0.7
"""
import sys
import os
import io
import json
import argparse

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from config import OUTPUT_DIR


def load_cache(cache_file: str) -> dict:
    """캐시 파일 로드"""
    # 파일 경로 처리
    if not os.path.isabs(cache_file):
        cache_file = os.path.join(OUTPUT_DIR, cache_file)

    if not os.path.exists(cache_file):
        print(f"   [ERROR] 캐시 파일을 찾을 수 없습니다: {cache_file}")
        sys.exit(1)

    with open(cache_file, "r", encoding="utf-8") as f:
        return json.load(f)


def calculate_stock_change(chart_data: list[dict], days: int) -> float:
    """종목 총 등락률 계산"""
    if len(chart_data) < days:
        return 0.0

    sorted_data = sorted(chart_data, key=lambda x: x.get("date", ""))
    recent_data = sorted_data[-days:]

    total = 0.0
    for data in recent_data:
        try:
            rate = float(data.get("rate", "0") or "0")
            total += rate
        except (ValueError, TypeError):
            pass

    return total


def is_stock_rising(chart_data: list[dict], days: int) -> bool:
    """종목 상승 여부 판단 (평균 등락률 양수)"""
    if len(chart_data) < days:
        return False
    avg_change = calculate_stock_change(chart_data, days) / days
    return avg_change > 0


def simulate(cache_data: dict, ratio: float) -> list[dict]:
    """특정 비율로 시뮬레이션"""
    days = cache_data["days"]
    theme_stocks = cache_data["theme_stocks"]
    theme_names = cache_data["theme_names"]
    stock_chart_cache = cache_data["stock_chart_cache"]

    rising_themes = []

    for tmcode, stocks in theme_stocks.items():
        if len(stocks) < 3:
            continue

        rising_count = 0
        total_change = 0.0
        analyzed_count = 0

        for stock in stocks:
            shcode = stock.get("단축코드", "")
            if shcode in stock_chart_cache:
                chart_data = stock_chart_cache[shcode]
                if chart_data and len(chart_data) >= days:
                    analyzed_count += 1
                    stock_change = calculate_stock_change(chart_data, days)
                    total_change += stock_change
                    if is_stock_rising(chart_data, days):
                        rising_count += 1

        if analyzed_count == 0:
            continue

        rise_ratio = rising_count / analyzed_count
        avg_change = total_change / analyzed_count

        # 조건 체크
        if rise_ratio >= ratio and avg_change > 0:
            rising_themes.append({
                "tmcode": tmcode,
                "tmname": theme_names.get(tmcode, ""),
                "rise_ratio": round(rise_ratio * 100, 1),
                "avg_change": round(avg_change, 2),
                "rising_stocks": rising_count,
                "analyzed_stocks": analyzed_count
            })

    # 상승 비율 기준 정렬
    rising_themes.sort(key=lambda x: x["rise_ratio"], reverse=True)
    return rising_themes


def print_results(rising_themes: list[dict], ratio: float):
    """결과 출력"""
    print(f"\n   [RESULT] 상승비율 >= {ratio*100:.0f}% 조건 충족 테마: {len(rising_themes)}개")

    if not rising_themes:
        print("   해당 조건을 충족하는 테마가 없습니다.")
        return

    print("-" * 80)
    print(f"   {'테마코드':<6} {'테마명':<20} {'상승비율':>8} {'평균등락':>10} {'상승/분석':>12}")
    print("-" * 80)

    for t in rising_themes[:20]:  # 상위 20개만 출력
        print(f"   {t['tmcode']:<6} {t['tmname'][:18]:<20} {t['rise_ratio']:>7.1f}% {t['avg_change']:>+9.2f}% {t['rising_stocks']:>4}/{t['analyzed_stocks']:<4}")

    print("-" * 80)

    if len(rising_themes) > 20:
        print(f"   ... 외 {len(rising_themes) - 20}개 더")


def run_multi_simulation(cache_data: dict, ratios: list[float]):
    """여러 비율로 시뮬레이션 요약"""
    print("\n" + "=" * 60)
    print("   [SIMULATION] 비율별 상승 테마 수 시뮬레이션")
    print("=" * 60)
    print(f"   기준일: {cache_data.get('actual_base_date', cache_data['base_date'])}")
    print(f"   기간: {cache_data['days']}거래일")
    print("=" * 60)

    print(f"\n   {'비율':>8} {'상승테마수':>12}")
    print("-" * 30)

    for ratio in sorted(ratios):
        themes = simulate(cache_data, ratio)
        print(f"   {ratio*100:>7.0f}% {len(themes):>12}개")

    print("-" * 30)


def main():
    parser = argparse.ArgumentParser(
        description="테마 상승 비율 시뮬레이션 (API 호출 없음)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python simulate.py cache_20251104_3d.json
    python simulate.py cache_20251104_3d.json --ratio 0.5
    python simulate.py cache_20251104_3d.json --ratio 0.3 0.4 0.5 0.6 0.7
    python simulate.py cache_20251104_3d.json --all
        """
    )

    parser.add_argument(
        "cache_file",
        type=str,
        help="캐시 파일 경로 (output 폴더 내 파일명만 입력 가능)"
    )
    parser.add_argument(
        "--ratio",
        type=float,
        nargs="+",
        default=[0.6],
        help="상승 비율 (기본값: 0.6, 여러 개 지정 가능)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="10%~90%까지 전체 시뮬레이션"
    )

    args = parser.parse_args()

    # 캐시 로드
    cache_data = load_cache(args.cache_file)
    print(f"\n   [CACHE] 캐시 로드 완료")
    print(f"   기준일: {cache_data.get('actual_base_date', cache_data['base_date'])}")
    print(f"   기간: {cache_data['days']}거래일")
    print(f"   테마 수: {len(cache_data['theme_stocks'])}개")
    print(f"   종목 캐시: {len(cache_data['stock_chart_cache'])}개")

    # 시뮬레이션 실행
    if args.all:
        ratios = [i / 10 for i in range(1, 10)]  # 0.1 ~ 0.9
        run_multi_simulation(cache_data, ratios)
    elif len(args.ratio) > 1:
        run_multi_simulation(cache_data, args.ratio)
    else:
        ratio = args.ratio[0]
        rising_themes = simulate(cache_data, ratio)
        print_results(rising_themes, ratio)


if __name__ == "__main__":
    main()
