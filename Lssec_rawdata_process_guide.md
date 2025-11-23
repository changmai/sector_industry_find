
````markdown
# 📘 LS증권 WebSocket Raw Data 처리 및 가공 가이드

## 1. 개요 (Overview)
본 문서는 LS증권 WebSocket API를 통해 수신된 **Raw Data(JSON 텍스트)**를 파싱하여, **실시간 틱(Tick) 리스트**와 **가격대별 누적 거래량(Footprint/Orderflow)** 차트를 구현하기 위한 데이터 처리 명세서입니다.

이 가이드는 Python(`main.py`, `data_worker.py`)으로 작성된 원본 소스 코드를 기반으로 작성되었으며, 타 언어(C#, JavaScript, C++ 등)로 이식할 때의 표준 로직을 정의합니다.

---

## 2. 데이터 흐름 (Data Architecture)

1.  **수신 (Ingest):** WebSocket 스트림을 통해 패킷 수신
2.  **로깅 (Log):** 수신된 JSON 패킷을 줄바꿈(`\n`) 단위로 `.txt` 파일에 Append (Raw Data 확보)
3.  **파싱 (Parse):** 텍스트 라인을 JSON 객체로 변환
4.  **정제 (Clean):** 문자열 데이터를 숫자형으로 변환 및 포맷팅
5.  **가공 (Process):** 매수/매도 판별 및 Footprint 집계 알고리즘 수행
6.  **표현 (Visualize):** UI 컴포넌트에 렌더링

---

## 3. Raw Data 구조 명세

저장된 텍스트 파일(`raw_data_*.txt`)은 **Newline Delimited JSON (NDJSON)** 형식을 따릅니다.

### 3.1 JSON 패킷 예시
```json
{
  "header": {
    "tr_cd": "S3_",
    "tr_key": "005930"
  },
  "body": {
    "chetime": "123143",
    "price": "96600",
    "cvolume": "5",
    "cgubun": "+",
    "volume": "11707848",
    "drate": "-1.23",
    "value": "1126294",
    "change": "1200",
    "opentime": "090015",
    "status": "00"
  }
}
````

### 3.2 핵심 필드 정의 (Key Fields Definition)

프로그램 구현 시 `body` 객체 내에서 반드시 추출해야 하는 필드입니다.

| 필드명 (Key) | 설명 | 데이터 타입 (Raw) | 변환 타입 | 비고 |
| :--- | :--- | :--- | :--- | :--- |
| **`tr_cd`** | 트랜잭션 코드 | String | String | Header에 위치. `S3_` (KOSPI 체결) 확인용 |
| **`chetime`** | 체결 시간 | String | String | `HHMMSS` 포맷 (예: `093000`) |
| **`price`** | 현재가 | String | **Int** | 콤마 없는 숫자 문자열 |
| **`cvolume`** | **순간 체결량** | String | **Int** | ⚠️ `volume`(누적)이 아닌 반드시 이 필드 사용 |
| **`cgubun`** | 체결 구분 | String | String | `+`: 매수, `-` 혹은 기타: 매도 |
| **`drate`** | 등락률 | String | Float | 참고용 (예: `-1.23`) |

-----

## 4\. 데이터 가공 로직 (Data Processing Logic)

### 4.1 파싱 및 형변환 (Parsing & Casting)

Raw Data는 기본적으로 모두 문자열(String)입니다. 산술 연산을 위해 반드시 형변환을 수행해야 합니다.

1.  **JSON 디코딩:** 텍스트 한 줄을 읽어 JSON 객체로 변환합니다.
2.  **유효성 검사:** `body`가 `null`이거나 비어있는지 확인합니다.
3.  **형변환:**
      * `price = Integer.parseInt(body["price"])`
      * `vol = Integer.parseInt(body["cvolume"])`
      * *예외 처리:* `price`가 `0`인 데이터(장전 데이터 등)는 무시합니다.

### 4.2 시간 포맷팅 (Time Formatting)

가독성을 위해 `HHMMSS` 문자열을 표준 시간 포맷으로 변환합니다.

  * **입력:** `"123143"` (6자리 문자열)
  * **로직:** `Slice(0,2)` : `Slice(2,4)` : `Slice(4,6)`
  * **출력:** `"12:31:43"`

### 4.3 매수/매도 사이드 결정 (Side Determination)

`cgubun` 필드를 통해 해당 체결이 \*\*매수 주도(Buy-initiated)\*\*인지 \*\*매도 주도(Sell-initiated)\*\*인지 판별합니다. 이는 차트의 색상을 결정하는 가장 중요한 로직입니다.

  * **매수 (Buy):** `cgubun == "+"`
  * **매도 (Sell):** `cgubun != "+"` (주로 `-` 혹은 파란색 처리)

-----

## 5\. 집계 알고리즘 (Aggregation Algorithm)

### 5.1 Footprint (누적 매물대) 계산

가격대별로 매수 체결량과 매도 체결량을 각각 누적하여 \*\*Delta(매수-매도 차이)\*\*를 계산하는 로직입니다.

**자료구조 예시 (Map/Dictionary):**

```json
{
  "96600": { "buy": 105, "sell": 20, "delta": 85 },
  "96500": { "buy": 50,  "sell": 90, "delta": -40 }
}
```

**업데이트 로직 (Pseudo-code):**

```python
function updateFootprint(price, volume, isBuy):
    // 1. 해당 가격의 행이 없으면 초기화
    if not dataMap.has(price):
        dataMap[price] = { buy: 0, sell: 0, delta: 0 }

    // 2. 매수/매도별 거래량 누적
    if isBuy:
        dataMap[price].buy += volume
    else:
        dataMap[price].sell += volume

    // 3. 델타(Delta) 재계산
    dataMap[price].delta = dataMap[price].buy - dataMap[price].sell
```

### 5.2 실시간 틱 리스트 관리

  * 새로운 데이터는 리스트의 \*\*최상단(Index 0)\*\*에 삽입합니다.
  * 메모리 관리를 위해 리스트의 최대 개수를 제한합니다 (권장: 500개).
  * 500개가 넘어가면 가장 오래된(마지막 인덱스) 데이터를 삭제합니다.

-----

## 6\. UI/UX 가이드라인 (Visualization)

제공된 파이썬 소스(`ui_widgets.py`)에서 추출한 시각화 표준입니다.

### 6.1 색상 팔레트 (Color Scheme)

어두운 배경(`Dark Mode`)을 기준으로 한 색상 코드입니다.

| 구분 | 역할 | HEX 코드 | 텍스트 색상명 |
| :--- | :--- | :--- | :--- |
| **매수 (Buy)** | 매수 체결가/체결량 강조 | `#ff6666` | Red / Light Red |
| **매도 (Sell)** | 매도 체결가/체결량 강조 | `#66b3ff` | Blue / Light Blue |
| **체결량 강조** | 순간 체결량 시인성 확보 | `#FFFF00` | Yellow |
| **배경색** | 전체 UI 배경 | `#1e1e1e` | Dark Gray |
| **델타 양수** | 매수 우세 | `#FF0000` | Red |
| **델타 음수** | 매도 우세 | `#0000FF` | Blue |

### 6.2 테이블 구성 제안

**Footprint 테이블 (좌측)**

  * 컬럼: [가격, 매도량, 매수량, 델타]
  * 정렬: 가격 내림차순 (높은 가격이 위로)
  * 특징: 델타값에 따라 폰트 색상 변경

**Tick 리스트 (우측)**

  * 컬럼: [시간, 가격, 구분, 체결량]
  * 정렬: 시간 내림차순 (최신 체결이 위로)
  * 특징: 체결량 컬럼은 노란색으로 강조하여 눈에 띄게 처리

-----

## 7\. 개발 체크리스트 (Checklist)

다른 언어 또는 환경에서 개발 시 다음 사항을 점검하십시오.

  - [ ] **JSON Parser:** 데이터 수신 시 `try-catch` 블록을 사용하여 JSON 파싱 에러로 인한 프로그램 중단을 방지했는가?
  - [ ] **Data Type:** `price`와 `cvolume`을 정수형(Int/Long)으로 올바르게 변환했는가?
  - [ ] **Volume Logic:** 누적 거래량(`volume`)과 순간 체결량(`cvolume`)을 혼동하지 않았는가?
  - [ ] **Encoding:** 텍스트 파일 읽기/쓰기 시 `UTF-8` 인코딩을 명시했는가?
  - [ ] **Keep-Alive:** WebSocket 연결 유지를 위해 PING/PONG 프레임 처리를 구현했는가? (LS증권은 PING 수신 시 PONG 전송 필요)

<!-- end list -->

```
```