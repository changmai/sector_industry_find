# 5거래일 연속 상승 테마/업종 및 종목 탐색기 - 오늘자 기준으로만 검토 가능함

LS증권 Open API를 활용하여 **N거래일 연속 상승한 테마(섹터)와 업종**을 찾고, 두 조건을 동시에 만족하는 종목을 탐색하는 Python 프로그램입니다.

---

## 프로젝트 구조

```
consecutive_rise_finder/
├── __init__.py           # 패키지 초기화
├── config.py             # API 설정 (토큰, URL 등)
├── ls_api_client.py      # LS증권 API 클라이언트
├── theme_finder.py       # 테마 연속상승 탐색
├── sector_finder.py      # 업종 연속상승 탐색
├── stock_matcher.py      # 조건 동시만족 종목 매칭
├── main.py               # 메인 실행
├── requirements.txt      # 의존성
└── output/               # 결과 저장 디렉토리
    └── consecutive_rise_5days_YYYYMMDD_HHMMSS.json
```

---

## 탐색 조건

### 조건1: 테마(섹터) N거래일 연속 상승
- `t8425` API로 전체 테마 목록 조회
- `t1533` API를 `chgdate=1,2,3,4,5`로 N번 호출
- 각 날짜별 상승 테마(chgdiff > 0) 추출
- N일 모두 상승한 테마 = 교집합으로 필터링

### 조건2: 업종 N거래일 연속 상승
- `t8424` API로 전체 업종 목록 조회
- `t1514` API로 각 업종의 N일치 기간별 추이 조회
- `sign` 값이 N일 모두 "1"(상한) 또는 "2"(상승)인 업종 필터링

### 조건1+2: 동시 만족 종목
- `ls_stock_list_final.json`에서 각 종목의 `섹터코드`와 `업종코드` 확인
- 연속상승 테마코드 ∩ 종목의 섹터코드 ≠ 공집합
- 연속상승 업종코드 ∩ 종목의 업종코드 ≠ 공집합
- 두 조건 모두 만족하는 종목 추출

---

## 사용법

### 기본 실행 (5일 연속 상승)
```bash
cd consecutive_rise_finder
python main.py
```

### 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `-d`, `--days` | 연속 상승 판단 기준 일수 (기본: 5일) | `python main.py -d 3` |
| `-b`, `--base-date` | 기준일 (YYYYMMDD 형식, 기본: 오늘) | `python main.py -b 20251201` |
| `-o`, `--output` | 결과 저장 디렉토리 | `python main.py -o ./results` |
| `--no-save` | 결과를 파일로 저장하지 않음 | `python main.py --no-save` |
| `--theme-only` | 테마(섹터) 연속 상승만 탐색 | `python main.py --theme-only` |
| `--sector-only` | 업종 연속 상승만 탐색 | `python main.py --sector-only` |

> **참고**: `--base-date` 옵션은 **업종(t1514)만 지원**합니다. 테마(t1533) API는 기준일 지정을 지원하지 않아 항상 오늘 기준으로 조회됩니다.

### 사용 예시

```bash
# 3일 연속 상승으로 조회
python main.py -d 3

# 테마만 탐색
python main.py --theme-only

# 업종만 탐색
python main.py --sector-only

# 특정 날짜 기준으로 업종 조회 (YYYYMMDD)
python main.py --sector-only -b 20251201

# 특정 날짜 기준 전체 탐색 (테마는 오늘, 업종은 지정일 기준)
python main.py -b 20251201

# 결과 파일 저장하지 않음
python main.py --no-save

# 7일 연속 상승, 커스텀 출력 경로
python main.py -d 7 -o ./my_results
```

---

## 실행 결과 예시 (2025-12-05 기준)

```
======================================================================
   [SUMMARY] 최종 요약
======================================================================
   실행 시간: 2025-12-05 14:03:01
   연속 상승 기준: 5거래일
   API 호출 횟수: 139회
----------------------------------------------------------------------
   [THEME] 연속 상승 테마: 83개
   [SECTOR] 연속 상승 업종: 11개
   [RESULT] 동시 만족 종목: 51개
======================================================================
```

### 주요 연속 상승 테마 (상위 10개)
| 테마코드 | 테마명 | 평균등락율 |
|----------|--------|-----------|
| 0322 | 건설 중소형 | +9.58% |
| 0563 | 낙태/피임 | +8.49% |
| 0237 | GTX(수도권 광역급행철도) | +4.64% |
| 0154 | 건설 대표주 | +4.61% |
| 0197 | 폐기물처리 | +4.14% |
| 0159 | 자동차 대표주 | +3.82% |
| 0401 | 원자력발전소 해체 | +3.59% |
| 0323 | 셰일가스(Shale Gas) | +3.47% |
| 0205 | 원자력발전 | +3.38% |
| 0559 | 고체산화물 연료전지(SOFC) | +3.27% |

### 주요 연속 상승 업종
| 업종코드 | 업종명 | 총등락율 |
|----------|--------|----------|
| 307 | 건설 | +9.70% |
| 019 | 운수창고 | +6.17% |
| 531 | KRX 경기소비재 | +6.17% |
| 215 | KOSPI 우선주 | +4.70% |
| 028 | 부동산 | +1.88% |

### 동시 만족 종목 예시
- 건설주: KCC건설, KD, 서한, 동원개발 등
- 리츠: ESR켄달스퀘어리츠, KB스타리츠, SK리츠 등
- 해운/항공: 대한항공, 대한해운, 팬오션, 제주항공 등

---

## 결과 JSON 구조

```json
{
  "execution_time": "2025-12-05 14:03:01",
  "consecutive_days": 5,
  "api_call_count": 139,
  "summary": {
    "rising_themes_count": 83,
    "rising_sectors_count": 11,
    "matched_stocks_count": 51
  },
  "rising_themes": [
    {
      "tmcode": "0322",
      "tmname": "건설 중소형",
      "avgdiff": "9.58",
      "daily_changes": {
        "day1": 9.57,
        "day2": 15.04,
        "day3": 23.74,
        "day4": 24.74,
        "day5": 24.19
      }
    }
  ],
  "rising_sectors": [
    {
      "upcode": "307",
      "hname": "건설",
      "total_change": 9.70,
      "period_data": [...]
    }
  ],
  "matched_stocks": [
    {
      "종목코드": "021320",
      "종목명": "KCC건설",
      "시장구분": "코스닥",
      "매칭테마코드": ["0322"],
      "매칭테마명": ["건설 중소형"],
      "매칭업종코드": ["307"],
      "매칭업종명": ["건설"]
    }
  ]
}
```

---

## 사용 API

| API | Endpoint | 용도 | 핵심 파라미터 |
|-----|----------|------|--------------|
| t8425 | POST /stock/sector | 전체 테마 목록 | `dummy: ""` |
| t1533 | POST /stock/sector | 테마 N일 대비 등락 | `gubun: "7"`, `chgdate: 1~5` |
| t8424 | POST /indtp/market-data | 전체 업종 목록 | `gubun1: ""` |
| t1514 | POST /indtp/market-data | 업종 기간별 추이 | `gubun2: "1"`, `cnt: 5` |

---

## 환경 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정
`backend/.env` 파일에 LS증권 API 키 설정:
```
LS_APP_KEY=your_app_key
LS_APP_SECRET=your_app_secret
```

---

## 주의사항

1. **API 호출 제한**: Rate limit이 적용되어 있음 (기본 1초 딜레이, 5회마다 추가 2초)
2. **토큰 관리**: OAuth 토큰은 자동 발급됨
3. **종목 리스트**: `backend/ls_stock_list_final.json` 파일 필요
4. **실행 시간**: 전체 탐색 시 약 2-3분 소요 (API 호출 약 140회)
5. **기준일 제한**: `--base-date` 옵션은 업종(t1514)만 지원. 테마(t1533)는 항상 오늘 기준
6. **휴장일 처리**: 휴장일을 지정하면 가장 가까운 거래일 데이터가 조회됨

---

## 모듈 설명

### `ls_api_client.py`
LS증권 API 클라이언트. 토큰 발급, Rate Limiting, 재시도 로직 포함.

### `theme_finder.py`
테마(섹터) 연속 상승 탐색. t8425, t1533 API 사용.

### `sector_finder.py`
업종 연속 상승 탐색. t8424, t1514 API 사용.

### `stock_matcher.py`
조건 동시 만족 종목 매칭. 종목 리스트에서 테마/업종 코드 비교.

### `main.py`
메인 실행 파일. CLI 인터페이스 제공.

---

## 라이선스

내부 사용 목적
