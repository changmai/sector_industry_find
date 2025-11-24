# Footprint Chart Backend

LS증권 WebSocket API를 통해 실시간 체결 데이터를 수신하고 Frontend로 중계하는 백엔드 서버입니다.

## 설치 및 실행

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

### 3. 서버 실행

#### 방법 1: 프로젝트 루트에서

```bash
npm run backend
```

#### 방법 2: 백엔드 폴더에서 직접

```bash
python -m uvicorn main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

## API 엔드포인트

### WebSocket: `/ws`

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
  "chetime": "153045"
}
```

### GET: `/`

서버 상태 확인 (헬스 체크)

**응답 예시:**
```json
{
  "status": "running",
  "target_code": "005930",
  "connected_clients": 1
}
```

## 주요 기능

1. **LS증권 API 연결**
   - OAuth2 토큰 자동 발급
   - WebSocket 연결 및 구독 (TR: US3 - 통합체결)
   - PING/PONG 자동 처리

2. **데이터 중계**
   - Frontend로 실시간 체결 데이터 브로드캐스트
   - 다중 클라이언트 연결 지원

3. **데이터 저장**
   - 수신한 원본 데이터를 `raw_data_{종목코드}_{날짜}.txt`로 저장
   - NDJSON 형식 (한 줄에 하나의 JSON 객체)

4. **종목 변경**
   - Frontend에서 종목 코드 변경 요청 가능
   - WebSocket 메시지: `{"type": "change_code", "code": "005930"}`

## 파일 구조

```
backend/
├── main.py              # FastAPI 서버 메인
├── ls_websocket.py      # LS증권 WebSocket 클라이언트
├── requirements.txt     # Python 의존성
├── .env                 # API 키 설정 (Git 제외)
├── .env.example         # API 키 템플릿
└── raw_data_*.txt       # 저장된 틱 데이터 (자동 생성)
```

## 문제 해결

### 토큰 발급 실패
- `.env` 파일의 API KEY와 SECRET이 정확한지 확인
- LS증권 API 서버 상태 확인 (모의투자 서버 사용 중)

### WebSocket 연결 실패
- 백엔드 서버가 실행 중인지 확인 (`http://localhost:8000` 접속)
- 방화벽 설정 확인
- Frontend의 WebSocket URL 확인 (`ws://localhost:8000/ws`)

### 데이터 수신 안됨
- 종목 코드가 올바른지 확인 (기본: 005930 - 삼성전자)
- 장 운영 시간인지 확인 (모의투자는 운영 시간 제한 있음)
- 콘솔 로그에서 에러 메시지 확인
