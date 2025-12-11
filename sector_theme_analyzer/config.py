"""
설정 모듈

API 키, URL, 분석 파라미터 등을 관리합니다.
"""
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# .env 파일 로드 (backend 폴더)
env_path = os.path.join(os.path.dirname(__file__), '..', 'backend', '.env')
load_dotenv(env_path)

# LS증권 API 설정
# backend/.env에서는 APP_KEY, APP_SECRET으로 저장됨
LS_APP_KEY = os.getenv("LS_APP_KEY", "") or os.getenv("APP_KEY", "")
LS_APP_SECRET = os.getenv("LS_APP_SECRET", "") or os.getenv("APP_SECRET", "")
LS_REST_URL = "https://openapi.ls-sec.co.kr:8080"

# API 엔드포인트
INDUSTRY_ENDPOINT = "/indtp/market-data"  # 업종 (t8424, t1514)
CHART_ENDPOINT = "/stock/chart"           # 차트 (t8410)

# 종목 리스트 경로
STOCK_LIST_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'backend', 'ls_stock_list_final.json'
)

# 출력 디렉토리
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')


@dataclass
class AnalysisConfig:
    """분석 설정 클래스"""

    # 기준 날짜 (YYYYMMDD)
    base_date: str = ""

    # 연속 상승 일수
    consecutive_days: int = 5

    # 테마 상승 판정 비율 (60% = 0.6)
    theme_rise_ratio: float = 0.6

    # 업종코드 범위 (실제 산업분류: 005~030)
    sector_range: tuple = (5, 30)

    # API 호출 딜레이 (초)
    api_delay: float = 1.0

    # 추가 딜레이 간격 (N회마다)
    extra_delay_interval: int = 20

    # 추가 딜레이 (초)
    extra_delay: float = 3.0

    # Rate Limit 대기 시간 (초)
    rate_limit_wait: float = 65.0

    # 최대 재시도 횟수
    max_retries: int = 3


# 기본 설정 인스턴스
DEFAULT_CONFIG = AnalysisConfig()
