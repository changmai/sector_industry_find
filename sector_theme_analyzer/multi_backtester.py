"""
멀티 조건 백테스터 (Multi-Condition Backtester)

조건 조합으로 필터링된 종목들의 매매 시뮬레이션을 수행합니다.

주요 기능:
    1. 매일 조건 충족 종목 추출 → 다음날 시가 매수
    2. 손절/익절 조건 체크
    3. 보유기간별 수익률 분석
    4. TP/SL 최적화

사용법:
    backtester = MultiBacktester(engine, parser)
    results = backtester.run(start_date, end_date, "A AND B")
    backtester.print_report()
"""
import sys
import io
from dataclasses import dataclass, field
from typing import Optional
from collections import defaultdict

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

from condition_engine import ConditionEngine
from condition_parser import ConditionParser


@dataclass
class TradeResult:
    """개별 매매 결과"""
    code: str               # 종목코드
    name: str               # 종목명
    signal_date: str        # 조건 충족일 (신호 발생일)
    entry_date: str         # 매수일 (signal_date + 1 거래일)
    entry_price: float      # 매수가 (시가)
    exit_date: str          # 매도일
    exit_price: float       # 매도가
    exit_reason: str        # 매도 사유: 'take_profit', 'stop_loss', 'max_holding', 'trailing', 'time_cut'
    return_pct: float       # 수익률 %
    holding_days: int       # 보유일수
    peak_return: float = 0.0  # 보유 중 최고 수익률 (트레일링용)


@dataclass
class BacktestReport:
    """백테스트 결과 리포트"""
    condition_expr: str                 # 조건 표현식
    start_date: str                     # 시작일
    end_date: str                       # 종료일
    stop_loss: float                    # 손절 라인 %
    take_profit: float                  # 익절 라인 %
    max_holding_days: int               # 최대 보유일

    total_trades: int = 0               # 총 매매 횟수
    win_count: int = 0                  # 승리 횟수 (수익 > 0)
    loss_count: int = 0                 # 패배 횟수
    win_rate: float = 0.0               # 승률 %

    avg_return: float = 0.0             # 평균 수익률 %
    total_return: float = 0.0           # 총 수익률 %
    max_return: float = 0.0             # 최대 수익률 %
    min_return: float = 0.0             # 최대 손실률 %

    tp_count: int = 0                   # 익절 횟수
    sl_count: int = 0                   # 손절 횟수
    max_hold_count: int = 0             # 보유기간 만료 횟수
    trailing_count: int = 0             # 트레일링 청산 횟수
    time_cut_count: int = 0             # 타임컷 청산 횟수

    avg_holding_days: float = 0.0       # 평균 보유일수

    # 보유기간별 통계
    returns_by_day: dict = field(default_factory=dict)  # {일수: [수익률들]}

    trades: list = field(default_factory=list)  # 개별 매매 결과들


class MultiBacktester:
    """멀티 조건 백테스터"""

    def __init__(
        self,
        engine: ConditionEngine,
        stop_loss: float = -5.0,
        take_profit: float = 10.0,
        max_holding_days: int = 10,
        # 트레일링 스탑 옵션
        trailing_start: float = None,    # 트레일링 활성화 수익률 (예: 5.0 = 5% 수익 시 활성화)
        trailing_offset: float = None,   # 고점 대비 하락 허용폭 (예: 3.0 = 고점 대비 3% 하락 시 청산)
        # 타임 컷 옵션
        time_cut_days: int = None,       # N일 후 최소 수익률 체크
        time_cut_min_return: float = None  # 최소 수익률 (미달 시 청산)
    ):
        """
        Args:
            engine: 조건 평가 엔진
            stop_loss: 손절 라인 % (기본 -5%)
            take_profit: 익절 라인 % (기본 +10%)
            max_holding_days: 최대 보유일 (기본 10일)
            trailing_start: 트레일링 시작 수익률 % (None이면 비활성화)
            trailing_offset: 고점 대비 하락 허용폭 %
            time_cut_days: 타임컷 체크 일수 (None이면 비활성화)
            time_cut_min_return: 타임컷 최소 수익률 %
        """
        self.engine = engine
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.max_holding_days = max_holding_days

        # 트레일링 스탑
        self.trailing_start = trailing_start
        self.trailing_offset = trailing_offset

        # 타임 컷
        self.time_cut_days = time_cut_days
        self.time_cut_min_return = time_cut_min_return

        self.report: BacktestReport = None
        self.trades: list[TradeResult] = []

        # 성능 최적화: 종목별 데이터 캐시
        self._stock_data_cache: dict = {}
        self._cache_prepared = False

    def _prepare_stock_cache(self):
        """종목별로 데이터를 미리 분리하여 캐시 (O(1) 조회 가능)"""
        if self._cache_prepared:
            return

        df = self.engine.df_daily
        if df is None or len(df) == 0:
            return

        # 종목코드별로 그룹화하여 딕셔너리로 저장
        for code, group in df.groupby('종목코드'):
            # 날짜를 인덱스로 설정하여 O(1) 조회 가능하게 함
            df_code = group.set_index('날짜').sort_index()
            self._stock_data_cache[code] = df_code

        self._cache_prepared = True

    def run(
        self,
        start_date: str,
        end_date: str,
        condition_expr: str,
        params: dict = None,
        verbose: bool = True,
        progress_callback: callable = None
    ) -> BacktestReport:
        """
        백테스트 실행

        Args:
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)
            condition_expr: 조건 표현식
            params: 조건별 파라미터
            verbose: 진행 상황 출력
            progress_callback: 진행률 콜백 함수 (current, total) -> None

        Returns:
            BacktestReport: 백테스트 결과
        """
        self.trades = []
        self.skipped_trades = 0  # 중복 매수로 스킵된 거래 수
        parser = ConditionParser(self.engine, params)

        # 성능 최적화: 캐시 준비
        self._prepare_stock_cache()

        # 전체 거래일 목록
        all_trading_days = self.engine.get_all_trading_days()
        trading_days = [d for d in all_trading_days if start_date <= d <= end_date]

        # 성능 최적화: 거래일 인덱스 dict (O(n) list.index() → O(1) dict lookup)
        trading_days_dict = {date: idx for idx, date in enumerate(all_trading_days)}

        if len(trading_days) < 2:
            print("   [ERROR] 거래일이 부족합니다.")
            return None

        if verbose:
            print(f"\n   [BACKTEST] 백테스팅 시작...")
            print(f"   기간: {start_date} ~ {end_date} ({len(trading_days)}일)")
            print(f"   조건: {condition_expr}")
            print(f"   손절: {self.stop_loss}% | 익절: {self.take_profit}%")
            if self.trailing_start is not None and self.trailing_offset is not None:
                print(f"   트레일링: {self.trailing_start:+.1f}% 도달 시 활성화, 고점 대비 -{self.trailing_offset:.1f}% 하락 시 청산")
            if self.time_cut_days is not None and self.time_cut_min_return is not None:
                print(f"   타임컷: {self.time_cut_days}일 후 수익률 {self.time_cut_min_return:+.1f}% 미만 시 청산")

        # 매일 조건 평가 및 매매 시뮬레이션 (신호일 다음날 시가 매수)
        total_days = len(trading_days)

        # 중복 매수 방지: 보유 중인 종목 추적 {code: exit_date}
        holdings = {}

        # 마지막 날은 다음날 매수 불가하므로 제외
        for i, signal_date in enumerate(trading_days[:-1]):
            # 진행률 콜백 호출 (5% 단위로)
            if progress_callback and (i == 0 or (i + 1) % max(1, (total_days - 1) // 20) == 0):
                progress_callback(i + 1, total_days - 1)

            # 진행률 표시 (verbose 모드)
            if verbose and (i + 1) % 20 == 0:
                pct = (i + 1) / (total_days - 1) * 100
                print(f"   진행: {i + 1}/{total_days - 1} ({pct:.0f}%)")

            # 다음날 매수 (신호일 다음날 시가 매수)
            entry_date = trading_days[i + 1]

            # 청산된 종목 제거 (exit_date <= entry_date인 종목, 매수일 기준)
            holdings = {code: exit_date for code, exit_date in holdings.items()
                       if exit_date > entry_date}

            # 조건 충족 종목 추출
            matched_stocks = parser.parse(condition_expr, signal_date)

            if not matched_stocks:
                continue

            # 각 종목에 대해 매매 시뮬레이션
            for code in matched_stocks:
                # 중복 매수 방지: 이미 보유 중인 종목은 스킵
                if code in holdings:
                    self.skipped_trades += 1
                    continue

                # 전체 거래일 목록 전달 (보유기간 동안 범위 밖 데이터 필요)
                trade = self._simulate_trade(code, signal_date, entry_date, all_trading_days, trading_days_dict)
                if trade:
                    self.trades.append(trade)
                    # 보유 종목에 추가 (청산일까지 재매수 불가)
                    holdings[code] = trade.exit_date

        # 리포트 생성
        self.report = self._generate_report(condition_expr, start_date, end_date)

        if verbose:
            skip_msg = f" (중복스킵: {self.skipped_trades}건)" if self.skipped_trades > 0 else ""
            print(f"   [DONE] 총 {len(self.trades)}건 매매 완료{skip_msg}")

        return self.report

    def _simulate_trade(
        self,
        code: str,
        signal_date: str,
        entry_date: str,
        all_trading_days: list[str],
        trading_days_dict: dict[str, int] = None
    ) -> Optional[TradeResult]:
        """개별 종목 매매 시뮬레이션 (트레일링 스탑 + 타임컷 지원)"""

        # 캐시에서 종목 데이터 조회 (O(1))
        df_code = self._stock_data_cache.get(code)
        if df_code is None or len(df_code) == 0:
            return None

        # 매수일 데이터 (인덱스로 O(1) 조회)
        if entry_date not in df_code.index:
            return None

        entry_row = df_code.loc[entry_date]
        # 다음날 시가 매수 + 슬리피지 0.004% (수수료 포함)
        entry_price = entry_row['시가'] * 1.00004
        if entry_price <= 0:
            return None

        # 매수일 인덱스 (O(1) dict lookup)
        if trading_days_dict is not None:
            entry_idx = trading_days_dict.get(entry_date)
            if entry_idx is None:
                return None
        else:
            # fallback (호환성 유지)
            try:
                entry_idx = all_trading_days.index(entry_date)
            except ValueError:
                return None

        # 트레일링 스탑 활성화 여부
        use_trailing = (self.trailing_start is not None and self.trailing_offset is not None)

        # 타임컷 활성화 여부
        use_time_cut = (self.time_cut_days is not None and self.time_cut_min_return is not None)

        # 매도 시뮬레이션
        exit_date = None
        exit_price = None
        exit_reason = None
        last_valid_date = None
        last_valid_close = None

        # 트레일링 스탑 추적 변수
        peak_return = 0.0  # 고점 수익률
        trailing_active = False
        current_trailing_sl = self.stop_loss  # 현재 트레일링 손절 라인

        for hold_day in range(1, self.max_holding_days + 1):
            check_idx = entry_idx + hold_day
            if check_idx >= len(all_trading_days):
                break

            check_date = all_trading_days[check_idx]

            # 캐시에서 O(1) 조회
            if check_date not in df_code.index:
                continue

            row = df_code.loc[check_date]
            high = row['고가']
            low = row['저가']
            close = row['종가']

            # 마지막 유효 데이터 기록 (데이터 부족 시 기간만료용)
            last_valid_date = check_date
            last_valid_close = close

            # 수익률 계산
            high_pct = (high - entry_price) / entry_price * 100 if high > 0 else 0
            low_pct = (low - entry_price) / entry_price * 100 if low > 0 else 0
            close_pct = (close - entry_price) / entry_price * 100 if close > 0 else 0

            # 고점 수익률 갱신
            if high_pct > peak_return:
                peak_return = high_pct

            # 트레일링 스탑 처리
            if use_trailing:
                # 트레일링 활성화 체크
                if not trailing_active and peak_return >= self.trailing_start:
                    trailing_active = True

                # 트레일링 활성화 시 손절 라인 갱신 (고점 - offset)
                if trailing_active:
                    current_trailing_sl = peak_return - self.trailing_offset

            # 1. 손절/트레일링 손절 체크 (저가 기준)
            if low > 0 and low_pct <= current_trailing_sl:
                exit_date = check_date
                exit_price = entry_price * (1 + current_trailing_sl / 100)
                if use_trailing and trailing_active and current_trailing_sl > self.stop_loss:
                    exit_reason = 'trailing'
                else:
                    exit_reason = 'stop_loss'
                break

            # 2. 익절 체크 (고가 기준)
            if high > 0 and high_pct >= self.take_profit:
                exit_date = check_date
                exit_price = entry_price * (1 + self.take_profit / 100)
                exit_reason = 'take_profit'
                break

            # 3. 타임컷 체크 (지정일 종가 기준)
            if use_time_cut and hold_day == self.time_cut_days:
                if close_pct < self.time_cut_min_return:
                    exit_date = check_date
                    exit_price = close
                    exit_reason = 'time_cut'
                    break

            # 4. 최대 보유기간 도달
            if hold_day == self.max_holding_days:
                exit_date = check_date
                exit_price = close
                exit_reason = 'max_holding'
                break

        # 데이터 부족으로 최대 보유기간 전에 종료된 경우 - 마지막 유효 데이터로 기간만료 처리
        if exit_date is None and last_valid_date is not None:
            exit_date = last_valid_date
            exit_price = last_valid_close
            exit_reason = 'max_holding'

        # 매도 실패 (데이터가 전혀 없음)
        if exit_date is None:
            return None

        # 수익률 계산
        return_pct = (exit_price - entry_price) / entry_price * 100

        # 보유일수 계산 (O(1) dict lookup)
        if trading_days_dict is not None:
            exit_idx = trading_days_dict.get(exit_date)
            holding_days = (exit_idx - entry_idx) if exit_idx is not None else 0
        else:
            try:
                holding_days = all_trading_days.index(exit_date) - entry_idx
            except ValueError:
                holding_days = 0

        return TradeResult(
            code=code,
            name=self.engine.get_stock_name(code),
            signal_date=signal_date,
            entry_date=entry_date,
            entry_price=entry_price,
            exit_date=exit_date,
            exit_price=exit_price,
            exit_reason=exit_reason,
            return_pct=round(return_pct, 2),
            holding_days=holding_days,
            peak_return=round(peak_return, 2)
        )

    def _generate_report(self, condition_expr: str, start_date: str, end_date: str) -> BacktestReport:
        """백테스트 리포트 생성"""
        report = BacktestReport(
            condition_expr=condition_expr,
            start_date=start_date,
            end_date=end_date,
            stop_loss=self.stop_loss,
            take_profit=self.take_profit,
            max_holding_days=self.max_holding_days,
            trades=self.trades
        )

        if not self.trades:
            return report

        returns = [t.return_pct for t in self.trades]

        report.total_trades = len(self.trades)
        report.win_count = sum(1 for r in returns if r > 0)
        report.loss_count = sum(1 for r in returns if r <= 0)
        report.win_rate = report.win_count / report.total_trades * 100 if report.total_trades > 0 else 0

        report.avg_return = np.mean(returns)
        report.total_return = np.sum(returns)
        report.max_return = np.max(returns)
        report.min_return = np.min(returns)

        report.tp_count = sum(1 for t in self.trades if t.exit_reason == 'take_profit')
        report.sl_count = sum(1 for t in self.trades if t.exit_reason == 'stop_loss')
        report.max_hold_count = sum(1 for t in self.trades if t.exit_reason == 'max_holding')
        report.trailing_count = sum(1 for t in self.trades if t.exit_reason == 'trailing')
        report.time_cut_count = sum(1 for t in self.trades if t.exit_reason == 'time_cut')

        report.avg_holding_days = np.mean([t.holding_days for t in self.trades])

        # 보유기간별 통계
        for day in [1, 3, 5, 10]:
            day_returns = [t.return_pct for t in self.trades if t.holding_days <= day]
            report.returns_by_day[day] = day_returns

        return report

    def print_report(self):
        """리포트 출력"""
        if not self.report:
            print("   [ERROR] 리포트가 없습니다. run()을 먼저 실행하세요.")
            return

        r = self.report

        print("\n" + "=" * 70)
        print("   BACKTEST RESULT")
        print("=" * 70)
        print(f"   조건: {r.condition_expr}")
        print(f"   기간: {r.start_date} ~ {r.end_date}")
        print(f"   손절: {r.stop_loss}% | 익절: {r.take_profit}%")
        print("=" * 70)

        print("\n[매매 통계]")
        print(f"   총 매매 횟수: {r.total_trades}회")
        print(f"   평균 보유 기간: {r.avg_holding_days:.1f}일")

        print("\n[수익률]")
        print(f"   평균 수익률: {r.avg_return:+.2f}%")
        print(f"   총 수익률: {r.total_return:+.2f}%")
        print(f"   승률: {r.win_rate:.1f}% ({r.win_count}/{r.total_trades})")
        print(f"   최대 수익: {r.max_return:+.2f}%")
        print(f"   최대 손실: {r.min_return:+.2f}%")

        print("\n[청산 사유 통계]")
        if r.total_trades > 0:
            tp_pct = r.tp_count / r.total_trades * 100
            sl_pct = r.sl_count / r.total_trades * 100
            mh_pct = r.max_hold_count / r.total_trades * 100
            tr_pct = r.trailing_count / r.total_trades * 100
            tc_pct = r.time_cut_count / r.total_trades * 100
            print(f"   익절({r.take_profit:+}%): {r.tp_count}회 ({tp_pct:.1f}%)")
            print(f"   손절({r.stop_loss}%): {r.sl_count}회 ({sl_pct:.1f}%)")
            if r.trailing_count > 0:
                print(f"   트레일링: {r.trailing_count}회 ({tr_pct:.1f}%)")
            if r.time_cut_count > 0:
                print(f"   타임컷: {r.time_cut_count}회 ({tc_pct:.1f}%)")
            print(f"   기간만료: {r.max_hold_count}회 ({mh_pct:.1f}%)")

        print("\n[보유기간별 수익률]")
        for day in [1, 3, 5, 10]:
            day_returns = r.returns_by_day.get(day, [])
            if day_returns:
                avg = np.mean(day_returns)
                win = sum(1 for x in day_returns if x > 0)
                win_rate = win / len(day_returns) * 100
                print(f"   {day}일 이내: 평균 {avg:+.2f}% | 승률 {win_rate:.1f}% ({len(day_returns)}건)")

        print("=" * 70)

    def optimize_tp_sl(
        self,
        start_date: str,
        end_date: str,
        condition_expr: str,
        params: dict = None,
        tp_range: tuple = (5, 10),
        sl_range: tuple = (-5, -3),
        step: float = 1.0,
        verbose: bool = True,
        progress_callback: callable = None
    ) -> list[dict]:
        """
        TP/SL 최적화

        Args:
            start_date: 시작일
            end_date: 종료일
            condition_expr: 조건 표현식
            params: 조건별 파라미터
            tp_range: 익절 범위 (min, max)
            sl_range: 손절 범위 (min, max) - 음수
            step: 스텝 크기
            verbose: 진행 상황 출력
            progress_callback: 진행률 콜백 함수 (current, total) -> None

        Returns:
            list[dict]: 최적화 결과 (승률/수익률 기준 정렬)
        """
        import time

        results = []

        # TP/SL 조합 생성
        tp_values = np.arange(tp_range[0], tp_range[1] + step, step)
        sl_values = np.arange(sl_range[0], sl_range[1] + step, step)

        total_combinations = len(tp_values) * len(sl_values)

        if verbose:
            print(f"\n   [OPTIMIZE] TP/SL 최적화 시작")
            print(f"   익절 범위: {tp_range[0]}% ~ {tp_range[1]}%")
            print(f"   손절 범위: {sl_range[0]}% ~ {sl_range[1]}%")
            print(f"   테스트 조합: {total_combinations}개")
            print("-" * 50)

        count = 0
        start_time = time.time()
        elapsed_times = []

        for tp in tp_values:
            for sl in sl_values:
                count += 1
                iter_start = time.time()

                # 진행률 콜백 호출
                if progress_callback:
                    progress_callback(count, total_combinations)

                # 백테스트 실행 (조용히)
                self.take_profit = tp
                self.stop_loss = sl

                report = self.run(
                    start_date, end_date, condition_expr, params, verbose=False
                )

                iter_elapsed = time.time() - iter_start
                elapsed_times.append(iter_elapsed)

                if report and report.total_trades > 0:
                    results.append({
                        'tp': tp,
                        'sl': sl,
                        'win_rate': report.win_rate,
                        'avg_return': report.avg_return,
                        'total_trades': report.total_trades,
                        'tp_count': report.tp_count,
                        'sl_count': report.sl_count,
                        'avg_holding_days': report.avg_holding_days
                    })

                if verbose:
                    # 예상 남은 시간 계산
                    avg_time = sum(elapsed_times) / len(elapsed_times)
                    remaining = (total_combinations - count) * avg_time
                    remaining_min = int(remaining // 60)
                    remaining_sec = int(remaining % 60)

                    pct = count / total_combinations * 100
                    trades_str = f"{report.total_trades}건" if report and report.total_trades > 0 else "0건"
                    print(f"   [{count:>3}/{total_combinations}] TP={tp:+.0f}%, SL={sl:.0f}% → "
                          f"{trades_str} "
                          f"(남은: {remaining_min}분 {remaining_sec}초)")
                else:
                    # verbose=False 일 때도 간단한 진행 표시 (점으로)
                    if count % 10 == 0 or count == total_combinations:
                        print(f".", end='', flush=True)

        # 평균 수익률 기준 정렬
        results.sort(key=lambda x: x['avg_return'], reverse=True)

        if verbose:
            self._print_optimize_results(results)

        return results

    def _print_optimize_results(self, results: list[dict]):
        """최적화 결과 출력"""
        print("\n" + "=" * 70)
        print("   TP/SL 최적화 결과")
        print("=" * 70)
        print(f"   {'순위':>4} {'TP':>6} {'SL':>6} {'승률':>8} {'평균수익률':>10} {'매매수':>6}")
        print("-" * 70)

        for i, r in enumerate(results[:10], 1):
            mark = " ← 최적" if i == 1 else ""
            print(f"   {i:>4} {r['tp']:>+5.0f}% {r['sl']:>+5.0f}% {r['win_rate']:>7.1f}% {r['avg_return']:>+9.2f}% {r['total_trades']:>5}회{mark}")

        if results:
            best = results[0]
            print("-" * 70)
            print(f"   [BEST] TP={best['tp']:+.0f}%, SL={best['sl']:.0f}%")
            print(f"          승률 {best['win_rate']:.1f}%, 평균수익률 {best['avg_return']:+.2f}%")
        print("=" * 70)


if __name__ == "__main__":
    # 테스트
    engine = ConditionEngine()
    if engine.load_data():
        backtester = MultiBacktester(engine, stop_loss=-5.0, take_profit=10.0)

        # 단순 테스트
        report = backtester.run(
            start_date="20241209",
            end_date="20251205",
            condition_expr="A"
        )

        backtester.print_report()
