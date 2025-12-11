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

# ETF 파일 경로 (지수 조건용)
ETF_KOSPI_PATH = os.path.join(OUTPUT_DIR, "etf_069500_KOSPI200_daily.parquet")
ETF_KOSDAQ_PATH = os.path.join(OUTPUT_DIR, "etf_229200_KOSDAQ150_daily.parquet")


class ConditionEngine:
    """조건 평가 엔진"""

    def __init__(self, parquet_path: str = None, json_path: str = None):
        """
        Args:
            parquet_path: 일봉 OHLC Parquet 파일 경로
            json_path: 종목 리스트 JSON 경로
        """
        self.parquet_path = parquet_path
        self.json_path = json_path or STOCK_LIST_PATH

        self.df_daily: pd.DataFrame = None  # 일봉 데이터
        self.stocks: list[dict] = []         # 종목 리스트
        self.stock_info: dict = {}           # {종목코드: 종목정보}

        # 캐시
        self._ma_cache: dict = {}            # 이동평균 캐시
        self._trading_days_cache: dict = {}  # 거래일 캐시
        self._indicator_cache: dict = {}     # GT 지표 캐시 (MACD, RSI 등)
        self._condition_cache: dict = {}     # 조건 결과 캐시 {(condition_id, base_date, params_hash): result}

        # ETF 데이터 (지수 조건용)
        self.df_kospi_etf: pd.DataFrame = None
        self.df_kosdaq_etf: pd.DataFrame = None

    def load_data(self) -> bool:
        """데이터 로드 (일봉 전용)"""
        print("\n   [LOAD] 데이터 로드 중...")

        # Parquet 로드
        if self.parquet_path and os.path.exists(self.parquet_path):
            df = pd.read_parquet(self.parquet_path)
        else:
            # 기본 경로에서 일봉 파일 찾기 (30m 제외, 회전율 포함 파일 우선)
            all_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.parquet') and '30m' not in f]
            turnover_files = [f for f in all_files if 'with_turnover' in f]
            default_files = turnover_files if turnover_files else all_files

            if default_files:
                self.parquet_path = os.path.join(OUTPUT_DIR, sorted(default_files)[-1])
                df = pd.read_parquet(self.parquet_path)
            else:
                print("   [ERROR] 일봉 Parquet 파일을 찾을 수 없습니다.")
                return False

        print(f"   -> Parquet: {len(df):,}행, {df['종목코드'].nunique()}종목")

        # JSON 로드
        with open(self.json_path, "r", encoding="utf-8") as f:
            self.stocks = json.load(f)

        # 종목 정보 딕셔너리 생성
        for stock in self.stocks:
            code = stock.get("단축코드", "")
            self.stock_info[code] = stock

        print(f"   -> JSON: {len(self.stocks)}종목")

        # 일봉 데이터 처리
        self._load_daily(df)

        # ETF 데이터 로드 (GT 지수 조건용)
        self._load_etf_data()

        return True

    def _load_etf_data(self):
        """ETF 데이터 로드 (GT 지수 조건용)"""
        if os.path.exists(ETF_KOSPI_PATH):
            self.df_kospi_etf = pd.read_parquet(ETF_KOSPI_PATH)
            self.df_kospi_etf = self.df_kospi_etf.sort_values('날짜')
            print(f"   -> KOSPI ETF: {len(self.df_kospi_etf)}행")
        else:
            print(f"   [WARN] KOSPI ETF 파일 없음: {ETF_KOSPI_PATH}")

        if os.path.exists(ETF_KOSDAQ_PATH):
            self.df_kosdaq_etf = pd.read_parquet(ETF_KOSDAQ_PATH)
            self.df_kosdaq_etf = self.df_kosdaq_etf.sort_values('날짜')
            print(f"   -> KOSDAQ ETF: {len(self.df_kosdaq_etf)}행")

    def _load_daily(self, df: pd.DataFrame):
        """일봉 데이터 로드 및 전처리"""
        print("   [DAILY] 일봉 데이터 로드")

        # 숫자 타입 변환
        numeric_cols = ['시가', '고가', '저가', '종가', '거래량', '거래대금', '발행주식수', '거래회전율']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # 정렬
        df = df.sort_values(['종목코드', '날짜'])

        # 전일종가, 등락률 계산 (기존에 없으면 생성)
        if '전일종가' not in df.columns or df['전일종가'].isna().all():
            df['전일종가'] = df.groupby('종목코드')['종가'].shift(1)
        if '등락률' not in df.columns or df['등락률'].isna().all():
            df['등락률'] = ((df['종가'] - df['전일종가']) / df['전일종가'] * 100).round(2)

        self.df_daily = df

        # 회전율 컬럼 존재 여부 출력
        has_turnover = '거래회전율' in df.columns and not df['거래회전율'].isna().all()
        print(f"   -> 일봉: {len(self.df_daily):,}행")
        if has_turnover:
            print(f"   -> 회전율 컬럼: 있음 (평균 {df['거래회전율'].mean():.2f}%)")

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
    def condition_A(self, base_date: str, days: int = 5, ratio: float = 0.6, with_details: bool = False):
        """
        조건 A: 섹터+업종 N일 연속 상승

        섹터와 업종 모두 N일 동안 매일 평균 등락률이 양수인 경우에만 충족

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 연속 상승 기간 (기본 5일)
            ratio: (미사용, 하위 호환성 유지)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        trading_days = self.get_trading_days(base_date, days)
        if not trading_days:
            return {} if with_details else set()

        df_period = self.df_daily[self.df_daily['날짜'].isin(trading_days)]

        # 상승 업종 찾기
        rising_industries = self._find_rising_industries(df_period)

        # 상승 섹터 찾기
        rising_sectors = self._find_rising_sectors(df_period, ratio)

        if not rising_industries or not rising_sectors:
            return {} if with_details else set()

        # 동시 충족 종목
        rising_ind_codes = {ind["code"] for ind in rising_industries}
        rising_sec_codes = {sec["code"] for sec in rising_sectors}

        # 해당 기간에 거래 데이터가 있는 종목코드 집합
        valid_codes = set(df_period['종목코드'].unique())

        matched = set()
        details = {}
        for stock in self.stocks:
            code = stock.get("단축코드", "")

            # 해당 기간에 거래 데이터가 있는 종목만 (local_analyzer.py와 동일)
            if code not in valid_codes:
                continue

            ind_codes = stock.get("업종코드") or []
            sec_codes = stock.get("섹터코드") or []

            matched_ind = [c for c in ind_codes if c in rising_ind_codes]
            matched_sec = [c for c in sec_codes if c in rising_sec_codes]

            if matched_ind and matched_sec:
                matched.add(code)
                if with_details:
                    details[code] = {
                        '업종수': len(matched_ind),
                        '섹터수': len(matched_sec)
                    }

        return details if with_details else matched

    def _find_rising_industries(self, df_period: pd.DataFrame) -> list[dict]:
        """연속 상승 업종 찾기 (매일 양수)"""
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
        trading_days = sorted(df_period['날짜'].unique())

        for ind_code, stock_codes in industry_stocks.items():
            df_ind = df_period[df_period['종목코드'].isin(stock_codes)]
            if len(df_ind) == 0:
                continue

            # 날짜별 업종 평균 등락률 계산
            daily_avg = df_ind.groupby('날짜')['등락률'].mean()

            # 모든 날짜에서 양수인지 확인 (연속 상승)
            if len(daily_avg) == len(trading_days) and (daily_avg > 0).all():
                rising.append({
                    "code": ind_code,
                    "name": industry_names.get(ind_code, ""),
                    "avg_change": daily_avg.mean(),
                    "consecutive_days": len(trading_days)
                })

        return rising

    def _find_rising_sectors(self, df_period: pd.DataFrame, ratio: float) -> list[dict]:
        """연속 상승 섹터 찾기 (매일 양수)"""
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
        trading_days = sorted(df_period['날짜'].unique())

        for sec_code, stock_codes in sector_stocks.items():
            if len(stock_codes) < 3:
                continue

            df_sec = df_period[df_period['종목코드'].isin(stock_codes)]
            if len(df_sec) == 0:
                continue

            # 날짜별 섹터 평균 등락률 계산
            daily_avg = df_sec.groupby('날짜')['등락률'].mean()

            # 모든 날짜에서 양수인지 확인 (연속 상승)
            if len(daily_avg) == len(trading_days) and (daily_avg > 0).all():
                rising.append({
                    "code": sec_code,
                    "name": sector_names.get(sec_code, ""),
                    "avg_change": daily_avg.mean(),
                    "consecutive_days": len(trading_days)
                })

        return rising

    # =========================================================================
    # 조건 B: N일 신고거래대금
    # =========================================================================
    def condition_B(self, base_date: str, days: int = 60, with_details: bool = False):
        """
        조건 B: N일 중 신고거래대금

        해당일의 거래대금이 최근 N일 중 최고인 종목

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 비교 일수 (기본 60일)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: rolling max 사용
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # N일 rolling max 계산 (groupby transform)
        rolling_max = df.groupby('종목코드')['거래대금'].transform(
            lambda x: x.rolling(window=days, min_periods=days).max()
        )

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]

        # 조건: 현재 거래대금 == N일 최대 거래대금
        current_val = df_day['거래대금'].values
        max_val = rolling_max.values[day_mask]
        mask = (current_val >= max_val) & (current_val > 0)

        codes = df_day['종목코드'].values[mask]
        values = current_val[mask]
        max_values = max_val[mask]

        if with_details:
            return {
                code: {'거래대금': int(val), 'N일최대': int(mx)}
                for code, val, mx in zip(codes, values, max_values)
            }
        return set(codes)

    # =========================================================================
    # 조건 C: 거래량 회전율 상위
    # =========================================================================
    def condition_C(self, base_date: str, min_rate: float = 0.0, top_n: int = 100, with_details: bool = False):
        """
        조건 C: 거래량 회전율 상위 N종목

        회전율 = 당일 거래량 / 상장주식수 * 100

        Args:
            base_date: 기준일 (YYYYMMDD)
            min_rate: 최소 회전율 % (기본 0%)
            top_n: 상위 N종목 (기본 100)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        df_day = self.df_daily[self.df_daily['날짜'] == base_date]

        if len(df_day) == 0:
            return {} if with_details else set()

        # 벡터화: 발행주식수 매핑 (apply 대신 map 사용)
        stock_shares = {code: info.get('발행주식수', 0) for code, info in self.stock_info.items()}
        shares = df_day['종목코드'].map(stock_shares).fillna(0)

        # 벡터화: 회전율 계산 (apply 대신 벡터 연산)
        turnover = np.where(shares > 0, df_day['거래량'] / shares * 100, 0)

        # 임시 DataFrame 생성 (필터링용)
        result_df = pd.DataFrame({
            '종목코드': df_day['종목코드'].values,
            '회전율': turnover
        })

        # 최소 회전율 필터링 및 상위 N개
        result_df = result_df[result_df['회전율'] >= min_rate].nlargest(top_n, '회전율')

        if with_details:
            return {
                row['종목코드']: {'회전율': round(row['회전율'], 2)}
                for _, row in result_df.iterrows()
            }
        return set(result_df['종목코드'])

    # =========================================================================
    # 조건 D: 이평 정배열
    # =========================================================================
    def condition_D(self, base_date: str, short: int = 20, mid: int = 60, long: int = 120, with_details: bool = False):
        """
        조건 D: 이동평균 정배열

        단기 MA > 중기 MA > 장기 MA (종가 기준)

        Args:
            base_date: 기준일 (YYYYMMDD)
            short: 단기 이평 기간 (기본 20)
            mid: 중기 이평 기간 (기본 60)
            long: 장기 이평 기간 (기본 120)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 이동평균 계산 (캐시 활용)
        df = self._get_ma_data(base_date, [short, mid, long])

        if df is None or len(df) == 0:
            return {} if with_details else set()

        # 기준일 데이터
        df_day = df[df['날짜'] == base_date]

        # 정배열 조건
        ma_short = f'MA{short}'
        ma_mid = f'MA{mid}'
        ma_long = f'MA{long}'

        if ma_short not in df_day.columns or ma_mid not in df_day.columns or ma_long not in df_day.columns:
            return {} if with_details else set()

        df_aligned = df_day[
            (df_day[ma_short] > df_day[ma_mid]) &
            (df_day[ma_mid] > df_day[ma_long])
        ]

        if with_details:
            return {
                row['종목코드']: {
                    f'MA{short}': int(row[ma_short]),
                    f'MA{mid}': int(row[ma_mid]),
                    f'MA{long}': int(row[ma_long])
                }
                for _, row in df_aligned.iterrows()
            }
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
    # 조건 E: N일 신고가 대비 등락률
    # =========================================================================
    def condition_E(self, base_date: str, days: int = 60, min_pct: float = -5.0, max_pct: float = 0.0, with_details: bool = False):
        """
        조건 E: N일 신고가 대비 현재가 등락률 범위

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 비교 일수 (기본 60일)
            min_pct: 최소 등락률 % (기본 -5%)
            max_pct: 최대 등락률 % (기본 0%)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: rolling max 사용 (df.copy() 제거)
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # N일 rolling max 고가 계산
        rolling_high = df.groupby('종목코드')['고가'].transform(
            lambda x: x.rolling(window=days, min_periods=days).max()
        )

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]

        # 신고가 대비 등락률 계산
        close_values = df_day['종가'].values
        high_values = rolling_high.values[day_mask]

        # 0 나누기 방지
        with np.errstate(divide='ignore', invalid='ignore'):
            pct = np.where(high_values > 0, (close_values - high_values) / high_values * 100, np.nan)

        # 조건: min_pct <= 등락률 <= max_pct
        mask = (pct >= min_pct) & (pct <= max_pct) & ~np.isnan(pct)
        codes = df_day['종목코드'].values[mask]
        close_filtered = close_values[mask]
        high_filtered = high_values[mask]
        pct_filtered = pct[mask]

        if with_details:
            return {
                code: {
                    '신고가': int(high),
                    '현재가': int(close),
                    '신고가대비': round(p, 2)
                }
                for code, high, close, p in zip(codes, high_filtered, close_filtered, pct_filtered)
            }
        return set(codes)

    # =========================================================================
    # 조건 F: 거래량 비교
    # =========================================================================
    def condition_F(self, base_date: str, compare_days: int = 5, min_ratio: float = 150, max_ratio: float = 9000, with_details: bool = False):
        """
        조건 F: 거래량 비교 (N일전 대비)

        (현재 5일 평균 거래량) / (N일전 5일 평균 거래량) * 100

        Args:
            base_date: 기준일 (YYYYMMDD)
            compare_days: 비교 기준 일수 간격 (기본 5일)
            min_ratio: 최소 비율 % (기본 150%)
            max_ratio: 최대 비율 % (기본 9000%)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: rolling mean 사용 (df.copy() 제거)
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 5일 이동평균 거래량 계산
        vol_ma5 = df.groupby('종목코드')['거래량'].transform(
            lambda x: x.rolling(window=5, min_periods=5).mean()
        )

        # N일전 5일 이동평균 (shift로 N일전 값)
        vol_ma5_ago = df.groupby('종목코드').apply(
            lambda x: x.assign(vol_ma5_shifted=vol_ma5.loc[x.index].shift(compare_days)),
            include_groups=False
        )['vol_ma5_shifted']

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]
        vol_ma5_now = vol_ma5.values[day_mask]
        vol_ma5_ago_day = vol_ma5_ago.values[day_mask]

        # 거래량 비율 계산
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = np.where(vol_ma5_ago_day > 0, vol_ma5_now / vol_ma5_ago_day * 100, np.nan)

        # 조건: min_ratio <= 비율 <= max_ratio
        mask = (ratio >= min_ratio) & (ratio <= max_ratio) & ~np.isnan(ratio)
        codes = df_day['종목코드'].values[mask]
        now_filtered = vol_ma5_now[mask]
        ago_filtered = vol_ma5_ago_day[mask]
        ratio_filtered = ratio[mask]

        if with_details:
            return {
                code: {
                    '현재5일평균': int(now),
                    'N일전5일평균': int(ago),
                    '거래량비율': round(r, 1)
                }
                for code, now, ago, r in zip(codes, now_filtered, ago_filtered, ratio_filtered)
            }
        return set(codes)

    # =========================================================================
    # 조건 G: 회전율 범위
    # =========================================================================
    def condition_G(self, base_date: str, min_rate: float = 1.0, max_rate: float = 100.0, with_details: bool = False):
        """
        조건 G: 회전율 X% ~ Y% 범위 필터링

        회전율 = 당일 거래량 / 발행주식수 * 100

        Args:
            base_date: 기준일 (YYYYMMDD)
            min_rate: 최소 회전율 % (기본 1%)
            max_rate: 최대 회전율 % (기본 100%)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        df_day = self.df_daily[self.df_daily['날짜'] == base_date]

        if len(df_day) == 0:
            return {} if with_details else set()

        # 벡터화: 발행주식수 매핑 (apply 대신 map 사용)
        stock_shares = {code: info.get('발행주식수', 0) for code, info in self.stock_info.items()}
        shares = df_day['종목코드'].map(stock_shares).fillna(0)

        # 벡터화: 회전율 계산 (apply 대신 벡터 연산)
        turnover = np.where(shares > 0, df_day['거래량'].values / shares.values * 100, 0)

        # 회전율 범위 필터링
        mask = (turnover >= min_rate) & (turnover <= max_rate)
        codes = df_day['종목코드'].values[mask]
        turnover_filtered = turnover[mask]

        if with_details:
            return {
                code: {'회전율': round(t, 2)}
                for code, t in zip(codes, turnover_filtered)
            }
        return set(codes)

    # =========================================================================
    # GT 전략 헬퍼 함수 (기술적 지표 계산)
    # =========================================================================
    def _calc_macd(self, close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        """MACD 계산 (EMA 기반)"""
        ema_fast = close.ewm(span=fast, adjust=False).mean()
        ema_slow = close.ewm(span=slow, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal, adjust=False).mean()
        histogram = macd_line - signal_line
        return macd_line, signal_line, histogram

    def _calc_rsi(self, close: pd.Series, period: int = 14) -> pd.Series:
        """RSI 계산"""
        delta = close.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = (-delta).where(delta < 0, 0.0)

        avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
        avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calc_sma(self, close: pd.Series, period: int) -> pd.Series:
        """단순 이동평균 계산"""
        return close.rolling(window=period, min_periods=period).mean()

    def _get_etf_for_market(self, market: str) -> pd.DataFrame:
        """시장구분에 따른 ETF 데이터 반환"""
        if market == "코스피":
            return self.df_kospi_etf
        elif market == "코스닥":
            return self.df_kosdaq_etf
        return None

    def _get_stock_market(self, code: str) -> str:
        """종목코드의 시장구분 반환"""
        return self.stock_info.get(code, {}).get("시장구분명", "")

    # =========================================================================
    # GT 조건 - 종목 풀 조건
    # =========================================================================
    def condition_GT_P1(self, base_date: str, target_themes: list = None, with_details: bool = False):
        """
        조건 GT_P1: 특정 테마(섹터) 소속 종목

        Args:
            base_date: 기준일 (YYYYMMDD)
            target_themes: 타겟 테마코드 리스트 (예: ["0426", "0331"])
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        if not target_themes:
            return {} if with_details else set()

        target_set = set(target_themes)
        matched = set()
        details = {}

        for stock in self.stocks:
            code = stock.get("단축코드", "")
            sec_codes = stock.get("섹터코드") or []

            matched_themes = [c for c in sec_codes if c in target_set]
            if matched_themes:
                matched.add(code)
                if with_details:
                    sec_names = stock.get("섹터명") or []
                    matched_names = []
                    for i, sc in enumerate(sec_codes):
                        if sc in target_set and i < len(sec_names):
                            matched_names.append(sec_names[i])
                    details[code] = {
                        '매칭테마': matched_themes,
                        '테마명': matched_names
                    }

        return details if with_details else matched

    # =========================================================================
    # GT 조건 - 시장 조건 (지수 기반)
    # =========================================================================
    def condition_GT_M1(self, base_date: str, market: str = None,
                        macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9,
                        with_details: bool = False):
        """
        조건 GT_M1: 지수 MACD 상승 추세

        MACD선이 Signal선 위에 있으면 True

        Args:
            base_date: 기준일 (YYYYMMDD)
            market: 시장구분 ("코스피" 또는 "코스닥")
            macd_fast: MACD 빠른 EMA 기간
            macd_slow: MACD 느린 EMA 기간
            macd_signal: Signal 기간
            with_details: True면 상세값 dict 반환

        Returns:
            bool 또는 dict: 조건 충족 여부 또는 상세값
        """
        df_etf = self._get_etf_for_market(market) if market else self.df_kospi_etf

        if df_etf is None or len(df_etf) == 0:
            return {"result": False} if with_details else False

        # 날짜 비교를 위해 타입 맞추기 (ETF 데이터는 int64 타입일 수 있음)
        compare_date = int(base_date) if df_etf['날짜'].dtype == 'int64' else base_date
        df_filtered = df_etf[df_etf['날짜'] <= compare_date]
        if len(df_filtered) < macd_slow + macd_signal:
            return {"result": False} if with_details else False

        close = df_filtered['종가'].astype(float)
        macd_line, signal_line, _ = self._calc_macd(close, macd_fast, macd_slow, macd_signal)

        current_macd = macd_line.iloc[-1]
        current_signal = signal_line.iloc[-1]
        result = current_macd > current_signal

        if with_details:
            return {
                "result": result,
                "MACD": round(current_macd, 2),
                "Signal": round(current_signal, 2),
                "market": market or "코스피"
            }
        return result

    def condition_GT_M2(self, base_date: str, market: str = None,
                        rsi_period: int = 14, rsi_overbought: float = 70.0,
                        with_details: bool = False):
        """
        조건 GT_M2: 지수 RSI 과매수 아님

        RSI < 70이면 True

        Args:
            base_date: 기준일 (YYYYMMDD)
            market: 시장구분 ("코스피" 또는 "코스닥")
            rsi_period: RSI 기간
            rsi_overbought: 과매수 기준선
            with_details: True면 상세값 dict 반환

        Returns:
            bool 또는 dict: 조건 충족 여부 또는 상세값
        """
        df_etf = self._get_etf_for_market(market) if market else self.df_kospi_etf

        if df_etf is None or len(df_etf) == 0:
            return {"result": False} if with_details else False

        # 날짜 비교를 위해 타입 맞추기 (ETF 데이터는 int64 타입일 수 있음)
        compare_date = int(base_date) if df_etf['날짜'].dtype == 'int64' else base_date
        df_filtered = df_etf[df_etf['날짜'] <= compare_date]
        if len(df_filtered) < rsi_period:
            return {"result": False} if with_details else False

        close = df_filtered['종가'].astype(float)
        rsi = self._calc_rsi(close, rsi_period)

        current_rsi = rsi.iloc[-1]
        result = current_rsi < rsi_overbought

        if with_details:
            return {
                "result": result,
                "RSI": round(current_rsi, 2),
                "기준": rsi_overbought,
                "market": market or "코스피"
            }
        return result

    # =========================================================================
    # GT 조건 - 종목 진입 조건 (벡터화 최적화)
    # =========================================================================
    def _prepare_gt_indicators(self, base_date: str, macd_fast: int = 12, macd_slow: int = 26,
                                macd_signal: int = 9, rsi_period: int = 14):
        """GT 조건용 기술적 지표 일괄 계산 (벡터화)"""
        cache_key = (base_date, macd_fast, macd_slow, macd_signal, rsi_period)
        if cache_key in self._indicator_cache:
            return self._indicator_cache[cache_key]

        df = self.df_daily[self.df_daily['날짜'] <= base_date].copy()
        df = df.sort_values(['종목코드', '날짜'])
        df['종가'] = pd.to_numeric(df['종가'], errors='coerce')

        # EMA 계산 (groupby transform)
        df['EMA_fast'] = df.groupby('종목코드')['종가'].transform(
            lambda x: x.ewm(span=macd_fast, adjust=False).mean()
        )
        df['EMA_slow'] = df.groupby('종목코드')['종가'].transform(
            lambda x: x.ewm(span=macd_slow, adjust=False).mean()
        )
        df['MACD'] = df['EMA_fast'] - df['EMA_slow']
        df['Signal'] = df.groupby('종목코드')['MACD'].transform(
            lambda x: x.ewm(span=macd_signal, adjust=False).mean()
        )

        # RSI 계산 (groupby transform)
        df['delta'] = df.groupby('종목코드')['종가'].diff()
        df['gain'] = df['delta'].where(df['delta'] > 0, 0.0)
        df['loss'] = (-df['delta']).where(df['delta'] < 0, 0.0)
        df['avg_gain'] = df.groupby('종목코드')['gain'].transform(
            lambda x: x.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        )
        df['avg_loss'] = df.groupby('종목코드')['loss'].transform(
            lambda x: x.ewm(com=rsi_period - 1, min_periods=rsi_period).mean()
        )
        df['RSI'] = 100 - (100 / (1 + df['avg_gain'] / df['avg_loss']))

        # 전일값 계산
        df['MACD_prev'] = df.groupby('종목코드')['MACD'].shift(1)
        df['Signal_prev'] = df.groupby('종목코드')['Signal'].shift(1)
        df['RSI_prev'] = df.groupby('종목코드')['RSI'].shift(1)
        df['RSI_prev2'] = df.groupby('종목코드')['RSI'].shift(2)

        self._indicator_cache[cache_key] = df
        return df

    def condition_GT_A(self, base_date: str,
                       macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9,
                       with_details: bool = False):
        """
        조건 GT_A: MACD 골든크로스 (벡터화 최적화)
        MACD선이 Signal선을 상향 돌파 (당일 발생)
        """
        df = self._prepare_gt_indicators(base_date, macd_fast, macd_slow, macd_signal)

        # 기준일 데이터만 필터링
        df_day = df[df['날짜'] == base_date].copy()

        # 골든크로스 조건: 오늘 MACD > Signal AND 어제 MACD <= Signal
        mask = (df_day['MACD'] > df_day['Signal']) & (df_day['MACD_prev'] <= df_day['Signal_prev'])
        df_matched = df_day[mask]

        if with_details:
            return {
                row['종목코드']: {
                    'MACD': round(row['MACD'], 2),
                    'Signal': round(row['Signal'], 2),
                    '전일MACD': round(row['MACD_prev'], 2),
                    '전일Signal': round(row['Signal_prev'], 2)
                }
                for _, row in df_matched.iterrows()
            }
        return set(df_matched['종목코드'])

    def condition_GT_B1(self, base_date: str,
                        rsi_period: int = 14, rsi_oversold: float = 30.0,
                        with_details: bool = False):
        """
        조건 GT_B1: RSI 과매도 탈출 (벡터화 최적화)
        RSI가 30선을 상향 돌파
        """
        df = self._prepare_gt_indicators(base_date, rsi_period=rsi_period)

        # 기준일 데이터만 필터링
        df_day = df[df['날짜'] == base_date].copy()

        # RSI 30 상향 돌파: 오늘 > 30 AND 어제 <= 30
        mask = (df_day['RSI'] > rsi_oversold) & (df_day['RSI_prev'] <= rsi_oversold)
        df_matched = df_day[mask]

        if with_details:
            return {
                row['종목코드']: {
                    'RSI': round(row['RSI'], 2),
                    '전일RSI': round(row['RSI_prev'], 2)
                }
                for _, row in df_matched.iterrows()
            }
        return set(df_matched['종목코드'])

    def condition_GT_B2(self, base_date: str,
                        rsi_period: int = 14,
                        with_details: bool = False):
        """
        조건 GT_B2: RSI 상승 전환 (벡터화 최적화)
        RSI가 2일 연속 상승
        """
        df = self._prepare_gt_indicators(base_date, rsi_period=rsi_period)

        # 기준일 데이터만 필터링
        df_day = df[df['날짜'] == base_date].copy()

        # 2일 연속 상승: RSI[today] > RSI[yesterday] > RSI[day_before]
        mask = (df_day['RSI'] > df_day['RSI_prev']) & (df_day['RSI_prev'] > df_day['RSI_prev2'])
        df_matched = df_day[mask]

        if with_details:
            return {
                row['종목코드']: {
                    'RSI': round(row['RSI'], 2),
                    '전일RSI': round(row['RSI_prev'], 2),
                    '전전일RSI': round(row['RSI_prev2'], 2)
                }
                for _, row in df_matched.iterrows()
            }
        return set(df_matched['종목코드'])

    def condition_GT_B(self, base_date: str,
                       rsi_period: int = 14, rsi_oversold: float = 30.0,
                       with_details: bool = False):
        """
        조건 GT_B: RSI 매수 신호

        GT_B1 OR GT_B2

        Args:
            base_date: 기준일 (YYYYMMDD)
            rsi_period: RSI 기간
            rsi_oversold: 과매도 기준선
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        result_b1 = self.condition_GT_B1(base_date, rsi_period, rsi_oversold, with_details)
        result_b2 = self.condition_GT_B2(base_date, rsi_period, with_details)

        if with_details:
            merged = {}
            for code, detail in result_b1.items():
                merged[code] = {**detail, 'type': 'B1'}
            for code, detail in result_b2.items():
                if code in merged:
                    merged[code]['type'] = 'B1+B2'
                else:
                    merged[code] = {**detail, 'type': 'B2'}
            return merged

        return result_b1 | result_b2

    def condition_GT_C(self, base_date: str,
                       rsi_period: int = 14, rsi_overbought: float = 70.0,
                       with_details: bool = False):
        """
        조건 GT_C: RSI 과매수 아님 (벡터화 최적화)

        RSI < 70

        Args:
            base_date: 기준일 (YYYYMMDD)
            rsi_period: RSI 기간
            rsi_overbought: 과매수 기준선
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        df = self._prepare_gt_indicators(base_date, rsi_period=rsi_period)

        # 기준일 데이터만 필터링
        df_day = df[df['날짜'] == base_date].copy()

        # RSI < 과매수 기준
        mask = df_day['RSI'] < rsi_overbought
        df_matched = df_day[mask]

        if with_details:
            return {
                row['종목코드']: {'RSI': round(row['RSI'], 2)}
                for _, row in df_matched.iterrows()
            }
        return set(df_matched['종목코드'])

    def condition_GT_D(self, base_date: str,
                       lookback_days: int = 20, bounce_pct: float = 0.03,
                       with_details: bool = False):
        """
        조건 GT_D: 바닥 패턴 (저점 대비 반등) - 벡터화 최적화

        최근 N일 저점 대비 일정 비율 이상 반등

        Args:
            base_date: 기준일 (YYYYMMDD)
            lookback_days: 저점 탐색 기간
            bounce_pct: 반등 비율 (0.03 = 3%)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: df.copy() 제거
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 최근 N일 저점 계산 (rolling min)
        rolling_low = df.groupby('종목코드')['저가'].transform(
            lambda x: x.rolling(window=lookback_days, min_periods=lookback_days).min()
        )

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]
        rolling_low_day = rolling_low.values[day_mask]
        close_day = df_day['종가'].values

        # 반등 조건: 현재가 > 저점 * (1 + bounce_pct)
        bounce_target = rolling_low_day * (1 + bounce_pct)
        mask = close_day > bounce_target

        codes = df_day['종목코드'].values[mask]
        close_filtered = close_day[mask]
        low_filtered = rolling_low_day[mask]

        if with_details:
            return {
                code: {
                    '최근저점': int(low),
                    '현재가': int(close),
                    '반등률': round((close - low) / low * 100, 2)
                }
                for code, close, low in zip(codes, close_filtered, low_filtered)
            }
        return set(codes)

    def condition_GT_D2(self, base_date: str,
                        short_period: int = 5, long_period: int = 20,
                        with_details: bool = False):
        """
        조건 GT_D2: 변동성 축소 - 벡터화 최적화

        최근 단기 변동성이 장기 평균보다 축소됨

        Args:
            base_date: 기준일 (YYYYMMDD)
            short_period: 단기 기간
            long_period: 장기 기간
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: df.copy() 제거
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 일중 변동폭 (%) - 벡터 연산
        intraday_range = (df['고가'] - df['저가']) / df['저가'] * 100

        # 단기/장기 변동성 평균 계산 (rolling)
        short_vol = df.groupby('종목코드').apply(
            lambda x: intraday_range.loc[x.index].rolling(window=short_period, min_periods=short_period).mean(),
            include_groups=False
        ).droplevel(0)

        long_vol = df.groupby('종목코드').apply(
            lambda x: intraday_range.loc[x.index].rolling(window=long_period, min_periods=long_period).mean(),
            include_groups=False
        ).droplevel(0)

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]
        short_vol_day = short_vol.values[day_mask]
        long_vol_day = long_vol.values[day_mask]

        # 변동성 축소 조건: 단기 < 장기
        mask = short_vol_day < long_vol_day
        codes = df_day['종목코드'].values[mask]
        short_filtered = short_vol_day[mask]
        long_filtered = long_vol_day[mask]

        if with_details:
            return {
                code: {
                    '단기변동성': round(s, 2),
                    '장기변동성': round(l, 2)
                }
                for code, s, l in zip(codes, short_filtered, long_filtered)
            }
        return set(codes)

    def condition_GT_E(self, base_date: str,
                       short_period: int = 5, long_period: int = 60,
                       convergence_pct: float = 0.03,
                       with_details: bool = False):
        """
        조건 GT_E: 이평선 수렴 - 벡터화 최적화

        단기/장기 이평선이 수렴 상태 (차이 N% 이내)

        Args:
            base_date: 기준일 (YYYYMMDD)
            short_period: 단기 이평 기간
            long_period: 장기 이평 기간
            convergence_pct: 수렴 비율 (0.03 = 3%)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: df.copy() 제거
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 단기/장기 SMA 계산 (rolling)
        sma_short = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=short_period, min_periods=short_period).mean()
        )
        sma_long = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=long_period, min_periods=long_period).mean()
        )

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]
        sma_short_day = sma_short.values[day_mask]
        sma_long_day = sma_long.values[day_mask]

        # 차이 비율 계산
        with np.errstate(divide='ignore', invalid='ignore'):
            diff_ratio = np.abs(sma_short_day - sma_long_day) / sma_long_day

        # 수렴 조건: 차이 비율 < convergence_pct
        mask = (sma_long_day > 0) & (diff_ratio < convergence_pct) & ~np.isnan(diff_ratio)
        codes = df_day['종목코드'].values[mask]
        short_filtered = sma_short_day[mask]
        long_filtered = sma_long_day[mask]
        diff_filtered = diff_ratio[mask]

        if with_details:
            return {
                code: {
                    f'MA{short_period}': int(s),
                    f'MA{long_period}': int(l),
                    '차이비율': round(d * 100, 2)
                }
                for code, s, l, d in zip(codes, short_filtered, long_filtered, diff_filtered)
            }
        return set(codes)

    def condition_GT_F(self, base_date: str,
                       avg_period: int = 20, volume_multiplier: float = 2.0,
                       with_details: bool = False):
        """
        조건 GT_F: 거래량 급증 - 벡터화 최적화

        당일 거래량이 N일 평균 대비 M배 이상

        Args:
            base_date: 기준일 (YYYYMMDD)
            avg_period: 평균 계산 기간
            volume_multiplier: 배수 기준
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: df.copy() 제거
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 전일까지의 N일 평균 거래량 (shift로 당일 제외)
        vol_shifted = df.groupby('종목코드')['거래량'].shift(1)
        avg_vol = df.groupby('종목코드').apply(
            lambda x: vol_shifted.loc[x.index].rolling(window=avg_period, min_periods=avg_period).mean(),
            include_groups=False
        ).droplevel(0)

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]
        vol_day = df_day['거래량'].values
        avg_vol_day = avg_vol.values[day_mask]

        # 거래량 배수 계산
        with np.errstate(divide='ignore', invalid='ignore'):
            multiplier = np.where(avg_vol_day > 0, vol_day / avg_vol_day, np.nan)

        # 급증 조건: 배수 >= volume_multiplier
        mask = (avg_vol_day > 0) & (multiplier >= volume_multiplier) & ~np.isnan(multiplier)
        codes = df_day['종목코드'].values[mask]
        vol_filtered = vol_day[mask]
        avg_filtered = avg_vol_day[mask]
        mult_filtered = multiplier[mask]

        if with_details:
            return {
                code: {
                    '당일거래량': int(v),
                    '평균거래량': int(a),
                    '배수': round(m, 2)
                }
                for code, v, a, m in zip(codes, vol_filtered, avg_filtered, mult_filtered)
            }
        return set(codes)

    # =========================================================================
    # 조건 H: 20일선 눌림목 전략 (Reno_Swing_20MA)
    # =========================================================================
    def condition_H(self, base_date: str,
                    ma_short: int = 20, ma_mid: int = 60, ma_long: int = 120,
                    smart_money_turnover: float = 10.0, smart_money_lookback: int = 20,
                    support_margin: float = 0.03,
                    volume_dry_ratio: float = 0.7,
                    with_details: bool = False):
        """
        조건 H: 20일선 눌림목 전략 (Reno_Swing_20MA)

        세력 진입 후 20일선까지 건전한 조정을 받은 종목 (C파동 공략)

        조건:
        1. 추세: Close > MA120 AND MA20 > MA60 (상승 추세)
        2. 세력: 최근 20일 내 회전율 10% 이상 발생 이력
        3. 위치: MA20 <= Close <= MA20 * 1.03 (20일선 지지)
        4. 거래량: 전일대비 30% 급감 OR 20일 평균 미만 (매도세 소멸)

        Args:
            base_date: 기준일 (YYYYMMDD)
            ma_short: 단기 이평 (기본 20)
            ma_mid: 중기 이평 (기본 60)
            ma_long: 장기 이평 (기본 120)
            smart_money_turnover: 세력 진입 회전율 기준 (기본 10%)
            smart_money_lookback: 세력 진입 탐색 기간 (기본 20일)
            support_margin: 20일선 대비 허용 마진 (기본 3%)
            volume_dry_ratio: 전일대비 거래량 감소 비율 (기본 0.7 = 30% 감소)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: df.copy() 제거
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 이동평균 계산
        ma_short_val = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=ma_short, min_periods=ma_short).mean()
        )
        ma_mid_val = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=ma_mid, min_periods=ma_mid).mean()
        )
        ma_long_val = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=ma_long, min_periods=ma_long).mean()
        )

        # 거래량 이동평균
        vol_ma20 = df.groupby('종목코드')['거래량'].transform(
            lambda x: x.rolling(window=20, min_periods=20).mean()
        )

        # 회전율 처리 (컬럼이 없을 수 있음)
        if '거래회전율' in df.columns:
            turnover = df['거래회전율'].fillna(0)
        else:
            turnover = pd.Series(0, index=df.index)

        # 최근 N일 최대 회전율 (세력 진입 흔적)
        max_turnover = df.groupby('종목코드').apply(
            lambda x: turnover.loc[x.index].rolling(window=smart_money_lookback, min_periods=1).max(),
            include_groups=False
        ).droplevel(0)

        # 전일 거래량
        prev_volume = df.groupby('종목코드')['거래량'].shift(1)

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]

        if len(df_day) == 0:
            return {} if with_details else set()

        # 기준일 값들 추출
        close_day = df_day['종가'].values
        vol_day = df_day['거래량'].values
        ma_short_day = ma_short_val.values[day_mask]
        ma_mid_day = ma_mid_val.values[day_mask]
        ma_long_day = ma_long_val.values[day_mask]
        vol_ma20_day = vol_ma20.values[day_mask]
        max_turnover_day = max_turnover.values[day_mask]
        prev_vol_day = prev_volume.values[day_mask]

        # 조건 1: 추세 (Close > MA120 AND MA20 > MA60)
        cond_trend = (close_day > ma_long_day) & (ma_short_day > ma_mid_day)

        # 조건 2: 세력 진입 (최근 N일 내 회전율 10% 이상)
        cond_smart_money = max_turnover_day >= smart_money_turnover

        # 조건 3: 위치 (MA20 <= Close <= MA20 * 1.03)
        cond_position = (close_day >= ma_short_day) & (close_day <= ma_short_day * (1 + support_margin))

        # 조건 4: 거래량 급감 (전일대비 30% 급감 OR 20일 평균 미만)
        cond_volume_dry = (vol_day < prev_vol_day * volume_dry_ratio) | (vol_day < vol_ma20_day)

        # 모든 조건 충족
        mask = cond_trend & cond_smart_money & cond_position & cond_volume_dry
        codes = df_day['종목코드'].values[mask]

        if with_details:
            return {
                code: {
                    '종가': int(close),
                    f'MA{ma_short}': int(mas),
                    f'MA{ma_mid}': int(mam),
                    f'MA{ma_long}': int(mal),
                    '최대회전율': round(mt, 2),
                    '거래량': int(v),
                    '전일거래량': int(pv) if not np.isnan(pv) else 0,
                    '20일평균거래량': int(vm) if not np.isnan(vm) else 0
                }
                for code, close, mas, mam, mal, mt, v, pv, vm in zip(
                    codes, close_day[mask], ma_short_day[mask], ma_mid_day[mask], ma_long_day[mask],
                    max_turnover_day[mask], vol_day[mask], prev_vol_day[mask], vol_ma20_day[mask]
                )
            }
        return set(codes)

    # =========================================================================
    # 조건 I: 5일선 급등주 전략 (Reno_Momentum_5MA)
    # =========================================================================
    def condition_I(self, base_date: str,
                    ma_short: int = 5, ma_mid: int = 20,
                    disparity_min: float = 1.15,
                    support_margin: float = 0.02,
                    min_turnover: float = 3.0,
                    with_details: bool = False):
        """
        조건 I: 5일선 급등주 전략 (Reno_Momentum_5MA)

        강한 모멘텀으로 상승 중인 종목이 5일선에서 짧은 조정 후 재상승 공략

        조건:
        1. 모멘텀: Close >= MA20 * 1.15 (20일선 대비 15% 이상 급등)
        2. 위치: MA5 <= Close <= MA5 * 1.02 (5일선 지지)
        3. 수급: 회전율 >= 3% (시장 관심 지속)
        4. 매물소화: 거래량 < 전일 거래량 (과열 방지)

        Args:
            base_date: 기준일 (YYYYMMDD)
            ma_short: 단기 이평 (기본 5)
            ma_mid: 중기 이평 (기본 20)
            disparity_min: 20일선 대비 최소 이격도 (기본 1.15 = 15%)
            support_margin: 5일선 대비 허용 마진 (기본 2%)
            min_turnover: 최소 회전율 (기본 3%)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        # 벡터화: df.copy() 제거
        df = self.df_daily[self.df_daily['날짜'] <= base_date]

        # 이동평균 계산
        ma_short_val = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=ma_short, min_periods=ma_short).mean()
        )
        ma_mid_val = df.groupby('종목코드')['종가'].transform(
            lambda x: x.rolling(window=ma_mid, min_periods=ma_mid).mean()
        )

        # 전일 거래량
        prev_volume = df.groupby('종목코드')['거래량'].shift(1)

        # 기준일 데이터만 필터링 (인덱스 일관성을 위해 mask 먼저 생성)
        day_mask = (df['날짜'] == base_date).values
        df_day = df[day_mask]

        if len(df_day) == 0:
            return {} if with_details else set()

        # 기준일 값들 추출
        close_day = df_day['종가'].values
        vol_day = df_day['거래량'].values
        ma_short_day = ma_short_val.values[day_mask]
        ma_mid_day = ma_mid_val.values[day_mask]
        prev_vol_day = prev_volume.values[day_mask]

        # 회전율 처리
        if '거래회전율' in df.columns:
            turnover_day = df['거래회전율'].fillna(0).values[day_mask]
        else:
            turnover_day = np.zeros(len(df_day))

        # 이격도 계산
        with np.errstate(divide='ignore', invalid='ignore'):
            disparity = np.where(ma_mid_day > 0, close_day / ma_mid_day, 0)

        # 조건 1: 모멘텀 (Close >= MA20 * 1.15)
        cond_momentum = disparity >= disparity_min

        # 조건 2: 위치 (MA5 <= Close <= MA5 * 1.02)
        cond_position = (close_day >= ma_short_day) & (close_day <= ma_short_day * (1 + support_margin))

        # 조건 3: 수급 (회전율 >= 3%)
        cond_active = turnover_day >= min_turnover

        # 조건 4: 매물소화 (거래량 < 전일 거래량)
        cond_volume_control = vol_day < prev_vol_day

        # 모든 조건 충족
        mask = cond_momentum & cond_position & cond_active & cond_volume_control
        codes = df_day['종목코드'].values[mask]

        if with_details:
            return {
                code: {
                    '종가': int(close),
                    f'MA{ma_short}': int(mas),
                    f'MA{ma_mid}': int(mam),
                    '이격도': round(d * 100, 2),
                    '회전율': round(t, 2),
                    '거래량': int(v),
                    '전일거래량': int(pv) if not np.isnan(pv) else 0
                }
                for code, close, mas, mam, d, t, v, pv in zip(
                    codes, close_day[mask], ma_short_day[mask], ma_mid_day[mask],
                    disparity[mask], turnover_day[mask], vol_day[mask], prev_vol_day[mask]
                )
            }
        return set(codes)

    # =========================================================================
    # 유틸리티 메서드
    # =========================================================================
    def _make_cache_key(self, condition_id: str, base_date: str, params: dict) -> tuple:
        """캐시 키 생성 (파라미터를 hashable하게 변환)"""
        # params를 정렬된 튜플로 변환
        params_tuple = tuple(sorted(params.items())) if params else ()
        return (condition_id.upper(), base_date, params_tuple)

    def clear_condition_cache(self):
        """조건 결과 캐시 초기화 (새로운 TP/SL 테스트 시 호출 불필요)"""
        self._condition_cache.clear()

    def evaluate(self, condition_id: str, base_date: str, params: dict = None, with_details: bool = False):
        """
        조건 ID로 평가 (캐싱 지원)

        Args:
            condition_id: 조건 ID (A, B, C, D, E, F, G)
            base_date: 기준일
            params: 조건별 파라미터 (없으면 기본값 사용)
            with_details: True면 상세값 dict 반환

        Returns:
            set[str] 또는 dict[str, dict]: 조건 충족 종목코드 집합 또는 상세값
        """
        params = params or {}
        # description 필드 제외 (함수 파라미터가 아님)
        filtered_params = {k: v for k, v in params.items() if k != 'description'}

        # 캐시 키 생성 (with_details=False 결과만 캐싱)
        # with_details=True는 매번 계산 (디버깅/상세정보용, 자주 호출되지 않음)
        if not with_details:
            cache_key = self._make_cache_key(condition_id, base_date, filtered_params)
            if cache_key in self._condition_cache:
                return self._condition_cache[cache_key]

        eval_params = {**filtered_params, 'with_details': with_details}

        condition_map = {
            'A': lambda: self.condition_A(base_date, **eval_params),
            'B': lambda: self.condition_B(base_date, **eval_params),
            'C': lambda: self.condition_C(base_date, **eval_params),
            'D': lambda: self.condition_D(base_date, **eval_params),
            'E': lambda: self.condition_E(base_date, **eval_params),
            'F': lambda: self.condition_F(base_date, **eval_params),
            'G': lambda: self.condition_G(base_date, **eval_params),
            'H': lambda: self.condition_H(base_date, **eval_params),
            'I': lambda: self.condition_I(base_date, **eval_params),
            # GT 전략 조건들
            'GT_P1': lambda: self.condition_GT_P1(base_date, **eval_params),
            'GT_M1': lambda: self.condition_GT_M1(base_date, **eval_params),
            'GT_M2': lambda: self.condition_GT_M2(base_date, **eval_params),
            'GT_A': lambda: self.condition_GT_A(base_date, **eval_params),
            'GT_B': lambda: self.condition_GT_B(base_date, **eval_params),
            'GT_B1': lambda: self.condition_GT_B1(base_date, **eval_params),
            'GT_B2': lambda: self.condition_GT_B2(base_date, **eval_params),
            'GT_C': lambda: self.condition_GT_C(base_date, **eval_params),
            'GT_D': lambda: self.condition_GT_D(base_date, **eval_params),
            'GT_D2': lambda: self.condition_GT_D2(base_date, **eval_params),
            'GT_E': lambda: self.condition_GT_E(base_date, **eval_params),
            'GT_F': lambda: self.condition_GT_F(base_date, **eval_params),
        }

        if condition_id.upper() not in condition_map:
            print(f"   [WARN] 알 수 없는 조건: {condition_id}")
            return {} if with_details else set()

        result = condition_map[condition_id.upper()]()

        # 캐시에 저장 (with_details=False 결과만)
        if not with_details:
            self._condition_cache[cache_key] = result

        return result

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
    'G': '회전율 X%~Y% 범위',
    'H': '20일선 눌림목 (세력진입 후 조정)',
    'I': '5일선 급등주 (모멘텀 조정)',
    # GT 전략 조건들
    'GT_P1': '특정 테마(섹터) 소속 종목',
    'GT_M1': '지수 MACD 상승 추세',
    'GT_M2': '지수 RSI 과매수 아님',
    'GT_A': 'MACD 골든크로스',
    'GT_B': 'RSI 매수 신호 (B1 OR B2)',
    'GT_B1': 'RSI 과매도 탈출 (30 상향돌파)',
    'GT_B2': 'RSI 2일 연속 상승',
    'GT_C': 'RSI 과매수 아님 (<70)',
    'GT_D': '바닥 패턴 (저점대비 반등)',
    'GT_D2': '변동성 축소',
    'GT_E': '이평선 수렴',
    'GT_F': '거래량 급증',
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
