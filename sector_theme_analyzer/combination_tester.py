"""
조건 조합 자동 테스트 도구 (Combination Tester)

여러 조건의 모든 AND 조합을 자동으로 테스트하여 최적의 조합을 찾습니다.
파라미터 조합 테스트, 2단계 자동 최적화도 지원합니다.

================================================================================
사용 예시
================================================================================

[1] 기본 조합 테스트 (고정 TP/SL)
--------------------------------------------------------------------------------
    # A,B,C,D 조건의 모든 2~4개 조합 테스트
    python combination_tester.py --conditions A,B,C,D --start-date 20231115 --end-date 20251205 --tp 10 --sl -5

    # GT 조건 포함 테스트
    python combination_tester.py --conditions A,D,GT_A,GT_B --start-date 20231115 --end-date 20251205

    # 2~3개 조합만 테스트
    python combination_tester.py --conditions A,B,C,D,E --min-size 2 --max-size 3

    # 필수 조건 고정 + 나머지 조합 테스트 (A AND B 고정, C,D,E 중 조합)
    python combination_tester.py --required A,B --conditions C,D,E --min-size 1 --max-size 2

[2] TP/SL 최적화 모드
--------------------------------------------------------------------------------
    # 각 조합별 최적 TP/SL 자동 탐색
    python combination_tester.py --conditions A,D,GT_A --optimize --tp-min 5 --tp-max 15 --sl-min -7 --sl-max -3

[3] 파라미터 그리드 테스트 (--param-grid)
--------------------------------------------------------------------------------
    # 단일 조건 파라미터 최적화
    python combination_tester.py --conditions H --param-grid "H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03"

    # 여러 조건 파라미터 동시 테스트
    python combination_tester.py --conditions A,D,H --param-grid "A.days:2,3,5;H.smart_money_turnover:5,10"

    # 조건명 생략 시 모든 조건에 해당 파라미터 적용
    python combination_tester.py --conditions A,B --param-grid "days:2,3,5"

[4] 2단계 자동 최적화 (--auto-optimize)
--------------------------------------------------------------------------------
    [1단계] 각 조건별 파라미터 최적화 (DEFAULT_PARAM_GRIDS 기반)
    [2단계] 최적 파라미터로 조건 조합 테스트

    # 자동 최적화 실행
    python combination_tester.py --conditions A,D,H,I --auto-optimize --start-date 20240101 --end-date 20241231

    # 자동 최적화 후 default.json에 최적 파라미터 저장
    python combination_tester.py --conditions H,I --auto-optimize --update-defaults --start-date 20240101 --end-date 20241231

[5] 트레일링스탑 / 타임컷 옵션
--------------------------------------------------------------------------------
    # 트레일링스탑: 5% 수익 시 활성화, 고점 대비 3% 하락 시 청산
    python combination_tester.py --conditions A,D --trailing-start 5 --trailing-offset 3

    # 타임컷: 3일 후 수익률 2% 미만 시 청산
    python combination_tester.py --conditions A,D --time-cut-days 3 --time-cut-min-return 2

[6] 로그 저장 및 병렬 처리
--------------------------------------------------------------------------------
    # 로그 파일 저장 (logs/ 폴더에 자동 생성)
    python combination_tester.py --conditions A,B,C,D --log

    # 병렬 처리 (4개 워커)
    python combination_tester.py --conditions A,B,C,D,E,F --workers 4

================================================================================
주요 옵션 설명
================================================================================

조건 관련:
  --conditions, -c      테스트할 조건 목록 (필수). 예: A,B,C,D 또는 A,D,GT_A,GT_B
  --required, -r        필수 조건 (모든 조합에 포함). 예: "A AND B" 또는 "A,B"
  --min-size            최소 조합 크기 (기본: 2)
  --max-size            최대 조합 크기 (기본: 전체)
  --min-trades          최소 거래 건수 (기본: 100)

TP/SL 관련:
  --tp                  익절선 % (기본: 10)
  --sl                  손절선 % (기본: -5)
  --max-holding         최대 보유일 (기본: 14)
  --optimize            TP/SL 최적화 활성화
  --tp-min, --tp-max    TP 최적화 범위
  --sl-min, --sl-max    SL 최적화 범위
  --step                최적화 스텝 (기본: 1)

파라미터 최적화:
  --param-grid, -pg     파라미터 그리드 테스트
  --auto-optimize, -ao  2단계 자동 최적화
  --update-defaults     자동 최적화 후 default.json 업데이트

트레일링/타임컷:
  --trailing-start      트레일링 시작 수익률 %
  --trailing-offset     고점 대비 하락 허용폭 %
  --time-cut-days       타임컷 체크 일수
  --time-cut-min-return 타임컷 최소 수익률 %

출력/로그:
  --sort-by             정렬 기준 (win_rate, avg_return)
  --top                 상위 N개 출력 (기본: 20)
  --log                 로그 파일 저장
  --workers, -w         병렬 워커 수 (기본: 1)
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

# Dask 분산 처리 (선택적)
DASK_AVAILABLE = False
try:
    from dask.distributed import Client, LocalCluster
    import dask
    DASK_AVAILABLE = True
except ImportError:
    pass

from condition_engine import ConditionEngine
from multi_backtester import MultiBacktester, warmup_numba_kernel, NUMBA_AVAILABLE
from itertools import product


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
# 파라미터 그리드 파싱 및 조합 생성
# ============================================================================
def parse_param_grid(param_grid_str: str) -> dict:
    """
    파라미터 그리드 문자열 파싱

    형식:
        "param1:val1,val2,val3;param2:val1,val2"
        "H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03"

    Returns:
        {
            'H': {'smart_money_turnover': [5, 10, 15], 'support_margin': [0.02, 0.03]},
            ...
        }
        또는 조건 지정 없으면:
        {
            None: {'param1': [val1, val2], 'param2': [val1, val2]}
        }
    """
    if not param_grid_str:
        return {}

    result = {}

    # 세미콜론으로 파라미터 분리
    for param_spec in param_grid_str.split(';'):
        param_spec = param_spec.strip()
        if not param_spec or ':' not in param_spec:
            continue

        param_part, values_part = param_spec.split(':', 1)
        param_part = param_part.strip()
        values_part = values_part.strip()

        # 조건명.파라미터명 형식인지 확인
        if '.' in param_part:
            condition, param_name = param_part.split('.', 1)
            condition = condition.upper()
        else:
            # 조건 지정 없으면 모든 조건에 적용
            condition = None
            param_name = param_part

        # 값 파싱 (숫자로 변환 시도)
        values = []
        for v in values_part.split(','):
            v = v.strip()
            try:
                # 정수 시도
                if '.' not in v:
                    values.append(int(v))
                else:
                    values.append(float(v))
            except ValueError:
                # bool 처리
                if v.lower() == 'true':
                    values.append(True)
                elif v.lower() == 'false':
                    values.append(False)
                else:
                    values.append(v)

        # 결과에 추가
        if condition not in result:
            result[condition] = {}
        result[condition][param_name] = values

    return result


def generate_param_combinations(param_grid: dict, base_params: dict, conditions: list[str]) -> list[dict]:
    """
    파라미터 그리드에서 모든 조합 생성

    Args:
        param_grid: parse_param_grid() 결과
        base_params: default.json 기본 파라미터
        conditions: 테스트 대상 조건 목록

    Returns:
        파라미터 조합 리스트, 각 항목은 {condition: {param: value}} 형태
    """
    if not param_grid:
        return [base_params.copy()]

    # 파라미터 키-값 리스트 생성
    param_keys = []  # [(condition, param_name), ...]
    param_values = []  # [[val1, val2], [val1, val2, val3], ...]

    for condition, params in param_grid.items():
        for param_name, values in params.items():
            if condition is None:
                # 조건 미지정: 해당 파라미터를 가진 모든 조건에 적용
                for cond in conditions:
                    cond_upper = cond.upper()
                    if cond_upper in base_params and param_name in base_params[cond_upper]:
                        param_keys.append((cond_upper, param_name))
                        param_values.append(values)
            else:
                param_keys.append((condition, param_name))
                param_values.append(values)

    if not param_keys:
        return [base_params.copy()]

    # 모든 조합 생성
    combinations_list = []
    for combo in product(*param_values):
        # 기본 파라미터 복사
        new_params = {}
        for cond, params in base_params.items():
            new_params[cond] = params.copy() if isinstance(params, dict) else params

        # 조합 값 적용
        for (condition, param_name), value in zip(param_keys, combo):
            if condition in new_params:
                new_params[condition][param_name] = value

        combinations_list.append(new_params)

    return combinations_list


def get_param_diff_str(params: dict, base_params: dict, conditions: list[str]) -> str:
    """파라미터 차이를 문자열로 반환 (변경된 것만)"""
    diffs = []
    for cond in conditions:
        cond_upper = cond.upper()
        if cond_upper not in params or cond_upper not in base_params:
            continue

        for param_name, value in params[cond_upper].items():
            if param_name == 'description':
                continue
            base_value = base_params.get(cond_upper, {}).get(param_name)
            if base_value != value:
                diffs.append(f"{cond_upper}.{param_name}={value}")

    return ', '.join(diffs) if diffs else "(기본값)"


# ============================================================================
# 조건별 기본 파라미터 그리드 (자동 최적화용)
# ============================================================================
DEFAULT_PARAM_GRIDS = {
    'A': {
        'days': [2, 3, 5]
    },
    'B': {
        'days': [20, 40, 60]
    },
    'C': {
        'top_n': [50, 100, 200],
        'min_rate': [0.0, 1.0, 3.0]
    },
    'D': {
        'short': [5, 10, 20],
        'mid': [20, 40, 60],
        'long': [60, 90, 120]
    },
    'E': {
        'days': [20, 40, 60],
        'min_pct': [-10.0, -5.0, -3.0],
        'max_pct': [0.0, 3.0, 5.0]
    },
    'F': {
        'compare_days': [3, 5, 10],
        'min_ratio': [150, 200, 300]
    },
    'G': {
        'min_rate': [3.0, 5.0, 10.0],
        'max_rate': [50.0, 100.0, 500.0]
    },
    'H': {
        'smart_money_turnover': [5.0, 10.0, 15.0],
        'support_margin': [0.02, 0.03, 0.05],
        'min_trade_value': [300000000, 500000000, 1000000000]
    },
    'I': {
        'disparity_min': [1.08, 1.10, 1.12, 1.15],
        'disparity_max': [1.20, 1.25, 1.30],
        'min_turnover': [2.0, 3.0, 5.0]
    },
    'GT_A': {
        'macd_fast': [9, 12, 15],
        'macd_slow': [20, 26, 30]
    },
    'GT_B': {
        'rsi_period': [7, 14, 21],
        'rsi_oversold': [25.0, 30.0, 35.0]
    },
    'GT_C': {
        'rsi_overbought': [65.0, 70.0, 75.0]
    },
    'GT_D': {
        'lookback_days': [10, 20, 30],
        'bounce_pct': [0.02, 0.03, 0.05]
    },
    'GT_D2': {
        'short_period': [3, 5, 7],
        'long_period': [15, 20, 30]
    },
    'GT_E': {
        'short_period': [5, 10, 20],
        'long_period': [40, 60, 120],
        'convergence_pct': [0.02, 0.03, 0.05]
    },
    'GT_F': {
        'avg_period': [10, 20, 30],
        'volume_multiplier': [1.5, 2.0, 3.0]
    }
}


def get_default_param_grid(condition: str) -> dict:
    """조건에 대한 기본 파라미터 그리드 반환"""
    return DEFAULT_PARAM_GRIDS.get(condition.upper(), {})


def update_default_json(optimized_params: dict, json_path: str = None):
    """최적화된 파라미터로 default.json 업데이트"""
    if json_path is None:
        json_path = os.path.join(os.path.dirname(__file__), 'conditions', 'default.json')

    # 기존 파일 로드
    with open(json_path, 'r', encoding='utf-8') as f:
        current_params = json.load(f)

    # 업데이트
    for condition, params in optimized_params.items():
        if condition in current_params:
            for param_name, value in params.items():
                if param_name != 'description':
                    current_params[condition][param_name] = value

    # 저장
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(current_params, f, ensure_ascii=False, indent=2)

    return json_path


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
        # [최적화] GT 지표 사전계산 (워커당 1회, 이후 필터링만 수행)
        _worker_engine.precompute_gt_indicators(verbose=False)
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

    # Numba JIT 워밍업 (첫 호출 시 컴파일 오버헤드 제거)
    warmup_numba_kernel()

    # 파라미터 로드
    _worker_params = load_default_params()


def _test_single_combo(args):
    """단일 조합 테스트 (워커에서 실행)"""
    import gc
    expr, start_date, end_date, tp, sl, min_trades = args

    global _worker_engine, _worker_backtester, _worker_params

    try:
        report = _worker_backtester.run(
            start_date, end_date, expr, _worker_params, verbose=False
        )

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

        # [최적화] 테스트 완료 후 캐시 클리어 및 GC 강제 (메모리 누수 방지)
        _worker_engine.clear_cache()
        gc.collect()

        return result
    except Exception as e:
        # 에러 시에도 캐시 클리어
        _worker_engine.clear_cache()
        gc.collect()

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


# ============================================================================
# Mode 3 (--param-grid) 병렬 처리용 워커 함수들
# ============================================================================
_pg_worker_engine = None
_pg_worker_backtester = None
_pg_worker_base_params = None
_pg_worker_condition_expr = None
_pg_worker_conditions = None
_pg_worker_min_trades = None


def _init_param_grid_worker(tp, sl, max_holding, trailing_start, trailing_offset,
                            time_cut_days, time_cut_min_return, base_params,
                            condition_expr, conditions, min_trades):
    """파라미터 그리드 워커 프로세스 초기화"""
    global _pg_worker_engine, _pg_worker_backtester, _pg_worker_base_params
    global _pg_worker_condition_expr, _pg_worker_conditions, _pg_worker_min_trades

    # 데이터 로드 (프로세스당 1회) - 워커에서는 출력 억제
    import sys
    import io
    _old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        _pg_worker_engine = ConditionEngine()
        _pg_worker_engine.load_data()
        # [최적화] GT 지표 사전계산 (워커당 1회)
        _pg_worker_engine.precompute_gt_indicators(verbose=False)
    finally:
        sys.stdout = _old_stdout

    # 백테스터 생성
    _pg_worker_backtester = MultiBacktester(
        _pg_worker_engine,
        stop_loss=sl,
        take_profit=tp,
        max_holding_days=max_holding,
        trailing_start=trailing_start,
        trailing_offset=trailing_offset,
        time_cut_days=time_cut_days,
        time_cut_min_return=time_cut_min_return
    )

    # Numba JIT 워밍업 (첫 호출 시 컴파일 오버헤드 제거)
    warmup_numba_kernel()

    # 공유 파라미터 저장
    _pg_worker_base_params = base_params
    _pg_worker_condition_expr = condition_expr
    _pg_worker_conditions = conditions
    _pg_worker_min_trades = min_trades


def _test_single_param_combo(args):
    """단일 파라미터 조합 테스트 (워커에서 실행)"""
    import gc
    params, start_date, end_date, tp, sl = args

    global _pg_worker_engine, _pg_worker_backtester, _pg_worker_base_params
    global _pg_worker_condition_expr, _pg_worker_conditions, _pg_worker_min_trades

    try:
        report = _pg_worker_backtester.run(
            start_date, end_date, _pg_worker_condition_expr, params, verbose=False
        )

        param_diff = get_param_diff_str(params, _pg_worker_base_params, _pg_worker_conditions)

        result = {
            'expression': _pg_worker_condition_expr,
            'params': param_diff,
            'params_dict': {k: v for k, v in params.items() if k in [c.upper() for c in _pg_worker_conditions]},
            'total_trades': report.total_trades if report else 0,
            'win_rate': report.win_rate if report else 0,
            'avg_return': report.avg_return if report else 0,
            'total_return': report.total_return if report else 0,
            'avg_holding_days': report.avg_holding_days if report else 0,
            'tp': tp,
            'sl': sl,
            'valid': (report.total_trades >= _pg_worker_min_trades) if report else False
        }

        # [최적화] 테스트 완료 후 캐시 클리어 및 GC 강제
        _pg_worker_engine.clear_cache()
        gc.collect()

        return result
    except Exception as e:
        _pg_worker_engine.clear_cache()
        gc.collect()

        return {
            'expression': _pg_worker_condition_expr,
            'params': str(params),
            'params_dict': {},
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


# ============================================================================
# Dask 분산 처리 함수들 (메모리 공유 + 클러스터 확장)
# ============================================================================
_dask_client = None
_dask_df_future = None
_dask_stocks_future = None
_dask_params = None


def _init_dask_cluster(workers: int = 8):
    """
    Dask 로컬 클러스터 초기화 (데이터 1회 로드 후 공유)

    Returns:
        client: Dask Client
        df_future: scatter된 DataFrame Future
        stocks_future: scatter된 stocks Future
    """
    global _dask_client, _dask_df_future, _dask_stocks_future, _dask_params

    if not DASK_AVAILABLE:
        raise ImportError("Dask가 설치되지 않았습니다: pip install dask[distributed]")

    print(f"   [DASK] 클러스터 초기화 중 (워커: {workers}개)...")

    # 로컬 클러스터 생성
    cluster = LocalCluster(
        n_workers=workers,
        threads_per_worker=1,
        memory_limit='auto',
        silence_logs=40  # WARNING 이상만 출력
    )
    _dask_client = Client(cluster)

    # 데이터 1회 로드
    print("   [DASK] 데이터 로드 중...")
    engine = ConditionEngine()
    engine.load_data()

    # 대용량 데이터를 워커들에 scatter (복사 없이 참조)
    print("   [DASK] 데이터 scatter 중...")
    _dask_df_future = _dask_client.scatter(engine.df_daily, broadcast=True)
    _dask_stocks_future = _dask_client.scatter(engine.stocks, broadcast=True)
    _dask_params = load_default_params()

    print(f"   [DASK] 클러스터 준비 완료")
    print(f"   [DASK] 대시보드: {_dask_client.dashboard_link}")

    return _dask_client, _dask_df_future, _dask_stocks_future


def _shutdown_dask_cluster():
    """Dask 클러스터 종료"""
    global _dask_client
    if _dask_client is not None:
        _dask_client.close()
        _dask_client = None
        print("   [DASK] 클러스터 종료됨")


def _test_single_combo_dask(args):
    """
    Dask 워커에서 실행되는 단일 조합 테스트 함수

    Note: Dask submit으로 호출되며, 공유된 데이터를 사용
    """
    expr, start_date, end_date, tp, sl, max_holding, \
        trailing_start, trailing_offset, time_cut_days, time_cut_min_return, \
        min_trades, df_daily, stocks, params = args

    try:
        # 공유 데이터로 엔진 생성
        engine = ConditionEngine(preloaded_df=df_daily, preloaded_stocks=stocks)
        engine.load_data()  # preloaded 모드에서도 load_data 호출 필요

        # 백테스터 생성
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

        # Numba 워밍업
        warmup_numba_kernel()

        # 백테스트 실행
        report = backtester.run(start_date, end_date, expr, params, verbose=False)

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


def run_parallel_tests_dask(
    combinations_list: list[str],
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
    workers: int = 8
) -> list[dict]:
    """
    Dask 기반 병렬 조합 테스트 (메모리 공유)

    Args:
        combinations_list: 테스트할 조건 조합 리스트
        workers: 워커 수

    Returns:
        list[dict]: 각 조합의 결과
    """
    if not DASK_AVAILABLE:
        print("   [ERROR] Dask가 설치되지 않았습니다. multiprocessing으로 대체합니다.")
        return None

    total = len(combinations_list)
    print(f"\n[조합 테스트 - Dask] {total}개 조합, {workers}개 워커")
    print("-" * 80)

    start_time = time.time()

    try:
        # 클러스터 초기화
        client, df_future, stocks_future = _init_dask_cluster(workers)
        params = _dask_params

        # 작업 생성
        futures = []
        for expr in combinations_list:
            args = (
                expr, start_date, end_date, tp, sl, max_holding,
                trailing_start, trailing_offset, time_cut_days, time_cut_min_return,
                min_trades, df_future, stocks_future, params
            )
            future = client.submit(_test_single_combo_dask, args)
            futures.append(future)

        # 결과 수집 (완료되는 대로)
        results = []
        for i, future in enumerate(dask.distributed.as_completed(futures), 1):
            result = future.result()
            results.append(result)

            elapsed = time.time() - start_time
            eta = elapsed / i * (total - i) if i > 0 else 0

            status = "OK" if result['valid'] else f"거래수 부족({result['total_trades']}건)"
            print(f"   [{i:>3}/{total}] {result['expression']:<30} → "
                  f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
                  f"수익률 {result['avg_return']:>+6.2f}% ({status})")

        total_time = time.time() - start_time
        print(f"\n   [DASK] 완료: {total_time:.1f}초 ({total}개 조합)")

        return results

    except Exception as e:
        print(f"   [DASK ERROR] {e}")
        return None

    finally:
        _shutdown_dask_cluster()


def run_parallel_param_grid_tests(
    base_params: dict,
    param_combinations: list[dict],
    condition_expr: str,
    conditions: list[str],
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
    멀티프로세싱으로 파라미터 그리드 테스트 (병렬 실행)

    Args:
        param_combinations: 테스트할 파라미터 조합 리스트
        workers: 병렬 워커 수

    Returns:
        list[dict]: 각 파라미터 조합의 결과
    """
    total = len(param_combinations)
    print(f"\n[파라미터 조합 테스트 - 병렬] 조건: {condition_expr}")
    print(f"   총 {total}개 파라미터 조합, {workers}개 워커 사용")
    print("-" * 80)

    start_time = time.time()

    # 작업 목록 생성
    tasks = [
        (params, start_date, end_date, tp, sl)
        for params in param_combinations
    ]

    results = []

    # 멀티프로세싱 풀 생성
    with mp.Pool(
        processes=workers,
        initializer=_init_param_grid_worker,
        initargs=(tp, sl, max_holding, trailing_start, trailing_offset,
                  time_cut_days, time_cut_min_return, base_params,
                  condition_expr, conditions, min_trades),
        maxtasksperchild=50
    ) as pool:
        # imap_unordered로 완료되는 대로 처리
        for i, result in enumerate(pool.imap_unordered(_test_single_param_combo, tasks), 1):
            results.append(result)
            elapsed = time.time() - start_time

            # 프로그레스 바 출력
            print_progress_bar(i, total, elapsed)

            # 상세 결과 출력
            status = "OK" if result['valid'] else f"거래수 부족({result['total_trades']}건)"
            params_str = result.get('params', '')[:50]
            print(f"\n   [{i:>3}/{total}] {params_str:<50} → "
                  f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
                  f"수익률 {result['avg_return']:>+6.2f}% ({status})")

    print()  # 마지막 줄바꿈
    return results


# ============================================================================
# Mode 2 (--optimize) 병렬 처리용 워커 함수들
# ============================================================================
_opt_worker_engine = None
_opt_worker_params = None


def _init_optimize_worker(max_holding, trailing_start, trailing_offset,
                          time_cut_days, time_cut_min_return, params):
    """TP/SL 최적화 워커 프로세스 초기화"""
    global _opt_worker_engine, _opt_worker_params

    # 데이터 로드 (프로세스당 1회) - 워커에서는 출력 억제
    import sys
    import io
    _old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        _opt_worker_engine = ConditionEngine()
        _opt_worker_engine.load_data()
        # [최적화] GT 지표 사전계산 (워커당 1회)
        _opt_worker_engine.precompute_gt_indicators(verbose=False)
    finally:
        sys.stdout = _old_stdout

    # Numba JIT 워밍업
    warmup_numba_kernel()

    # 파라미터 저장
    _opt_worker_params = params


def _test_single_tpsl_combo(args):
    """단일 TP/SL 조합 테스트 (워커에서 실행)"""
    import gc
    expr, start_date, end_date, tp, sl, min_trades, max_holding, \
        trailing_start, trailing_offset, time_cut_days, time_cut_min_return = args

    global _opt_worker_engine, _opt_worker_params

    try:
        # 백테스터 생성 (TP/SL이 다르므로 매번 새로 생성)
        backtester = MultiBacktester(
            _opt_worker_engine,
            stop_loss=sl,
            take_profit=tp,
            max_holding_days=max_holding,
            trailing_start=trailing_start,
            trailing_offset=trailing_offset,
            time_cut_days=time_cut_days,
            time_cut_min_return=time_cut_min_return
        )

        report = backtester.run(
            start_date, end_date, expr, _opt_worker_params, verbose=False
        )

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

        # [최적화] 테스트 완료 후 캐시 클리어 및 GC 강제
        _opt_worker_engine.clear_cache()
        gc.collect()

        return result
    except Exception as e:
        _opt_worker_engine.clear_cache()
        gc.collect()

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


def run_parallel_optimized_tests(
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
    time_cut_min_return: float = None,
    workers: int = 4
) -> list[dict]:
    """
    멀티프로세싱으로 TP/SL 최적화 테스트 (병렬 실행)

    각 조합 x 각 TP/SL 조합을 병렬로 테스트하고,
    조합별로 가장 좋은 TP/SL 결과를 반환합니다.

    Returns:
        list[dict]: 각 조합의 최적 TP/SL 결과
    """
    # TP/SL 조합 생성
    tp_values = np.arange(tp_min, tp_max + step, step)
    sl_values = np.arange(sl_min, sl_max + step, step)
    tpsl_count = len(tp_values) * len(sl_values)
    total_tests = len(combos) * tpsl_count

    print(f"\n[TP/SL 최적화 테스트 - 병렬] 총 {len(combos)}개 조합 x {tpsl_count} TP/SL = {total_tests}개 테스트")
    print(f"   {workers}개 워커 사용")
    print("-" * 80)

    start_time = time.time()

    # 작업 목록 생성: (조합, TP, SL) 모든 조합
    tasks = []
    for expr in combos:
        for tp in tp_values:
            for sl in sl_values:
                tasks.append((
                    expr, start_date, end_date, float(tp), float(sl), min_trades,
                    max_holding, trailing_start, trailing_offset, time_cut_days, time_cut_min_return
                ))

    # 결과 수집용 딕셔너리 (조합별로 최적 결과 저장)
    combo_results = {expr: [] for expr in combos}

    # 멀티프로세싱 풀 생성
    with mp.Pool(
        processes=workers,
        initializer=_init_optimize_worker,
        initargs=(max_holding, trailing_start, trailing_offset,
                  time_cut_days, time_cut_min_return, params),
        maxtasksperchild=50
    ) as pool:
        # imap_unordered로 완료되는 대로 처리
        for i, result in enumerate(pool.imap_unordered(_test_single_tpsl_combo, tasks), 1):
            expr = result['expression']
            combo_results[expr].append(result)

            elapsed = time.time() - start_time

            # 프로그레스 바 출력 (10개마다)
            if i % 10 == 0 or i == len(tasks):
                print_progress_bar(i, len(tasks), elapsed)

    print()  # 마지막 줄바꿈

    # 각 조합별 최적 결과 선택 (평균수익률 기준)
    results = []
    for expr in combos:
        expr_results = combo_results[expr]
        if expr_results:
            # 평균수익률 기준 정렬
            valid_results = [r for r in expr_results if r['valid']]
            if valid_results:
                best = max(valid_results, key=lambda x: x['avg_return'])
            else:
                best = max(expr_results, key=lambda x: x['total_trades'])
            results.append(best)
        else:
            results.append({
                'expression': expr,
                'total_trades': 0,
                'win_rate': 0,
                'avg_return': 0,
                'total_return': 0,
                'avg_holding_days': 0,
                'tp': tp_min,
                'sl': sl_min,
                'valid': False
            })

        # 조합별 결과 출력
        r = results[-1]
        status = "OK" if r['valid'] else f"거래수 부족({r['total_trades']}건)"
        print(f"   {expr:<30} → 최적 TP={r['tp']:.0f}%/SL={r['sl']:.0f}% | "
              f"거래 {r['total_trades']:>4}건, 승률 {r['win_rate']:>5.1f}%, "
              f"수익률 {r['avg_return']:>+6.2f}% ({status})")

    return results


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

    # Windows에서 데드락 방지: maxtasksperchild로 워커 주기적 재시작
    actual_workers = workers

    with mp.Pool(
        processes=actual_workers,
        initializer=_init_worker,
        initargs=init_args,
        maxtasksperchild=50  # 50개 작업 후 워커 재시작 (메모리 누수/데드락 방지)
    ) as pool:
        # imap_unordered로 완료되는 순서대로 결과 수집
        # chunksize를 설정하여 IPC 오버헤드 감소
        chunksize = max(1, total // (actual_workers * 4))
        for result in pool.imap_unordered(_test_single_combo, task_args, chunksize=chunksize):
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


def run_param_grid_tests(
    engine: ConditionEngine,
    base_params: dict,
    param_combinations: list[dict],
    condition_expr: str,
    conditions: list[str],
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
    파라미터 조합 테스트 실행

    Args:
        param_combinations: generate_param_combinations() 결과
        condition_expr: 조건 표현식 (예: "A AND D AND H")
        conditions: 조건 목록

    Returns:
        list[dict]: 각 파라미터 조합의 결과
    """
    results = []
    total = len(param_combinations)
    start_time = time.time()

    print(f"\n[파라미터 조합 테스트] 조건: {condition_expr}")
    print(f"   총 {total}개 파라미터 조합")
    print("-" * 80)

    # 백테스터 생성
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

    for i, params in enumerate(param_combinations, 1):
        param_diff = get_param_diff_str(params, base_params, conditions)
        prefix = f"   [{i:>3}/{total}] {param_diff:<50} "

        def make_progress_callback(p):
            def callback(current, total_days):
                print_inner_progress(current, total_days, p)
            return callback

        progress_cb = make_progress_callback(prefix)

        report = backtester.run(start_date, end_date, condition_expr, params,
                               verbose=False, progress_callback=progress_cb)

        elapsed = time.time() - start_time

        # 결과 저장
        result = {
            'expression': condition_expr,
            'params': param_diff,
            'params_dict': {k: v for k, v in params.items() if k in [c.upper() for c in conditions]},
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

        # 상세 결과 출력
        status = "OK" if result['valid'] else f"거래수 부족({result['total_trades']}건)"
        print(f"\n   [{i:>3}/{total}] {param_diff:<50} → "
              f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
              f"수익률 {result['avg_return']:>+6.2f}% ({status})")

    print()  # 마지막 줄바꿈
    return results


def run_auto_optimize(
    engine: ConditionEngine,
    base_params: dict,
    conditions: list[str],
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
    top_n_candidates: int = 3,
    combo_min_size: int = 2,
    combo_max_size: int = None
) -> dict:
    """
    2단계 자동 최적화 실행

    [1단계] 각 조건별 파라미터 최적화 (단일 조건으로 테스트)
    [2단계] 최적 파라미터로 조건 조합 테스트

    Args:
        conditions: 최적화할 조건 목록
        top_n_candidates: 1단계에서 각 조건별 상위 N개 후보 선정
        combo_min_size: 2단계 조합 최소 크기
        combo_max_size: 2단계 조합 최대 크기

    Returns:
        {
            'phase1_results': {조건: [결과들]},
            'phase2_results': [조합 결과들],
            'optimized_params': {조건: {최적 파라미터들}},
            'best_combination': 최고 조합 결과
        }
    """
    results = {
        'phase1_results': {},
        'phase2_results': [],
        'optimized_params': {},
        'best_combination': None
    }

    print("\n" + "=" * 80)
    print("   [1단계] 개별 조건 파라미터 최적화")
    print("=" * 80)

    # 백테스터 생성
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

    phase1_start = time.time()

    # 각 조건별 파라미터 최적화
    for cond_idx, condition in enumerate(conditions, 1):
        cond_upper = condition.upper()
        param_grid = get_default_param_grid(cond_upper)

        if not param_grid:
            print(f"\n   [{cond_idx}/{len(conditions)}] {cond_upper}: 파라미터 그리드 없음, 건너뜀")
            results['optimized_params'][cond_upper] = base_params.get(cond_upper, {}).copy()
            continue

        print(f"\n   [{cond_idx}/{len(conditions)}] {cond_upper} 파라미터 최적화")
        print(f"      파라미터: {list(param_grid.keys())}")

        # 파라미터 조합 생성
        param_keys = list(param_grid.keys())
        param_values = [param_grid[k] for k in param_keys]
        total_combos = 1
        for pv in param_values:
            total_combos *= len(pv)
        print(f"      조합 수: {total_combos}개")

        cond_results = []

        for combo_idx, combo in enumerate(product(*param_values), 1):
            # 파라미터 설정
            test_params = {}
            for k, v in base_params.items():
                test_params[k] = v.copy() if isinstance(v, dict) else v

            for param_name, value in zip(param_keys, combo):
                if cond_upper in test_params:
                    test_params[cond_upper][param_name] = value

            # 단일 조건 테스트
            report = backtester.run(start_date, end_date, cond_upper, test_params, verbose=False)

            param_str = ', '.join(f"{k}={v}" for k, v in zip(param_keys, combo))

            result = {
                'params': dict(zip(param_keys, combo)),
                'params_str': param_str,
                'total_trades': report.total_trades if report else 0,
                'win_rate': report.win_rate if report else 0,
                'avg_return': report.avg_return if report else 0,
                'valid': (report.total_trades >= min_trades) if report else False
            }
            cond_results.append(result)

            # 진행률 표시
            print(f"\r      [{combo_idx}/{total_combos}] {param_str:<40} → "
                  f"거래 {result['total_trades']:>4}건, 수익률 {result['avg_return']:>+6.2f}%",
                  end='', flush=True)

        print()  # 줄바꿈

        # 유효한 결과만 정렬
        valid_results = [r for r in cond_results if r['valid']]
        valid_results.sort(key=lambda x: x['avg_return'], reverse=True)

        results['phase1_results'][cond_upper] = valid_results[:top_n_candidates]

        # 최적 파라미터 저장
        if valid_results:
            best = valid_results[0]
            optimized = base_params.get(cond_upper, {}).copy()
            optimized.update(best['params'])
            results['optimized_params'][cond_upper] = optimized
            print(f"      [BEST] {best['params_str']} → 수익률 {best['avg_return']:+.2f}%")
        else:
            # 유효 결과 없으면 기본값 사용
            results['optimized_params'][cond_upper] = base_params.get(cond_upper, {}).copy()
            print(f"      [WARN] 유효한 결과 없음, 기본값 사용")

    phase1_elapsed = time.time() - phase1_start
    print(f"\n   [1단계 완료] 소요시간: {int(phase1_elapsed//60)}분 {int(phase1_elapsed%60)}초")

    # =========================================================================
    # 2단계: 최적 파라미터로 조합 테스트
    # =========================================================================
    print("\n" + "=" * 80)
    print("   [2단계] 최적 파라미터로 조건 조합 테스트")
    print("=" * 80)

    # 최적화된 파라미터로 새 params 생성
    optimized_full_params = base_params.copy()
    for cond, params in results['optimized_params'].items():
        optimized_full_params[cond] = params

    # 조합 생성
    if combo_max_size is None:
        combo_max_size = len(conditions)

    combos = generate_combinations(conditions, combo_min_size, combo_max_size)
    print(f"   조합 수: {len(combos)}개 ({combo_min_size}~{combo_max_size}개 조건)")

    phase2_start = time.time()
    phase2_results = []

    for combo_idx, expr in enumerate(combos, 1):
        report = backtester.run(start_date, end_date, expr, optimized_full_params, verbose=False)

        result = {
            'expression': expr,
            'total_trades': report.total_trades if report else 0,
            'win_rate': report.win_rate if report else 0,
            'avg_return': report.avg_return if report else 0,
            'total_return': report.total_return if report else 0,
            'avg_holding_days': report.avg_holding_days if report else 0,
            'valid': (report.total_trades >= min_trades) if report else False
        }
        phase2_results.append(result)

        status = "OK" if result['valid'] else f"거래수 부족"
        print(f"   [{combo_idx:>3}/{len(combos)}] {expr:<35} → "
              f"거래 {result['total_trades']:>4}건, 승률 {result['win_rate']:>5.1f}%, "
              f"수익률 {result['avg_return']:>+6.2f}% ({status})")

    phase2_elapsed = time.time() - phase2_start
    print(f"\n   [2단계 완료] 소요시간: {int(phase2_elapsed//60)}분 {int(phase2_elapsed%60)}초")

    results['phase2_results'] = phase2_results

    # 최고 조합 선정
    valid_combos = [r for r in phase2_results if r['valid']]
    if valid_combos:
        valid_combos.sort(key=lambda x: x['avg_return'], reverse=True)
        results['best_combination'] = valid_combos[0]

    return results


def print_auto_optimize_results(results: dict, conditions: list[str]):
    """자동 최적화 결과 출력"""
    print("\n" + "=" * 100)
    print("   [자동 최적화 결과 요약]")
    print("=" * 100)

    # 1단계 결과
    print("\n   [1단계] 개별 조건 최적 파라미터")
    print("-" * 100)
    for cond in conditions:
        cond_upper = cond.upper()
        phase1 = results['phase1_results'].get(cond_upper, [])
        optimized = results['optimized_params'].get(cond_upper, {})

        if phase1:
            best = phase1[0]
            print(f"   {cond_upper}: {best['params_str']}")
            print(f"         → 거래 {best['total_trades']}건, 수익률 {best['avg_return']:+.2f}%")
        else:
            print(f"   {cond_upper}: (기본값 사용)")

    # 2단계 결과
    print("\n   [2단계] 조건 조합 테스트 결과 (Top 10)")
    print("-" * 100)
    print("   순위 조건 조합                           거래수    승률   평균수익률    총수익률  평균보유")
    print("-" * 100)

    valid_results = [r for r in results['phase2_results'] if r['valid']]
    valid_results.sort(key=lambda x: x['avg_return'], reverse=True)

    for i, r in enumerate(valid_results[:10], 1):
        print(f"   {i:^5}{r['expression']:<35}{r['total_trades']:>8}{r['win_rate']:>7.1f}%"
              f"{r['avg_return']:>+11.2f}%{r['total_return']:>+11.1f}%{r['avg_holding_days']:>7.1f}일")

    print("=" * 100)

    # 최고 조합 강조
    if results['best_combination']:
        best = results['best_combination']
        print(f"\n   [BEST] {best['expression']}")
        print(f"          거래 {best['total_trades']}건, 승률 {best['win_rate']:.1f}%, "
              f"평균수익률 {best['avg_return']:+.2f}%, 평균보유 {best['avg_holding_days']:.1f}일")
        print("=" * 100)


def print_param_grid_results(
    results: list[dict],
    sort_by: str = 'avg_return',
    top_n: int = 20,
    min_trades: int = 100
):
    """파라미터 조합 테스트 결과 출력"""
    # 유효한 결과만 필터링
    valid_results = [r for r in results if r['valid']]
    invalid_results = [r for r in results if not r['valid']]

    # 정렬
    valid_results.sort(key=lambda x: x[sort_by], reverse=True)

    sort_name = "평균수익률" if sort_by == 'avg_return' else "승률"

    print("\n" + "=" * 110)
    print(f"   [파라미터 조합 결과 - {sort_name} 순]")
    print("=" * 110)
    print("   순위 파라미터 조합                                       거래수    승률   평균수익률    총수익률  평균보유")
    print("-" * 110)

    for i, r in enumerate(valid_results[:top_n], 1):
        print(f"   {i:^5}{r['params']:<55}{r['total_trades']:>8}{r['win_rate']:>7.1f}%"
              f"{r['avg_return']:>+11.2f}%{r['total_return']:>+11.1f}%{r['avg_holding_days']:>7.1f}일")

    print("=" * 110)

    # 필터링된 조합 출력
    if invalid_results:
        print(f"\n[필터링된 조합] (거래수 < {min_trades}건)")
        for r in invalid_results[:5]:
            print(f"   - {r['params']}: {r['total_trades']}건")
        if len(invalid_results) > 5:
            print(f"   ... 외 {len(invalid_results) - 5}개")

    # 최고 조합 강조
    if valid_results:
        best = valid_results[0]
        print("\n" + "=" * 110)
        print(f"   [BEST] {best['expression']}")
        print(f"          파라미터: {best['params']}")
        print(f"          거래 {best['total_trades']}건, 승률 {best['win_rate']:.1f}%, "
              f"평균수익률 {best['avg_return']:+.2f}%, 평균보유 {best['avg_holding_days']:.1f}일")
        print("=" * 110)


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

  # 파라미터 조합 테스트 (조건 H의 파라미터 최적화)
  python combination_tester.py --conditions H --param-grid "H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03"

  # 여러 조건의 파라미터 동시 테스트
  python combination_tester.py --conditions A,D,H --param-grid "A.days:2,3,5;H.smart_money_turnover:5,10"
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

    # 파라미터 그리드 옵션
    parser.add_argument('--param-grid', '-pg', type=str, default=None,
                        help='파라미터 그리드 테스트. 형식: "조건.파라미터:값1,값2;조건.파라미터:값1,값2" '
                             '예: "H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03"')

    # 자동 최적화 옵션
    parser.add_argument('--auto-optimize', '-ao', action='store_true',
                        help='2단계 자동 최적화: (1) 각 조건별 파라미터 최적화 → (2) 최적 파라미터로 조합 테스트')
    parser.add_argument('--update-defaults', action='store_true',
                        help='자동 최적화 후 최적 파라미터를 default.json에 저장 (--auto-optimize와 함께 사용)')

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
    parser.add_argument('--workers', '-w', type=int, default=6,
                        help='병렬 워커 수 (기본: 6, 0=자동=CPU코어수)')
    parser.add_argument('--use-dask', action='store_true',
                        help='Dask 분산 처리 사용 (메모리 공유, 클러스터 확장)')

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

    # 파라미터 그리드 파싱
    param_grid = parse_param_grid(args.param_grid) if args.param_grid else None
    param_grid_mode = param_grid is not None and len(param_grid) > 0

    # 조합 생성
    max_size = args.max_size if args.max_size else len(conditions)

    if param_grid_mode:
        # 파라미터 그리드 모드: 조건 조합은 하나로 고정
        if required_expr:
            condition_expr = required_expr + ' AND ' + ' AND '.join(conditions)
        else:
            condition_expr = ' AND '.join(conditions)
        combos = [condition_expr]  # 조건 조합은 1개
    else:
        combos = generate_combinations(conditions, args.min_size, max_size, required=required_expr)

    print("=" * 80)
    if args.auto_optimize:
        print("   2단계 자동 최적화 모드")
    elif param_grid_mode:
        print("   파라미터 조합 테스트")
    elif args.optimize:
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

    if args.auto_optimize:
        # 자동 최적화 모드 정보 출력
        print(f"   [1단계] 각 조건별 파라미터 최적화 (DEFAULT_PARAM_GRIDS)")
        print(f"   [2단계] 최적 파라미터로 조합 테스트")
        if args.update_defaults:
            print(f"   -> 최적화 후 default.json 자동 업데이트")
    elif param_grid_mode:
        # 파라미터 그리드 정보 출력
        print(f"   조건 표현식: {condition_expr}")
        print(f"   파라미터 그리드: {args.param_grid}")
    else:
        print(f"   조합 크기: {args.min_size} ~ {max_size}개")
        print(f"   총 조합 수: {len(combos)}개")

    # 워커 수 결정
    workers = args.workers
    if workers == 0:
        workers = mp.cpu_count()
    if workers > 1:
        print(f"   병렬 처리: {workers}개 워커")
    print("=" * 80)

    # 병렬 모드 여부 결정 (모든 모드에서 workers > 1이면 병렬 처리)
    # auto_optimize는 내부적으로 순차 처리 유지 (2단계 구조 때문)
    use_parallel = workers > 1 and not args.auto_optimize

    # Dask 모드 확인
    use_dask = getattr(args, 'use_dask', False) and DASK_AVAILABLE
    if getattr(args, 'use_dask', False) and not DASK_AVAILABLE:
        print("   [WARN] Dask가 설치되지 않았습니다. multiprocessing으로 대체합니다.")

    if use_dask:
        # Dask 모드: 메모리 공유 + 클러스터 확장
        print("\n[1] Dask 모드 - 데이터 공유 방식 사용")
        engine = None
        params = load_default_params()
    elif use_parallel:
        # 병렬 모드: 각 워커에서 데이터 로드
        print("\n[1] 병렬 모드 - 워커에서 데이터 로드 예정")
        engine = None
        # 파라미터는 워커에 전달하기 위해 로드
        params = load_default_params()
    else:
        # 순차 모드: 메인 프로세스에서 데이터 로드
        print("\n[1] 데이터 로드 중...")
        engine = ConditionEngine()
        if not engine.load_data():
            print("   [ERROR] 데이터 로드 실패")
            sys.exit(1)

        # [최적화] GT 지표 사전계산 (1회만 실행, 이후 필터링만 수행)
        engine.precompute_gt_indicators(verbose=True)

        # 파라미터 로드
        params = load_default_params()
        print(f"   -> 조건 파라미터 로드 완료")

    # 자동 최적화 모드 확인
    if args.auto_optimize:
        print("\n[2] 2단계 자동 최적화 시작...")
        start_time = time.time()

        auto_results = run_auto_optimize(
            engine, params, conditions,
            args.start_date, args.end_date,
            args.tp, args.sl,
            args.min_trades,
            args.max_holding,
            args.trailing_start,
            args.trailing_offset,
            args.time_cut_days,
            args.time_cut_min_return,
            top_n_candidates=3,
            combo_min_size=args.min_size,
            combo_max_size=args.max_size
        )

        elapsed = time.time() - start_time
        elapsed_min = int(elapsed // 60)
        elapsed_sec = int(elapsed % 60)
        print(f"\n   [완료] 총 소요시간: {elapsed_min}분 {elapsed_sec}초")

        # 결과 출력
        print_auto_optimize_results(auto_results, conditions)

        # default.json 업데이트 옵션
        if args.update_defaults and auto_results['optimized_params']:
            json_path = update_default_json(auto_results['optimized_params'])
            print(f"\n[default.json 업데이트 완료]")
            print(f"   파일: {json_path}")
            print(f"   업데이트된 조건: {', '.join(auto_results['optimized_params'].keys())}")

        # JSON 결과 저장 (로깅 활성화 시)
        if args.log and json_file:
            args_dict = {
                'mode': 'auto_optimize',
                'conditions': args.conditions,
                'start_date': args.start_date,
                'end_date': args.end_date,
                'tp': args.tp,
                'sl': args.sl,
                'max_holding': args.max_holding,
                'min_trades': args.min_trades,
                'elapsed_seconds': elapsed
            }
            # auto_results를 직렬화 가능하게 변환
            serializable_results = []
            for phase2_result in auto_results.get('phase2_results', []):
                serializable_results.append(phase2_result)

            save_results_json(serializable_results, json_file, args_dict)
            print(f"\n[로그 저장 완료]")
            print(f"   로그 파일: {log_file}")
            print(f"   결과 JSON: {json_file}")

        # 로거 정리
        if logger:
            sys.stdout = logger.terminal
            logger.close()

        return  # 자동 최적화 모드 종료

    # 테스트 실행
    if param_grid_mode:
        print("\n[2] 파라미터 조합 테스트 시작...")
    else:
        print("\n[2] 조합 테스트 시작...")
    start_time = time.time()

    if param_grid_mode:
        # 파라미터 그리드 테스트
        # 모든 조건 목록 생성 (required + conditions)
        all_conditions = required_conditions + conditions if required_conditions else conditions

        # 파라미터 조합 생성
        param_combinations = generate_param_combinations(param_grid, params, all_conditions)
        print(f"   총 {len(param_combinations)}개 파라미터 조합 생성됨")

        if use_parallel:
            # 병렬 파라미터 그리드 테스트
            results = run_parallel_param_grid_tests(
                params, param_combinations,
                condition_expr, all_conditions,
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
            # 순차 파라미터 그리드 테스트
            results = run_param_grid_tests(
                engine, params, param_combinations,
                condition_expr, all_conditions,
                args.start_date, args.end_date,
                args.tp, args.sl,
                args.min_trades,
                args.max_holding,
                args.trailing_start,
                args.trailing_offset,
                args.time_cut_days,
                args.time_cut_min_return
            )
    elif args.optimize:
        if use_parallel:
            # 병렬 TP/SL 최적화 테스트
            results = run_parallel_optimized_tests(
                params, combos,
                args.start_date, args.end_date,
                args.tp_min, args.tp_max,
                args.sl_min, args.sl_max,
                args.step,
                args.min_trades,
                args.max_holding,
                args.trailing_start,
                args.trailing_offset,
                args.time_cut_days,
                args.time_cut_min_return,
                workers=workers
            )
        else:
            # 순차 TP/SL 최적화 테스트
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
    elif use_dask:
        # Dask 병렬 테스트 (메모리 공유)
        results = run_parallel_tests_dask(
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
        # Dask 실패 시 multiprocessing으로 대체
        if results is None:
            print("   [WARN] Dask 실행 실패, multiprocessing으로 재시도...")
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
    elif use_parallel:
        # 병렬 테스트 (multiprocessing)
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
    if param_grid_mode:
        print_param_grid_results(
            results,
            sort_by=args.sort_by,
            top_n=args.top,
            min_trades=args.min_trades
        )
    else:
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
            'param_grid': args.param_grid,
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
