"""
조건별 종목 리스트 조회 CLI

특정 조건(A~G)을 충족하는 종목 리스트를 조회합니다.

사용 예시:
    # 조건 B 충족 종목 조회 (기본 날짜: 데이터 내 최신일)
    python condition_cli.py --condition B

    # 특정 날짜로 조건 A 조회
    python condition_cli.py --condition A --date 20251205

    # 모든 조건 한번에 조회
    python condition_cli.py --all --date 20251205

    # 상위 20개만 출력
    python condition_cli.py --condition C --date 20251205 --top 20

    # CSV로 저장
    python condition_cli.py --condition B --date 20251205 --output result.csv
"""
import sys
import os
import io
import json
import argparse
from datetime import datetime

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


# 조건별 상세 필드 정의
CONDITION_DETAIL_FIELDS = {
    'A': ['업종수', '섹터수'],
    'B': ['거래대금', '60봉최대'],
    'C': ['회전율'],
    'D': ['MA20', 'MA60', 'MA120'],
    'E': ['신고가', '현재가', '신고가대비'],
    'F': ['현재5봉평균', 'N봉전5봉평균', '거래량비율'],
    'G': ['회전율'],
}


def print_header():
    """헤더 출력"""
    print("\n" + "=" * 60)
    print("   조건별 종목 리스트 조회")
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
    default_params = {
        'A': {'days': 5, 'ratio': 0.6},
        'B': {'bars': 60},
        'C': {'min_rate': 0.0, 'top_n': 100},
        'D': {'short': 20, 'mid': 60, 'long': 120},
        'E': {'bars': 60, 'min_pct': -5.0, 'max_pct': 0.0},
        'F': {'compare_bars': 5, 'min_ratio': 150, 'max_ratio': 9000},
        'G': {'min_rate': 1.0, 'max_rate': 100.0},
    }

    if params_file and os.path.exists(params_file):
        with open(params_file, 'r', encoding='utf-8') as f:
            user_params = json.load(f)
            for key, value in user_params.items():
                if key in default_params:
                    default_params[key].update(value)
                else:
                    default_params[key] = value

    return default_params


def get_stock_details_with_condition(engine: ConditionEngine, condition_details: dict, base_date: str) -> list:
    """종목코드와 조건 상세값을 병합하여 상세 정보 반환"""
    details = []

    df_day = engine.df_daily[engine.df_daily['날짜'] == base_date]

    for code, cond_vals in condition_details.items():
        name = engine.get_stock_name(code)

        # 해당일 가격 정보
        stock_data = df_day[df_day['종목코드'] == code]
        if len(stock_data) > 0:
            row = stock_data.iloc[0]
            item = {
                'code': code,
                'name': name,
                'close': int(row['종가']) if row['종가'] else 0,
                'change': round(row['등락률'], 2) if row['등락률'] else 0,
                'volume': int(row['거래량']) if row['거래량'] else 0,
            }
        else:
            item = {
                'code': code,
                'name': name,
                'close': 0,
                'change': 0,
                'volume': 0,
            }

        # 조건 상세값 병합
        item['condition_vals'] = cond_vals
        details.append(item)

    # 등락률 기준 정렬
    details.sort(key=lambda x: x['change'], reverse=True)
    return details


def format_condition_value(key: str, value) -> str:
    """조건 상세값 포맷팅"""
    if key in ['회전율', '신고가대비', '거래량비율']:
        return f"{value}%"
    elif key in ['거래대금', '60봉최대', '현재5봉평균', 'N봉전5봉평균']:
        if value >= 100000000:  # 1억 이상
            return f"{value/100000000:.1f}억"
        elif value >= 10000:  # 1만 이상
            return f"{value/10000:.0f}만"
        else:
            return f"{value:,}"
    elif key in ['신고가', '현재가', 'MA20', 'MA60', 'MA120']:
        return f"{value:,}"
    elif key in ['업종수', '섹터수']:
        return f"{value}개"
    else:
        return str(value)


def print_stock_list_with_details(details: list, condition_id: str, base_date: str, top_n: int = None):
    """조건 상세값 포함 종목 리스트 출력"""
    desc = CONDITION_DESCRIPTIONS.get(condition_id, "알 수 없는 조건")
    detail_fields = CONDITION_DETAIL_FIELDS.get(condition_id, [])

    print(f"\n   조건 {condition_id}: {desc}")
    print(f"   기준일: {base_date}")
    print(f"   충족 종목: {len(details)}개")

    if top_n and len(details) > top_n:
        print(f"   (상위 {top_n}개만 표시)")
        details = details[:top_n]

    # 동적 헤더 생성
    detail_header = ""
    for field in detail_fields:
        detail_header += f" {field:>12}"

    line_len = 65 + len(detail_fields) * 13
    print("\n   " + "-" * line_len)
    print(f"   {'No':<5} {'종목코드':<10} {'종목명':<20} {'종가':>10} {'등락률':>10}{detail_header}")
    print("   " + "-" * line_len)

    for i, stock in enumerate(details, 1):
        change_str = f"{stock['change']:+.2f}%"

        # 조건 상세값 포맷팅
        detail_str = ""
        cond_vals = stock.get('condition_vals', {})
        for field in detail_fields:
            val = cond_vals.get(field, '-')
            if val != '-':
                val = format_condition_value(field, val)
            detail_str += f" {str(val):>12}"

        print(f"   {i:<5} {stock['code']:<10} {stock['name']:<20} {stock['close']:>10,} {change_str:>10}{detail_str}")

    print("   " + "-" * line_len)


def save_to_csv_with_details(details: list, condition_id: str, base_date: str, output_file: str):
    """조건 상세값 포함 CSV 파일로 저장"""
    import csv

    detail_fields = CONDITION_DETAIL_FIELDS.get(condition_id, [])

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        header = ['조건', '기준일', '종목코드', '종목명', '종가', '등락률', '거래량'] + detail_fields
        writer.writerow(header)

        for stock in details:
            row = [
                condition_id,
                base_date,
                stock['code'],
                stock['name'],
                stock['close'],
                stock['change'],
                stock['volume']
            ]
            cond_vals = stock.get('condition_vals', {})
            for field in detail_fields:
                row.append(cond_vals.get(field, ''))
            writer.writerow(row)

    print(f"\n   [저장완료] {output_file}")


def run_condition_query(engine: ConditionEngine, condition_id: str, base_date: str,
                       params: dict, top_n: int = None, output_file: str = None):
    """특정 조건 조회 실행"""
    condition_params = params.get(condition_id.upper(), {})

    # 조건 평가 (with_details=True로 상세값 포함)
    condition_details = engine.evaluate(condition_id, base_date, condition_params, with_details=True)

    if not condition_details:
        print(f"\n   조건 {condition_id}: 충족 종목 없음")
        return

    # 상세 정보 조회 (조건 상세값 병합)
    details = get_stock_details_with_condition(engine, condition_details, base_date)

    # 출력
    print_stock_list_with_details(details, condition_id, base_date, top_n)

    # CSV 저장
    if output_file:
        save_to_csv_with_details(details, condition_id, base_date, output_file)


def main():
    parser = argparse.ArgumentParser(description='조건별 종목 리스트 조회')
    parser.add_argument('--condition', '-c', type=str, help='조건 ID (A, B, C, D, E, F, G)')
    parser.add_argument('--all', '-a', action='store_true', help='모든 조건 조회')
    parser.add_argument('--date', '-d', type=str, help='기준일 (YYYYMMDD)')
    parser.add_argument('--params', '-p', type=str, help='파라미터 JSON 파일 경로')
    parser.add_argument('--top', '-t', type=int, help='상위 N개만 출력')
    parser.add_argument('--output', '-o', type=str, help='결과 저장 CSV 파일 경로')

    args = parser.parse_args()

    print_header()

    # 조건 미지정 시 도움말 출력
    if not args.condition and not args.all:
        print_conditions_table()
        print("\n   사용법:")
        print("   python condition_cli.py --condition B --date 20251205")
        print("   python condition_cli.py --all --date 20251205")
        print("   python condition_cli.py --condition C --top 20")
        print()
        return

    # 엔진 초기화
    print("\n   [INIT] 데이터 로드 중...")
    engine = ConditionEngine()
    if not engine.load_data():
        print("   [ERROR] 데이터 로드 실패")
        return

    # 기준일 설정 (미지정 시 최신일)
    if args.date:
        base_date = args.date
    else:
        all_dates = engine.get_all_trading_days()
        base_date = all_dates[-1] if all_dates else None
        if not base_date:
            print("   [ERROR] 거래일 데이터가 없습니다")
            return
        print(f"   [INFO] 기준일 자동 설정: {base_date}")

    # 파라미터 로드
    params = load_params(args.params)

    # 조건 조회 실행
    if args.all:
        for cond_id in CONDITION_DESCRIPTIONS.keys():
            run_condition_query(engine, cond_id, base_date, params, args.top, None)

        if args.output:
            print(f"\n   [INFO] --all 모드에서는 CSV 저장이 지원되지 않습니다.")
    else:
        condition_id = args.condition.upper()
        if condition_id not in CONDITION_DESCRIPTIONS:
            print(f"\n   [ERROR] 알 수 없는 조건: {condition_id}")
            print_conditions_table()
            return

        run_condition_query(engine, condition_id, base_date, params, args.top, args.output)

    print()


if __name__ == "__main__":
    main()
