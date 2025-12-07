"""
CSV를 Parquet으로 변환하는 스크립트

Parquet 장점:
- 압축률 좋음 (CSV 대비 70~80% 용량 감소)
- 로딩 속도 빠름 (5~10배)
- 컬럼 단위 조회 가능

사용법:
    python convert_to_parquet.py output/ohlc_20240101_20251205_30m.csv
    python convert_to_parquet.py output/ohlc_20230101_20251205.csv
    python convert_to_parquet.py output/*.csv  # 모든 CSV 변환
"""
import sys
import os
import io
import glob
import argparse

# stdout을 UTF-8로 설정 (Windows 호환성)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import pandas as pd
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError as e:
    print(f"   [ERROR] 필요한 패키지가 없습니다: {e}")
    print("   설치: pip install pandas pyarrow")
    sys.exit(1)

from config import OUTPUT_DIR


def convert_csv_to_parquet(csv_path: str, compression: str = "snappy") -> str:
    """
    CSV를 Parquet으로 변환

    Args:
        csv_path: CSV 파일 경로
        compression: 압축 방식 (snappy, gzip, zstd)

    Returns:
        str: 생성된 Parquet 파일 경로
    """
    # 파일 경로 처리
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(OUTPUT_DIR, csv_path)

    if not os.path.exists(csv_path):
        print(f"   [ERROR] 파일을 찾을 수 없습니다: {csv_path}")
        return ""

    # 출력 파일명
    parquet_path = csv_path.rsplit('.', 1)[0] + ".parquet"

    print(f"\n   [CONVERT] {os.path.basename(csv_path)}")
    print(f"   -> 읽는 중...")

    # CSV 읽기
    df = pd.read_csv(csv_path, encoding="utf-8-sig")

    # 데이터 타입 최적화
    print(f"   -> 데이터 타입 최적화 중...")

    # 숫자 컬럼 타입 변환
    numeric_cols = ['시가', '고가', '저가', '종가', '거래량', '거래대금']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 날짜/시간 컬럼을 문자열로 유지 (정렬/필터 편의)
    if '날짜' in df.columns:
        df['날짜'] = df['날짜'].astype(str)
    if '시간' in df.columns:
        df['시간'] = df['시간'].astype(str).str.zfill(6)

    # 종목코드 문자열 유지
    if '종목코드' in df.columns:
        df['종목코드'] = df['종목코드'].astype(str).str.zfill(6)

    # Parquet 저장
    print(f"   -> Parquet 저장 중 (압축: {compression})...")
    df.to_parquet(parquet_path, engine='pyarrow', compression=compression, index=False)

    # 결과 출력
    csv_size = os.path.getsize(csv_path) / (1024 * 1024)
    parquet_size = os.path.getsize(parquet_path) / (1024 * 1024)
    reduction = (1 - parquet_size / csv_size) * 100

    print(f"   [DONE] 변환 완료!")
    print(f"   CSV:     {csv_size:.1f} MB")
    print(f"   Parquet: {parquet_size:.1f} MB ({reduction:.0f}% 감소)")

    return parquet_path


def main():
    parser = argparse.ArgumentParser(
        description="CSV를 Parquet으로 변환",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
    python convert_to_parquet.py ohlc_20240101_20251205_30m.csv
    python convert_to_parquet.py output/ohlc_20230101_20251205.csv
    python convert_to_parquet.py *.csv                              # 모든 CSV 변환
    python convert_to_parquet.py ohlc*.csv --compression gzip       # gzip 압축
        """
    )

    parser.add_argument(
        "files",
        type=str,
        nargs="+",
        help="변환할 CSV 파일 (와일드카드 지원)"
    )
    parser.add_argument(
        "--compression",
        type=str,
        default="snappy",
        choices=["snappy", "gzip", "zstd", "none"],
        help="압축 방식 (기본값: snappy)"
    )

    args = parser.parse_args()

    # 파일 목록 확장 (와일드카드 처리)
    all_files = []
    for pattern in args.files:
        if not os.path.isabs(pattern):
            pattern = os.path.join(OUTPUT_DIR, pattern)
        matched = glob.glob(pattern)
        if matched:
            all_files.extend(matched)
        else:
            # 와일드카드가 아닌 경우 그대로 추가
            all_files.append(pattern)

    # CSV 파일만 필터링
    csv_files = [f for f in all_files if f.endswith('.csv')]

    if not csv_files:
        print("   [ERROR] 변환할 CSV 파일이 없습니다.")
        sys.exit(1)

    print("=" * 60)
    print("   CSV → Parquet 변환")
    print("=" * 60)
    print(f"   대상 파일: {len(csv_files)}개")
    print(f"   압축 방식: {args.compression}")

    # 변환 실행
    compression = None if args.compression == "none" else args.compression
    success_count = 0

    for csv_file in csv_files:
        result = convert_csv_to_parquet(csv_file, compression)
        if result:
            success_count += 1

    print("\n" + "=" * 60)
    print(f"   완료: {success_count}/{len(csv_files)}개 변환 성공")
    print("=" * 60)


if __name__ == "__main__":
    main()
