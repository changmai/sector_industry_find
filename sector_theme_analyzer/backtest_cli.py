"""
멀티 조건 백테스팅 CLI

두 가지 모드 지원:
    1. 인터랙티브 모드: python backtest_cli.py
    2. 직접 실행 모드: python backtest_cli.py --start-date ... --conditions "A AND B"

사용 예시:
    # 인터랙티브 모드
    python backtest_cli.py

    # 직접 실행 모드
    python backtest_cli.py --start-date 20241209 --end-date 20251205 --conditions "A AND B"

    # TP/SL 최적화
    python backtest_cli.py --start-date 20241209 --end-date 20251205 --conditions "A" --optimize
"""
import sys
import os
import io
import json
import argparse
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

from condition_engine import ConditionEngine, CONDITION_DESCRIPTIONS
from condition_parser import ConditionParser
from multi_backtester import MultiBacktester


def print_header():
    """헤더 출력"""
    print("\n" + "=" * 60)
    print("   멀티 조건 백테스팅 시스템")
    print("=" * 60)


def print_conditions_table():
    """사용 가능한 조건 테이블 출력"""
    print("\n   사용 가능한 조건:")
    print("   " + "-" * 50)
    print(f"   {'ID':<6} {'설명':<40}")
    print("   " + "-" * 50)
    for cond_id, desc in CONDITION_DESCRIPTIONS.items():
        print(f"   {cond_id:<6} {desc:<40}")
    print("   " + "-" * 50)


def load_params(params_file: str = None) -> dict:
    """조건 파라미터 로드"""
    # 기본 파라미터
    default_params = {
        'A': {'days': 5, 'ratio': 0.6},
        'B': {'bars': 60},
        'C': {'min_rate': 0.0, 'top_n': 100},
        'D': {'short': 20, 'mid': 60, 'long': 120},
        'E': {'bars': 60, 'min_pct': -5.0, 'max_pct': 0.0},
        'F': {'compare_bars': 5, 'min_ratio': 150, 'max_ratio': 9000},
    }

    if params_file and os.path.exists(params_file):
        with open(params_file, 'r', encoding='utf-8') as f:
            user_params = json.load(f)
            # 사용자 파라미터로 오버라이드
            for key, value in user_params.items():
                if key in default_params:
                    default_params[key].update(value)
                else:
                    default_params[key] = value

    return default_params


def interactive_mode():
    """인터랙티브 모드"""
    print_header()

    # 데이터 로드
    print("\n   데이터 로드 중...")
    engine = ConditionEngine()
    if not engine.load_data():
        print("   [ERROR] 데이터 로드 실패")
        return

    trading_days = engine.get_all_trading_days()
    print(f"   -> 거래일: {trading_days[0]} ~ {trading_days[-1]} ({len(trading_days)}일)")

    # Step 1: 기간 설정
    print("\n" + "-" * 60)
    print("[1단계] 백테스팅 기간 설정")
    print("-" * 60)

    while True:
        start_date = input(f"   시작일 입력 (YYYYMMDD, 기본: {trading_days[0]}): ").strip()
        if not start_date:
            start_date = trading_days[0]

        if start_date not in trading_days:
            # 가장 가까운 거래일 찾기
            valid = [d for d in trading_days if d >= start_date]
            if valid:
                start_date = valid[0]
                print(f"   -> 조정된 시작일: {start_date}")
            else:
                print("   [ERROR] 유효하지 않은 날짜입니다.")
                continue
        break

    while True:
        end_date = input(f"   종료일 입력 (YYYYMMDD, 기본: {trading_days[-1]}): ").strip()
        if not end_date:
            end_date = trading_days[-1]

        if end_date not in trading_days:
            valid = [d for d in trading_days if d <= end_date]
            if valid:
                end_date = valid[-1]
                print(f"   -> 조정된 종료일: {end_date}")
            else:
                print("   [ERROR] 유효하지 않은 날짜입니다.")
                continue
        break

    # Step 2: 조건 선택
    print("\n" + "-" * 60)
    print("[2단계] 적용할 조건 선택")
    print("-" * 60)

    print_conditions_table()

    print("\n   조건 조합식 입력 (예: A AND B, A AND (B OR C)):")
    condition_expr = input("   > ").strip().upper()

    if not condition_expr:
        condition_expr = "A"
        print(f"   -> 기본값 사용: {condition_expr}")

    # 유효성 검사
    parser = ConditionParser(engine)
    valid, msg = parser.validate_expression(condition_expr)
    if not valid:
        print(f"   [ERROR] {msg}")
        return

    # Step 3: 매매 설정
    print("\n" + "-" * 60)
    print("[3단계] 매매 설정")
    print("-" * 60)

    sl_input = input("   손절 라인 (%, 기본 -5): ").strip()
    stop_loss = float(sl_input) if sl_input else -5.0

    tp_input = input("   익절 라인 (%, 기본 10): ").strip()
    take_profit = float(tp_input) if tp_input else 10.0

    max_hold_input = input("   최대 보유일 (기본 10): ").strip()
    max_holding_days = int(max_hold_input) if max_hold_input else 10

    # Step 4: 확인
    print("\n" + "-" * 60)
    print("[4단계] 확인")
    print("-" * 60)
    print(f"   기간: {start_date} ~ {end_date}")
    print(f"   조건: {condition_expr}")
    print(f"   손절: {stop_loss}% | 익절: {take_profit}%")
    print(f"   최대 보유일: {max_holding_days}일")
    print("-" * 60)

    confirm = input("   진행하시겠습니까? (y/n): ").strip().lower()
    if confirm != 'y':
        print("   취소되었습니다.")
        return

    # Step 5: 최적화 여부
    optimize = input("\n   TP/SL 최적화를 실행하시겠습니까? (y/n, 기본 n): ").strip().lower()

    if optimize == 'y':
        # 최적화 모드
        tp_min = float(input("   익절 최소값 (%, 기본 5): ").strip() or "5")
        tp_max = float(input("   익절 최대값 (%, 기본 10): ").strip() or "10")
        sl_min = float(input("   손절 최소값 (%, 기본 -5): ").strip() or "-5")
        sl_max = float(input("   손절 최대값 (%, 기본 -3): ").strip() or "-3")

        params = load_params()
        backtester = MultiBacktester(engine, stop_loss=stop_loss, take_profit=take_profit, max_holding_days=max_holding_days)

        results = backtester.optimize_tp_sl(
            start_date=start_date,
            end_date=end_date,
            condition_expr=condition_expr,
            params=params,
            tp_range=(tp_min, tp_max),
            sl_range=(sl_min, sl_max)
        )
    else:
        # 일반 백테스트
        params = load_params()
        backtester = MultiBacktester(engine, stop_loss=stop_loss, take_profit=take_profit, max_holding_days=max_holding_days)

        report = backtester.run(
            start_date=start_date,
            end_date=end_date,
            condition_expr=condition_expr,
            params=params
        )

        backtester.print_report()


def direct_mode(args):
    """직접 실행 모드"""
    print_header()

    # 데이터 로드
    print("\n   데이터 로드 중...")
    engine = ConditionEngine()
    if not engine.load_data():
        print("   [ERROR] 데이터 로드 실패")
        return

    params = load_params(args.params)

    backtester = MultiBacktester(
        engine,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        max_holding_days=args.max_holding
    )

    if args.optimize:
        # 최적화 모드
        results = backtester.optimize_tp_sl(
            start_date=args.start_date,
            end_date=args.end_date,
            condition_expr=args.conditions,
            params=params,
            tp_range=(args.tp_min, args.tp_max),
            sl_range=(args.sl_min, args.sl_max),
            step=args.step
        )
    else:
        # 일반 백테스트
        report = backtester.run(
            start_date=args.start_date,
            end_date=args.end_date,
            condition_expr=args.conditions,
            params=params
        )

        backtester.print_report()


def parse_args():
    """커맨드라인 인자 파싱"""
    parser = argparse.ArgumentParser(
        description="멀티 조건 백테스팅 시스템",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    # 인터랙티브 모드
    python backtest_cli.py

    # 직접 실행 모드
    python backtest_cli.py --start-date 20241209 --end-date 20251205 --conditions "A AND B"

    # TP/SL 최적화
    python backtest_cli.py --start-date 20241209 --end-date 20251205 --conditions "A" --optimize

    # 커스텀 최적화 범위
    python backtest_cli.py --conditions "A" --optimize --tp-min 5 --tp-max 15 --sl-min -7 --sl-max -2
        """
    )

    # 기본 옵션
    parser.add_argument("--start-date", type=str, help="시작일 (YYYYMMDD)")
    parser.add_argument("--end-date", type=str, help="종료일 (YYYYMMDD)")
    parser.add_argument("--conditions", "-c", type=str, help="조건 표현식 (예: 'A AND B')")
    parser.add_argument("--params", type=str, help="조건 파라미터 JSON 파일 경로")

    # 매매 설정
    parser.add_argument("--stop-loss", "-sl", type=float, default=-5.0, help="손절 라인 %% (기본: -5)")
    parser.add_argument("--take-profit", "-tp", type=float, default=10.0, help="익절 라인 %% (기본: 10)")
    parser.add_argument("--max-holding", type=int, default=10, help="최대 보유일 (기본: 10)")

    # 최적화 옵션
    parser.add_argument("--optimize", "-o", action="store_true", help="TP/SL 최적화 모드")
    parser.add_argument("--tp-min", type=float, default=5.0, help="익절 최소값 %% (기본: 5)")
    parser.add_argument("--tp-max", type=float, default=10.0, help="익절 최대값 %% (기본: 10)")
    parser.add_argument("--sl-min", type=float, default=-5.0, help="손절 최소값 %% (기본: -5)")
    parser.add_argument("--sl-max", type=float, default=-3.0, help="손절 최대값 %% (기본: -3)")
    parser.add_argument("--step", type=float, default=1.0, help="최적화 스텝 (기본: 1)")

    return parser.parse_args()


def main():
    args = parse_args()

    # 필수 인자가 있으면 직접 실행 모드
    if args.start_date and args.end_date and args.conditions:
        direct_mode(args)
    else:
        # 인터랙티브 모드
        interactive_mode()


if __name__ == "__main__":
    main()
