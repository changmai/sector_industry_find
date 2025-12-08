"""
Parquet 파일에 회전율(거래회전율) 컬럼 추가

회전율 = (거래량 / 발행주식수) * 100

사용법:
    python add_turnover_to_parquet.py
"""
import pandas as pd
import json
import os

def main():
    # 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parquet_path = os.path.join(script_dir, 'output', 'ohlc_20230327_20251205.parquet')
    stock_list_path = os.path.join(script_dir, '..', 'backend', 'ls_stock_list_final.json')
    output_path = os.path.join(script_dir, 'output', 'ohlc_20230327_20251205_with_turnover.parquet')

    print("=" * 60)
    print("   Parquet 파일에 회전율 추가")
    print("=" * 60)

    # 1. 발행주식수 데이터 로드
    print("\n[1] 발행주식수 데이터 로드...")
    with open(stock_list_path, 'r', encoding='utf-8') as f:
        stock_list = json.load(f)

    # 종목코드 -> 발행주식수 매핑
    shares_map = {}
    for stock in stock_list:
        code = stock.get('단축코드', '')
        shares = stock.get('발행주식수', 0)
        if code and shares > 0:
            shares_map[code] = shares

    print(f"   -> {len(shares_map)}개 종목의 발행주식수 로드 완료")

    # 2. Parquet 파일 로드
    print("\n[2] Parquet 파일 로드...")
    df = pd.read_parquet(parquet_path)
    print(f"   -> {len(df):,}개 행, {len(df['종목코드'].unique())}개 종목")
    print(f"   -> 기존 컬럼: {list(df.columns)}")

    # 3. 발행주식수 컬럼 추가
    print("\n[3] 발행주식수 매핑...")
    df['발행주식수'] = df['종목코드'].map(shares_map)

    # 매핑 안 된 종목 확인
    unmapped = df[df['발행주식수'].isna()]['종목코드'].unique()
    print(f"   -> 매핑 완료: {len(df) - df['발행주식수'].isna().sum():,}개 행")
    print(f"   -> 매핑 실패: {len(unmapped)}개 종목")

    if len(unmapped) > 0 and len(unmapped) <= 20:
        print(f"   -> 미매핑 종목: {list(unmapped)}")

    # 4. 회전율 계산
    print("\n[4] 회전율 계산...")
    # 회전율 = (거래량 / 발행주식수) * 100
    df['거래회전율'] = (df['거래량'] / df['발행주식수']) * 100

    # NaN 처리 (발행주식수 없는 경우 0으로)
    df['거래회전율'] = df['거래회전율'].fillna(0)
    df['발행주식수'] = df['발행주식수'].fillna(0)

    # 소수점 2자리로 반올림
    df['거래회전율'] = df['거래회전율'].round(2)

    print(f"   -> 회전율 통계:")
    print(f"      평균: {df['거래회전율'].mean():.2f}%")
    print(f"      최대: {df['거래회전율'].max():.2f}%")
    print(f"      중앙값: {df['거래회전율'].median():.2f}%")

    # 5. 저장
    print("\n[5] 새 Parquet 파일 저장...")
    df.to_parquet(output_path, index=False)

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"   -> 저장 완료: {output_path}")
    print(f"   -> 파일 크기: {file_size:.1f} MB")
    print(f"   -> 최종 컬럼: {list(df.columns)}")

    # 6. 샘플 데이터 확인
    print("\n[6] 샘플 데이터 확인 (회전율 상위 10개):")
    sample = df.nlargest(10, '거래회전율')[['종목코드', '종목명', '날짜', '거래량', '발행주식수', '거래회전율']]
    print(sample.to_string(index=False))

    print("\n" + "=" * 60)
    print("   완료!")
    print("=" * 60)

    return output_path


if __name__ == "__main__":
    main()
