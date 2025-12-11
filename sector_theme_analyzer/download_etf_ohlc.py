"""
ETF OHLC 데이터 다운로드 스크립트

특정 ETF 종목들의 일봉/30분봉 데이터를 다운로드합니다.
- 069500 (KODEX 200) - 코스피
- 229200 (KODEX 코스닥150) - 코스닥
"""
import sys
import os
import io
import csv
from datetime import datetime

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from config import OUTPUT_DIR
from ls_api_client import LSApiClient

# 다운로드 대상 ETF
ETF_LIST = [
    {"code": "069500", "name": "KODEX 200", "market": "코스피"},
    {"code": "229200", "name": "KODEX 코스닥150", "market": "코스닥"},
]

# 기간 설정
DAILY_START = "20231117"
DAILY_END = "20251208"
MINUTE_START = "20241209"
MINUTE_END = "20251208"


def download_daily_ohlc(client: LSApiClient, code: str, name: str, start_date: str, end_date: str):
    """일봉 데이터 다운로드 (기간 분할 조회)"""
    print(f"\n[일봉] {code} ({name}) 다운로드 중...")
    print(f"   기간: {start_date} ~ {end_date}")

    # 기간을 6개월 단위로 분할해서 조회 (API 500건 제한 회피)
    date_ranges = client._split_date_range(start_date, end_date, months=6)

    all_data = []
    for range_start, range_end in date_ranges:
        print(f"   ... 조회 중: {range_start} ~ {range_end}")
        chunk = client.get_stock_chart_range(code, range_start, range_end)
        if chunk:
            all_data.extend(chunk)

    if not all_data:
        print(f"   [ERROR] 데이터 없음")
        return False

    # 중복 제거 및 정렬
    seen = set()
    unique_data = []
    for row in all_data:
        date = row.get("date", "")
        if date not in seen:
            seen.add(date)
            unique_data.append(row)

    unique_data.sort(key=lambda x: x.get("date", ""))

    # CSV 저장
    output_path = os.path.join(OUTPUT_DIR, f"etf_{code}_daily.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 헤더
        writer.writerow(["종목코드", "날짜", "시가", "고가", "저가", "종가", "거래량"])

        for row in unique_data:
            writer.writerow([
                code,
                row.get("date", ""),
                row.get("open", 0),
                row.get("high", 0),
                row.get("low", 0),
                row.get("close", 0),
                row.get("jdiff_vol", 0),
            ])

    print(f"   -> 저장 완료: {output_path} ({len(unique_data)}행)")
    return True


def download_minute_ohlc(client: LSApiClient, code: str, name: str, start_date: str, end_date: str, ncnt: int = 30):
    """분봉 데이터 다운로드"""
    print(f"\n[{ncnt}분봉] {code} ({name}) 다운로드 중...")
    print(f"   기간: {start_date} ~ {end_date}")

    data = client.get_stock_minute_chart(code, start_date, end_date, ncnt)

    if not data:
        print(f"   [ERROR] 데이터 없음")
        return False

    # CSV 저장
    output_path = os.path.join(OUTPUT_DIR, f"etf_{code}_{ncnt}m.csv")

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # 헤더
        writer.writerow(["종목코드", "날짜", "시간", "시가", "고가", "저가", "종가", "거래량"])

        for row in data:
            writer.writerow([
                code,
                row.get("date", ""),
                row.get("time", ""),
                row.get("open", 0),
                row.get("high", 0),
                row.get("low", 0),
                row.get("close", 0),
                row.get("jdiff_vol", 0),
            ])

    print(f"   -> 저장 완료: {output_path} ({len(data)}행)")
    return True


def main():
    print("=" * 60)
    print("   ETF OHLC 데이터 다운로드")
    print("=" * 60)
    print(f"   대상: {', '.join([f'{e['code']} ({e['name']})' for e in ETF_LIST])}")
    print(f"   일봉 기간: {DAILY_START} ~ {DAILY_END}")
    print(f"   30분봉 기간: {MINUTE_START} ~ {MINUTE_END}")
    print("=" * 60)

    # API 클라이언트 생성
    client = LSApiClient()

    # 출력 디렉토리 확인
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 각 ETF에 대해 다운로드
    for etf in ETF_LIST:
        code = etf["code"]
        name = etf["name"]

        # 일봉 다운로드
        download_daily_ohlc(client, code, name, DAILY_START, DAILY_END)

        # 30분봉 다운로드
        download_minute_ohlc(client, code, name, MINUTE_START, MINUTE_END, ncnt=30)

    print("\n" + "=" * 60)
    print("   다운로드 완료!")
    print("=" * 60)


if __name__ == "__main__":
    main()
