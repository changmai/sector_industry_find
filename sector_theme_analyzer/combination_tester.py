"""
조건 조합 자동 테스트 도구 (Combination Tester)

여러 조건의 모든 AND 조합을 자동으로 테스트하여 최적의 조합을 찾습니다.

사용 예시:
    # 기본 조건 A,B,C,D의 모든 조합 테스트 (고정 TP/SL)
    python combination_tester.py --conditions A,B,C,D --start-date 20231115 --end-date 20251205 --tp 10 --sl -5

    # GT 조건 포함 + TP/SL 최적화
    python combination_tester.py --conditions A,D,GT_A,GT_B --start-date 20231115 --end-date 20251205 --optimize

    # 2~3개 조합만 테스트
    python combination_tester.py --conditions A,B,C,D,E --min-size 2 --max-size 3

    # 로그 파일 저장 (진행상황 + 최종결과)
    python combination_tester.py --conditions A,B,C,D --log --start-date 20231115 --end-date 20251205
"""
import sys
import io
import os
import json
import argparse
import time
import multiprocessing as mp
from datetime import datetime
from itertools import combinations
from typing import Optional
from functools import partial

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
    import numpy as np
except ImportError:
    print("   [ERROR] numpy가 필요합니다: pip install numpy")
    sys.exit(1)

from condition_engine import ConditionEngine
from multi_backtester import MultiBacktester


# ============================================================================
# 로깅 시스템
# ============================================================================
class TeeLogger:
    """콘솔과 파일에 동시에 출력하는 로거"""

    def __init__(self, log_file: str):
        self.terminal = sys.stdout
        self.log_file = open(log_file, 'w', encoding='utf-8')
        self.log_path = log_file

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        # ANSI escape codes 제거 (로그 파일용)
        clean_message = self._remove_ansi(message)
        self.log_file.write(clean_message)
        self.log_file.flush()

    def _remove_ansi(self, text):
        """ANSI escape codes 제거"""
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()

    def close(self):
        self.log_file.close()


def setup_logging(log_dir: str = None, prefix: str = "combo_test") -> tuple:
    """
    로깅 설정

    Returns:
        (log_file_path, json_file_path): 로그 파일 경로들
    """
    if log_dir is None:
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')

    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"{prefix}_{timestamp}.log")
    json_file = os.path.join(log_dir, f"{prefix}_{timestamp}_results.json")

    return log_file, json_file


def save_results_json(results: list[dict], json_path: str, args: dict):
    """결과를 JSON 파일로 저장"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'parameters': args,
        'results': results,
        'summary': {
            'total_combinations': len(results),
            'valid_combinations': len([r for r in results if r.get('valid', False)]),
            'best_combination': None
        }
    }

    # 최고 조합 찾기
    valid_results = [r for r in results if r.get('valid', False)]
    if valid_results:
        best = max(valid_results, key=lambda x: x.get('avg_return', 0))
        output['summary']['best_combination'] = best

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return json_path


def format_time(seconds: float) -> str:
    """초를 HH:MM:SS 형식으로 변환"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def print_progress_bar(current: int, total: int, elapsed: float, width: int = 40):
    """ASCII 프로그레스 바 출력"""
    if total == 0:
        return

    pct = current / total
    filled = int(width * pct)
    bar = '#' * filled + '-' * (width - filled)

    # 시간 계산
    if current > 0:
        avg_time = elapsed / current
        remaining = (total - current) * avg_time
        total_estimated = elapsed + remaining
        eta_str = format_time(remaining)
        elapsed_str = format_time(elapsed)
        total_str = format_time(total_estimated)
    else:
        eta_str = '--:--'
        elapsed_str = '00:00'
        total_str = '--:--'

    # 출력 (줄바꿈 없이)
    print(f"\r   [{bar}] {current}/{total} ({pct*100:.1f}%) | "
          f"경과: {elapsed_str} | 예상총시간: {total_str} | 남은: {eta_str}  ", end='', flush=True)


def print_inner_progress(current: int, total: int, prefix: str = "", width: int = 20):
    """조합 내부 진행률 표시 (날짜 처리 진행)"""
    if total == 0:
        return

    pct = current / total
    filled = int(width * pct)
    bar = '#' * filled + '-' * (width - filled)

    print(f"\r{prefix}[{bar}] {pct*100:>3.0f}%", end='', flush=True)


def load_default_params() -> dict:
    """default.json에서 조건 파라미터 로드"""
    params_path = os.path.join(os.path.dirname(__file__), 'conditions', 'default.json')
    if os.path.exists(params_path):
        with open(params_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# ============================================================================
# 멀티프로세싱 워커
# ============================================================================
_worker_engine = None
_worker_backtester = None
_worker_params = None


def _init_worker(tp, sl, max_holding, trailing_start, trailing_offset,
                 time_cut_days, time_cut_min_return):
    """워커 프로세스 초기화 - 각 프로세스에서 한 번만 실행"""
    global _worker_engine, _worker_backtester, _worker_params

    # 데이터 로드 (프로세스당 1회) - 워커에서는 출력 억제
    import sys
    import io
    _old_stdout = sys.stdout
    sys.stdout = io.StringIO()  # 출력 억제
    try:
        _worker_engine = ConditionEngine()
        _worker_engine.load_data()
    finally:
        sys.stdout = _old_stdout

    # 백테스터 생성
    _worker_backtester = MultiBacktester(
        _worker_engine,
        stop_loss=sl,
        take_profit=tp,
        max_holding_days=max_holding,
        trailing_start=trailing_start,
        trailing_offset=trailing_offset,
        time_cut_days=time_cut_days,
        time_cut_min_return=time_cut_min_return
    )

    # 파라미터 로드
    _worker_params = load_default_params()


def _test_single_combo(args):
    """단일 조합 테스트 (워커에서 실행)"""
    expr, start_date, end_date, tp, sl, min_trades = args

    global _worker_engine, _worker_backtester, _worker_params

    try:
        report = _worker_backtester.run(
            start_date, end_date, expr, _worker_params, verbose=False
        )

        return {
            'expression': expr,
            'total_trades': report.total_trades if report else 0,
            'win_rate': report.win_rate if report else 0,
            'avg_return': report.avg_return if report else 0,
            'total_return': report.total_return if report else 0,
            'avg_holding_days': report.avg_holding_days if report else 0,
            'tp': tp,
            'sl': sl,
            'valid': (report.total_trades >= min_trades) if report else False
        }
    except Exception as e:
        return {
            'expression': expr,
            'total_trades': 0,
            'win_rate': 0,
            'avg_return': 0,
            'total_return': 0,
            'avg_holding_days': 0,
            'tp': tp,
            'sl': sl,
            'valid': False,
            'error': str(e)
        }


def generate_combinations(
    conditions: list[str],
    min_size: int = 2,
    max_size: int = None,
    required: str = None
) -> list[str]:
    """
    조건 목록에서 가능한 모든 AND 조합 생성

    Args:
        conditions: ['A', 'B', 'C', 'D']
        min_size: 최소 조합 크기 (기본 2) - required 제외한 조합 크기
        max_size: 최대 조합 크기 (기본: 전체) - required 제외한 조합 크기
        required: 필수 조건 표현식 (예: "A AND B") - 모든 조합에 포함됨

    Returns:
        ['A AND B', 'A AND C', ..., 'A AND B AND C AND D']
        또는 required가 있으면:
        ['A AND B AND C', 'A AND B AND D', ..., 'A AND B AND C AND D']
    """
    if max_size is None:
        max_size = len(conditions)

    all_combinations = []

    if required:
        # 필수 조건이 있는 경우: 나머지 조건들의 조합에 필수 조건을 앞에 붙임
        for r in range(min_size, max_size + 1):
            if r == 0:
                # min_size=0인 경우: 필수 조건만 테스트
                all_combinations.append(required)
            else:
                for combo in combinations(conditions, r):
                    expr = required + ' AND ' + ' AND '.join(combo)
                    all_combinations.append(expr)
    else:
        # 필수 조건이 없는 경우: 기존 방식
        for r in range(min_size, max_size + 1):
            for combo in combinations(conditions, r):
                expr = ' AND '.join(combo)
                all_combinations.append(expr)

    return all_combinations


def run_fixed_tpsl_tests(
    engine: ConditionEngine,
    params: dict,
    combos: list[str],
    start_date: str,
    end_date: str,
    tp: float,
    sl: float,
    min_trades: int,
    max_holding: int = 14,
    trailing_start: float = None,
    trailing_offset: float = None,
    time_cut_days: int = None,
    time_cut_min_return: float = None
) -> list[dict]:
    """
    고정 TP/SL로 모든 조합 테스트 (최적화 버전)

    Returns:
        list[dict]: 각 조합의 결과
    """
    results = []
    total = len(combos)
    start_time = time.time()

    print(f"\n[테스트 진행] 총 {total}개 조합")
    print("-" * 80)

    # 인스턴스 재사용: 루프 외부에서 1회만 생성
    backtester = MultiBacktester(
        engine,
        stop_loss=sl,
        take_profit=tp,
        max_holding_days=max_holding,
        trailing_start=trailing_start,
        trailing_offset=trailing_offset,
        time_cut_days=time_cut_days,
        time_cut_min_return=time_cut_min_return
    )

    for i, expr in enumerate(combos, 1):
        # 진행률 콜백 생성 (조합 번호와 표현식 포함)
        prefix = f"   [{i:>3}/{total}] {expr:<30} "

        def make_progress_callback(p):
            def callback(current, total_days):
                print_inner_progress(current, total_days, p)
            return callback

        progress_cb = make_progress_callback(prefix)

        report = backtester.run(start_date, end_date, expr, params, verbose=False,
                               progress_callback=progress_cb)

        elapsed = time.time() - start_time

        # 결과 저장
        result = {
            'expression': expr,
            'total_trades': report.total_trades if report else 0,
            'win_rate': report.win_rate if report else 0,
            'avg_return': report.avg_return if report else 0,
            'total_return': report.total_return if report else 0,
            'avg_holding_days': report.avg_holding_days if report else 0,
            'tp': tp,
            'sl': sl,
            'valid': (report.total_trades >= min_trades) if report else False
        }
        results.append(result)

        # 프로그레스 바 출력
        print_progress_bar(i, total, elapsed)

        # 상세 결과 출력 (새 줄에)
        status = "OK" if result['valid'] else f"거래수 부족({result['total_trades']}건)"
        print(f"\n   [{i:>3}/{total}] {expr:<30} → "
              f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
              f"수익률 {result['avg_return']:>+6.2f}% ({status})")

    print()  # 마지막 줄바꿈
    return results


def run_parallel_tests(
    combos: list[str],
    start_date: str,
    end_date: str,
    tp: float,
    sl: float,
    min_trades: int,
    max_holding: int = 14,
    trailing_start: float = None,
    trailing_offset: float = None,
    time_cut_days: int = None,
    time_cut_min_return: float = None,
    workers: int = 4
) -> list[dict]:
    """
    멀티프로세싱으로 조합 테스트 (병렬 실행)

    Args:
        combos: 테스트할 조건 조합 리스트
        workers: 병렬 워커 수

    Returns:
        list[dict]: 각 조합의 결과
    """
    total = len(combos)
    start_time = time.time()

    print(f"\n[테스트 진행] 총 {total}개 조합 (병렬 {workers}개 워커)")
    print("-" * 80)
    print(f"   워커 초기화 중... (각 워커에서 데이터 로드)", flush=True)

    # 작업 인자 준비
    task_args = [(expr, start_date, end_date, tp, sl, min_trades) for expr in combos]

    # 멀티프로세싱 풀 생성
    init_args = (tp, sl, max_holding, trailing_start, trailing_offset,
                 time_cut_days, time_cut_min_return)

    results = []
    completed = 0

    with mp.Pool(
        processes=workers,
        initializer=_init_worker,
        initargs=init_args
    ) as pool:
        # imap_unordered로 완료되는 순서대로 결과 수집
        for result in pool.imap_unordered(_test_single_combo, task_args):
            completed += 1
            elapsed = time.time() - start_time
            results.append(result)

            # 프로그레스 바 출력
            print_progress_bar(completed, total, elapsed)

            # 결과 출력
            status = "OK" if result['valid'] else f"거래수 부족({result['total_trades']}건)"
            print(f"\n   [{completed:>3}/{total}] {result['expression']:<30} → "
                  f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
                  f"수익률 {result['avg_return']:>+6.2f}% ({status})")

    print()  # 마지막 줄바꿈

    # 원래 순서대로 정렬 (조합 순서 유지)
    combo_order = {expr: i for i, expr in enumerate(combos)}
    results.sort(key=lambda x: combo_order.get(x['expression'], 999999))

    return results


def run_optimized_tests(
    engine: ConditionEngine,
    params: dict,
    combos: list[str],
    start_date: str,
    end_date: str,
    tp_min: float,
    tp_max: float,
    sl_min: float,
    sl_max: float,
    step: float,
    min_trades: int,
    max_holding: int = 14,
    trailing_start: float = None,
    trailing_offset: float = None,
    time_cut_days: int = None,
    time_cut_min_return: float = None
) -> list[dict]:
    """
    각 조합별로 TP/SL 최적화 수행 (최적화 버전)

    Returns:
        list[dict]: 각 조합의 최적 TP/SL 결과
    """
    results = []
    total = len(combos)

    # TP/SL 조합 수 계산
    tp_values = np.arange(tp_min, tp_max + step, step)
    sl_values = np.arange(sl_min, sl_max + step, step)
    tpsl_count = len(tp_values) * len(sl_values)

    print(f"\n[테스트 진행] 총 {total}개 조합 x {tpsl_count} TP/SL = {total * tpsl_count}개 테스트")
    print("-" * 80)

    start_time = time.time()

    # 인스턴스 재사용: 루프 외부에서 1회만 생성
    backtester = MultiBacktester(
        engine,
        max_holding_days=max_holding,
        trailing_start=trailing_start,
        trailing_offset=trailing_offset,
        time_cut_days=time_cut_days,
        time_cut_min_return=time_cut_min_return
    )

    for i, expr in enumerate(combos, 1):
        # 진행률 콜백 생성 (조합 번호와 표현식 포함)
        prefix = f"   [{i:>3}/{total}] {expr:<25} "

        def make_progress_callback(p):
            def callback(current, total_tpsl):
                print_inner_progress(current, total_tpsl, p)
            return callback

        progress_cb = make_progress_callback(prefix)

        # 이 조합에 대해 TP/SL 최적화
        opt_results = backtester.optimize_tp_sl(
            start_date, end_date, expr, params,
            tp_range=(tp_min, tp_max),
            sl_range=(sl_min, sl_max),
            step=step,
            verbose=False,
            progress_callback=progress_cb
        )

        elapsed = time.time() - start_time

        # 최적 결과 선택
        if opt_results:
            best = opt_results[0]  # 평균수익률 기준 정렬되어 있음
            result = {
                'expression': expr,
                'total_trades': best['total_trades'],
                'win_rate': best['win_rate'],
                'avg_return': best['avg_return'],
                'total_return': best.get('total_return', best['avg_return'] * best['total_trades']),
                'avg_holding_days': best.get('avg_holding_days', 0),
                'tp': best['tp'],
                'sl': best['sl'],
                'valid': best['total_trades'] >= min_trades
            }
        else:
            result = {
                'expression': expr,
                'total_trades': 0,
                'win_rate': 0,
                'avg_return': 0,
                'total_return': 0,
                'avg_holding_days': 0,
                'tp': tp_min,
                'sl': sl_min,
                'valid': False
            }

        results.append(result)

        # 상세 결과 출력 (진행바 라인 덮어쓰기)
        status = "OK" if result['valid'] else f"거래수 부족({result['total_trades']}건)"
        print(f"\r   [{i:>3}/{total}] {expr:<25} → 최적 TP={result['tp']:+.0f}%/SL={result['sl']:.0f}%, "
              f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
              f"수익률 {result['avg_return']:>+6.2f}% ({status})")

        # 프로그레스 바 출력 (다음 조합 시작 전)
        print_progress_bar(i, total, elapsed)
        print()  # 줄바꿈

    print()  # 마지막 줄바꿈
    return results


def print_results(
    results: list[dict],
    sort_by: str = 'avg_return',
    top_n: int = 20,
    min_trades: int = 100,
    optimize_mode: bool = False
):
    """결과 출력"""
    # 유효한 결과만 필터링
    valid_results = [r for r in results if r['valid']]
    invalid_results = [r for r in results if not r['valid']]

    # 정렬
    valid_results.sort(key=lambda x: x[sort_by], reverse=True)

    sort_name = "평균수익률" if sort_by == 'avg_return' else "승률"

    print("\n" + "=" * 100)
    if optimize_mode:
        print(f"   [결과 - {sort_name} 순 (각 조합의 최적 TP/SL 적용)]")
    else:
        print(f"   [결과 - {sort_name} 순]")
    print("=" * 100)

    if optimize_mode:
        # 데이터: {i:^5}{expr:<30}{tp:>+7.0f}%{sl:>+7.0f}%{trades:>8}{wr:>7.1f}%{avg:>+11.2f}%{hold:>7.1f}일
        # 너비:    5    +   30   +   8    +   8    +  8   +   8   +    12    +   8   = 87
        print("   순위 조건 조합                      최적TP  최적SL  거래수    승률   평균수익률  평균보유")
    else:
        # 데이터: {i:^5}{expr:<30}{trades:>8}{wr:>7.1f}%{avg:>+11.2f}%{total:>+11.1f}%{hold:>7.1f}일
        # 너비:    5    +   30   +   8    +   8   +    12    +    12    +   8   = 83
        print("   순위 조건 조합                      거래수    승률   평균수익률    총수익률  평균보유")
    print("-" * 100)

    for i, r in enumerate(valid_results[:top_n], 1):
        if optimize_mode:
            print(f"   {i:^5}{r['expression']:<30}{r['tp']:>+7.0f}%{r['sl']:>+7.0f}%"
                  f"{r['total_trades']:>8}{r['win_rate']:>7.1f}%{r['avg_return']:>+11.2f}%{r['avg_holding_days']:>7.1f}일")
        else:
            print(f"   {i:^5}{r['expression']:<30}{r['total_trades']:>8}{r['win_rate']:>7.1f}%"
                  f"{r['avg_return']:>+11.2f}%{r['total_return']:>+11.1f}%{r['avg_holding_days']:>7.1f}일")

    print("=" * 100)

    # 필터링된 조합 출력
    if invalid_results:
        print(f"\n[필터링된 조합] (거래수 < {min_trades}건)")
        for r in invalid_results[:10]:
            print(f"   - {r['expression']}: {r['total_trades']}건")
        if len(invalid_results) > 10:
            print(f"   ... 외 {len(invalid_results) - 10}개")

    # 최고 조합 강조
    if valid_results:
        best = valid_results[0]
        print("\n" + "=" * 100)
        print(f"   [BEST] {best['expression']}")
        if optimize_mode:
            print(f"          최적 TP={best['tp']:+.0f}%, SL={best['sl']:.0f}%")
        print(f"          거래 {best['total_trades']}건, 승률 {best['win_rate']:.1f}%, 평균수익률 {best['avg_return']:+.2f}%, 평균보유 {best['avg_holding_days']:.1f}일")
        print("=" * 100)


def parse_args():
    """CLI 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="조건 조합 자동 테스트 도구",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  # 고정 TP/SL로 테스트
  python combination_tester.py --conditions A,B,C,D --start-date 20231115 --end-date 20251205 --tp 10 --sl -5

  # TP/SL 최적화 포함
  python combination_tester.py --conditions A,D,GT_A,GT_B --start-date 20231115 --end-date 20251205 --optimize

  # 2~3개 조합만 테스트
  python combination_tester.py --conditions A,B,C,D,E,F,G --min-size 2 --max-size 3 --min-trades 50

  # 필수 조건 + 조합 테스트 (A AND B는 고정, C,D,E 중 1~2개 조합)
  python combination_tester.py --required A,B --conditions C,D,E --min-size 1 --max-size 2
        """
    )

    # 필수 인자
    parser.add_argument('--conditions', '-c', required=True,
                        help='테스트할 조건 목록 (콤마 구분). 예: A,B,C,D 또는 A,D,GT_A,GT_B')
    parser.add_argument('--required', '-r', default=None,
                        help='필수 조건 (모든 조합에 포함). 예: "A AND B" 또는 "A,B" (콤마→AND 변환)')
    parser.add_argument('--start-date', '-s', required=True,
                        help='백테스트 시작일 (YYYYMMDD)')
    parser.add_argument('--end-date', '-e', required=True,
                        help='백테스트 종료일 (YYYYMMDD)')

    # 조합 옵션
    parser.add_argument('--min-size', type=int, default=2,
                        help='최소 조합 크기 (기본: 2)')
    parser.add_argument('--max-size', type=int, default=None,
                        help='최대 조합 크기 (기본: 전체)')
    parser.add_argument('--min-trades', type=int, default=100,
                        help='최소 거래 건수 - 이하는 무효 처리 (기본: 100)')

    # TP/SL 옵션 (고정 모드)
    parser.add_argument('--tp', type=float, default=10.0,
                        help='익절선 %% (기본: 10)')
    parser.add_argument('--sl', type=float, default=-5.0,
                        help='손절선 %% (기본: -5)')
    parser.add_argument('--max-holding', type=int, default=14,
                        help='최대 보유일 (기본: 14)')

    # 트레일링 스탑 옵션
    parser.add_argument('--trailing-start', type=float, default=None,
                        help='트레일링 시작 수익률 %% (예: 5 = 5%% 수익 시 활성화)')
    parser.add_argument('--trailing-offset', type=float, default=None,
                        help='고점 대비 하락 허용폭 %% (예: 3 = 고점 대비 3%% 하락 시 청산)')

    # 타임컷 옵션
    parser.add_argument('--time-cut-days', type=int, default=None,
                        help='타임컷 체크 일수 (예: 5 = 5일차에 수익률 체크)')
    parser.add_argument('--time-cut-min-return', type=float, default=None,
                        help='타임컷 최소 수익률 %% (이하면 청산, 예: 3 = 3%% 미만 시 청산)')

    # TP/SL 최적화 옵션
    parser.add_argument('--optimize', action='store_true',
                        help='조합별 TP/SL 최적화 활성화')
    parser.add_argument('--tp-min', type=float, default=5.0,
                        help='TP 최적화 최소값 (기본: 5)')
    parser.add_argument('--tp-max', type=float, default=15.0,
                        help='TP 최적화 최대값 (기본: 15)')
    parser.add_argument('--sl-min', type=float, default=-7.0,
                        help='SL 최적화 최소값 (기본: -7)')
    parser.add_argument('--sl-max', type=float, default=-3.0,
                        help='SL 최적화 최대값 (기본: -3)')
    parser.add_argument('--step', type=float, default=1.0,
                        help='TP/SL 최적화 스텝 (기본: 1)')

    # 출력 옵션
    parser.add_argument('--sort-by', choices=['win_rate', 'avg_return'], default='avg_return',
                        help='정렬 기준 (기본: avg_return)')
    parser.add_argument('--top', type=int, default=20,
                        help='상위 N개만 출력 (기본: 20)')

    # 로깅 옵션
    parser.add_argument('--log', action='store_true',
                        help='로그 파일 저장 (logs/ 폴더에 자동 생성)')
    parser.add_argument('--log-dir', type=str, default=None,
                        help='로그 저장 디렉토리 (기본: ./logs)')

    # 병렬 처리 옵션
    parser.add_argument('--workers', '-w', type=int, default=1,
                        help='병렬 워커 수 (기본: 1, 0=자동=CPU코어수)')

    return parser.parse_args()


def main():
    args = parse_args()

    # 로깅 설정
    logger = None
    log_file = None
    json_file = None

    if args.log:
        log_file, json_file = setup_logging(args.log_dir)
        logger = TeeLogger(log_file)
        sys.stdout = logger
        print(f"[로그 저장 활성화]")
        print(f"   로그 파일: {log_file}")
        print(f"   결과 JSON: {json_file}")
        print()

    # 조건 목록 파싱
    conditions = [c.strip().upper() for c in args.conditions.split(',')]

    # 필수 조건 파싱 (콤마 → AND 변환)
    required_expr = None
    required_conditions = []
    if args.required:
        # "A,B" 형식이면 "A AND B"로 변환
        if ',' in args.required and ' AND ' not in args.required.upper():
            required_conditions = [c.strip().upper() for c in args.required.split(',')]
            required_expr = ' AND '.join(required_conditions)
        else:
            required_expr = args.required.upper()
            # "A AND B" 형식에서 조건 추출
            required_conditions = [c.strip() for c in required_expr.replace(' AND ', ',').split(',')]

    # 유효한 조건인지 확인
    valid_conditions = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                        'GT_P1', 'GT_M1', 'GT_M2', 'GT_A', 'GT_B', 'GT_B1', 'GT_B2',
                        'GT_C', 'GT_D', 'GT_D2', 'GT_E', 'GT_F'}

    # 조합 조건 검증
    invalid = [c for c in conditions if c not in valid_conditions]
    if invalid:
        print(f"   [ERROR] 알 수 없는 조건: {', '.join(invalid)}")
        print(f"   사용 가능한 조건: {', '.join(sorted(valid_conditions))}")
        sys.exit(1)

    # 필수 조건 검증
    if required_conditions:
        invalid_req = [c for c in required_conditions if c not in valid_conditions]
        if invalid_req:
            print(f"   [ERROR] 필수 조건에 알 수 없는 조건: {', '.join(invalid_req)}")
            print(f"   사용 가능한 조건: {', '.join(sorted(valid_conditions))}")
            sys.exit(1)

    # 조합 생성
    max_size = args.max_size if args.max_size else len(conditions)
    combos = generate_combinations(conditions, args.min_size, max_size, required=required_expr)

    print("=" * 80)
    if args.optimize:
        print("   조건 조합 테스트 (TP/SL 최적화 모드)")
    else:
        print("   조건 조합 테스트")
    print("=" * 80)
    if required_expr:
        print(f"   필수 조건: {required_expr}")
        print(f"   조합 조건: {', '.join(conditions)}")
    else:
        print(f"   테스트 조건: {', '.join(conditions)}")
    print(f"   기간: {args.start_date} ~ {args.end_date}")
    if args.optimize:
        print(f"   TP 범위: {args.tp_min}% ~ {args.tp_max}% | SL 범위: {args.sl_min}% ~ {args.sl_max}% (step: {args.step})")
    else:
        print(f"   TP: +{args.tp}% | SL: {args.sl}%")
    print(f"   최대 보유일: {args.max_holding}일")
    if args.trailing_start is not None and args.trailing_offset is not None:
        print(f"   트레일링: {args.trailing_start:+.1f}% 도달 시 활성화, 고점 대비 -{args.trailing_offset:.1f}% 하락 시 청산")
    if args.time_cut_days is not None and args.time_cut_min_return is not None:
        print(f"   타임컷: {args.time_cut_days}일 후 수익률 {args.time_cut_min_return:+.1f}% 미만 시 청산")
    print(f"   최소 거래수: {args.min_trades}건")
    print(f"   조합 크기: {args.min_size} ~ {max_size}개")
    print(f"   총 조합 수: {len(combos)}개")

    # 워커 수 결정
    workers = args.workers
    if workers == 0:
        workers = mp.cpu_count()
    if workers > 1 and not args.optimize:
        print(f"   병렬 처리: {workers}개 워커")
    print("=" * 80)

    # 병렬 모드 여부 결정 (최적화 모드는 아직 병렬 미지원)
    use_parallel = workers > 1 and not args.optimize

    if use_parallel:
        # 병렬 모드: 각 워커에서 데이터 로드
        print("\n[1] 병렬 모드 - 워커에서 데이터 로드 예정")
        engine = None
        params = None
    else:
        # 순차 모드: 메인 프로세스에서 데이터 로드
        print("\n[1] 데이터 로드 중...")
        engine = ConditionEngine()
        if not engine.load_data():
            print("   [ERROR] 데이터 로드 실패")
            sys.exit(1)

        # 파라미터 로드
        params = load_default_params()
        print(f"   -> 조건 파라미터 로드 완료")

    # 테스트 실행
    print("\n[2] 조합 테스트 시작...")
    start_time = time.time()

    if args.optimize:
        results = run_optimized_tests(
            engine, params, combos,
            args.start_date, args.end_date,
            args.tp_min, args.tp_max,
            args.sl_min, args.sl_max,
            args.step,
            args.min_trades,
            args.max_holding,
            args.trailing_start,
            args.trailing_offset,
            args.time_cut_days,
            args.time_cut_min_return
        )
    elif use_parallel:
        # 병렬 테스트
        results = run_parallel_tests(
            combos,
            args.start_date, args.end_date,
            args.tp, args.sl,
            args.min_trades,
            args.max_holding,
            args.trailing_start,
            args.trailing_offset,
            args.time_cut_days,
            args.time_cut_min_return,
            workers=workers
        )
    else:
        # 순차 테스트
        results = run_fixed_tpsl_tests(
            engine, params, combos,
            args.start_date, args.end_date,
            args.tp, args.sl,
            args.min_trades,
            args.max_holding,
            args.trailing_start,
            args.trailing_offset,
            args.time_cut_days,
            args.time_cut_min_return
        )

    elapsed = time.time() - start_time
    elapsed_min = int(elapsed // 60)
    elapsed_sec = int(elapsed % 60)
    print(f"\n   [완료] 총 소요시간: {elapsed_min}분 {elapsed_sec}초")

    # 결과 출력
    print_results(
        results,
        sort_by=args.sort_by,
        top_n=args.top,
        min_trades=args.min_trades,
        optimize_mode=args.optimize
    )

    # JSON 결과 저장 (로깅 활성화 시)
    if args.log and json_file:
        args_dict = {
            'conditions': args.conditions,
            'required': args.required,
            'start_date': args.start_date,
            'end_date': args.end_date,
            'tp': args.tp,
            'sl': args.sl,
            'max_holding': args.max_holding,
            'min_trades': args.min_trades,
            'min_size': args.min_size,
            'max_size': args.max_size,
            'optimize': args.optimize,
            'trailing_start': args.trailing_start,
            'trailing_offset': args.trailing_offset,
            'time_cut_days': args.time_cut_days,
            'time_cut_min_return': args.time_cut_min_return,
            'elapsed_seconds': elapsed
        }
        save_results_json(results, json_file, args_dict)
        print(f"\n[로그 저장 완료]")
        print(f"   로그 파일: {log_file}")
        print(f"   결과 JSON: {json_file}")

    # 로거 정리
    if logger:
        sys.stdout = logger.terminal
        logger.close()


if __name__ == "__main__":
    main()
