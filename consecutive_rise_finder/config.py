"""
LS증권 API 설정 및 환경변수 관리
"""
import os
from dotenv import load_dotenv

# .env 파일 로드 (backend 폴더에 있음)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

# LS증권 API 설정
LS_APP_KEY = os.getenv("LS_APP_KEY", "")
LS_APP_SECRET = os.getenv("LS_APP_SECRET", "")
LS_REST_URL = "https://openapi.ls-sec.co.kr:8080"

# API 엔드포인트
SECTOR_ENDPOINT = "/stock/sector"       # 테마(섹터) 관련 API
INDUSTRY_ENDPOINT = "/indtp/market-data"  # 업종 관련 API

# Rate Limiting 설정
BASE_DELAY = 1.0           # 기본 딜레이 (초)
EXTRA_DELAY = 2.0          # 추가 딜레이 (초)
EXTRA_DELAY_INTERVAL = 5   # 추가 딜레이 적용 간격 (N회마다)
MAX_RETRIES = 3            # 최대 재시도 횟수
RATE_LIMIT_WAIT = 60       # API 제한 시 대기 시간 (초)

# 기본 설정
DEFAULT_CONSECUTIVE_DAYS = 5  # 연속 상승 판단 기준 일수

# 종목 리스트 파일 경로
STOCK_LIST_PATH = os.path.join(
    os.path.dirname(__file__),
    '..',
    'backend',
    'ls_stock_list_final.json'
)

# 결과 저장 경로
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
