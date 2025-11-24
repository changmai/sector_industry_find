# WEBSOCKET[기타] 실시간 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=6ad419a5-f0ce-47c2-a52a-91685fa86a31&api_id=eddd61f7-d595-4370-b9c3-49c4c6178096

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | wss://openapi.ls-sec.co.kr:9443   |
| 운영 도메인       | wss://openapi.ls-sec.co.kr:9443   |
| 모의투자 도메인     | wss://openapi.ls-sec.co.kr:29443  |
| URL          | /websocket                        |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 장운영정보  등 기타 정보를 실시간으로 확인할 수 있습니다. |


## 🏷️ 장운영정보 (JIF)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description                                  |
|:----------|:--------|:-------|:-----------|---------:|:---------------------------------------------|
| token     | 접근토큰    | String | Y          |     1000 | Access Token을 설정하기 위한 Header Parameter       |
| tr_type   | 거래 Type | String | Y          |        1 | 1: 계좌등록, 2: 계좌해제, 3: 실시간 시세 등록, 4: 실시간 시세 해제 |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                     |
|:----------|:------|:-------|:-----------|---------:|:------------------------------------------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드                                       |
| tr_key    | 단축코드  | String | N          |        8 | 단축코드 6자리 또는 8자리 (단건, 연속), (계좌등록/해제 일 경우 필수값 아님) |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드     |


### 응답 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|:----------|:------|:-------|:-----------|---------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| jangubun  | 장구분   | String | Y          |        1 | 1:코스피2:코스닥5:선물/옵션6:NXT전용8:KRX야간파생9:미국주식A:중국주식오전B:중국주식오후C:홍콩주식오전D:홍콩주식오후E:일본주식오전F:일본주식오후                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| jstatus   | 장상태   | String | Y          |        2 | 공통사용11:장전동시호가개시21:장시작22:장개시10초전23:장개시1분전24:장개시5분전25:장개시10분전31:장후동시호가개시41:장마감42:장마감10초전43:장마감1분전44:장마감5분전51:시간외종가매매개시52:시간외종가매매종료,시간외단일가매매개시53:사용안함54:시간외단일가매매종료55:프리마켓 개시A2:프리마켓 장개시,10초전A3:프리마켓 장개시,1분전A4:프리마켓 장개시,5분전A5:프리마켓 장개시,10분전56:에프터마켓 개시B2:에프터마켓 장개시,10초전B3:에프터마켓 장개시,1분전B4:에프터마켓 장개시,5분전B5:에프터마켓 장개시,10분전57:프리마켓 마감C2:프리마켓 장마감,10초전C3:프리마켓 장마감,1분전C4:프리마켓 장마감,5분전58:에프터마켓 마감D2:에프터마켓 장마감,10초전D3:에프터마켓 장마감,1분전D4:에프터마켓 장마감,5분전KOSPI / KOSDAQ (jangubun 1,2 인 경우)61:서킷브레이크1단계발동62:서킷브레이크1단계해제,호가접수개시63:서킷브레이크1단계,동시호가종료64:사이드카 매도발동65:사이드카 매도해제66:사이드카 매수발동67:사이드카 매수해제68:서킷브레이크2단계발동69:서킷브레이크3단계발동,당일 장종료70:서킷브레이크2단계해제,호가접수개시71:서킷브레이크2단계,동시호가종료선물/옵션 (jangubun 5인 경우)61:코스피관련파생상품,당일 장종료62:서킷브레이크 해제,호가접수개시63:서킷브레이크, 장중동시마감70:2단계상한가,5분 후 확대 예정71:2단계하한가,5분 후 확대 예정72:3단계상한가,5분 후 확대 예정73:3단계하한가,5분 후 확대 예정74:2단계상한가,확대 적용75:2단계하한가,확대 적용76:3단계상한가,확대 적용77:3단계하한가,확대 적용 |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "JIF",
  "tr_key": "0"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "JIF",
  "tr_key": "0"
 },
 "body": {
  "jangubun": "C",
  "jstatus": "21"
 }
}
```

---

## 🏷️ 실시간뉴스제목패킷 (NWS)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description                                  |
|:----------|:--------|:-------|:-----------|---------:|:---------------------------------------------|
| token     | 접근토큰    | String | Y          |     1000 | Access Token을 설정하기 위한 Header Parameter       |
| tr_type   | 거래 Type | String | Y          |        1 | 1: 계좌등록, 2: 계좌해제, 3: 실시간 시세 등록, 4: 실시간 시세 해제 |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                     |
|:----------|:------|:-------|:-----------|---------:|:------------------------------------------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드                                       |
| tr_key    | 단축코드  | String | N          |        8 | 단축코드 6자리 또는 8자리 (단건, 연속), (계좌등록/해제 일 경우 필수값 아님) |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드     |


### 응답 Body
| Element   | 한글명    | type   | Required   |   Length | Description   |
|:----------|:-------|:-------|:-----------|---------:|:--------------|
| date      | 날짜     | String | Y          |        8 |               |
| time      | 시간     | String | Y          |        6 |               |
| id        | 뉴스구분자  | String | Y          |        2 |               |
| realkey   | 키값     | String | Y          |       24 |               |
| title     | 제목     | String | Y          |      300 |               |
| code      | 단축종목코드 | String | Y          |      240 |               |
| bodysize  | BODY길이 | String | Y          |        8 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "NWS",
  "tr_key": "NWS001"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "NWS",
  "tr_key": "NWS001"
 },
 "body": {
  "date": "20230614",
  "code": "000000011810",
  "realkey": "202306140952172704000165",
  "bodysize": "4841",
  "time": "095217",
  "id": "27",
  "title": "STX, ‘2차전지 핵심’ 수산화리튬 사업 박차…中 영정리튬과 MOU"
 }
}
```

---
