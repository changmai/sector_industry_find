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
    exit_reason: str        # 매도 사유: 'take_profit', 'stop_loss', 'max_holding'
    return_pct: float       # 수익률 %
    holding_days: int       # 보유일수


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
        max_holding_days: int = 10
    ):
        """
        Args:
            engine: 조건 평가 엔진
            stop_loss: 손절 라인 % (기본 -5%)
            take_profit: 익절 라인 % (기본 +10%)
            max_holding_days: 최대 보유일 (기본 10일)
        """
        self.engine = engine
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.max_holding_days = max_holding_days

        self.report: BacktestReport = None
        self.trades: list[TradeResult] = []

    def run(
        self,
        start_date: str,
        end_date: str,
        condition_expr: str,
        params: dict = None,
        verbose: bool = True
    ) -> BacktestReport:
        """
        백테스트 실행

        Args:
            start_date: 시작일 (YYYYMMDD)
            end_date: 종료일 (YYYYMMDD)
            condition_expr: 조건 표현식
            params: 조건별 파라미터
            verbose: 진행 상황 출력

        Returns:
            BacktestReport: 백테스트 결과
        """
        self.trades = []
        parser = ConditionParser(self.engine, params)

        # 전체 거래일 목록
        all_trading_days = self.engine.get_all_trading_days()
        trading_days = [d for d in all_trading_days if start_date <= d <= end_date]

        if len(trading_days) < 2:
            print("   [ERROR] 거래일이 부족합니다.")
            return None

        if verbose:
            print(f"\n   [BACKTEST] 백테스팅 시작...")
            print(f"   기간: {start_date} ~ {end_date} ({len(trading_days)}일)")
            print(f"   조건: {condition_expr}")
            print(f"   손절: {self.stop_loss}% | 익절: {self.take_profit}%")

        # 매일 조건 평가 및 매매 시뮬레이션
        total_days = len(trading_days) - 1  # 마지막 날은 매수 불가

        for i, signal_date in enumerate(trading_days[:-1]):
            # 진행률 표시
            if verbose and (i + 1) % 20 == 0:
                pct = (i + 1) / total_days * 100
                print(f"   진행: {i + 1}/{total_days} ({pct:.0f}%)")

            # 조건 충족 종목 추출
            matched_stocks = parser.parse(condition_expr, signal_date)

            if not matched_stocks:
                continue

            # 다음 거래일 (매수일)
            entry_date = trading_days[i + 1]

            # 각 종목에 대해 매매 시뮬레이션
            for code in matched_stocks:
                trade = self._simulate_trade(code, signal_date, entry_date, trading_days)
                if trade:
                    self.trades.append(trade)

        # 리포트 생성
        self.report = self._generate_report(condition_expr, start_date, end_date)

        if verbose:
            print(f"   [DONE] 총 {len(self.trades)}건 매매 완료")

        return self.report

    def _simulate_trade(
        self,
        code: str,
        signal_date: str,
        entry_date: str,
        all_trading_days: list[str]
    ) -> Optional[TradeResult]:
        """개별 종목 매매 시뮬레이션"""
        df = self.engine.df_daily

        # 매수일 데이터
        df_entry = df[(df['종목코드'] == code) & (df['날짜'] == entry_date)]
        if len(df_entry) == 0:
            return None

        entry_price = df_entry.iloc[0]['시가']
        if entry_price <= 0:
            return None

        # 매수일 인덱스
        try:
            entry_idx = all_trading_days.index(entry_date)
        except ValueError:
            return None

        # 매도 시뮬레이션
        exit_date = None
        exit_price = None
        exit_reason = None

        for hold_day in range(1, self.max_holding_days + 1):
            check_idx = entry_idx + hold_day
            if check_idx >= len(all_trading_days):
                break

            check_date = all_trading_days[check_idx]
            df_check = df[(df['종목코드'] == code) & (df['날짜'] == check_date)]

            if len(df_check) == 0:
                continue

            row = df_check.iloc[0]
            high = row['고가']
            low = row['저가']
            close = row['종가']

            # 손절 체크 (저가 기준)
            if low > 0:
                low_pct = (low - entry_price) / entry_price * 100
                if low_pct <= self.stop_loss:
                    exit_date = check_date
                    # 손절가로 매도 (손절 라인 도달 가격)
                    exit_price = entry_price * (1 + self.stop_loss / 100)
                    exit_reason = 'stop_loss'
                    break

            # 익절 체크 (고가 기준)
            if high > 0:
                high_pct = (high - entry_price) / entry_price * 100
                if high_pct >= self.take_profit:
                    exit_date = check_date
                    # 익절가로 매도 (익절 라인 도달 가격)
                    exit_price = entry_price * (1 + self.take_profit / 100)
                    exit_reason = 'take_profit'
                    break

            # 최대 보유기간 도달
            if hold_day == self.max_holding_days:
                exit_date = check_date
                exit_price = close
                exit_reason = 'max_holding'
                break

        # 매도 실패 (데이터 부족)
        if exit_date is None:
            return None

        # 수익률 계산
        return_pct = (exit_price - entry_price) / entry_price * 100

        # 보유일수 계산
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
            holding_days=holding_days
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

        print("\n[손절/익절 통계]")
        if r.total_trades > 0:
            tp_pct = r.tp_count / r.total_trades * 100
            sl_pct = r.sl_count / r.total_trades * 100
            mh_pct = r.max_hold_count / r.total_trades * 100
            print(f"   익절({r.take_profit:+}%): {r.tp_count}회 ({tp_pct:.1f}%)")
            print(f"   손절({r.stop_loss}%): {r.sl_count}회 ({sl_pct:.1f}%)")
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
        verbose: bool = True
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
                        'sl_count': report.sl_count
                    })

                    if verbose:
                        # 예상 남은 시간 계산
                        avg_time = sum(elapsed_times) / len(elapsed_times)
                        remaining = (total_combinations - count) * avg_time
                        remaining_min = int(remaining // 60)
                        remaining_sec = int(remaining % 60)

                        pct = count / total_combinations * 100
                        print(f"   [{count:>3}/{total_combinations}] TP={tp:+.0f}%, SL={sl:.0f}% → "
                              f"승률 {report.win_rate:>5.1f}%, 수익률 {report.avg_return:>+6.2f}% "
                              f"(남은시간: {remaining_min}분 {remaining_sec}초)")

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
