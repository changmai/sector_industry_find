# Footprint Chart Backend

LS증권 WebSocket API를 통해 실시간 체결 데이터를 수신하고 Frontend로 중계하는 백엔드 서버입니다.

## 🚀 주요 기능 (Server-Driven Architecture)

### 1. **서버 시작 시 자동 데이터 수집**
- 서버가 시작되면 `watchlist.json`에 정의된 **모든 관심종목**에 대해 자동으로 LS증권 WebSocket 연결
- 브라우저 접속 여부와 **무관하게 24시간 데이터 수집 및 저장**
- 연결 끊김 시 **자동 재연결** (5초 대기 후 재시도)

### 2. **멀티 종목 동시 구독**
- 하나의 WebSocket 연결로 여러 종목 동시 구독
- 종목별로 개별 파일에 저장 (`raw_data_{종목코드}_{날짜}.txt`)

### 3. **과거 데이터 조회 API**
- Frontend가 접속 시 해당 종목의 과거 데이터를 조회하여 차트 복구 가능
- 엔드포인트: `GET /api/history?code={종목코드}&date={날짜}`

---

## 📦 설치 및 실행

### 1. Python 의존성 설치

```bash
cd backend
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일에 LS증권 API 키를 설정합니다:

```bash
LS_APP_KEY=your_app_key_here
LS_APP_SECRET=your_app_secret_here
```

### 3. 관심종목 설정

`backend/watchlist.json` 파일을 편집하여 수집할 종목을 설정합니다:

```json
{
  "codes": [
    "005930",
    "000660"
  ],
  "description": "관심종목 리스트 - 서버 시작 시 자동으로 모든 종목 데이터 수집"
}
```

### 4. 서버 실행

#### 방법 1: 프로젝트 루트에서

```bash
npm run backend
```

#### 방법 2: 백엔드 폴더에서 직접

```bash
cd backend
python -m uvicorn main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

---

## 🔌 API 엔드포인트

### 1. GET `/`

서버 상태 확인 (헬스 체크)

**응답 예시:**
```json
{
  "status": "running",
  "watchlist": ["005930", "000660"],
  "connected_clients": 1,
  "ls_client_running": true
}
```

---

### 2. WebSocket `/ws`

Frontend와 WebSocket 연결을 맺고 실시간 체결 데이터를 전달합니다.

**연결 예시:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
```

**수신 데이터 형식:**
```json
{
  "price": "72500",
  "cvolume": "150",
  "cgubun": "+",
  "chetime": "153045",
  "code": "005930"
}
```

**주요 특징:**
- 서버는 `watchlist.json`에 있는 **모든 종목** 데이터를 브로드캐스트
- Frontend에서 `code` 필드를 보고 필요한 종목만 필터링
- 클라이언트 연결 해제 시에도 **LS증권 연결은 유지** (계속 데이터 수집)

---

### 3. GET `/api/history`

과거 틱 데이터 조회 (파일에서 읽기)

**파라미터:**
- `code` (필수): 종목코드 (예: "005930")
- `date` (선택): 날짜 (YYYYMMDD, default=오늘)

**요청 예시:**
```
GET /api/history?code=005930
GET /api/history?code=005930&date=20251125
```

**응답 예시:**
```json
[
  {
    "chetime": "153045",
    "price": "72500",
    "cvolume": "150",
    "cgubun": "+"
  },
  ...
]
```

**동작:**
1. `backend/raw_data_{code}_{date}.txt` 파일 존재 확인
2. NDJSON 파싱하여 JSON 배열로 반환
3. 파일 없으면 빈 배열 `[]` 반환

---

### 4. GET `/api/stock/{code}`

LS증권 t1102 TR을 사용하여 종목 정보 조회

**요청 예시:**
```
GET /api/stock/005930
```

**응답 예시:**
```json
{
  "code": "005930",
  "name": "삼성전자",
  "status": "success"
}
```

---

## 📂 파일 구조

```
backend/
├── main.py                  # FastAPI 서버 메인 (Lifespan 이벤트)
├── ls_websocket.py          # LS증권 WebSocket 클라이언트 (Multi-Stock + Auto Reconnect)
├── watchlist.json           # 관심종목 설정 파일
├── requirements.txt         # Python 의존성
├── .env                     # API 키 설정 (Git 제외)
├── .env.example             # API 키 템플릿
└── raw_data_*.txt           # 저장된 틱 데이터 (자동 생성)
```

---

## 🔄 데이터 흐름

```
┌─────────────────────────────────────────────────────────────┐
│  SERVER STARTUP                                             │
│  1. Load watchlist.json                                     │
│  2. Connect to LS증권 WebSocket                             │
│  3. Subscribe all stocks in watchlist                       │
│  4. Start background data collection (24/7)                 │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA COLLECTION (Running in Background)                    │
│  - Receive tick data from LS증권                            │
│  - Save to file: raw_data_{code}_{date}.txt                │
│  - Broadcast to all connected frontend clients              │
│  - Auto reconnect on connection loss                        │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND CONNECTION                                        │
│  1. Browser connects → GET /api/history (load past data)   │
│  2. Connect WebSocket → Receive real-time data              │
│  3. Filter by stock code on frontend                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛡️ 안전성 및 최적화

### 자동 재연결
- 연결 끊김 감지 → 5초 대기 → 자동 재시도
- 새벽 증권사 점검 시에도 자동으로 재연결

### 파일 무결성
- 모든 `write()` 후 `flush()` 호출로 즉시 디스크 기록
- 서버 강제 종료 시에도 데이터 손실 최소화

### 메모리 관리
- Backend는 데이터를 메모리에 쌓지 않고 **파일에만 저장**
- Stateless 설계로 안정적인 장기 운영 가능

---

## 🐛 문제 해결

### 토큰 발급 실패
- `.env` 파일의 API KEY와 SECRET이 정확한지 확인
- LS증권 API 서버 상태 확인 (모의투자 서버 사용 중)

### WebSocket 연결 실패
- 백엔드 서버가 실행 중인지 확인 (`http://localhost:8000` 접속)
- 방화벽 설정 확인
- Frontend의 WebSocket URL 확인 (`ws://localhost:8000/ws`)

### 데이터 수신 안됨
- 종목 코드가 올바른지 확인 (`watchlist.json` 확인)
- 장 운영 시간인지 확인 (모의투자는 운영 시간 제한 있음)
- 콘솔 로그에서 에러 메시지 확인
- `GET /` 엔드포인트로 서버 상태 확인 (`ls_client_running: true` 확인)

### 과거 데이터 조회 안됨
- 파일 경로 확인: `backend/raw_data_{종목코드}_{날짜}.txt`
- 파일이 존재하는지 확인
- 서버 콘솔 로그 확인

---

## 📝 변경 이력

### v2.0 - Server-Driven Architecture
- ✅ Lifespan 이벤트 기반 서버 시작 시 자동 데이터 수집
- ✅ 멀티 종목 동시 구독 (하나의 WebSocket 연결)
- ✅ 자동 재연결 로직 (24시간 안정적 운영)
- ✅ 과거 데이터 조회 API (`/api/history`)
- ✅ 브라우저 연결 해제 시에도 데이터 수집 유지

### v1.0 - Client-Driven Architecture (Legacy)
- 브라우저 접속 시에만 WebSocket 연결
- 단일 종목만 구독 가능
- 브라우저 종료 시 데이터 수집 중단
