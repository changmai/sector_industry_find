# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

한국 주식 트레이딩 분석 플랫폼 - React/TypeScript 프론트엔드 + Python FastAPI 백엔드로 구성. LS증권 API를 통해 실시간 시장 데이터를 수집하고, Footprint 차트, 프로그램 매매 연구, 업종/테마 분석 도구를 제공.

## Build & Run Commands

```bash
# Frontend (Vite + React)
npm install
npm run dev           # localhost:5173

# Backend (FastAPI)
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 또는 루트에서: npm run backend

# Analysis Tools
cd consecutive_rise_finder && python main.py -d 5
cd sector_theme_analyzer && python local_analyzer.py --base-date 20251205 --days 5
```

## Architecture

### Frontend → Backend Communication
```
React (localhost:5173)
  ├── /ws                    WebSocket (실시간 틱 데이터)
  ├── GET /api/history       과거 NDJSON 데이터
  ├── GET /api/watchlist     구독 종목 목록
  ├── POST /api/subscribe/{code}  종목 추가
  └── GET /api/research/*    연구 도구 API
```

### Backend → LS증권 Integration
- OAuth2 토큰 자동 관리
- WebSocket: 실시간 체결 데이터 (S3_, H1_, UPH TR)
- REST API: t1102, t1514, t1533, t8410, t8412, t8424, t8425
- Rate Limiting 자동 처리 (딜레이/재시도)

### Server-Driven Architecture
- **핵심**: 백엔드가 24/7 데이터 수집, 프론트는 연결/해제만
- `watchlist.json` 기반 종목 자동 구독
- 다중 클라이언트 동시 연결 지원 (stateless frontend)

## Key Modules

### backend/
| 파일 | 역할 |
|------|------|
| `main.py` | FastAPI 서버, 30+ 엔드포인트, lifespan 이벤트 |
| `ls_websocket.py` | LS증권 WebSocket (다중종목, 자동재연결) |
| `industry_mapper.py` | 종목↔업종코드 매핑 |
| `research/` | 이벤트 감지, 가격추적, 백테스팅, 리포트 |

### consecutive_rise_finder/
- **용도**: 오늘 기준 N일 연속 상승 테마/업종 탐색
- **한계**: 테마 API(t1533)는 오늘만 조회 가능
- `main.py -d 5 --theme-only` 또는 `--sector-only`

### sector_theme_analyzer/
- **용도**: 과거 날짜 기준 멀티 조건 백테스팅
- **핵심 CLI**:
  - `single_day_test.py`: 일별 TP/SL 시뮬레이션 (벡터화, 고성능)
  - `backtest_cli.py`: 멀티 조건 백테스팅 + TP/SL 최적화
  - `condition_cli.py`: 개별 조건 테스트 및 종목 목록 확인
- **엔진**:
  - `condition_engine.py`: 조건 A~I + GT 조건 로직
  - `condition_parser.py`: AND/OR 표현식 파서 ("A AND (B OR C)")
  - `multi_backtester.py`: TP/SL 백테스팅 엔진 (트레일링스탑, 타임컷 지원)
  - `combination_tester.py`: 조건 조합 자동 테스트 + TP/SL 최적화
- **데이터**:
  - `download_ohlc.py`: OHLC 데이터 다운로드 (분봉/일봉)
  - `convert_to_parquet.py`: CSV→Parquet 변환 (70-80% 용량 감소)
  - `conditions/default.json`: 조건별 기본 파라미터 (single source of truth)

### Frontend Components
- `components/FootprintTable.tsx`: 메인 풋프린트 차트
- `components/CVDChart.tsx`: CVD(누적거래량델타) 시각화
- `components/research/`: 연구 대시보드 UI
- `pages/FootprintPage.tsx`: Mock/Raw/Live 데이터 소스 전환

## Data Flow

1. **Startup**: watchlist.json 로드 → LS WebSocket 연결 → 연구도구 초기화
2. **Live**: LS 틱 수신 → 파일 저장 + 클라이언트 브로드캐스트 → 이벤트 감지
3. **Analysis**: Parquet 로드 → 30분봉→일봉 변환 → 조건 필터링

## Configuration

```bash
# backend/.env (필수)
LS_APP_KEY=your_app_key
LS_APP_SECRET=your_app_secret

# 주요 설정 파일
backend/watchlist.json              # 구독 종목 리스트
backend/ls_stock_list_final.json    # 전체 종목 마스터 (섹터/업종코드/발행주식수 포함)
backend/industry_mapping_cache.json # 업종 매핑 캐시
```

## Research Tools (v2.0)

- **이벤트 감지**: 비차익 매수/매도 급증 (기본 3천만원 이상)
- **가격 추적**: 이벤트 후 1m/5m/10m/30m 가격 변화 기록
- **다이버전스 분석**: 가격 추세 vs 프로그램 매매 신호 비교
- **백테스팅**: UPH raw 데이터 기반 과거 이벤트 시뮬레이션

## Backtesting Commands (sector_theme_analyzer)

```bash
# 일별 TP/SL 시뮬레이션 (범위 모드)
cd sector_theme_analyzer
python single_day_test.py --start-date 20251101 --end-date 20251130 --conditions "A" --days 7 --tp 10 --sl -5

# TP/SL 우선순위 선택 (같은날 동시 도달 시)
python single_day_test.py --date 20251105 --conditions "A AND D" --priority tp  # 익절 우선

# 멀티 조건 백테스팅 + 최적화
python backtest_cli.py --conditions "A AND D AND G" --optimize --tp-min 5 --tp-max 15 --sl-min -7 --sl-max -3

# 개별 조건 테스트
python condition_cli.py --condition A --date 20251205 --top 20
```

### 조건 시스템 (A~I + GT)

| 조건 | 설명 |
|------|------|
| A | 섹터+업종 N일 연속 상승 |
| B | N일 신고거래대금 |
| C | 거래량 회전율 상위 N종목 |
| D | 이평 정배열 (단기>중기>장기) |
| E | N일 신고가 대비 등락률 범위 |
| F | N일전 대비 거래량 비율 |
| G | 회전율 X%~Y% 범위 |
| H | 20일선 눌림목 (세력진입 후 조정) |
| I | 5일선 급등주 (모멘텀 조정) |
| GT_* | 기술적 지표 조건 (MACD, RSI 등) |

조건 파라미터 변경은 `conditions/default.json` 수정 후 자동 적용됨.

### 조합 테스트 (combination_tester.py)

```bash
# 기본 조합 테스트
python combination_tester.py --conditions A,B,D,H --start-date 20251101 --end-date 20251130 --tp 10 --sl -5

# 필수 조건 + 조합 (A,B 고정, C,D,E 중 조합)
python combination_tester.py --required A,B --conditions C,D,E --min-size 1 --max-size 2

# TP/SL 최적화 모드
python combination_tester.py --conditions A,D,H --optimize --tp-min 5 --tp-max 15 --sl-min -7 --sl-max -3

# 트레일링스탑 + 타임컷
python combination_tester.py --conditions A,H --trailing-start 5 --trailing-offset 3 --time-cut-days 3 --time-cut-min-return 2
```

## Code Conventions

- **한국어 변수/주석**: 도메인 용어는 한국어 사용 (업종코드, 종목명 등)
- **Color Convention**: 빨강=상승(Korean market), 파랑=하락
- **API 응답**: `{ status: "success", ... }` 또는 HTTPException
- **캐시 전략**: 종목명은 ls_stock_list_final.json에서 로드 (API 호출 최소화)
- **조건 파라미터**: `conditions/default.json`이 single source of truth (하드코딩 금지)
