"""
특정 날짜(범위) 조건 충족 종목 수익률 조회 (TP/SL 적용)

사용법:
    # 단일 날짜
    python single_day_test.py --date 20240502 --conditions "A AND D AND G"
    python single_day_test.py --date 20240502 --conditions "A" --days 7 --tp 10 --sl -5

    # 날짜 범위 (보유 중 종목 중복 매수 방지)
    python single_day_test.py --start-date 20250804 --end-date 20250808 --conditions "A" --days 7 --tp 20 --sl -5
"""
import argparse
import json
import os
import re
import numpy as np
import pandas as pd
from condition_engine import ConditionEngine, CONDITION_DESCRIPTIONS
from condition_parser import ConditionParser


# 조건별 설명 템플릿
CONDITION_DESC_TEMPLATES = {
    'A': '섹터+업종 {days}일 동시 상승 (비율 {ratio})',
    'B': '{days}일 신고거래대금',
    'C': '회전율 상위 {top_n}종목 (최소 {min_rate}%)',
    'D': '이평 정배열 ({short}>{mid}>{long}일)',
    'E': '{days}일 신고가 대비 {min_pct}%~{max_pct}%',
    'F': '{compare_days}일전 대비 거래량 {min_ratio}%~{max_ratio}%',
    'G': '회전율 {min_rate}%~{max_rate}%',
}


def load_condition_params():
    """default.json에서 조건 파라미터 로드"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    params_path = os.path.join(script_dir, 'conditions', 'default.json')

    if os.path.exists(params_path):
        with open(params_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def print_condition_details(condition_expr: str):
    """조건식에서 사용된 조건들의 상세 정보 출력 (default.json에서 파라미터 로드)"""
    # 조건식에서 조건 ID 추출 (A, B, C, ... 단독으로 사용된 것만)
    # AND, OR 등의 키워드에서 A를 추출하지 않도록 단어 경계 사용
    condition_ids = set(re.findall(r'\b([A-G])\b', condition_expr.upper()))

    if not condition_ids:
        return

    # default.json에서 실제 파라미터 로드
    params_from_file = load_condition_params()

    print("\n[조건 상세]")
    print("-" * 70)

    for cond_id in sorted(condition_ids):
        if cond_id in CONDITION_DESC_TEMPLATES and cond_id in params_from_file:
            template = CONDITION_DESC_TEMPLATES[cond_id]
            params = params_from_file[cond_id]
            # description 키 제외하고 파라미터만 추출
            param_values = {k: v for k, v in params.items() if k != 'description'}
            try:
                desc = template.format(**param_values)
                print(f"   {cond_id}: {desc}")
            except KeyError as e:
                print(f"   {cond_id}: {params.get('description', '설명 없음')} (파라미터 오류: {e})")

    print("-" * 70)


def simulate_single_stock(code, base_date, base_close, stock_name, turnover, future_days, stock_data, tp, sl):
    """단일 종목 TP/SL 시뮬레이션 (벡터화 버전)"""
    result = {
        '종목코드': code,
        '종목명': stock_name,
        '매수일': base_date,
        '매수가': base_close,
        '회전율': turnover,
        '청산일': None,
        '보유일': 0,
        '청산가': None,
        '수익률': 0,
        '청산사유': '기간만료'
    }

    # 미래 날짜 데이터 한번에 필터링 (벡터화)
    future_dates_set = set(future_days[1:])
    future_data = stock_data[stock_data['날짜'].isin(future_dates_set)]

    if future_data.empty:
        # 기간만료 처리
        result['청산일'] = base_date
        result['보유일'] = 0
        result['청산가'] = base_close
        result['수익률'] = 0
        return result

    # 날짜순 정렬
    future_data = future_data.sort_values('날짜')

    # numpy 배열로 변환 (벡터 연산)
    highs = future_data['고가'].values
    lows = future_data['저가'].values
    closes = future_data['종가'].values
    dates = future_data['날짜'].values

    # 수익률 벡터 계산 (한번에)
    high_rets = (highs - base_close) / base_close * 100
    low_rets = (lows - base_close) / base_close * 100

    # 첫 TP/SL 도달 인덱스 찾기 (numpy)
    sl_hits = np.where(low_rets <= sl)[0]
    tp_hits = np.where(high_rets >= tp)[0]

    first_sl = sl_hits[0] if len(sl_hits) > 0 else len(future_data)
    first_tp = tp_hits[0] if len(tp_hits) > 0 else len(future_data)

    # 손절이 먼저 도달하거나 같은 날이면 손절 우선
    if first_sl <= first_tp and first_sl < len(future_data):
        result['청산일'] = dates[first_sl]
        result['보유일'] = first_sl + 1
        result['청산가'] = base_close * (1 + sl / 100)
        result['수익률'] = sl
        result['청산사유'] = '손절'
    elif first_tp < first_sl and first_tp < len(future_data):
        result['청산일'] = dates[first_tp]
        result['보유일'] = first_tp + 1
        result['청산가'] = base_close * (1 + tp / 100)
        result['수익률'] = tp
        result['청산사유'] = '익절'
    else:
        # 기간만료
        result['청산일'] = dates[-1]
        result['보유일'] = len(dates)
        result['청산가'] = closes[-1]
        result['수익률'] = (closes[-1] - base_close) / base_close * 100
        result['청산사유'] = '기간만료'

    return result


def run_single_date(engine, cond_parser, df, trading_days, base_date, conditions, max_days, tp, sl, holdings=None, stock_groups=None):
    """단일 날짜 시뮬레이션 실행 (최적화 버전)"""
    if holdings is None:
        holdings = {}

    # 조건 평가
    stocks = cond_parser.parse(conditions, base_date)
    total_matched = len(stocks)

    if total_matched == 0:
        return [], holdings, {'total_matched': 0, 'new_buys': 0, 'skipped': 0}

    # 보유 중인 종목 제외 (청산일이 오늘 이후인 것만 유지)
    stocks_to_buy = [s for s in stocks if s not in holdings or holdings[s] <= base_date]
    skipped = total_matched - len(stocks_to_buy)

    # 이후 거래일 찾기
    base_idx = trading_days.index(base_date)
    future_days = trading_days[base_idx:base_idx + max_days + 1]

    if len(future_days) < 2:
        return [], holdings, {'total_matched': total_matched, 'new_buys': 0, 'skipped': skipped}

    results = []
    has_turnover = '거래회전율' in df.columns

    for code in stocks_to_buy:
        # O(1) 그룹 접근 (stock_groups 사용 시)
        try:
            if stock_groups is not None:
                stock_data = stock_groups.get_group(code)
            else:
                stock_data = df[df['종목코드'] == code]
        except KeyError:
            continue

        if stock_data.empty:
            continue

        # 기준일 데이터
        base_data = stock_data[stock_data['날짜'] == base_date]
        if base_data.empty:
            continue

        base_close = base_data['종가'].values[0]
        stock_name = base_data['종목명'].values[0]
        turnover = base_data['거래회전율'].values[0] if has_turnover else 0

        # 시뮬레이션
        result = simulate_single_stock(
            code, base_date, base_close, stock_name, turnover,
            future_days, stock_data, tp, sl
        )

        if result['청산일']:
            results.append(result)
            # 보유 종목에 추가 (청산일 기록)
            holdings[code] = result['청산일']

    stats = {
        'total_matched': total_matched,
        'new_buys': len(results),
        'skipped': skipped
    }

    return results, holdings, stats


def print_single_date_results(results, tp, sl):
    """단일 날짜 결과 상세 출력"""
    if not results:
        print("   결과 없음")
        return

    result_df = pd.DataFrame(results)
    result_df = result_df.sort_values('수익률', ascending=False)

    total = len(result_df)
    avg_ret = result_df['수익률'].mean()
    avg_days = result_df['보유일'].mean()
    win_rate = (result_df['수익률'] > 0).sum() / total * 100

    exit_stats = result_df['청산사유'].value_counts().to_dict()

    print(f"\n   평균 수익률: {avg_ret:+.2f}%")
    print(f"   평균 보유일: {avg_days:.1f}일")
    print(f"   승률: {win_rate:.1f}%")
    print("-" * 70)

    print(f"\n[청산 사유]")
    print(f"   익절({tp:+.1f}%): {exit_stats.get('익절', 0)}회 ({exit_stats.get('익절', 0)/total*100:.1f}%)")
    print(f"   손절({sl:.1f}%): {exit_stats.get('손절', 0)}회 ({exit_stats.get('손절', 0)/total*100:.1f}%)")
    print(f"   기간만료: {exit_stats.get('기간만료', 0)}회 ({exit_stats.get('기간만료', 0)/total*100:.1f}%)")
    print("-" * 70)

    # 상위 종목 표시
    display_cols = ['종목코드', '종목명', '매수가', '회전율', '보유일', '청산사유', '수익률']
    display_cols = [c for c in display_cols if c in result_df.columns]

    print(f"\n[상위 {min(50, len(result_df))}개 종목]")
    top_df = result_df.head(50)[display_cols].copy()

    for col in top_df.columns:
        if col == '매수가':
            top_df[col] = top_df[col].apply(lambda x: f"{x:,.0f}")
        elif col == '회전율':
            top_df[col] = top_df[col].apply(lambda x: f"{x:.2f}%")
        elif col == '수익률':
            top_df[col] = top_df[col].apply(lambda x: f"{x:+.2f}%")

    print(top_df.to_string(index=False))

    # 하위 종목
    if len(result_df) > 50:
        print(f"\n[하위 10개 종목]")
        bottom_df = result_df.tail(10)[display_cols].copy()
        for col in bottom_df.columns:
            if col == '매수가':
                bottom_df[col] = bottom_df[col].apply(lambda x: f"{x:,.0f}")
            elif col == '회전율':
                bottom_df[col] = bottom_df[col].apply(lambda x: f"{x:.2f}%")
            elif col == '수익률':
                bottom_df[col] = bottom_df[col].apply(lambda x: f"{x:+.2f}%")
        print(bottom_df.to_string(index=False))


def main():
    parser = argparse.ArgumentParser(description="특정 날짜(범위) 조건 충족 종목 수익률 조회 (TP/SL 적용)")

    # 날짜 옵션 (단일 또는 범위)
    parser.add_argument("--date", "-d", type=str, help="단일 기준일 (YYYYMMDD)")
    parser.add_argument("--start-date", type=str, help="시작일 (YYYYMMDD)")
    parser.add_argument("--end-date", type=str, help="종료일 (YYYYMMDD)")

    # 조건 및 매매 설정
    parser.add_argument("--conditions", "-c", type=str, default="A", help="조건 표현식")
    parser.add_argument("--days", type=int, default=14, help="최대 보유 기간 (기본: 14일)")
    parser.add_argument("--tp", type=float, default=10.0, help="익절 라인 %% (기본: 10)")
    parser.add_argument("--sl", type=float, default=-5.0, help="손절 라인 %% (기본: -5)")
    parser.add_argument("--top", "-t", type=int, default=50, help="상위 N개 표시")
    args = parser.parse_args()

    # 날짜 옵션 검증
    if args.date and (args.start_date or args.end_date):
        print("[ERROR] --date와 --start-date/--end-date는 동시에 사용할 수 없습니다.")
        return

    if not args.date and not (args.start_date and args.end_date):
        print("[ERROR] --date 또는 --start-date와 --end-date를 지정해야 합니다.")
        return

    is_range_mode = args.start_date and args.end_date

    print("=" * 70)
    if is_range_mode:
        print(f"   날짜 범위 수익률 조회: {args.start_date} ~ {args.end_date}")
    else:
        print(f"   특정 날짜 수익률 조회: {args.date}")
    print(f"   조건: {args.conditions}")
    print(f"   TP: {args.tp:+.1f}% | SL: {args.sl:.1f}% | 최대보유: {args.days}일")
    print("=" * 70)

    # 조건 상세 정보 출력
    print_condition_details(args.conditions)

    # 데이터 로드
    print("\n[1] 데이터 로드...")
    engine = ConditionEngine()
    if not engine.load_data():
        print("   [ERROR] 데이터 로드 실패")
        return

    trading_days = engine.get_all_trading_days()
    df = engine.df_daily

    # 종목별 그룹화 (1회만 실행 - O(1) 접근용)
    print("   -> 종목별 데이터 그룹화...")
    stock_groups = df.groupby('종목코드')
    print(f"   -> {len(stock_groups)}개 종목 그룹화 완료")

    # 대상 날짜 결정
    if is_range_mode:
        # 범위 내 거래일 추출
        target_dates = [d for d in trading_days if args.start_date <= d <= args.end_date]
        if not target_dates:
            print(f"   [ERROR] {args.start_date}~{args.end_date} 범위에 거래일이 없습니다.")
            return
        print(f"   -> 대상 거래일: {len(target_dates)}일 ({target_dates[0]} ~ {target_dates[-1]})")
    else:
        # 단일 날짜
        if args.date not in trading_days:
            valid = [d for d in trading_days if d >= args.date]
            if valid:
                print(f"   [WARN] {args.date}는 거래일이 아닙니다. {valid[0]}로 조정")
                args.date = valid[0]
            else:
                print(f"   [ERROR] {args.date} 이후 거래일 없음")
                return
        target_dates = [args.date]

    # default.json에서 조건 파라미터 로드
    condition_params = load_condition_params()
    cond_parser = ConditionParser(engine, condition_params)

    # 시뮬레이션 실행
    if is_range_mode:
        print(f"\n[2] 날짜 범위 시뮬레이션 (보유 중 종목 중복 매수 방지)...")

        all_results = []
        daily_summaries = []
        holdings = {}  # 보유 중 종목 추적

        total_matched_all = 0
        total_new_buys_all = 0
        total_skipped_all = 0

        for i, date in enumerate(target_dates):
            # 오늘 기준으로 청산된 종목 제거 (청산일이 오늘 이전인 것 제거)
            holdings = {code: exit_date for code, exit_date in holdings.items() if exit_date > date}

            results, holdings, stats = run_single_date(
                engine, cond_parser, df, trading_days, date,
                args.conditions, args.days, args.tp, args.sl, holdings, stock_groups
            )

            all_results.extend(results)
            total_matched_all += stats['total_matched']
            total_new_buys_all += stats['new_buys']
            total_skipped_all += stats['skipped']

            # 날짜별 요약
            if results:
                avg_ret = sum(r['수익률'] for r in results) / len(results)
                win_count = sum(1 for r in results if r['수익률'] > 0)
                win_rate = win_count / len(results) * 100
            else:
                avg_ret = 0
                win_rate = 0

            daily_summaries.append({
                '날짜': date,
                '조건충족': stats['total_matched'],
                '신규매수': stats['new_buys'],
                '보유중스킵': stats['skipped'],
                '평균수익률': avg_ret,
                '승률': win_rate
            })

            # 진행률 출력
            print(f"\r   진행: {i+1}/{len(target_dates)} ({date}) - 신규매수: {stats['new_buys']}개", end="")

        print()  # 줄바꿈

        # 날짜별 결과 테이블
        print("\n" + "=" * 70)
        print("[날짜별 결과]")
        print("-" * 70)
        print(f"{'날짜':<12} {'조건충족':>8} {'신규매수':>8} {'스킵':>6} {'평균수익률':>10} {'승률':>8}")
        print("-" * 70)

        for s in daily_summaries:
            print(f"{s['날짜']:<12} {s['조건충족']:>8} {s['신규매수']:>8} {s['보유중스킵']:>6} "
                  f"{s['평균수익률']:>+9.2f}% {s['승률']:>7.1f}%")

        print("-" * 70)

        # 전체 통합 결과
        if all_results:
            result_df = pd.DataFrame(all_results)
            total = len(result_df)
            avg_ret = result_df['수익률'].mean()
            avg_days = result_df['보유일'].mean()
            win_rate = (result_df['수익률'] > 0).sum() / total * 100
            exit_stats = result_df['청산사유'].value_counts().to_dict()

            print(f"\n[전체 통합 결과]")
            print(f"   총 거래: {total}회 (조건충족 {total_matched_all}회 중 중복제외)")
            print(f"   스킵된 거래: {total_skipped_all}회 (보유 중)")
            print(f"   평균 수익률: {avg_ret:+.2f}%")
            print(f"   평균 보유일: {avg_days:.1f}일")
            print(f"   승률: {win_rate:.1f}%")
            print("-" * 70)
            print(f"\n[청산 사유]")
            print(f"   익절({args.tp:+.1f}%): {exit_stats.get('익절', 0)}회 ({exit_stats.get('익절', 0)/total*100:.1f}%)")
            print(f"   손절({args.sl:.1f}%): {exit_stats.get('손절', 0)}회 ({exit_stats.get('손절', 0)/total*100:.1f}%)")
            print(f"   기간만료: {exit_stats.get('기간만료', 0)}회 ({exit_stats.get('기간만료', 0)/total*100:.1f}%)")
        else:
            print("\n   결과 없음")

    else:
        # 단일 날짜 모드
        print(f"\n[2] 조건 평가: {args.conditions}")
        results, _, stats = run_single_date(
            engine, cond_parser, df, trading_days, args.date,
            args.conditions, args.days, args.tp, args.sl, None, stock_groups
        )
        print(f"   -> {stats['total_matched']}개 종목 충족")

        if not results:
            print("   조건 충족 종목 없음")
            return

        print(f"\n[3] TP/SL 시뮬레이션 (TP:{args.tp:+.1f}%, SL:{args.sl:.1f}%, 최대{args.days}일)...")
        print(f"\n[4] 결과 ({len(results)}개 종목)")
        print("-" * 70)

        print_single_date_results(results, args.tp, args.sl)

    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
