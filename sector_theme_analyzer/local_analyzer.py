"""
로컬 데이터 기반 업종 + 섹터 동시 상승 종목 분석기

API 호출 없이 Parquet + JSON 데이터만으로 분석합니다.
기존 API 기반 분석 대비 수백 배 빠릅니다.

사용법:
    python local_analyzer.py --base-date 20251105 --days 5
    python local_analyzer.py --base-date 20251105 --days 3 --ratio 0.7
"""
import sys
import os
import io
import json
import argparse
from datetime import datetime
from collections import defaultdict

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import pandas as pd
except ImportError:
    print("   [ERROR] pandas가 필요합니다: pip install pandas")
    sys.exit(1)

from config import OUTPUT_DIR, STOCK_LIST_PATH


class LocalAnalyzer:
    """로컬 데이터 기반 업종 + 섹터 분석기"""

    def __init__(self, parquet_path: str = None, json_path: str = None):
        """
        Args:
            parquet_path: OHLC Parquet 파일 경로
            json_path: 종목 리스트 JSON 경로
        """
        self.parquet_path = parquet_path
        self.json_path = json_path or STOCK_LIST_PATH

        self.df_minute: pd.DataFrame = None  # 30분봉 데이터
        self.df_daily: pd.DataFrame = None   # 일봉 데이터
        self.stocks: list[dict] = []          # 종목 리스트
        self.stock_info: dict = {}            # {종목코드: 종목정보}

        self.rising_industries: list[dict] = []  # 상승 업종
        self.rising_sectors: list[dict] = []     # 상승 섹터
        self.matched_stocks: list[dict] = []     # 매칭 종목

    def load_data(self):
        """데이터 로드"""
        print("\n   [LOAD] 데이터 로드 중...")

        # Parquet 로드
        if self.parquet_path and os.path.exists(self.parquet_path):
            self.df_minute = pd.read_parquet(self.parquet_path)
            print(f"   -> Parquet: {len(self.df_minute):,}행, {self.df_minute['종목코드'].nunique()}종목")
        else:
            # 기본 경로에서 찾기
            default_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.parquet') and '30m' in f]
            if default_files:
                self.parquet_path = os.path.join(OUTPUT_DIR, sorted(default_files)[-1])
                self.df_minute = pd.read_parquet(self.parquet_path)
                print(f"   -> Parquet: {os.path.basename(self.parquet_path)}")
                print(f"      {len(self.df_minute):,}행, {self.df_minute['종목코드'].nunique()}종목")
            else:
                print("   [ERROR] Parquet 파일을 찾을 수 없습니다.")
                return False

        # JSON 로드
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.stocks = json.load(f)

        # 종목 정보 딕셔너리 생성
        for stock in self.stocks:
            code = stock.get("단축코드", "")
            self.stock_info[code] = stock

        print(f"   -> JSON: {len(self.stocks)}종목")

        return True

    def convert_to_daily(self):
        """30분봉 → 일봉 변환"""
        print("\n   [CONVERT] 30분봉 → 일봉 변환 중...")

        # 날짜별 OHLC 집계
        df = self.df_minute.copy()

        # 숫자 타입 확인 및 변환
        numeric_cols = ['시가', '고가', '저가', '종가', '거래량']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 일봉 집계
        self.df_daily = df.groupby(['종목코드', '종목명', '날짜']).agg({
            '시가': 'first',
            '고가': 'max',
            '저가': 'min',
            '종가': 'last',
            '거래량': 'sum'
        }).reset_index()

        # 등락률 계산 (전일 대비)
        self.df_daily = self.df_daily.sort_values(['종목코드', '날짜'])
        self.df_daily['전일종가'] = self.df_daily.groupby('종목코드')['종가'].shift(1)
        self.df_daily['등락률'] = ((self.df_daily['종가'] - self.df_daily['전일종가']) / self.df_daily['전일종가'] * 100).round(2)

        print(f"   -> 일봉: {len(self.df_daily):,}행")
        print(f"   -> 날짜 범위: {self.df_daily['날짜'].min()} ~ {self.df_daily['날짜'].max()}")

        return self.df_daily

    def get_trading_days(self, base_date: str, days: int) -> list[str]:
        """기준일 포함 최근 N 거래일 반환"""
        all_dates = sorted(self.df_daily['날짜'].unique())

        # 기준일 이하 날짜만 필터링
        valid_dates = [d for d in all_dates if d <= base_date]

        if len(valid_dates) < days:
            print(f"   [WARN] 요청 {days}일, 가용 {len(valid_dates)}일")
            return valid_dates

        return valid_dates[-days:]

    def analyze_industries(self, base_date: str, days: int) -> list[dict]:
        """업종별 상승 분석"""
        print(f"\n   [INDUSTRY] 업종 {days}일 평균 상승 분석...")

        trading_days = self.get_trading_days(base_date, days)
        if not trading_days:
            print("   [ERROR] 거래일 데이터가 없습니다.")
            return []

        print(f"   -> 분석 기간: {trading_days[0]} ~ {trading_days[-1]}")

        # 해당 기간 데이터 필터링
        df_period = self.df_daily[self.df_daily['날짜'].isin(trading_days)]

        # 업종별 종목 그룹핑 (005~030 실제 산업분류만)
        industry_stocks = defaultdict(list)
        industry_names = {}

        for stock in self.stocks:
            code = stock.get("단축코드", "")
            industry_codes = stock.get("업종코드") or []
            industry_name_list = stock.get("업종명") or []

            for i, ind_code in enumerate(industry_codes):
                # 005~030 범위의 업종코드만 (실제 산업분류)
                if ind_code and ind_code.isdigit() and 5 <= int(ind_code) <= 30:
                    industry_stocks[ind_code].append(code)
                    if ind_code not in industry_names and i < len(industry_name_list):
                        industry_names[ind_code] = industry_name_list[i]

        # 업종별 평균 등락률 계산
        rising_industries = []

        for ind_code, stock_codes in industry_stocks.items():
            # 해당 업종 종목들의 등락률
            df_ind = df_period[df_period['종목코드'].isin(stock_codes)]

            if len(df_ind) == 0:
                continue

            # 종목별 평균 등락률
            stock_avg = df_ind.groupby('종목코드')['등락률'].mean()

            # 업종 전체 평균
            industry_avg = stock_avg.mean()

            if industry_avg > 0:
                rising_industries.append({
                    "ind_code": ind_code,
                    "ind_name": industry_names.get(ind_code, ""),
                    "avg_change": round(industry_avg, 2),
                    "stock_count": len(stock_codes),
                    "analyzed_count": len(stock_avg)
                })

        # 평균 등락률 기준 정렬
        rising_industries.sort(key=lambda x: x["avg_change"], reverse=True)
        self.rising_industries = rising_industries

        print(f"   [RESULT] 상승 업종: {len(rising_industries)}개")

        return rising_industries

    def analyze_sectors(self, base_date: str, days: int, ratio: float = 0.6) -> list[dict]:
        """섹터별 상승 분석"""
        print(f"\n   [SECTOR] 섹터 {days}일 평균 상승 분석 (비율: {ratio*100:.0f}%)...")

        trading_days = self.get_trading_days(base_date, days)
        if not trading_days:
            return []

        # 해당 기간 데이터 필터링
        df_period = self.df_daily[self.df_daily['날짜'].isin(trading_days)]

        # 섹터별 종목 그룹핑
        sector_stocks = defaultdict(list)
        sector_names = {}

        for stock in self.stocks:
            code = stock.get("단축코드", "")
            sector_codes = stock.get("섹터코드") or []
            sector_name_list = stock.get("섹터명") or []

            for i, sec_code in enumerate(sector_codes):
                if sec_code:
                    sector_stocks[sec_code].append(code)
                    if sec_code not in sector_names and i < len(sector_name_list):
                        sector_names[sec_code] = sector_name_list[i]

        # 섹터별 분석
        rising_sectors = []

        for sec_code, stock_codes in sector_stocks.items():
            if len(stock_codes) < 3:  # 최소 3종목
                continue

            # 해당 섹터 종목들의 등락률
            df_sec = df_period[df_period['종목코드'].isin(stock_codes)]

            if len(df_sec) == 0:
                continue

            # 종목별 평균 등락률
            stock_avg = df_sec.groupby('종목코드')['등락률'].mean()

            if len(stock_avg) == 0:
                continue

            # 상승 종목 수 (평균 등락률 > 0)
            rising_count = (stock_avg > 0).sum()
            rise_ratio = rising_count / len(stock_avg)

            # 섹터 전체 평균
            sector_avg = stock_avg.mean()

            # 조건: 비율 이상 상승 AND 평균 양수
            if rise_ratio >= ratio and sector_avg > 0:
                rising_sectors.append({
                    "sec_code": sec_code,
                    "sec_name": sector_names.get(sec_code, ""),
                    "avg_change": round(sector_avg, 2),
                    "rise_ratio": round(rise_ratio * 100, 1),
                    "rising_count": int(rising_count),
                    "analyzed_count": len(stock_avg),
                    "total_count": len(stock_codes)
                })

        # 상승 비율 기준 정렬
        rising_sectors.sort(key=lambda x: x["rise_ratio"], reverse=True)
        self.rising_sectors = rising_sectors

        print(f"   [RESULT] 상승 섹터: {len(rising_sectors)}개")

        return rising_sectors

    def match_stocks(self, base_date: str, days: int) -> list[dict]:
        """업종 + 섹터 동시 상승 종목 매칭"""
        print(f"\n   [MATCH] 업종 + 섹터 동시 상승 종목 탐색...")

        if not self.rising_industries or not self.rising_sectors:
            print("   [WARN] 상승 업종 또는 섹터가 없습니다.")
            return []

        trading_days = self.get_trading_days(base_date, days)
        df_period = self.df_daily[self.df_daily['날짜'].isin(trading_days)]

        # 상승 업종/섹터 코드 집합
        rising_ind_codes = {ind["ind_code"] for ind in self.rising_industries}
        rising_sec_codes = {sec["sec_code"] for sec in self.rising_sectors}

        matched = []

        for stock in self.stocks:
            code = stock.get("단축코드", "")
            name = stock.get("종목명", "")

            # 업종 체크
            ind_codes = stock.get("업종코드") or []
            matched_industries = [c for c in ind_codes if c in rising_ind_codes]

            # 섹터 체크
            sec_codes = stock.get("섹터코드") or []
            matched_sectors = [c for c in sec_codes if c in rising_sec_codes]

            # 둘 다 충족
            if matched_industries and matched_sectors:
                # 해당 종목의 등락률 계산
                df_stock = df_period[df_period['종목코드'] == code]
                if len(df_stock) > 0:
                    avg_change = df_stock['등락률'].mean()

                    matched.append({
                        "code": code,
                        "name": name,
                        "avg_change": round(avg_change, 2),
                        "matched_industries": matched_industries,
                        "matched_sectors": matched_sectors,
                        "industry_count": len(matched_industries),
                        "sector_count": len(matched_sectors)
                    })

        # 등락률 기준 정렬
        matched.sort(key=lambda x: x["avg_change"], reverse=True)
        self.matched_stocks = matched

        print(f"   [RESULT] 매칭 종목: {len(matched)}개")

        return matched

    def run(self, base_date: str, days: int = 5, ratio: float = 0.6):
        """전체 분석 실행"""
        import time
        start_time = time.time()

        print("\n" + "=" * 60)
        print("   LOCAL ANALYZER")
        print("   로컬 데이터 기반 업종 + 섹터 동시 상승 종목 분석")
        print("=" * 60)
        print(f"   기준일: {base_date}")
        print(f"   분석 기간: {days}일")
        print(f"   섹터 상승 비율: {ratio*100:.0f}%")
        print("=" * 60)

        # 1. 데이터 로드
        if not self.load_data():
            return

        # 2. 일봉 변환
        self.convert_to_daily()

        # 3. 업종 분석
        self.analyze_industries(base_date, days)

        # 4. 섹터 분석
        self.analyze_sectors(base_date, days, ratio)

        # 5. 종목 매칭
        self.match_stocks(base_date, days)

        elapsed = time.time() - start_time

        # 결과 출력
        self.print_results()

        print(f"\n   [TIME] 소요 시간: {elapsed:.2f}초")

    def print_results(self):
        """결과 출력"""
        # 업종 결과
        if self.rising_industries:
            print("\n" + "-" * 70)
            print(f"   {'업종코드':<8} {'업종명':<20} {'평균등락률':>10} {'종목수':>8}")
            print("-" * 70)
            for ind in self.rising_industries[:10]:
                print(f"   {ind['ind_code']:<8} {ind['ind_name']:<20} {ind['avg_change']:>+9.2f}% {ind['analyzed_count']:>7}개")
            if len(self.rising_industries) > 10:
                print(f"   ... 외 {len(self.rising_industries) - 10}개")
            print("-" * 70)

        # 섹터 결과
        if self.rising_sectors:
            print("\n" + "-" * 80)
            print(f"   {'섹터코드':<8} {'섹터명':<20} {'상승비율':>8} {'평균등락':>10} {'상승/분석':>12}")
            print("-" * 80)
            for sec in self.rising_sectors[:10]:
                print(f"   {sec['sec_code']:<8} {sec['sec_name'][:18]:<20} {sec['rise_ratio']:>7.1f}% {sec['avg_change']:>+9.2f}% {sec['rising_count']:>4}/{sec['analyzed_count']:<4}")
            if len(self.rising_sectors) > 10:
                print(f"   ... 외 {len(self.rising_sectors) - 10}개")
            print("-" * 80)

        # 매칭 종목 결과
        if self.matched_stocks:
            print("\n" + "-" * 80)
            print(f"   {'종목코드':<8} {'종목명':<16} {'평균등락률':>10} {'업종수':>8} {'섹터수':>8}")
            print("-" * 80)
            for stock in self.matched_stocks[:20]:
                print(f"   {stock['code']:<8} {stock['name'][:14]:<16} {stock['avg_change']:>+9.2f}% {stock['industry_count']:>7}개 {stock['sector_count']:>7}개")
            if len(self.matched_stocks) > 20:
                print(f"   ... 외 {len(self.matched_stocks) - 20}개")
            print("-" * 80)


def parse_args():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="로컬 데이터 기반 업종 + 섹터 동시 상승 종목 분석",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python local_analyzer.py --base-date 20251105 --days 5
    python local_analyzer.py --base-date 20251105 --days 3 --ratio 0.7
    python local_analyzer.py --base-date 20251105 --parquet output/ohlc_xxx.parquet
        """
    )

    parser.add_argument(
        "--base-date",
        type=str,
        required=True,
        help="기준 날짜 (YYYYMMDD)"
    )
    parser.add_argument(
        "--days",
        type=int,
        default=5,
        help="분석 기간 (기본값: 5일)"
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.6,
        help="섹터 상승 판정 비율 (기본값: 0.6 = 60%%)"
    )
    parser.add_argument(
        "--parquet",
        type=str,
        default=None,
        help="Parquet 파일 경로"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Parquet 경로 처리
    parquet_path = args.parquet
    if parquet_path and not os.path.isabs(parquet_path):
        parquet_path = os.path.join(OUTPUT_DIR, parquet_path)

    analyzer = LocalAnalyzer(parquet_path=parquet_path)
    analyzer.run(args.base_date, args.days, args.ratio)


if __name__ == "__main__":
    main()
