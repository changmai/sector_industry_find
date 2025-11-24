# WEBSOCKET[업종] 실시간 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=f82999f4-eb1a-4ead-a0b1-a4386e8721ab&api_id=3c2b0280-6663-41e2-8995-a179de99e074

## 📌 기본 정보
| 항목           | 내용                               |
|:-------------|:---------------------------------|
| Method       | POST                             |
| Domain       | wss://openapi.ls-sec.co.kr:9443  |
| 운영 도메인       | wss://openapi.ls-sec.co.kr:9443  |
| 모의투자 도메인     | wss://openapi.ls-sec.co.kr:29443 |
| URL          | /websocket                       |
| Format       | JSON                             |
| Content-Type | application/json; charset=UTF-8  |
| Description  | 업종 관련 정보를 실시간으로 확인할 수 있습니다.      |


## 🏷️ 업종별투자자별매매현황 (BM_)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description                                  |
|:----------|:--------|:-------|:-----------|---------:|:---------------------------------------------|
| token     | 접근토큰    | String | Y          |     1000 | Access Token을 설정하기 위한 Header Parameter       |
| tr_type   | 거래 Type | String | Y          |        1 | 1: 계좌등록, 2: 계좌해제, 3: 실시간 시세 등록, 4: 실시간 시세 해제 |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                                                                                                                                            |
|:----------|:------|:-------|:-----------|---------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드                                                                                                                                                              |
| tr_key    | 단축코드  | String | N          |        3 | 001 : 코스피101 : KP200301 : 코스닥550 : ELW560 : ETF600 : 주식선물700 : 콜옵션800 : 풋옵션900 : 선물940 : 미니KP200선물941 : 미니KP200옵션-콜942 : 미니KP200옵션-풋946 : 코스피200위클리-콜947 : 코스피200위클리-풋 |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드     |


### 응답 Body
| Element   | 한글명         | type   | Required   |   Length | Description                                                 |
|:----------|:------------|:-------|:-----------|---------:|:------------------------------------------------------------|
| tjjcode   | 투자자코드       | String | Y          |        4 | 001:코스피101:KP200301:코스닥900:선  물700:콜옵션800:풋옵션550:ELW560:ETF |
| tjjtime   | 수신시간        | String | Y          |        8 |                                                             |
| msvolume  | 매수거래량       | String | Y          |        8 |                                                             |
| mdvolume  | 매도거래량       | String | Y          |        8 |                                                             |
| msvol     | 거래량순매수      | String | Y          |        8 |                                                             |
| p_msvol   | 거래량순매수직전대비  | String | Y          |        8 |                                                             |
| msvalue   | 매수거래대금      | String | Y          |        6 |                                                             |
| mdvalue   | 매도거래대금      | String | Y          |        6 |                                                             |
| msval     | 거래대금순매수     | String | Y          |        6 |                                                             |
| p_msval   | 거래대금순매수직전대비 | String | Y          |        6 |                                                             |
| upcode    | 업종코드        | String | Y          |        3 |                                                             |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "BM_",
  "tr_key": "001"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "BM_",
  "tr_key": "001"
 },
 "body": {
  "p_msval": "21",
  "tjjtime": "09510000",
  "p_msvol": "123",
  "mdvalue": "54037",
  "msvolume": "236487",
  "upcode": "001",
  "tjjcode": "9999",
  "msvalue": "53764",
  "mdvolume": "241626",
  "msvol": "-5139",
  "msval": "-273"
 }
}
```

---
