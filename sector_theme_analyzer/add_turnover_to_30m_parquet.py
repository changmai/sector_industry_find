"""
30분봉 Parquet 파일에 회전율(거래회전율) 컬럼 추가

회전율 = (거래량 / 발행주식수) * 100

사용법:
    python add_turnover_to_30m_parquet.py
"""
import pandas as pd
import json
import os
import glob

def main():
    # 경로 설정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    stock_list_path = os.path.join(script_dir, '..', 'backend', 'ls_stock_list_final.json')

    # 30분봉 파일 찾기
    parquet_files = glob.glob(os.path.join(output_dir, '*_30m.parquet'))
    if not parquet_files:
        print("[ERROR] 30분봉 Parquet 파일을 찾을 수 없습니다.")
        return

    # 가장 최신 파일 선택
    parquet_path = sorted(parquet_files)[-1]
    filename = os.path.basename(parquet_path)
    output_filename = filename.replace('.parquet', '_with_turnover.parquet')
    output_path = os.path.join(output_dir, output_filename)

    print("=" * 60)
    print("   30분봉 Parquet 파일에 회전율 추가")
    print("=" * 60)
    print(f"   입력: {filename}")
    print(f"   출력: {output_filename}")

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

    # 소수점 4자리로 반올림 (30분봉은 회전율이 낮으므로)
    df['거래회전율'] = df['거래회전율'].round(4)

    print(f"   -> 회전율 통계:")
    print(f"      평균: {df['거래회전율'].mean():.4f}%")
    print(f"      최대: {df['거래회전율'].max():.4f}%")
    print(f"      중앙값: {df['거래회전율'].median():.4f}%")

    # 5. 저장
    print("\n[5] 새 Parquet 파일 저장...")
    df.to_parquet(output_path, index=False)

    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"   -> 저장 완료: {output_path}")
    print(f"   -> 파일 크기: {file_size:.1f} MB")
    print(f"   -> 최종 컬럼: {list(df.columns)}")

    # 6. 샘플 데이터 확인
    print("\n[6] 샘플 데이터 확인 (회전율 상위 10개):")
    sample = df.nlargest(10, '거래회전율')[['종목코드', '종목명', '날짜', '시간', '거래량', '발행주식수', '거래회전율']]
    print(sample.to_string(index=False))

    print("\n" + "=" * 60)
    print("   완료!")
    print("=" * 60)

    return output_path


if __name__ == "__main__":
    main()
