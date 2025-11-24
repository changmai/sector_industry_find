# LS Footprint Chart Pro

실시간 Footprint 차트 시뮬레이터 - LS증권 WebSocket API 연동

## 기능

- **다중 데이터 소스 지원**
  - 🎲 Mock Data: 랜덤 시뮬레이션 데이터
  - 📊 Raw Data: 저장된 실제 시장 데이터
  - 🔴 Live WebSocket: LS증권 실시간 체결 데이터

- **Footprint 분석**
  - 가격별 매수/매도 거래량 시각화
  - POC (Point of Control) 표시
  - Imbalance & Stacked Imbalance 감지
  - Unfinished Business 마커
  - Delta 추적 (누적/최대/최소)

- **유연한 회전 모드**
  - VOLUME: 거래량 기준 바 회전
  - TIME: 시간 기준 바 회전
  - RANGE: 가격 범위 기준 바 회전

## 실행 방법

### 1. Frontend 실행

```bash
# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

Frontend는 `http://localhost:5173`에서 실행됩니다.

### 2. Backend 실행 (WebSocket 실시간 데이터용)

```bash
# Python 의존성 설치
cd backend
pip install -r requirements.txt

# 환경변수 설정 (.env 파일 편집)
# LS_APP_KEY와 LS_APP_SECRET 입력

# 백엔드 서버 실행
cd ..
npm run backend
```

Backend는 `http://localhost:8000`에서 실행됩니다.

**또는 두 개의 터미널에서 동시 실행:**

터미널 1:
```bash
npm run dev
```

터미널 2:
```bash
npm run backend
```

### 3. 애플리케이션 사용

1. 브라우저에서 `http://localhost:5173` 접속
2. 우측 상단 드롭다운에서 데이터 소스 선택:
   - **Mock Data**: 실시간 시뮬레이션 (백엔드 불필요)
   - **Raw Data**: 저장된 데이터 재생 (백엔드 불필요)
   - **Live WebSocket**: LS증권 실시간 데이터 (백엔드 필요)

## 프로젝트 구조

```
footprint_chart_single_table/
├── App.tsx                      # 메인 애플리케이션
├── components/                  # UI 컴포넌트
│   ├── Header.tsx               # 상단 헤더 (현재가, CVD 등)
│   ├── FootprintTable.tsx       # Footprint 차트 테이블
│   ├── FootprintBarComponent.tsx # 개별 바 렌더링
│   └── TickList.tsx             # 실시간 틱 리스트
├── services/                    # 데이터 서비스
│   ├── mockDataService.ts       # Mock 데이터 생성
│   ├── rawDataService.ts        # Raw 데이터 로딩
│   └── websocketDataService.ts  # WebSocket 클라이언트
├── backend/                     # Python 백엔드
│   ├── main.py                  # FastAPI 서버
│   ├── ls_websocket.py          # LS증권 WebSocket 클라이언트
│   ├── requirements.txt         # Python 의존성
│   └── .env                     # API 키 설정
├── types.ts                     # TypeScript 타입 정의
├── constants.ts                 # 설정 상수
└── utils.ts                     # Footprint 지표 계산
```

## 설정

### Frontend 설정 (constants.ts)

```typescript
export const CONFIG = {
  TARGET_NAME: "Samsung Electronics",
  TARGET_CODE: "005930",
  INITIAL_PRICE: 72500,
  PRICE_STEP: 100,
  IMBALANCE_RATIO: 3.0,
  TICK_RATE_MS: 200,
};
```

### Backend 설정 (backend/.env)

```bash
LS_APP_KEY=your_app_key_here
LS_APP_SECRET=your_app_secret_here
```

## 기술 스택

### Frontend
- React 19.2
- TypeScript 5.8
- Vite 6.2
- Tailwind CSS
- Lucide React (아이콘)

### Backend
- Python 3.x
- FastAPI
- WebSockets
- Uvicorn

## 데이터 저장

WebSocket 모드로 실행 시, 수신한 원본 틱 데이터는 자동으로 저장됩니다:

- **위치**: `backend/raw_data_{종목코드}_{날짜}.txt`
- **형식**: NDJSON (한 줄에 하나의 JSON)
- **용도**: 나중에 Raw Data 모드로 재생 가능

## 문제 해결

### WebSocket 연결 실패
1. 백엔드 서버가 실행 중인지 확인
2. `.env` 파일의 API 키가 올바른지 확인
3. 방화벽 설정 확인

### 데이터 수신 안됨
1. 종목 코드 확인 (기본: 005930)
2. 장 운영 시간 확인 (모의투자 서버 제한)
3. 콘솔 로그에서 에러 확인

## 라이선스

MIT

## 기여

Issues 및 Pull Requests 환영합니다.
