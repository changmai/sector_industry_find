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
- **용도**: 과거 날짜 기준 백테스팅
- **local_analyzer.py**: Parquet 기반 ~3초 분석 (권장)
- **main.py**: API 기반 ~50분 분석
- `download_ohlc.py`: OHLC 데이터 다운로드 (분봉/일봉)
- `convert_to_parquet.py`: CSV→Parquet 변환 (70-80% 용량 감소)

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
backend/watchlist.json          # 구독 종목 리스트
backend/ls_stock_list.json      # 전체 종목 마스터 (섹터/업종코드 포함)
backend/industry_mapping_cache.json  # 업종 매핑 캐시
```

## Research Tools (v2.0)

- **이벤트 감지**: 비차익 매수/매도 급증 (기본 3천만원 이상)
- **가격 추적**: 이벤트 후 1m/5m/10m/30m 가격 변화 기록
- **다이버전스 분석**: 가격 추세 vs 프로그램 매매 신호 비교
- **백테스팅**: UPH raw 데이터 기반 과거 이벤트 시뮬레이션

## Code Conventions

- **한국어 변수/주석**: 도메인 용어는 한국어 사용 (업종코드, 종목명 등)
- **Color Convention**: 빨강=상승(Korean market), 파랑=하락
- **API 응답**: `{ status: "success", ... }` 또는 HTTPException
- **캐시 전략**: 종목명은 ls_stock_list.json에서 로드 (API 호출 최소화)
