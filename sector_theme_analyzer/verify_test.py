"""
single_day_test.py 교차 검증 스크립트

프로그램의 결과를 독립적으로 계산하여 비교합니다.
"""
import pandas as pd
import json
from collections import defaultdict

# 설정
BASE_DATE = "20251105"
TP = 10.0
SL = -5.0
MAX_DAYS = 5
CONSECUTIVE_DAYS = 2  # 조건 A 연속 상승일

print("=" * 70)
print("single_day_test.py 교차 검증")
print("=" * 70)
print(f"기준일: {BASE_DATE}")
print(f"TP: {TP}%, SL: {SL}%, 최대보유: {MAX_DAYS}일")
print("=" * 70)

# 1. 데이터 로드
print("\n[1] 데이터 로드...")
df = pd.read_parquet("output/ohlc_20230327_20251205_with_turnover.parquet")
print(f"   -> 일봉 데이터: {len(df):,}행")

with open("C:/01 Project/Trading_Machnie/sector_industry_find/backend/ls_stock_list_final.json", "r", encoding="utf-8") as f:
    stocks = json.load(f)
print(f"   -> 종목 정보: {len(stocks):,}종목")

# 등락률 계산
df = df.sort_values(['종목코드', '날짜'])
df['전일종가'] = df.groupby('종목코드')['종가'].shift(1)
df['등락률'] = ((df['종가'] - df['전일종가']) / df['전일종가'] * 100).round(2)

# 거래일 목록
trading_days = sorted(df['날짜'].unique())
print(f"   -> 거래일: {trading_days[0]} ~ {trading_days[-1]} ({len(trading_days)}일)")

# 2. 조건 A 검증: 섹터+업종 2일 연속 상승
print("\n[2] 조건 A 검증: 섹터+업종 2일 연속 상승")
print("-" * 70)

# 기준일 위치 및 연속 상승 확인할 N일 범위
base_idx = trading_days.index(BASE_DATE)
check_days = trading_days[base_idx-CONSECUTIVE_DAYS+1:base_idx+1]  # N일
print(f"   확인 기간: {check_days}")

df_period = df[df['날짜'].isin(check_days)].copy()

# === 업종 연속 상승 찾기 (원본 로직과 동일) ===
industry_stocks = defaultdict(list)  # 업종코드 -> 종목코드 리스트

for stock in stocks:
    code = stock.get("단축코드", "")
    ind_codes = stock.get("업종코드") or []

    for ind_code in ind_codes:
        # 업종코드가 5~30 사이인 것만 (원본과 동일)
        if ind_code and ind_code.isdigit() and 5 <= int(ind_code) <= 30:
            industry_stocks[ind_code].append(code)

rising_industries = []
for ind_code, stock_codes in industry_stocks.items():
    df_ind = df_period[df_period['종목코드'].isin(stock_codes)]
    if len(df_ind) == 0:
        continue

    # 날짜별 업종 평균 등락률 계산
    daily_avg = df_ind.groupby('날짜')['등락률'].mean()

    # 모든 날짜에서 양수인지 확인 (연속 상승)
    if len(daily_avg) == len(check_days) and (daily_avg > 0).all():
        rising_industries.append(ind_code)

print(f"   연속 상승 업종: {len(rising_industries)}개")

# === 섹터 연속 상승 찾기 (원본 로직과 동일) ===
sector_stocks = defaultdict(list)  # 섹터코드 -> 종목코드 리스트

for stock in stocks:
    code = stock.get("단축코드", "")
    sec_codes = stock.get("섹터코드") or []

    for sec_code in sec_codes:
        if sec_code:
            sector_stocks[sec_code].append(code)

rising_sectors = []
for sec_code, stock_codes in sector_stocks.items():
    if len(stock_codes) < 3:  # 3종목 이상인 섹터만 (원본과 동일)
        continue

    df_sec = df_period[df_period['종목코드'].isin(stock_codes)]
    if len(df_sec) == 0:
        continue

    # 날짜별 섹터 평균 등락률 계산
    daily_avg = df_sec.groupby('날짜')['등락률'].mean()

    # 모든 날짜에서 양수인지 확인 (연속 상승)
    if len(daily_avg) == len(check_days) and (daily_avg > 0).all():
        rising_sectors.append(sec_code)

print(f"   연속 상승 섹터: {len(rising_sectors)}개")

# === 조건 A 충족 종목 찾기 (원본 로직과 동일) ===
rising_ind_set = set(rising_industries)
rising_sec_set = set(rising_sectors)
valid_codes = set(df_period['종목코드'].unique())

condition_a_stocks = []
for stock in stocks:
    code = stock.get("단축코드", "")

    # 해당 기간에 거래 데이터가 있는 종목만
    if code not in valid_codes:
        continue

    ind_codes = stock.get("업종코드") or []
    sec_codes = stock.get("섹터코드") or []

    # 업종코드 중 5~30 범위만 체크 (원본과 동일)
    valid_ind_codes = [c for c in ind_codes if c and c.isdigit() and 5 <= int(c) <= 30]
    matched_ind = [c for c in valid_ind_codes if c in rising_ind_set]
    matched_sec = [c for c in sec_codes if c in rising_sec_set]

    if matched_ind and matched_sec:
        condition_a_stocks.append(code)

print(f"   조건 A 충족 종목: {len(condition_a_stocks)}개")

# 3. 몇 가지 종목 상세 검증
print("\n[3] 개별 종목 TP/SL 시뮬레이션 검증")
print("-" * 70)

# 프로그램 출력에서 몇 개 종목 선택
test_stocks = [
    ("000540", "흥국화재", 3655, "익절", 5),     # 5일차 익절
    ("031210", "코웰패션", 49550, "익절", 3),    # 3일차 익절
    ("009420", "한올바이오파마", 44400, "익절", 1),  # 1일차 익절
    ("003850", "보령", 8950, "손절", 2),         # 2일차 손절
    ("317450", "카카오페이", 78600, "손절", 1),  # 1일차 손절
    ("001450", "현대해상", 27400, "기간만료", 5), # 기간만료
]

# 미래 거래일 계산
future_days = trading_days[base_idx:base_idx + MAX_DAYS + 1]
print(f"   매수일 포함 미래 거래일: {future_days}")

def verify_stock(code, name, expected_base_close, expected_exit, expected_days):
    """개별 종목 검증"""
    stock_data = df[df['종목코드'] == code].copy()

    # 기준일 종가
    base_row = stock_data[stock_data['날짜'] == BASE_DATE]
    if base_row.empty:
        return False, f"기준일 데이터 없음"

    base_close = base_row['종가'].values[0]

    print(f"\n   [{code}] {name}")
    print(f"   기준일 종가: {base_close:,.0f}원 (프로그램: {expected_base_close:,}원)")

    # 미래 일별 데이터
    print(f"   {'일차':<6} {'날짜':<12} {'고가':<12} {'저가':<12} {'고가수익률':<12} {'저가수익률':<12}")

    actual_exit = None
    actual_days = 0
    actual_return = 0

    for i, day in enumerate(future_days[1:], 1):  # 매수 다음날부터
        day_data = stock_data[stock_data['날짜'] == day]
        if day_data.empty:
            print(f"   {i:<6} {day:<12} {'데이터없음':<12}")
            continue

        high = day_data['고가'].values[0]
        low = day_data['저가'].values[0]
        close = day_data['종가'].values[0]
        high_ret = (high - base_close) / base_close * 100
        low_ret = (low - base_close) / base_close * 100

        print(f"   {i:<6} {day:<12} {high:>10,.0f}원 {low:>10,.0f}원 {high_ret:>+10.2f}% {low_ret:>+10.2f}%")

        # TP/SL 체크 (손절 우선)
        if actual_exit is None:
            if low_ret <= SL:
                actual_exit = "손절"
                actual_days = i
                actual_return = SL
            elif high_ret >= TP:
                actual_exit = "익절"
                actual_days = i
                actual_return = TP

    # 기간만료 체크
    if actual_exit is None:
        actual_exit = "기간만료"
        actual_days = MAX_DAYS
        # 마지막 날 종가로 수익률 계산
        last_day = future_days[-1] if len(future_days) > MAX_DAYS else future_days[-1]
        last_data = stock_data[stock_data['날짜'] == last_day]
        if not last_data.empty:
            last_close = last_data['종가'].values[0]
            actual_return = (last_close - base_close) / base_close * 100

    # 결과 비교
    match = actual_exit == expected_exit and actual_days == expected_days
    mark = "O 일치" if match else "X 불일치"
    print(f"   결과: {actual_exit} ({actual_days}일차, {actual_return:+.2f}%)")
    print(f"   기대: {expected_exit} ({expected_days}일차)")
    print(f"   검증: {mark}")

    return match, actual_exit

print("\n[개별 종목 상세 검증]")
match_count = 0
for code, name, base_close, expected_exit, expected_days in test_stocks:
    match, _ = verify_stock(code, name, base_close, expected_exit, expected_days)
    if match:
        match_count += 1

print(f"\n   개별 검증 결과: {match_count}/{len(test_stocks)} 종목 일치")

# 4. 전체 수익률 계산 검증
print("\n" + "=" * 70)
print("[4] 전체 수익률 계산 검증")
print("-" * 70)

all_returns = []
exit_reasons = {"익절": 0, "손절": 0, "기간만료": 0}
total_days = 0

for code in condition_a_stocks:
    stock_data = df[df['종목코드'] == code].copy()
    base_row = stock_data[stock_data['날짜'] == BASE_DATE]

    if base_row.empty:
        continue

    base_close = base_row['종가'].values[0]
    exit_reason = None
    ret = 0
    days = 0

    for i, day in enumerate(future_days[1:], 1):
        day_data = stock_data[stock_data['날짜'] == day]
        if day_data.empty:
            continue

        high = day_data['고가'].values[0]
        low = day_data['저가'].values[0]
        high_ret = (high - base_close) / base_close * 100
        low_ret = (low - base_close) / base_close * 100

        if exit_reason is None:
            if low_ret <= SL:
                exit_reason = "손절"
                days = i
                ret = SL
            elif high_ret >= TP:
                exit_reason = "익절"
                days = i
                ret = TP

    if exit_reason is None:
        exit_reason = "기간만료"
        days = MAX_DAYS
        last_day = future_days[-1] if len(future_days) > MAX_DAYS else future_days[-1]
        last_data = stock_data[stock_data['날짜'] == last_day]
        if not last_data.empty:
            last_close = last_data['종가'].values[0]
            ret = (last_close - base_close) / base_close * 100

    all_returns.append(ret)
    exit_reasons[exit_reason] += 1
    total_days += days

# 계산 결과
avg_return = sum(all_returns) / len(all_returns) if all_returns else 0
avg_days = total_days / len(all_returns) if all_returns else 0
win_rate = sum(1 for r in all_returns if r > 0) / len(all_returns) * 100 if all_returns else 0

print(f"\n   [독립 계산 결과]")
print(f"   총 거래: {len(all_returns)}회")
print(f"   평균 수익률: {avg_return:+.2f}%")
print(f"   평균 보유일: {avg_days:.1f}일")
print(f"   승률: {win_rate:.1f}%")
print(f"   청산 사유:")
print(f"     익절: {exit_reasons['익절']}회 ({exit_reasons['익절']/len(all_returns)*100:.1f}%)")
print(f"     손절: {exit_reasons['손절']}회 ({exit_reasons['손절']/len(all_returns)*100:.1f}%)")
print(f"     기간만료: {exit_reasons['기간만료']}회 ({exit_reasons['기간만료']/len(all_returns)*100:.1f}%)")

print(f"\n   [프로그램 결과]")
print(f"   총 거래: 50회")
print(f"   평균 수익률: +3.34%")
print(f"   평균 보유일: 4.0일")
print(f"   승률: 76.0%")
print(f"   청산 사유:")
print(f"     익절: 13회 (26.0%)")
print(f"     손절: 10회 (20.0%)")
print(f"     기간만료: 27회 (54.0%)")

print("\n" + "=" * 70)
print("[5] 검증 결론")
print("=" * 70)

# 차이 분석
diff_return = abs(avg_return - 3.34)
diff_trades = abs(len(all_returns) - 50)
diff_win = abs(win_rate - 76.0)

issues = []
if diff_trades > 0:
    issues.append(f"거래 수 차이: {len(all_returns)} vs 50 ({diff_trades}개)")
if diff_return > 0.5:
    issues.append(f"수익률 차이: {avg_return:+.2f}% vs +3.34% ({diff_return:.2f}%p)")
if diff_win > 3:
    issues.append(f"승률 차이: {win_rate:.1f}% vs 76.0% ({diff_win:.1f}%p)")

if not issues:
    print("   O 프로그램이 정상적으로 작동합니다.")
    print("   - 조건 A 충족 종목 탐색: 정상")
    print("   - TP/SL 시뮬레이션: 정상")
    print("   - 수익률/승률 계산: 정상")
else:
    print("   발견된 차이점:")
    for issue in issues:
        print(f"     - {issue}")

print("=" * 70)
