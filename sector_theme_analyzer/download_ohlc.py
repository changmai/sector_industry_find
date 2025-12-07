"""
OHLC 데이터 다운로드 프로그램

섹터가 있는 종목들의 OHLC 데이터를 다운로드합니다.
일봉, 분봉(1분, 5분, 30분 등) 지원.
백테스팅용 데이터로 사용됩니다.

사용법:
    python download_ohlc.py                    # 일봉 (기본)
    python download_ohlc.py --interval 30m    # 30분봉
    python download_ohlc.py --interval 5m     # 5분봉
    python download_ohlc.py --interval 1m     # 1분봉
"""
import sys
import os
import io
import json
import time
import argparse
from datetime import datetime

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from config import AnalysisConfig, STOCK_LIST_PATH, OUTPUT_DIR
from ls_api_client import LSApiClient


def parse_args():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="OHLC 데이터 다운로드 (일봉/분봉)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python download_ohlc.py                    # 일봉 (기본)
    python download_ohlc.py --interval 30m    # 30분봉
    python download_ohlc.py --interval 5m     # 5분봉
    python download_ohlc.py --interval 1m     # 1분봉
        """
    )

    parser.add_argument(
        "--interval",
        type=str,
        default="1d",
        help="데이터 간격 (1d=일봉, 1m/5m/10m/30m=분봉, 기본값: 1d)"
    )

    return parser.parse_args()


def parse_interval(interval: str) -> tuple[str, int]:
    """
    간격 문자열 파싱

    Args:
        interval: 간격 (1d, 1m, 5m, 10m, 30m 등)

    Returns:
        tuple: (타입, 분 단위) - ("day", 0) 또는 ("minute", 30)
    """
    interval = interval.lower().strip()

    if interval in ("1d", "d", "day", "daily"):
        return ("day", 0)
    elif interval.endswith("m"):
        try:
            minutes = int(interval[:-1])
            if minutes in (1, 3, 5, 10, 15, 30, 60):
                return ("minute", minutes)
            else:
                print(f"   [ERROR] 지원하지 않는 분봉 단위: {minutes}분")
                print("   지원 단위: 1m, 3m, 5m, 10m, 15m, 30m, 60m")
                sys.exit(1)
        except ValueError:
            pass

    print(f"   [ERROR] 잘못된 간격 형식: {interval}")
    print("   예시: 1d (일봉), 1m, 5m, 30m (분봉)")
    sys.exit(1)


def get_user_input(interval_type: str, interval_minutes: int) -> tuple[str, str]:
    """사용자로부터 시작일과 종료일 입력받기"""
    interval_name = "일봉" if interval_type == "day" else f"{interval_minutes}분봉"

    print("\n" + "=" * 60)
    print("   OHLC 데이터 다운로드")
    print(f"   (섹터가 있는 종목 {interval_name} 데이터)")
    print("=" * 60)

    while True:
        start_date = input("\n   시작일 입력 (YYYYMMDD, 예: 20240101): ").strip()
        if len(start_date) == 8 and start_date.isdigit():
            try:
                datetime.strptime(start_date, "%Y%m%d")
                break
            except ValueError:
                print("   [ERROR] 유효하지 않은 날짜입니다.")
        else:
            print("   [ERROR] YYYYMMDD 형식으로 입력하세요.")

    while True:
        end_date = input("   종료일 입력 (YYYYMMDD, 예: 20241231): ").strip()
        if len(end_date) == 8 and end_date.isdigit():
            try:
                datetime.strptime(end_date, "%Y%m%d")
                if end_date >= start_date:
                    break
                else:
                    print("   [ERROR] 종료일은 시작일보다 같거나 커야 합니다.")
            except ValueError:
                print("   [ERROR] 유효하지 않은 날짜입니다.")
        else:
            print("   [ERROR] YYYYMMDD 형식으로 입력하세요.")

    return start_date, end_date


def confirm_download(start_date: str, end_date: str, stock_count: int,
                     interval_type: str, interval_minutes: int) -> bool:
    """다운로드 전 확인"""
    # 대략적인 거래일 수 계산 (1년 약 250일 기준)
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d")
    days = (end - start).days
    trading_days = int(days * 250 / 365)

    interval_name = "일봉" if interval_type == "day" else f"{interval_minutes}분봉"

    # 예상 API 호출 수 계산
    if interval_type == "day":
        # 일봉: 1회 호출로 최대 500일
        calls_per_stock = max(1, trading_days // 500 + (1 if trading_days % 500 else 0))
    else:
        # 분봉: 하루 약 390분 / interval_minutes = 봉 수
        bars_per_day = 390 // interval_minutes
        total_bars = trading_days * bars_per_day
        calls_per_stock = max(1, total_bars // 500 + (1 if total_bars % 500 else 0))

    api_calls = stock_count * calls_per_stock
    estimated_seconds = api_calls * 1.0 + (api_calls // 20) * 3.0
    estimated_minutes = estimated_seconds / 60

    print("\n" + "-" * 60)
    print(f"   데이터 타입: {interval_name}")
    print(f"   시작일: {start_date}")
    print(f"   종료일: {end_date}")
    print(f"   기간: 약 {days}일 (거래일 약 {trading_days}일)")
    print(f"   대상 종목: {stock_count}개 (섹터 있는 종목)")
    print(f"   예상 API 호출: {api_calls}회 ({calls_per_stock}회/종목)")
    if estimated_minutes < 60:
        print(f"   예상 소요 시간: 약 {estimated_minutes:.0f}분")
    else:
        print(f"   예상 소요 시간: 약 {estimated_minutes/60:.1f}시간 ({estimated_minutes:.0f}분)")
    print("-" * 60)

    while True:
        confirm = input("\n   다운로드를 시작하시겠습니까? (y/n): ").strip().lower()
        if confirm in ('y', 'yes'):
            return True
        elif confirm in ('n', 'no'):
            return False
        else:
            print("   y 또는 n을 입력하세요.")


def load_stocks_with_sector() -> list[dict]:
    """섹터가 있는 종목 로드"""
    print(f"\n   [JSON] 종목 리스트 로드 중...")

    with open(STOCK_LIST_PATH, "r", encoding="utf-8") as f:
        all_stocks = json.load(f)

    # 섹터코드가 있는 종목만 필터링
    stocks = [
        s for s in all_stocks
        if s.get("섹터코드") and len(s.get("섹터코드")) > 0
    ]

    print(f"   -> {len(stocks)}개 종목 로드 완료 (섹터 있는 종목만, 전체 {len(all_stocks)}개)")
    return stocks


def download_ohlc(api: LSApiClient, stocks: list[dict], start_date: str, end_date: str,
                  interval_type: str, interval_minutes: int) -> dict:
    """OHLC 데이터 다운로드"""
    interval_name = "일봉" if interval_type == "day" else f"{interval_minutes}분봉"
    print(f"\n   [DOWNLOAD] {interval_name} OHLC 데이터 다운로드 시작...")
    print(f"   기간: {start_date} ~ {end_date}")

    ohlc_data = {}
    total = len(stocks)
    success_count = 0
    fail_count = 0

    start_time = time.time()

    for i, stock in enumerate(stocks, 1):
        shcode = stock.get("단축코드", "")
        name = stock.get("종목명", "")

        # 진행 상황 출력
        if i % 50 == 0 or i == 1:
            elapsed = time.time() - start_time
            remaining = (elapsed / i) * (total - i) if i > 0 else 0
            print(f"   -> 다운로드 중... {i}/{total} ({i/total*100:.1f}%) "
                  f"[경과: {elapsed/60:.1f}분, 남은시간: {remaining/60:.1f}분]", flush=True)

        # API 호출 (일봉 또는 분봉)
        if interval_type == "day":
            chart_data = api.get_stock_chart_range(shcode, start_date, end_date)
        else:
            chart_data = api.get_stock_minute_chart(shcode, start_date, end_date, interval_minutes)

        if chart_data:
            ohlc_data[shcode] = {
                "name": name,
                "sector_codes": stock.get("섹터코드", []),
                "sector_names": stock.get("섹터명", []),
                "industry_codes": stock.get("업종코드", []),
                "data": chart_data
            }
            success_count += 1
        else:
            fail_count += 1

    elapsed_total = time.time() - start_time
    print(f"\n   [COMPLETE] 다운로드 완료!")
    print(f"   성공: {success_count}개, 실패: {fail_count}개")
    print(f"   소요 시간: {elapsed_total/60:.1f}분")

    return ohlc_data


def save_ohlc_data(ohlc_data: dict, start_date: str, end_date: str,
                   interval_type: str, interval_minutes: int, format_type: str = "json"):
    """OHLC 데이터 저장"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 파일명에 간격 정보 포함
    interval_suffix = "1d" if interval_type == "day" else f"{interval_minutes}m"

    if format_type == "json":
        # 단일 JSON 파일로 저장
        filename = f"ohlc_{start_date}_{end_date}_{interval_suffix}.json"
        filepath = os.path.join(OUTPUT_DIR, filename)

        interval_name = "일봉" if interval_type == "day" else f"{interval_minutes}분봉"
        save_data = {
            "meta": {
                "start_date": start_date,
                "end_date": end_date,
                "interval": interval_suffix,
                "interval_name": interval_name,
                "stock_count": len(ohlc_data),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "stocks": ohlc_data
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False)

        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
        print(f"\n   [SAVE] 저장 완료: {filepath}")
        print(f"   파일 크기: {file_size:.1f} MB")

    elif format_type == "csv":
        # 통합 CSV 파일로 저장
        import csv

        filename = f"ohlc_{start_date}_{end_date}_{interval_suffix}.csv"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)

            # 분봉이면 시간 컬럼 추가
            if interval_type == "minute":
                writer.writerow(["종목코드", "종목명", "날짜", "시간", "시가", "고가", "저가", "종가", "거래량", "거래대금"])
            else:
                writer.writerow(["종목코드", "종목명", "날짜", "시가", "고가", "저가", "종가", "거래량", "거래대금"])

            for shcode, stock_info in ohlc_data.items():
                name = stock_info["name"]
                for row in stock_info["data"]:
                    if interval_type == "minute":
                        writer.writerow([
                            shcode,
                            name,
                            row.get("date", ""),
                            row.get("time", ""),
                            row.get("open", ""),
                            row.get("high", ""),
                            row.get("low", ""),
                            row.get("close", ""),
                            row.get("jdiff_vol", ""),
                            row.get("value", "")
                        ])
                    else:
                        writer.writerow([
                            shcode,
                            name,
                            row.get("date", ""),
                            row.get("open", ""),
                            row.get("high", ""),
                            row.get("low", ""),
                            row.get("close", ""),
                            row.get("jdiff_vol", ""),
                            row.get("value", "")
                        ])

        file_size = os.path.getsize(filepath) / (1024 * 1024)  # MB
        print(f"\n   [SAVE] 저장 완료: {filepath}")
        print(f"   파일 크기: {file_size:.1f} MB")


def main():
    """메인 함수"""
    # 0. 인자 파싱
    args = parse_args()
    interval_type, interval_minutes = parse_interval(args.interval)

    # 1. 사용자 입력
    start_date, end_date = get_user_input(interval_type, interval_minutes)

    # 2. 종목 로드
    stocks = load_stocks_with_sector()

    # 3. 다운로드 확인
    if not confirm_download(start_date, end_date, len(stocks), interval_type, interval_minutes):
        print("\n   다운로드가 취소되었습니다.")
        return

    # 4. API 클라이언트 초기화
    config = AnalysisConfig()
    api = LSApiClient(config)

    # 5. OHLC 다운로드
    ohlc_data = download_ohlc(api, stocks, start_date, end_date, interval_type, interval_minutes)

    # 6. 저장 형식 선택
    print("\n   저장 형식을 선택하세요:")
    print("   1. JSON (백테스팅용, 메타데이터 포함)")
    print("   2. CSV (엑셀/판다스 호환)")
    print("   3. 둘 다")

    while True:
        choice = input("   선택 (1/2/3): ").strip()
        if choice in ('1', '2', '3'):
            break
        print("   1, 2, 또는 3을 입력하세요.")

    # 7. 저장
    if choice == '1':
        save_ohlc_data(ohlc_data, start_date, end_date, interval_type, interval_minutes, "json")
    elif choice == '2':
        save_ohlc_data(ohlc_data, start_date, end_date, interval_type, interval_minutes, "csv")
    else:
        save_ohlc_data(ohlc_data, start_date, end_date, interval_type, interval_minutes, "json")
        save_ohlc_data(ohlc_data, start_date, end_date, interval_type, interval_minutes, "csv")

    print(f"\n   [STAT] 총 API 호출 횟수: {api.get_api_call_count()}회")
    print("\n   완료!\n")


if __name__ == "__main__":
    main()
