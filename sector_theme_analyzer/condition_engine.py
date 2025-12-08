"""
조건 평가 엔진 (Condition Engine)

각 조건(A, B, C, D, E, F...)을 평가하여 충족 종목코드 집합을 반환합니다.

조건 목록:
    A: 섹터+업종 동시 상승 (N일 평균)
    B: 60봉 신고거래대금
    C: 거래량 회전율 상위 N종목
    D: 이평 정배열 (단기 > 중기 > 장기)
    E: N봉 신고가 대비 등락률 범위
    F: 거래량 비교 (N봉 전 대비)

사용법:
    engine = ConditionEngine(parquet_path, json_path)
    engine.load_data()

    # 개별 조건 평가
    stocks_A = engine.condition_A("20251205", days=5)
    stocks_B = engine.condition_B("20251205")

    # 조건 조합
    result = stocks_A & stocks_B  # AND
    result = stocks_A | stocks_B  # OR
"""
import sys
import os
import io
import json
from datetime import datetime
from collections import defaultdict
from typing import Optional

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'buffer') and not isinstance(sys.stdout, io.TextIOWrapper):
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, 'buffer') and not isinstance(sys.stderr, io.TextIOWrapper):
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("   [ERROR] pandas, numpy가 필요합니다: pip install pandas numpy")
    sys.exit(1)

from config import OUTPUT_DIR, STOCK_LIST_PATH


class ConditionEngine:
    """조건 평가 엔진"""

    def __init__(self, parquet_path: str = None, json_path: str = None):
        """
        Args:
            parquet_path: OHLC Parquet 파일 경로 (30분봉)
            json_path: 종목 리스트 JSON 경로
        """
        self.parquet_path = parquet_path
        self.json_path = json_path or STOCK_LIST_PATH

        self.df_30m: pd.DataFrame = None    # 30분봉 원본 데이터
        self.df_daily: pd.DataFrame = None  # 일봉 데이터
        self.stocks: list[dict] = []         # 종목 리스트
        self.stock_info: dict = {}           # {종목코드: 종목정보}

        # 캐시
        self._ma_cache: dict = {}            # 이동평균 캐시
        self._trading_days_cache: dict = {}  # 거래일 캐시

    def load_data(self) -> bool:
        """데이터 로드"""
        print("\n   [LOAD] 데이터 로드 중...")

        # Parquet 로드
        if self.parquet_path and os.path.exists(self.parquet_path):
            self.df_30m = pd.read_parquet(self.parquet_path)
        else:
            # 기본 경로에서 찾기
            default_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.parquet') and '30m' in f]
            if default_files:
                self.parquet_path = os.path.join(OUTPUT_DIR, sorted(default_files)[-1])
                self.df_30m = pd.read_parquet(self.parquet_path)
            else:
                print("   [ERROR] Parquet 파일을 찾을 수 없습니다.")
                return False

        print(f"   -> Parquet: {len(self.df_30m):,}행, {self.df_30m['종목코드'].nunique()}종목")

        # JSON 로드
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.stocks = json.load(f)

        # 종목 정보 딕셔너리 생성
        for stock in self.stocks:
            code = stock.get("단축코드", "")
            self.stock_info[code] = stock

        print(f"   -> JSON: {len(self.stocks)}종목")

        # 일봉 변환
        self._convert_to_daily()

        return True

    def _convert_to_daily(self):
        """30분봉 → 일봉 변환"""
        print("   [CONVERT] 30분봉 → 일봉 변환 중...")

        df = self.df_30m.copy()

        # 숫자 타입 변환
        numeric_cols = ['시가', '고가', '저가', '종가', '거래량', '거래대금']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 일봉 집계
        self.df_daily = df.groupby(['종목코드', '종목명', '날짜']).agg({
            '시가': 'first',
            '고가': 'max',
            '저가': 'min',
            '종가': 'last',
            '거래량': 'sum',
            '거래대금': 'sum'
        }).reset_index()

        # 정렬
        self.df_daily = self.df_daily.sort_values(['종목코드', '날짜'])

        # 전일종가, 등락률 계산
        self.df_daily['전일종가'] = self.df_daily.groupby('종목코드')['종가'].shift(1)
        self.df_daily['등락률'] = ((self.df_daily['종가'] - self.df_daily['전일종가']) / self.df_daily['전일종가'] * 100).round(2)

        print(f"   -> 일봉: {len(self.df_daily):,}행")

    def get_trading_days(self, base_date: str, days: int) -> list[str]:
        """기준일 포함 최근 N 거래일 반환"""
        cache_key = (base_date, days)
        if cache_key in self._trading_days_cache:
            return self._trading_days_cache[cache_key]

        all_dates = sorted(self.df_daily['날짜'].unique())
        valid_dates = [d for d in all_dates if d <= base_date]

        result = valid_dates[-days:] if len(valid_dates) >= days else valid_dates
        self._trading_days_cache[cache_key] = result
        return result

    def get_all_trading_days(self) -> list[str]:
        """전체 거래일 목록 반환"""
        return sorted(self.df_daily['날짜'].unique())

    # =========================================================================
    # 조건 A: 섹터+업종 동시 상승
    # =========================================================================
    def condition_A(self, base_date: str, days: int = 5, ratio: float = 0.6) -> set[str]:
        """
        조건 A: 섹터+업종 N일 동시 상승

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 분석 기간 (기본 5일)
            ratio: 섹터 상승 판정 비율 (기본 60%)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        trading_days = self.get_trading_days(base_date, days)
        if not trading_days:
            return set()

        df_period = self.df_daily[self.df_daily['날짜'].isin(trading_days)]

        # 상승 업종 찾기
        rising_industries = self._find_rising_industries(df_period)

        # 상승 섹터 찾기
        rising_sectors = self._find_rising_sectors(df_period, ratio)

        if not rising_industries or not rising_sectors:
            return set()

        # 동시 충족 종목
        rising_ind_codes = {ind["code"] for ind in rising_industries}
        rising_sec_codes = {sec["code"] for sec in rising_sectors}

        # 해당 기간에 거래 데이터가 있는 종목코드 집합
        valid_codes = set(df_period['종목코드'].unique())

        matched = set()
        for stock in self.stocks:
            code = stock.get("단축코드", "")

            # 해당 기간에 거래 데이터가 있는 종목만 (local_analyzer.py와 동일)
            if code not in valid_codes:
                continue

            ind_codes = stock.get("업종코드") or []
            sec_codes = stock.get("섹터코드") or []

            has_rising_ind = any(c in rising_ind_codes for c in ind_codes)
            has_rising_sec = any(c in rising_sec_codes for c in sec_codes)

            if has_rising_ind and has_rising_sec:
                matched.add(code)

        return matched

    def _find_rising_industries(self, df_period: pd.DataFrame) -> list[dict]:
        """상승 업종 찾기"""
        industry_stocks = defaultdict(list)
        industry_names = {}

        for stock in self.stocks:
            code = stock.get("단축코드", "")
            ind_codes = stock.get("업종코드") or []
            ind_names = stock.get("업종명") or []

            for i, ind_code in enumerate(ind_codes):
                if ind_code and ind_code.isdigit() and 5 <= int(ind_code) <= 30:
                    industry_stocks[ind_code].append(code)
                    if ind_code not in industry_names and i < len(ind_names):
                        industry_names[ind_code] = ind_names[i]

        rising = []
        for ind_code, stock_codes in industry_stocks.items():
            df_ind = df_period[df_period['종목코드'].isin(stock_codes)]
            if len(df_ind) == 0:
                continue

            stock_avg = df_ind.groupby('종목코드')['등락률'].mean()
            industry_avg = stock_avg.mean()

            if industry_avg > 0:
                rising.append({
                    "code": ind_code,
                    "name": industry_names.get(ind_code, ""),
                    "avg_change": industry_avg
                })

        return rising

    def _find_rising_sectors(self, df_period: pd.DataFrame, ratio: float) -> list[dict]:
        """상승 섹터 찾기"""
        sector_stocks = defaultdict(list)
        sector_names = {}

        for stock in self.stocks:
            code = stock.get("단축코드", "")
            sec_codes = stock.get("섹터코드") or []
            sec_names = stock.get("섹터명") or []

            for i, sec_code in enumerate(sec_codes):
                if sec_code:
                    sector_stocks[sec_code].append(code)
                    if sec_code not in sector_names and i < len(sec_names):
                        sector_names[sec_code] = sec_names[i]

        rising = []
        for sec_code, stock_codes in sector_stocks.items():
            if len(stock_codes) < 3:
                continue

            df_sec = df_period[df_period['종목코드'].isin(stock_codes)]
            if len(df_sec) == 0:
                continue

            stock_avg = df_sec.groupby('종목코드')['등락률'].mean()
            if len(stock_avg) == 0:
                continue

            rising_count = (stock_avg > 0).sum()
            rise_ratio = rising_count / len(stock_avg)
            sector_avg = stock_avg.mean()

            if rise_ratio >= ratio and sector_avg > 0:
                rising.append({
                    "code": sec_code,
                    "name": sector_names.get(sec_code, ""),
                    "avg_change": sector_avg,
                    "rise_ratio": rise_ratio
                })

        return rising

    # =========================================================================
    # 조건 B: 60봉 신고거래대금
    # =========================================================================
    def condition_B(self, base_date: str, bars: int = 60) -> set[str]:
        """
        조건 B: N봉 중 신고거래대금

        해당일의 거래대금이 최근 N봉 중 최고인 종목

        Args:
            base_date: 기준일 (YYYYMMDD)
            bars: 비교 봉 수 (기본 60봉 = 약 5일)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        # 30분봉 데이터에서 해당일 이전 데이터 필터링
        df = self.df_30m[self.df_30m['날짜'] <= base_date].copy()
        df['거래대금'] = pd.to_numeric(df['거래대금'], errors='coerce')

        # groupby 벡터화 연산으로 최적화
        def check_new_high_value(group):
            if len(group) < bars:
                return None
            recent = group.tail(bars)
            current_value = recent.iloc[-1]['거래대금']
            max_value = recent['거래대금'].max()
            if current_value >= max_value and current_value > 0:
                return group.name
            return None

        result = df.groupby('종목코드', group_keys=False).apply(check_new_high_value, include_groups=False)
        matched = set(result.dropna().values)

        return matched

    # =========================================================================
    # 조건 C: 거래량 회전율 상위
    # =========================================================================
    def condition_C(self, base_date: str, min_rate: float = 0.0, top_n: int = 100) -> set[str]:
        """
        조건 C: 거래량 회전율 상위 N종목

        회전율 = 당일 거래량 / 상장주식수 * 100

        Args:
            base_date: 기준일 (YYYYMMDD)
            min_rate: 최소 회전율 % (기본 0%)
            top_n: 상위 N종목 (기본 100)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        df_day = self.df_daily[self.df_daily['날짜'] == base_date].copy()

        if len(df_day) == 0:
            return set()

        # 상장주식수 추가
        df_day['주식수'] = df_day['종목코드'].apply(
            lambda x: self.stock_info.get(x, {}).get('주식수', 0)
        )

        # 회전율 계산
        df_day['회전율'] = df_day.apply(
            lambda row: (row['거래량'] / row['주식수'] * 100) if row['주식수'] > 0 else 0,
            axis=1
        )

        # 최소 회전율 필터링
        df_filtered = df_day[df_day['회전율'] >= min_rate]

        # 상위 N개
        df_top = df_filtered.nlargest(top_n, '회전율')

        return set(df_top['종목코드'])

    # =========================================================================
    # 조건 D: 이평 정배열
    # =========================================================================
    def condition_D(self, base_date: str, short: int = 20, mid: int = 60, long: int = 120) -> set[str]:
        """
        조건 D: 이동평균 정배열

        단기 MA > 중기 MA > 장기 MA (종가 기준)

        Args:
            base_date: 기준일 (YYYYMMDD)
            short: 단기 이평 기간 (기본 20)
            mid: 중기 이평 기간 (기본 60)
            long: 장기 이평 기간 (기본 120)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        # 이동평균 계산 (캐시 활용)
        df = self._get_ma_data(base_date, [short, mid, long])

        if df is None or len(df) == 0:
            return set()

        # 기준일 데이터
        df_day = df[df['날짜'] == base_date]

        # 정배열 조건
        ma_short = f'MA{short}'
        ma_mid = f'MA{mid}'
        ma_long = f'MA{long}'

        if ma_short not in df_day.columns or ma_mid not in df_day.columns or ma_long not in df_day.columns:
            return set()

        df_aligned = df_day[
            (df_day[ma_short] > df_day[ma_mid]) &
            (df_day[ma_mid] > df_day[ma_long])
        ]

        return set(df_aligned['종목코드'])

    def _get_ma_data(self, base_date: str, periods: list[int]) -> pd.DataFrame:
        """이동평균 데이터 계산 (캐시)"""
        cache_key = tuple(sorted(periods))

        if cache_key not in self._ma_cache:
            df = self.df_daily.copy()

            for period in periods:
                ma_col = f'MA{period}'
                df[ma_col] = df.groupby('종목코드')['종가'].transform(
                    lambda x: x.rolling(window=period, min_periods=period).mean()
                )

            self._ma_cache[cache_key] = df

        return self._ma_cache[cache_key]

    # =========================================================================
    # 조건 E: N봉 신고가 대비 등락률
    # =========================================================================
    def condition_E(self, base_date: str, bars: int = 60, min_pct: float = -5.0, max_pct: float = 0.0) -> set[str]:
        """
        조건 E: N봉 신고가 대비 현재가 등락률 범위

        Args:
            base_date: 기준일 (YYYYMMDD)
            bars: 비교 봉 수 (기본 60)
            min_pct: 최소 등락률 % (기본 -5%)
            max_pct: 최대 등락률 % (기본 0%)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        # 30분봉 데이터
        df = self.df_30m[self.df_30m['날짜'] <= base_date].copy()
        df['고가'] = pd.to_numeric(df['고가'], errors='coerce')
        df['종가'] = pd.to_numeric(df['종가'], errors='coerce')

        # groupby 벡터화 연산으로 최적화
        def check_high_pct(group):
            if len(group) < bars:
                return None
            recent = group.tail(bars)
            high_n = recent['고가'].max()
            current_close = recent.iloc[-1]['종가']
            if high_n <= 0:
                return None
            pct = (current_close - high_n) / high_n * 100
            if min_pct <= pct <= max_pct:
                return group.name
            return None

        result = df.groupby('종목코드', group_keys=False).apply(check_high_pct, include_groups=False)
        matched = set(result.dropna().values)

        return matched

    # =========================================================================
    # 조건 F: 거래량 비교
    # =========================================================================
    def condition_F(self, base_date: str, compare_bars: int = 5, min_ratio: float = 150, max_ratio: float = 9000) -> set[str]:
        """
        조건 F: 거래량 비교 (N봉전 대비)

        (현재 5봉 평균 거래량) / (N봉전 5봉 평균 거래량) * 100

        Args:
            base_date: 기준일 (YYYYMMDD)
            compare_bars: 비교 기준 봉 간격 (기본 5)
            min_ratio: 최소 비율 % (기본 150%)
            max_ratio: 최대 비율 % (기본 9000%)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        # 30분봉 데이터
        df = self.df_30m[self.df_30m['날짜'] <= base_date].copy()
        df['거래량'] = pd.to_numeric(df['거래량'], errors='coerce')

        # groupby 벡터화 연산으로 최적화
        def check_volume_ratio(group):
            required_len = compare_bars * 2 + 5
            if len(group) < required_len:
                return None
            recent = group.tail(compare_bars * 3)
            if len(recent) < compare_bars * 2 + 5:
                return None
            vol_ma5_now = recent['거래량'].tail(5).mean()
            vol_ma5_ago = recent['거래량'].iloc[-(compare_bars + 5):-(compare_bars)].mean()
            if vol_ma5_ago <= 0:
                return None
            ratio = vol_ma5_now / vol_ma5_ago * 100
            if min_ratio <= ratio <= max_ratio:
                return group.name
            return None

        result = df.groupby('종목코드', group_keys=False).apply(check_volume_ratio, include_groups=False)
        matched = set(result.dropna().values)

        return matched

    # =========================================================================
    # 조건 G: 거래량 비율 범위 (당일/N일평균)
    # =========================================================================
    def condition_G(self, base_date: str, days: int = 20, min_ratio: float = 100, max_ratio: float = 500) -> set[str]:
        """
        조건 G: 거래량 비율 X% ~ Y% 범위 종목

        비율 = (당일 거래량 / N일 평균 거래량) * 100

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 평균 계산 기간 (기본 20일)
            min_ratio: 최소 비율 % (기본 100% = 평균과 동일)
            max_ratio: 최대 비율 % (기본 500% = 평균의 5배)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        trading_days = self.get_trading_days(base_date, days + 1)
        if len(trading_days) < 2:
            return set()

        df_period = self.df_daily[self.df_daily['날짜'].isin(trading_days)].copy()

        matched = set()
        for code, group in df_period.groupby('종목코드'):
            if len(group) < 2:
                continue
            group = group.sort_values('날짜')
            today = group[group['날짜'] == base_date]
            if len(today) == 0:
                continue
            today_vol = today.iloc[0]['거래량']
            avg_vol = group[group['날짜'] != base_date]['거래량'].mean()
            if avg_vol <= 0:
                continue
            ratio = (today_vol / avg_vol) * 100
            if min_ratio <= ratio <= max_ratio:
                matched.add(code)

        return matched

    # =========================================================================
    # 유틸리티 메서드
    # =========================================================================
    def evaluate(self, condition_id: str, base_date: str, params: dict = None) -> set[str]:
        """
        조건 ID로 평가

        Args:
            condition_id: 조건 ID (A, B, C, D, E, F)
            base_date: 기준일
            params: 조건별 파라미터 (없으면 기본값 사용)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        params = params or {}

        condition_map = {
            'A': lambda: self.condition_A(base_date, **params),
            'B': lambda: self.condition_B(base_date, **params),
            'C': lambda: self.condition_C(base_date, **params),
            'D': lambda: self.condition_D(base_date, **params),
            'E': lambda: self.condition_E(base_date, **params),
            'F': lambda: self.condition_F(base_date, **params),
            'G': lambda: self.condition_G(base_date, **params),
        }

        if condition_id.upper() not in condition_map:
            print(f"   [WARN] 알 수 없는 조건: {condition_id}")
            return set()

        return condition_map[condition_id.upper()]()

    def get_stock_name(self, code: str) -> str:
        """종목코드 → 종목명"""
        return self.stock_info.get(code, {}).get("종목명", code)

    def get_price_data(self, code: str, base_date: str, days: int = 10) -> pd.DataFrame:
        """특정 종목의 가격 데이터 반환"""
        trading_days = self.get_trading_days(base_date, days)
        df = self.df_daily[
            (self.df_daily['종목코드'] == code) &
            (self.df_daily['날짜'].isin(trading_days))
        ]
        return df.sort_values('날짜')


# 조건 설명 딕셔너리
CONDITION_DESCRIPTIONS = {
    'A': '섹터+업종 N일 동시 상승',
    'B': 'N봉 신고거래대금',
    'C': '거래량 회전율 상위 N종목',
    'D': '이평 정배열 (단기>중기>장기)',
    'E': 'N봉 신고가 대비 등락률 범위',
    'F': 'N봉전 대비 거래량 비율',
    'G': '거래량 비율 X%~Y% (당일/N일평균)',
}


if __name__ == "__main__":
    # 테스트
    engine = ConditionEngine()
    if engine.load_data():
        base_date = "20251205"

        print("\n[테스트] 각 조건 평가")
        print("=" * 60)

        for cond_id in ['A', 'B', 'C', 'D', 'E', 'F']:
            result = engine.evaluate(cond_id, base_date)
            print(f"   조건 {cond_id}: {len(result):>4}개 종목")

        print("=" * 60)
