# WEBSOCKET[선물/옵션] 실시간 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=2f1eea77-5606-4512-93c6-31b21d2ece90&api_id=57936c91-b49d-4702-b7f6-3935c6859462

## 📌 기본 정보
| 항목           | 내용                                      |
|:-------------|:----------------------------------------|
| Method       | POST                                    |
| Domain       | wss://openapi.ls-sec.co.kr:9443         |
| 운영 도메인       | wss://openapi.ls-sec.co.kr:9443         |
| 모의투자 도메인     | wss://openapi.ls-sec.co.kr:29443        |
| URL          | /websocket                              |
| Format       | JSON                                    |
| Content-Type | application/json; charset=UTF-8         |
| Description  | 선물옵션 주문현황 및 시세, 투자정보를 실시간으로 확인할 수 있습니다. |


## 🏷️ 선물주문체결 (C01)
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
| Element    | 한글명         | type   | Required   |   Length | Description   |
|:-----------|:------------|:-------|:-----------|---------:|:--------------|
| lineseq    | 라인일련번호      | String | Y          |     10   |               |
| accno      | 계좌번호        | String | Y          |     11   |               |
| user       | 조작자ID       | String | Y          |      8   |               |
| seq        | 일련번호        | String | Y          |     11   |               |
| trcode     | trcode      | String | Y          |     11   |               |
| megrpno    | 매칭그룹번호      | String | Y          |      2   |               |
| boardid    | 보드ID        | String | Y          |      2   |               |
| memberno   | 회원번호        | String | Y          |      5   |               |
| bpno       | 지점번호        | String | Y          |      5   |               |
| ordno      | 주문번호        | String | Y          |     10   |               |
| ordordno   | 원주문번호       | String | Y          |     10   |               |
| expcode    | 종목코드        | String | Y          |     12   |               |
| yakseq     | 약정번호        | String | Y          |     11   |               |
| cheprice   | 체결가격        | String | Y          |     11.2 |               |
| chevol     | 체결수량        | String | Y          |     10   |               |
| sessionid  | 세션ID        | String | Y          |      2   |               |
| chedate    | 체결일자        | String | Y          |      8   |               |
| chetime    | 체결시각        | String | Y          |      9   |               |
| spdprc1    | 최근월체결가격     | String | Y          |     11.2 |               |
| spdprc2    | 차근월체결가격     | String | Y          |     11.2 |               |
| dosugb     | 매도수구분       | String | Y          |      1   |               |
| accno1     | 계좌번호1       | String | Y          |     12   |               |
| sihogagb   | 시장조성호가구분    | String | Y          |      1   |               |
| jakino     | 위탁사번호       | String | Y          |      5   |               |
| daeyong    | 대용주권계좌번호    | String | Y          |     12   |               |
| mem_filler | mem_filler  | String | Y          |      7   |               |
| mem_accno  | mem_accno   | String | Y          |     11   |               |
| mem_filler | mem_filler1 | String | Y          |     42   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQ1Mzk5OTczLTcxYjctNGE0OC1iM2M3LWQzNzBkNjZhNGZmOCIsIm5iZiI6MTY4NjcyNTUzNSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2Nzc5OTk5LCJpYXQiOjE2ODY3MjU1MzUsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.N8F9oFC_jQRfnGTy3VeaZyraU5Bs70_XeC3ZEP1Qvh6wewHfbWVgbpYMGJ21UTXWGcMSbW_D9HrH1Aa8xep9YA",
  "tr_type": "1"
 },
 "body": {
  "tr_cd": "C01",
  "tr_key": ""
 }
}
```

### 💡 Response Example
```json
{
 "header":{
  "tr_cd":"C01"
 },
  "body":{
  "accno":"20277932702",
  "mem_filler":"",
  "accno1":"20277932702",
  "sessionid":"40",
  "sihogagb":"0",
  "trcode":"TTRTDP21301",
  "megrpno":"00",
  "memberno":"06300",
  "spdprc1":"0",
  "boardid":"G1",
  "spdprc2":"0",
  "seq":"247184",
  "yakseq":"00000099230",
  "lineseq":"100247184",
  "bpno":"00555",
  "chevol":"1",
  "daeyong":"",
  "chetime":"140833807",
  "chedate":"20240118",
  "ordno":"0000034881",
  "expcode":"KR4101V30005",
  "mem_accno":"20277932702",
  "cheprice":"327.65",
  "jakino":"",
  "user":"",
  "dosugb":"2",
  "ordordno":"0000000000"
 }
}
```

---

## 🏷️ 상품선물실시간상하한가 (CD0)
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
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| gubun         | 접속매매여부    | String | Y          |      1   |               |
| dy_gubun      | 실시간가격제한여부 | String | Y          |      1   |               |
| dy_uplmtprice | 실시간상한가    | String | Y          |      8.2 |               |
| dy_dnlmtprice | 실시간하한가    | String | Y          |      8.2 |               |
| futcode       | 단축코드      | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "CD0",
  "tr_key": "165T6000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "CD0",
  "tr_key": "165T6000"
 },
 "body": {
  "futcode": "165T6000",
  "dy_gubun": "1",
  "dy_uplmtprice": "104.56",
  "dy_dnlmtprice": "103.52",
  "gubun": ""
 }
}
```

---

## 🏷️ KOSPI200선물체결 (FC0)
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
| Element     | 한글명        | type   | Required   |   Length | Description   |
|:------------|:-----------|:-------|:-----------|---------:|:--------------|
| chetime     | 체결시간       | String | Y          |      6   |               |
| sign        | 전일대비구분     | String | Y          |      1   |               |
| change      | 전일대비       | String | Y          |      6.2 |               |
| drate       | 등락율        | String | Y          |      6.2 |               |
| price       | 현재가        | String | Y          |      6.2 |               |
| open        | 시가         | String | Y          |      6.2 |               |
| high        | 고가         | String | Y          |      6.2 |               |
| low         | 저가         | String | Y          |      6.2 |               |
| cgubun      | 체결구분       | String | Y          |      1   |               |
| cvolume     | 체결량        | String | Y          |      6   |               |
| volume      | 누적거래량      | String | Y          |     12   |               |
| value       | 누적거래대금     | String | Y          |     12   |               |
| mdvolume    | 매도누적체결량    | String | Y          |     12   |               |
| mdchecnt    | 매도누적체결건수   | String | Y          |      8   |               |
| msvolume    | 매수누적체결량    | String | Y          |     12   |               |
| mschecnt    | 매수누적체결건수   | String | Y          |      8   |               |
| cpower      | 체결강도       | String | Y          |      9.2 |               |
| offerho1    | 매도호가1      | String | Y          |      6.2 |               |
| bidho1      | 매수호가1      | String | Y          |      6.2 |               |
| openyak     | 미결제약정수량    | String | Y          |      8   |               |
| k200jisu    | KOSPI200지수 | String | Y          |      6.2 |               |
| theoryprice | 이론가        | String | Y          |      6.2 |               |
| kasis       | 괴리율        | String | Y          |      6.2 |               |
| sbasis      | 시장BASIS    | String | Y          |      6.2 |               |
| ibasis      | 이론BASIS    | String | Y          |      6.2 |               |
| openyakcha  | 미결제약정증감    | String | Y          |      8   |               |
| jgubun      | 장운영정보      | String | Y          |      2   |               |
| jnilvolume  | 전일동시간대거래량  | String | Y          |     12   |               |
| futcode     | 단축코드       | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "FC0",
  "tr_key": "101T9000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "FC0",
  "tr_key": "101T9000"
 },
 "body": {
  "futcode": "101T9000",
  "mdchecnt": "10849",
  "sign": "5",
  "mschecnt": "10759",
  "ibasis": "2.23",
  "mdvolume": "24994",
  "cpower": "102.07",
  "cvolume": "3",
  "high": "348.55",
  "low": "346.50",
  "price": "347.80",
  "kasis": "-0.18",
  "cgubun": "+",
  "bidho1": "347.75",
  "k200jisu": "346.18",
  "value": "4516509",
  "offerho1": "347.80",
  "jgubun": "40",
  "change": "0.60",
  "chetime": "093621",
  "openyak": "281563",
  "volume": "51968",
  "drate": "-0.17",
  "openyakcha": "3853",
  "jnilvolume": "41625",
  "msvolume": "25511",
  "sbasis": "1.62",
  "theoryprice": "348.41",
  "open": "348.30"
 }
}
```

---

## 🏷️ KOSPI200선물실시간상하한가 (FD0)
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
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| gubun         | 접속매매여부    | String | Y          |      1   |               |
| dy_gubun      | 실시간가격제한여부 | String | Y          |      1   |               |
| dy_uplmtprice | 실시간상한가    | String | Y          |      8.2 |               |
| dy_dnlmtprice | 실시간하한가    | String | Y          |      8.2 |               |
| futcode       | 단축코드      | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "FD0",
  "tr_key": "101T9000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "FD0",
  "tr_key": "101T9000"
 },
 "body": {
  "futcode": "101T9000",
  "dy_gubun": "1",
  "dy_uplmtprice": "351.25",
  "dy_dnlmtprice": "344.35",
  "gubun": ""
 }
}
```

---

## 🏷️ KOSPI200선물호가 (FH0)
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
| Element     | 한글명     | type   | Required   |   Length | Description   |
|:------------|:--------|:-------|:-----------|---------:|:--------------|
| hotime      | 호가시간    | String | Y          |      6   |               |
| offerho1    | 매도호가1   | String | Y          |      6.2 |               |
| bidho1      | 매수호가1   | String | Y          |      6.2 |               |
| offerrem1   | 매도호가수량1 | String | Y          |      6   |               |
| bidrem1     | 매수호가수량1 | String | Y          |      6   |               |
| offercnt1   | 매도호가건수1 | String | Y          |      5   |               |
| bidcnt1     | 매수호가건수1 | String | Y          |      5   |               |
| offerho2    | 매도호가2   | String | Y          |      6.2 |               |
| bidho2      | 매수호가2   | String | Y          |      6.2 |               |
| offerrem2   | 매도호가수량2 | String | Y          |      6   |               |
| bidrem2     | 매수호가수량2 | String | Y          |      6   |               |
| offercnt2   | 매도호가건수2 | String | Y          |      5   |               |
| bidcnt2     | 매수호가건수2 | String | Y          |      5   |               |
| offerho3    | 매도호가3   | String | Y          |      6.2 |               |
| bidho3      | 매수호가3   | String | Y          |      6.2 |               |
| offerrem3   | 매도호가수량3 | String | Y          |      6   |               |
| bidrem3     | 매수호가수량3 | String | Y          |      6   |               |
| offercnt3   | 매도호가건수3 | String | Y          |      5   |               |
| bidcnt3     | 매수호가건수3 | String | Y          |      5   |               |
| offerho4    | 매도호가4   | String | Y          |      6.2 |               |
| bidho4      | 매수호가4   | String | Y          |      6.2 |               |
| offerrem4   | 매도호가수량4 | String | Y          |      6   |               |
| bidrem4     | 매수호가수량4 | String | Y          |      6   |               |
| offercnt4   | 매도호가건수4 | String | Y          |      5   |               |
| bidcnt4     | 매수호가건수4 | String | Y          |      5   |               |
| offerho5    | 매도호가5   | String | Y          |      6.2 |               |
| bidho5      | 매수호가5   | String | Y          |      6.2 |               |
| offerrem5   | 매도호가수량5 | String | Y          |      6   |               |
| bidrem5     | 매수호가수량5 | String | Y          |      6   |               |
| offercnt5   | 매도호가건수5 | String | Y          |      5   |               |
| bidcnt5     | 매수호가건수5 | String | Y          |      5   |               |
| totofferrem | 매도호가총수량 | String | Y          |      6   |               |
| totbidrem   | 매수호가총수량 | String | Y          |      6   |               |
| totoffercnt | 매도호가총건수 | String | Y          |      5   |               |
| totbidcnt   | 매수호가총건수 | String | Y          |      5   |               |
| futcode     | 단축코드    | String | Y          |      8   |               |
| danhochk    | 단일가호가여부 | String | Y          |      1   |               |
| alloc_gubun | 배분적용구분  | String | Y          |      1   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "FH0",
  "tr_key": "101T9000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "FH0",
  "tr_key": "101T9000"
 },
 "body": {
  "offerrem2": "179",
  "offerho4": "347.85",
  "bidho5": "347.45",
  "offerho3": "347.80",
  "offerrem3": "176",
  "bidho4": "347.50",
  "futcode": "101T9000",
  "offerrem4": "165",
  "offerho5": "347.90",
  "offerrem5": "200",
  "offerrem1": "76",
  "totoffercnt": "2350",
  "totbidcnt": "2119",
  "bidrem3": "200",
  "bidrem4": "195",
  "bidrem1": "116",
  "bidrem2": "222",
  "bidcnt5": "51",
  "bidcnt4": "71",
  "bidcnt3": "49",
  "bidcnt2": "67",
  "bidcnt1": "55",
  "danhochk": "0",
  "bidho1": "347.65",
  "hotime": "093559",
  "offerho2": "347.75",
  "bidho3": "347.55",
  "bidrem5": "274",
  "offerho1": "347.70",
  "bidho2": "347.60",
  "offercnt5": "43",
  "offercnt3": "48",
  "offercnt4": "38",
  "offercnt1": "28",
  "offercnt2": "55",
  "alloc_gubun": "",
  "totofferrem": "15719",
  "totbidrem": "13071"
 }
}
```

---

## 🏷️ KOSPI200선물가격제한폭확대 (FX0)
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
| Element    | 한글명    | type   | Required   |   Length | Description   |
|:-----------|:-------|:-------|:-----------|---------:|:--------------|
| upstep     | 적용상한단계 | String | Y          |      2   |               |
| dnstep     | 적용하한단계 | String | Y          |      2   |               |
| uplmtprice | 적용상한가  | String | Y          |      6.2 |               |
| dnlmtprice | 적용하한가  | String | Y          |      6.2 |               |
| futcode    | 단축코드   | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQyNjA1YWEzLTA2YzEtNDliNi04ZmRjLTVmNjU1ZTQ1MTE2MiIsIm5iZiI6MTY4Njc4MjU0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2ODY2Mzk5LCJpYXQiOjE2ODY3ODI1NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.BRwxcX00HeeQKW_2MEAcBqk3ZkfLdDfg5WDv17U5X-kYIiudsdLpfkZ0Fo0B8mcTN_NlJuXXhdw6449-8okFYQ",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "FX0",
  "tr_key": "101T9000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "FX0",
  "tr_key": "101T9000"
 },
 "body": {
  "upstep": "01",
  "futcode": "101T9000",
  "uplmtprice": "3.86",
  "dnstep": "02",
  "dnlmtprice": "3.04"
 }
}
```

---

## 🏷️ 선물주문정정취소 (H01)
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


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjU1ZjEzNjI2LWRlYWEtNDE2OC05YTkxLTU4YzZjOTc5MDFiNyIsIm5iZiI6MTY4NzM5MDg0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg3NDcxMTk5LCJpYXQiOjE2ODczOTA4NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.wLgwwPtFK1jG3LlmJBd5wX_2NSUa_t8WQT1wmpIiUu1HHyq50181R8Bs2GIruxp88dp4oHH-2j3xlFUIkbPKdg",
  "tr_type": "1"
 },
 "body": {
  "tr_cd": "H01",
  "tr_key": ""
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "H01"
 },
 "body": {
  "creditcode": "10",
  "orddate": "20230622",
  "prgordde": "1",
  "accno": "20277932702",
  "macid": "000000000000",
  "mem_filler": "nmdkxjq",
  "accno1": "020277932702",
  "qty2": "5",
  "sihogagb": "00000000000",
  "trcode": "TTRODP11321",
  "megrpno": "01",
  "ordacpttm": "131635762",
  "substocnum": "",
  "memberno": "00063",
  "mocagb": "1",
  "price": "9999.99",
  "boardid": "99",
  "accgb": "31",
  "rcvtime": "131635750",
  "jakigb": "11",
  "treaid": "0",
  "seq": "1",
  "lineseq": "600000001",
  "rejcode": "0201",
  "bpno": "00100",
  "autogb": "0",
  "medcode": "4",
  "treacode": "0",
  "askcode": "00",
  "ptgb": "00",
  "ordgb": "2",
  "ordid": "010130001138",
  "trustnum": "",
  "nationcode": "410",
  "accmarggb": "10",
  "ordno": "0000069102",
  "qty": "0",
  "hogagb": "0",
  "forecode": "00",
  "expcode": "999999999999",
  "investgb": "8000",
  "mem_accno": "20277932702",
  "user": "",
  "dosugb": "2",
  "ordordno": ""
 }
}
```

---

## 🏷️ 주식선물체결 (JC0)
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
| Element     | 한글명        | type   | Required   |   Length | Description   |
|:------------|:-----------|:-------|:-----------|---------:|:--------------|
| futcode     | 단축코드       | String | Y          |      8   |               |
| chetime     | 체결시간       | String | Y          |      6   |               |
| sign        | 대비기호       | String | Y          |      1   |               |
| change      | 전일대비       | String | Y          |     10   |               |
| drate       | 등락율        | String | Y          |      6.2 |               |
| price       | 현재가        | String | Y          |     10   |               |
| open        | 시가         | String | Y          |     10   |               |
| high        | 고가         | String | Y          |     10   |               |
| low         | 저가         | String | Y          |     10   |               |
| cgubun      | 체결구분       | String | Y          |      1   |               |
| cvolume     | 체결량        | String | Y          |      6   |               |
| volume      | 누적거래량      | String | Y          |     12   |               |
| value       | 누적거래대금     | String | Y          |     15   |               |
| mdvolume    | 매도누적체결량    | String | Y          |     12   |               |
| mdchecnt    | 매도누적체결건수   | String | Y          |      8   |               |
| msvolume    | 매수누적체결량    | String | Y          |     12   |               |
| mschecnt    | 매수누적체결건수   | String | Y          |      8   |               |
| cpower      | 체결강도       | String | Y          |      9.2 |               |
| offerho1    | 매도호가1      | String | Y          |     10   |               |
| bidho1      | 매수호가1      | String | Y          |     10   |               |
| openyak     | 미결제약정수량    | String | Y          |      8   |               |
| k200jisu    | KOSPI200지수 | String | Y          |      6.2 |               |
| theoryprice | 이론가        | String | Y          |      8   |               |
| kasis       | 괴리율        | String | Y          |      6.3 |               |
| sbasis      | 시장BASIS    | String | Y          |      6   |               |
| ibasis      | 이론BASIS    | String | Y          |      6   |               |
| openyakcha  | 미결제약정증감    | String | Y          |      8   |               |
| jgubun      | 장운영정보      | String | Y          |      2   |               |
| jnilvolume  | 전일동시간대거래량  | String | Y          |     12   |               |
| basprice    | 기초자산현재가    | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "JC0",
  "tr_key": "111T7000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "JC0",
  "tr_key": "111T7000"
 },
 "body": {
  "futcode": "111T7000",
  "mdchecnt": "2375",
  "sign": "5",
  "mschecnt": "2374",
  "ibasis": "-141",
  "mdvolume": "500063",
  "cpower": "88.61",
  "cvolume": "1",
  "high": "72200",
  "low": "71100",
  "price": "71700",
  "kasis": "0.196",
  "cgubun": "+",
  "bidho1": "71600",
  "k200jisu": "1700.00",
  "value": "674790018",
  "offerho1": "71700",
  "jgubun": "40",
  "change": "400",
  "chetime": "143128",
  "openyak": "1144428",
  "volume": "944036",
  "drate": "-0.55",
  "openyakcha": "4612",
  "jnilvolume": "725849",
  "msvolume": "443085",
  "basprice": "71700",
  "sbasis": "0",
  "theoryprice": "71559",
  "open": "72200"
 }
}
```

---

## 🏷️ 주식선물실시간상하한가 (JD0)
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
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| gubun         | 접속매매여부    | String | Y          |        1 |               |
| dy_gubun      | 실시간가격제한여부 | String | Y          |        1 |               |
| dy_uplmtprice | 실시간상한가    | String | Y          |       10 |               |
| dy_dnlmtprice | 실시간하한가    | String | Y          |       10 |               |
| futcode       | 단축코드      | String | Y          |        8 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "JD0",
  "tr_key": "111T7000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "JD0",
  "tr_key": "111T7000"
 },
 "body": {
  "futcode": "111T7000",
  "dy_gubun": "1",
  "dy_uplmtprice": "73700",
  "dy_dnlmtprice": "69500",
  "gubun": ""
 }
}
```

---

## 🏷️ 주식선물호가 (JH0)
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
| Element     | 한글명      | type   | Required   |   Length | Description   |
|:------------|:---------|:-------|:-----------|---------:|:--------------|
| futcode     | 단축코드     | String | Y          |        8 |               |
| hotime      | 호가시간     | String | Y          |        6 |               |
| offerho1    | 매도호가1    | String | Y          |       10 |               |
| bidho1      | 매수호가1    | String | Y          |       10 |               |
| offerrem1   | 매도호가수량1  | String | Y          |        7 |               |
| bidrem1     | 매수호가수량1  | String | Y          |        7 |               |
| offercnt1   | 매도호가건수1  | String | Y          |        5 |               |
| bidcnt1     | 매수호가건수1  | String | Y          |        5 |               |
| offerho2    | 매도호가2    | String | Y          |       10 |               |
| bidho2      | 매수호가2    | String | Y          |       10 |               |
| offerrem2   | 매도호가수량2  | String | Y          |        7 |               |
| bidrem2     | 매수호가수량2  | String | Y          |        7 |               |
| offercnt2   | 매도호가건수2  | String | Y          |        5 |               |
| bidcnt2     | 매수호가건수2  | String | Y          |        5 |               |
| offerho3    | 매도호가3    | String | Y          |       10 |               |
| bidho3      | 매수호가3    | String | Y          |       10 |               |
| offerrem3   | 매도호가수량3  | String | Y          |        7 |               |
| bidrem3     | 매수호가수량3  | String | Y          |        7 |               |
| offercnt3   | 매도호가건수3  | String | Y          |        5 |               |
| bidcnt3     | 매수호가건수3  | String | Y          |        5 |               |
| offerho4    | 매도호가4    | String | Y          |       10 |               |
| bidho4      | 매수호가4    | String | Y          |       10 |               |
| offerrem4   | 매도호가수량4  | String | Y          |        7 |               |
| bidrem4     | 매수호가수량4  | String | Y          |        7 |               |
| offercnt4   | 매도호가건수4  | String | Y          |        5 |               |
| bidcnt4     | 매수호가건수4  | String | Y          |        5 |               |
| offerho5    | 매도호가5    | String | Y          |       10 |               |
| bidho5      | 매수호가5    | String | Y          |       10 |               |
| offerrem5   | 매도호가수량5  | String | Y          |        7 |               |
| bidrem5     | 매수호가수량5  | String | Y          |        7 |               |
| offercnt5   | 매도호가건수5  | String | Y          |        5 |               |
| bidcnt5     | 매수호가건수5  | String | Y          |        5 |               |
| offerho6    | 매도호가6    | String | Y          |       10 |               |
| bidho6      | 매수호가6    | String | Y          |       10 |               |
| offerrem6   | 매도호가수량6  | String | Y          |        7 |               |
| bidrem6     | 매수호가수량6  | String | Y          |        7 |               |
| offercnt6   | 매도호가건수6  | String | Y          |        5 |               |
| bidcnt6     | 매수호가건수6  | String | Y          |        5 |               |
| offerho7    | 매도호가7    | String | Y          |       10 |               |
| bidho7      | 매수호가7    | String | Y          |       10 |               |
| offerrem7   | 매도호가수량7  | String | Y          |        7 |               |
| bidrem7     | 매수호가수량7  | String | Y          |        7 |               |
| offercnt7   | 매도호가건수7  | String | Y          |        5 |               |
| bidcnt7     | 매수호가건수7  | String | Y          |        5 |               |
| offerho8    | 매도호가8    | String | Y          |       10 |               |
| bidho8      | 매수호가8    | String | Y          |       10 |               |
| offerrem8   | 매도호가수량8  | String | Y          |        7 |               |
| bidrem8     | 매수호가수량8  | String | Y          |        7 |               |
| offercnt8   | 매도호가건수8  | String | Y          |        5 |               |
| bidcnt8     | 매수호가건수8  | String | Y          |        5 |               |
| offerho9    | 매도호가9    | String | Y          |       10 |               |
| bidho9      | 매수호가9    | String | Y          |       10 |               |
| offerrem9   | 매도호가수량9  | String | Y          |        7 |               |
| bidrem9     | 매수호가수량9  | String | Y          |        7 |               |
| offercnt9   | 매도호가건수9  | String | Y          |        5 |               |
| bidcnt9     | 매수호가건수9  | String | Y          |        5 |               |
| offerho10   | 매도호가10   | String | Y          |       10 |               |
| bidho10     | 매수호가10   | String | Y          |       10 |               |
| offerrem10  | 매도호가수량10 | String | Y          |        7 |               |
| bidrem10    | 매수호가수량10 | String | Y          |        7 |               |
| offercnt10  | 매도호가건수10 | String | Y          |        5 |               |
| bidcnt10    | 매수호가건수10 | String | Y          |        5 |               |
| totofferrem | 매도호가총수량  | String | Y          |        8 |               |
| totbidrem   | 매수호가총수량  | String | Y          |        8 |               |
| totoffercnt | 매도호가총건수  | String | Y          |        5 |               |
| totbidcnt   | 매수호가총건수  | String | Y          |        5 |               |
| danhochk    | 단일가호가여부  | String | Y          |        1 |               |
| alloc_gubun | 배분적용구분   | String | Y          |        1 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "JH0",
  "tr_key": "111T7000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "JH0",
  "tr_key": "111T7000"
 },
 "body": {
  "offerho4": "72000",
  "futcode": "111T7000",
  "offerho3": "71900",
  "offerho6": "72200",
  "offerho5": "72100",
  "offerho8": "72400",
  "offerho7": "72300",
  "offerho9": "72500",
  "bidcnt10": "36",
  "bidcnt9": "41",
  "bidcnt8": "42",
  "bidcnt7": "92",
  "bidcnt6": "82",
  "bidcnt5": "92",
  "bidcnt4": "57",
  "bidcnt3": "68",
  "bidcnt2": "57",
  "bidcnt1": "40",
  "danhochk": "0",
  "hotime": "143130",
  "offerho2": "71800",
  "offerho1": "71700",
  "offercnt9": "38",
  "offercnt7": "42",
  "offercnt8": "43",
  "offercnt5": "64",
  "offercnt6": "57",
  "offercnt3": "84",
  "offercnt4": "76",
  "offercnt1": "38",
  "offercnt2": "101",
  "offerho10": "72600",
  "offercnt10": "28",
  "totofferrem": "267689",
  "totbidrem": "231253",
  "offerrem2": "27856",
  "bidho5": "71200",
  "offerrem3": "33820",
  "bidho4": "71300",
  "offerrem4": "30908",
  "bidho7": "71000",
  "offerrem5": "20042",
  "bidho6": "71100",
  "bidho9": "70800",
  "bidho8": "70900",
  "offerrem1": "13361",
  "totoffercnt": "843",
  "offerrem6": "10994",
  "totbidcnt": "796",
  "offerrem7": "9785",
  "offerrem8": "9703",
  "offerrem9": "9019",
  "bidrem3": "21544",
  "bidrem4": "21879",
  "bidrem1": "8245",
  "bidrem2": "23580",
  "bidrem9": "14890",
  "bidho1": "71600",
  "bidrem7": "18123",
  "bidrem8": "14104",
  "bidho3": "71400",
  "bidrem5": "17781",
  "bidho2": "71500",
  "bidrem6": "19349",
  "bidrem10": "13765",
  "bidho10": "70700",
  "alloc_gubun": "",
  "offerrem10": "7281"
 }
}
```

---

## 🏷️ 주식선물가격제한폭확대 (JX0)
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
| Element    | 한글명    | type   | Required   |   Length | Description   |
|:-----------|:-------|:-------|:-----------|---------:|:--------------|
| upstep     | 적용상한단계 | String | Y          |        2 |               |
| dnstep     | 적용하한단계 | String | Y          |        2 |               |
| uplmtprice | 적용상한가  | String | Y          |       10 |               |
| dnlmtprice | 적용하한가  | String | Y          |       10 |               |
| futcode    | 단축코드   | String | Y          |        8 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "JX0",
  "tr_key": "111T7000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "JX0",
  "tr_key": "111T7000"
 },
 "body": {
  "upstep": "02",
  "futcode": "111T7000",
  "uplmtprice": "2000000",
  "dnstep": "02",
  "dnlmtprice": "1000000"
 }
}
```

---

## 🏷️ 선물접수 (O01)
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


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQ1Mzk5OTczLTcxYjctNGE0OC1iM2M3LWQzNzBkNjZhNGZmOCIsIm5iZiI6MTY4NjcyNTUzNSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2Nzc5OTk5LCJpYXQiOjE2ODY3MjU1MzUsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.N8F9oFC_jQRfnGTy3VeaZyraU5Bs70_XeC3ZEP1Qvh6wewHfbWVgbpYMGJ21UTXWGcMSbW_D9HrH1Aa8xep9YA",
  "tr_type": "1"
 },
 "body": {
  "tr_cd": "O01",
  "tr_key": ""
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "O01"
 },
 "body": {
  "grpId": "",
  "execprc2": "0.00",
  "execprc1": "0.00",
  "trchno": "0000000000",
  "acntno": "20277932702",
  "fnoIsuptntp": "F",
  "acntnm": "충조감",
  "trcode": "SONBT001",
  "userid": "nmdkxjq",
  "fnobalevaltp": "2",
  "avrprc_2": "0.00",
  "avrprc_1": "0.00",
  "fnotrdunitamt": "250000.00000000",
  "len": "1106",
  "mgn": "95153175",
  "Itemno": "0000000000",
  "opdrtnno": "",
  "cont": "N",
  "allexecamt2": "0",
  "allexecamt1": "0",
  "compress": "0",
  "execprc": "0.00",
  "trxtime": "160237860",
  "gubun": "B",
  "trid": "2100160237197832",
  "mnyordableamt": "214924025",
  "varmsglen": "0",
  "ordno": "69039",
  "bnstp_2": "",
  "bnstp_1": "",
  "trsrc": "L",
  "fnoIsuno_1": "",
  "hogatype": "00",
  "reqcnt": " ",
  "mmgb": "03",
  "strtgcode": "",
  "lqdtqty2": "0",
  "fnoIsuno_2": "",
  "ordseqno": "0000000000",
  "bnstp2": "",
  "bnstp1": "",
  "lastqty": "0",
  "encrypt": "0",
  "ftsubtdsgnamt": "0",
  "acntno1": "",
  "contkey": "0",
  "fnoIsuno1": "",
  "mnymgn": "47576586",
  "fnoIsuno2": "",
  "seq": "000000194",
  "lineseq": "300000003",
  "peeamtcode": "40",
  "varlen": "50",
  "dps": "262500611",
  "fnoIsunm": "F 202306",
  "newqty": "0",
  "userId": "nmdkxjq",
  "fnoIsuno": "101T6000",
  "mrctp": "0",
  "isuno": "KR4101T60006",
  "firmno": "063",
  "filler": "",
  "prntordno": "000",
  "orgordno1": "000",
  "pubip": "010130001138",
  "prvip": "",
  "funckey": "C",
  "accno": "20277932702",
  "compreq": "0",
  "ctrcttime": "",
  "orgordmrcqty": "0",
  "termno": "",
  "qdtqty1": "0",
  "bpno": "000",
  "mgempno": "30207",
  "offset": "212",
  "trcode1": "FO01",
  "varhdlen": "0",
  "ifinfo": "",
  "lallexecqty": "0",
  "pdgrpcode": "01",
  "ptflno": "0000000000",
  "bnsplamt": "0",
  "eventid": "",
  "lqdtableqty_1": "0",
  "pcbpno": "000",
  "lqdtableqty_2": "0",
  "orgordno": "0",
  "brnno": "100",
  "ifid": "000",
  "media": "HT",
  "filler1": "",
  "orgordunercqty": "0",
  "ordno1": "000",
  "rjtcode": "",
  "commdacode": "40",
  "newqty1": "0",
  "newqty2": "0",
  "proctm": "160237872",
  "prntordno1": "0",
  "lang": "K",
  "unercqty": "5",
  "allexecamt": "0",
  "execqty": "0",
  "qdtqty": "0",
  "bskno": "0000000000",
  "ctrctno": "0000000000",
  "ordqty": "5",
  "outgu": "1",
  "msgcode": "9999",
  "ordableamt": "167347436",
  "ordmktcode": "40",
  "mrccnfqty": "0",
  "comid": "063",
  "bnstp": "2",
  "unsttqty_2": "0",
  "user": "nmdkxjq",
  "unsttqty_1": "0",
  "ordprc": "342.25"
 }
}
```

---

## 🏷️ KOSPI200옵션체결 (OC0)
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
| Element     | 한글명        | type   | Required   |   Length | Description   |
|:------------|:-----------|:-------|:-----------|---------:|:--------------|
| chetime     | 체결시간       | String | Y          |      6   |               |
| sign        | 전일대비구분     | String | Y          |      1   |               |
| change      | 전일대비       | String | Y          |      6.2 |               |
| drate       | 등락율        | String | Y          |      6.2 |               |
| price       | 현재가        | String | Y          |      6.2 |               |
| open        | 시가         | String | Y          |      6.2 |               |
| high        | 고가         | String | Y          |      6.2 |               |
| low         | 저가         | String | Y          |      6.2 |               |
| cgubun      | 체결구분       | String | Y          |      1   |               |
| cvolume     | 체결량        | String | Y          |      6   |               |
| volume      | 누적거래량      | String | Y          |     12   |               |
| value       | 누적거래대금     | String | Y          |     12   |               |
| mdvolume    | 매도누적체결량    | String | Y          |     12   |               |
| mdchecnt    | 매도누적체결건수   | String | Y          |      8   |               |
| msvolume    | 매수누적체결량    | String | Y          |     12   |               |
| mschecnt    | 매수누적체결건수   | String | Y          |      8   |               |
| cpower      | 체결강도       | String | Y          |      9.2 |               |
| offerho1    | 매도호가1      | String | Y          |      6.2 |               |
| bidho1      | 매수호가1      | String | Y          |      6.2 |               |
| openyak     | 미결제약정수량    | String | Y          |      8   |               |
| k200jisu    | KOSPI200지수 | String | Y          |      6.2 |               |
| eqva        | KOSPI등가    | String | Y          |      7.2 |               |
| theoryprice | 이론가        | String | Y          |      6.2 |               |
| impv        | 내재변동성      | String | Y          |      6.2 |               |
| openyakcha  | 미결제약정증감    | String | Y          |      8   |               |
| timevalue   | 시간가치       | String | Y          |      6.2 |               |
| jgubun      | 장운영정보      | String | Y          |      2   |               |
| jnilvolume  | 전일동시간대거래량  | String | Y          |     12   |               |
| optcode     | 단축코드       | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "OC0",
  "tr_key": "201T7347"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "OC0",
  "tr_key": "201T7347"
 },
 "body": {
  "mdchecnt": "1051",
  "sign": "5",
  "mschecnt": "1047",
  "mdvolume": "1384",
  "cpower": "123.77",
  "cvolume": "1",
  "high": "4.76",
  "low": "3.85",
  "price": "4.37",
  "cgubun": "-",
  "impv": "12.58",
  "bidho1": "4.37",
  "k200jisu": "346.27",
  "value": "3380",
  "offerho1": "4.38",
  "jgubun": "40",
  "optcode": "201T7347",
  "change": "0.39",
  "chetime": "093421",
  "openyak": "20098",
  "timevalue": "4.37",
  "volume": "3107",
  "drate": "-8.19",
  "openyakcha": "-246",
  "jnilvolume": "12943",
  "msvolume": "1713",
  "eqva": "2648.37",
  "theoryprice": "4.91",
  "open": "4.69"
 }
}
```

---

## 🏷️ KOSPI200옵션실시간상하한가 (OD0)
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
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| gubun         | 접속매매여부    | String | Y          |      1   |               |
| dy_gubun      | 실시간가격제한여부 | String | Y          |      1   |               |
| dy_uplmtprice | 실시간상한가    | String | Y          |      8.2 |               |
| dy_dnlmtprice | 실시간하한가    | String | Y          |      8.2 |               |
| opttcode      | 단축코드      | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "OD0",
  "tr_key": "201T7347"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "OD0",
  "tr_key": "201T7347"
 },
 "body": {
  "opttcode": "201T7347",
  "dy_gubun": "1",
  "dy_uplmtprice": "9.86",
  "dy_dnlmtprice": "0.01",
  "gubun": ""
 }
}
```

---

## 🏷️ KOSPI200옵션호가 (OH0)
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
| Element     | 한글명     | type   | Required   |   Length | Description   |
|:------------|:--------|:-------|:-----------|---------:|:--------------|
| hotime      | 호가시간    | String | Y          |      6   |               |
| offerho1    | 매도호가1   | String | Y          |      6.2 |               |
| bidho1      | 매수호가1   | String | Y          |      6.2 |               |
| offerrem1   | 매도호가수량1 | String | Y          |      7   |               |
| bidrem1     | 매수호가수량1 | String | Y          |      7   |               |
| offercnt1   | 매도호가건수1 | String | Y          |      5   |               |
| bidcnt1     | 매수호가건수1 | String | Y          |      5   |               |
| offerho2    | 매도호가2   | String | Y          |      6.2 |               |
| bidho2      | 매수호가2   | String | Y          |      6.2 |               |
| offerrem2   | 매도호가수량2 | String | Y          |      7   |               |
| bidrem2     | 매수호가수량2 | String | Y          |      7   |               |
| offercnt2   | 매도호가건수2 | String | Y          |      5   |               |
| bidcnt2     | 매수호가건수2 | String | Y          |      5   |               |
| offerho3    | 매도호가3   | String | Y          |      6.2 |               |
| bidho3      | 매수호가3   | String | Y          |      6.2 |               |
| offerrem3   | 매도호가수량3 | String | Y          |      7   |               |
| bidrem3     | 매수호가수량3 | String | Y          |      7   |               |
| offercnt3   | 매도호가건수3 | String | Y          |      5   |               |
| bidcnt3     | 매수호가건수3 | String | Y          |      5   |               |
| offerho4    | 매도호가4   | String | Y          |      6.2 |               |
| bidho4      | 매수호가4   | String | Y          |      6.2 |               |
| offerrem4   | 매도호가수량4 | String | Y          |      7   |               |
| bidrem4     | 매수호가수량4 | String | Y          |      7   |               |
| offercnt4   | 매도호가건수4 | String | Y          |      5   |               |
| bidcnt4     | 매수호가건수4 | String | Y          |      5   |               |
| offerho5    | 매도호가5   | String | Y          |      6.2 |               |
| bidho5      | 매수호가5   | String | Y          |      6.2 |               |
| offerrem5   | 매도호가수량5 | String | Y          |      7   |               |
| bidrem5     | 매수호가수량5 | String | Y          |      7   |               |
| offercnt5   | 매도호가건수5 | String | Y          |      5   |               |
| bidcnt5     | 매수호가건수5 | String | Y          |      5   |               |
| totofferrem | 매도호가총수량 | String | Y          |      7   |               |
| totbidrem   | 매수호가총수량 | String | Y          |      7   |               |
| totoffercnt | 매도호가총건수 | String | Y          |      5   |               |
| totbidcnt   | 매수호가총건수 | String | Y          |      5   |               |
| optcode     | 단축코드    | String | Y          |      8   |               |
| danhochk    | 단일가호가여부 | String | Y          |      1   |               |
| alloc_gubun | 배분적용구분  | String | Y          |      1   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "OH0",
  "tr_key": "201T7347"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "OH0",
  "tr_key": "201T7347"
 },
 "body": {
  "offerrem2": "11",
  "offerho4": "4.40",
  "bidho5": "4.31",
  "offerho3": "4.39",
  "offerrem3": "16",
  "bidho4": "4.32",
  "offerrem4": "4",
  "offerho5": "4.41",
  "offerrem5": "26",
  "offerrem1": "2",
  "totoffercnt": "224",
  "totbidcnt": "312",
  "bidrem3": "13",
  "bidrem4": "12",
  "bidrem1": "7",
  "bidrem2": "7",
  "bidcnt5": "4",
  "bidcnt4": "5",
  "bidcnt3": "5",
  "bidcnt2": "7",
  "bidcnt1": "6",
  "danhochk": "0",
  "bidho1": "4.35",
  "hotime": "093456",
  "offerho2": "4.38",
  "bidho3": "4.33",
  "bidrem5": "5",
  "offerho1": "4.37",
  "bidho2": "4.34",
  "optcode": "201T7347",
  "offercnt5": "8",
  "offercnt3": "7",
  "offercnt4": "3",
  "offercnt1": "2",
  "offercnt2": "8",
  "alloc_gubun": "",
  "totofferrem": "1017",
  "totbidrem": "1944"
 }
}
```

---

## 🏷️ KOSPI200옵션민감도 (OMG)
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
| Element     | 한글명        | type   | Required   |   Length | Description   |
|:------------|:-----------|:-------|:-----------|---------:|:--------------|
| chetime     | 체결시간       | String | Y          |      6   |               |
| actprice    | 행사가        | String | Y          |      6.2 |               |
| k200jisu    | KOSPI200지수 | String | Y          |      6.2 |               |
| fut200jisu  | 선물가격       | String | Y          |      6.2 |               |
| price       | 현재가        | String | Y          |      6.2 |               |
| capimpv     | 대표내재변동성    | String | Y          |      6.2 |               |
| impv        | 내재변동성      | String | Y          |      6.2 |               |
| delt        | 델타(블랙숄즈)   | String | Y          |      7.4 |               |
| gama        | 감마(블랙숄즈)   | String | Y          |      7.4 |               |
| ceta        | 세타(블랙숄즈)   | String | Y          |      7.4 |               |
| vega        | 베가(블랙숄즈)   | String | Y          |      7.4 |               |
| rhox        | 로우(블랙숄즈)   | String | Y          |      7.4 |               |
| theoryprice | 이론가(블랙숄즈)  | String | Y          |      6.2 |               |
| bimpv       | 전일가내재변동성   | String | Y          |      6.2 |               |
| offerimpv   | 매도가내재변동성   | String | Y          |      6.2 |               |
| bidimpv     | 매수가내재변동성   | String | Y          |      6.2 |               |
| optcode     | 옵션코드       | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "OMG",
  "tr_key": "201T7347"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "OMG",
  "tr_key": "201T7347"
 },
 "body": {
  "ceta": "-0.0947",
  "optcode": "201T7347",
  "bidimpv": "12.70",
  "fut200jisu": "348.00",
  "delt": "0.4966",
  "rhox": "0.1376",
  "chetime": "092803",
  "price": "4.50",
  "capimpv": "18.21",
  "offerimpv": "12.73",
  "bimpv": "13.41",
  "actprice": "347.50",
  "impv": "12.67",
  "k200jisu": "346.17",
  "theoryprice": "4.96",
  "gama": "0.0351",
  "vega": "0.4006"
 }
}
```

---

## 🏷️ KOSPI200옵션가격제한폭확대 (OX0)
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
| Element    | 한글명    | type   | Required   |   Length | Description   |
|:-----------|:-------|:-------|:-----------|---------:|:--------------|
| upstep     | 적용상한단계 | String | Y          |      2   |               |
| dnstep     | 적용하한단계 | String | Y          |      2   |               |
| uplmtprice | 적용상한가  | String | Y          |      6.2 |               |
| dnlmtprice | 적용하한가  | String | Y          |      6.2 |               |
| opttcode   | 단축코드   | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjU1ZjEzNjI2LWRlYWEtNDE2OC05YTkxLTU4YzZjOTc5MDFiNyIsIm5iZiI6MTY4NzM5MDg0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg3NDcxMTk5LCJpYXQiOjE2ODczOTA4NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.wLgwwPtFK1jG3LlmJBd5wX_2NSUa_t8WQT1wmpIiUu1HHyq50181R8Bs2GIruxp88dp4oHH-2j3xlFUIkbPKdg",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "OX0",
  "tr_key": "201T7395"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "OX0",
  "tr_key": "201T7395"
 },
 "body": {
  "upstep": "02",
  "opttcode": "201T7395",
  "uplmtprice": "10.00",
  "dnstep": "02",
  "dnlmtprice": "1.00"
 }
}
```

---

## 🏷️ 상품선물예상체결 (YC3)
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
| Element    | 한글명           | type   | Required   |   Length | Description   |
|:-----------|:--------------|:-------|:-----------|---------:|:--------------|
| ychetime   | 예상체결시간        | String | Y          |      6   |               |
| yeprice    | 예상체결가격        | String | Y          |      9.2 |               |
| yevolume   | 예상체결수량        | String | Y          |      6   |               |
| jnilysign  | 예상체결가전일종가대비구분 | String | Y          |      1   |               |
| jnilchange | 예상체결가전일종가대비   | String | Y          |      9.2 |               |
| jnilydrate | 예상체결가전일종가등락율  | String | Y          |      9.2 |               |
| shcode     | 단축코드          | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQyNjA1YWEzLTA2YzEtNDliNi04ZmRjLTVmNjU1ZTQ1MTE2MiIsIm5iZiI6MTY4Njc4MjU0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2ODY2Mzk5LCJpYXQiOjE2ODY3ODI1NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.BRwxcX00HeeQKW_2MEAcBqk3ZkfLdDfg5WDv17U5X-kYIiudsdLpfkZ0Fo0B8mcTN_NlJuXXhdw6449-8okFYQ",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "YC3",
  "tr_key": "165T6000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "YC3",
  "tr_key": "165T6000"
 },
 "body": {
  "ychetime": "083000",
  "jnilysign": "3",
  "jnilchange": "0.00",
  "yeprice": "104.02",
  "shcode": "165T6000",
  "yevolume": "0",
  "jnilydrate": "0.00"
 }
}
```

---

## 🏷️ 지수선물예상체결 (YFC)
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
| Element      | 한글명           | type   | Required   |   Length | Description   |
|:-------------|:--------------|:-------|:-----------|---------:|:--------------|
| ychetime     | 예상체결시간        | String | Y          |      6   |               |
| yeprice      | 예상체결가격        | String | Y          |      6.2 |               |
| jnilysign    | 예상체결가전일종가대비구분 | String | Y          |      1   |               |
| jnilchange   | 예상체결가전일종가대비   | String | Y          |      6.2 |               |
| jnilydrate   | 예상체결가전일종가등락율  | String | Y          |      6.2 |               |
| futcode      | 단축코드          | String | Y          |      8   |               |
| expct_ccls_q | 예상체결수량        | String | Y          |      9   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQyNjA1YWEzLTA2YzEtNDliNi04ZmRjLTVmNjU1ZTQ1MTE2MiIsIm5iZiI6MTY4Njc4MjU0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2ODY2Mzk5LCJpYXQiOjE2ODY3ODI1NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.BRwxcX00HeeQKW_2MEAcBqk3ZkfLdDfg5WDv17U5X-kYIiudsdLpfkZ0Fo0B8mcTN_NlJuXXhdw6449-8okFYQ",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "YFC",
  "tr_key": "101T9000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "YFC",
  "tr_key": "101T9000"
 },
 "body": {
  "ychetime": "083310",
  "jnilysign": "2",
  "futcode": "101T9000",
  "jnilchange": "0.80",
  "yeprice": "347.20",
  "jnilydrate": "0.23",
  "expct_ccls_q": "0"
 }
}
```

---

## 🏷️ 주식선물예상체결 (YJC)
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
| Element      | 한글명           | type   | Required   |   Length | Description   |
|:-------------|:--------------|:-------|:-----------|---------:|:--------------|
| ychetime     | 예상체결시간        | String | Y          |      6   |               |
| yeprice      | 예상체결가격        | String | Y          |     10   |               |
| jnilysign    | 예상체결가전일종가대비구분 | String | Y          |      1   |               |
| jnilchange   | 예상체결가전일종가대비   | String | Y          |     10   |               |
| jnilydrate   | 예상체결가전일종가등락율  | String | Y          |      6.2 |               |
| futcode      | 단축코드          | String | Y          |      8   |               |
| expct_ccls_q | 예상체결수량        | String | Y          |      9   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQyNjA1YWEzLTA2YzEtNDliNi04ZmRjLTVmNjU1ZTQ1MTE2MiIsIm5iZiI6MTY4Njc4MjU0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2ODY2Mzk5LCJpYXQiOjE2ODY3ODI1NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.BRwxcX00HeeQKW_2MEAcBqk3ZkfLdDfg5WDv17U5X-kYIiudsdLpfkZ0Fo0B8mcTN_NlJuXXhdw6449-8okFYQ",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "YJC",
  "tr_key": "111T7000"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "YJC",
  "tr_key": "111T7000"
 },
 "body": {
  "ychetime": "083000",
  "jnilysign": "3",
  "futcode": "111T7000",
  "jnilchange": "0",
  "yeprice": "0",
  "jnilydrate": "0.00",
  "expct_ccls_q": "0"
 }
}
```

---

## 🏷️ 지수옵션예상체결 (YOC)
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
| Element      | 한글명           | type   | Required   |   Length | Description   |
|:-------------|:--------------|:-------|:-----------|---------:|:--------------|
| ychetime     | 예상체결시간        | String | Y          |      6   |               |
| yeprice      | 예상체결가격        | String | Y          |      6.2 |               |
| jnilysign    | 예상체결가전일종가대비구분 | String | Y          |      1   |               |
| jnilchange   | 예상체결가전일종가대비   | String | Y          |      6.2 |               |
| jnilydrate   | 예상체결가전일종가등락율  | String | Y          |      6.2 |               |
| optcode      | 단축코드          | String | Y          |      8   |               |
| expct_ccls_q | 예상체결수량        | String | Y          |      9   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjQyNjA1YWEzLTA2YzEtNDliNi04ZmRjLTVmNjU1ZTQ1MTE2MiIsIm5iZiI6MTY4Njc4MjU0MSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2ODY2Mzk5LCJpYXQiOjE2ODY3ODI1NDEsImp0aSI6IlBTanpid3pFbE90UGtlbE5zUXZIQThPSkpPV2J6WE1NdUdpNCJ9.BRwxcX00HeeQKW_2MEAcBqk3ZkfLdDfg5WDv17U5X-kYIiudsdLpfkZ0Fo0B8mcTN_NlJuXXhdw6449-8okFYQ",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "YOC",
  "tr_key": "201T7345"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "YOC",
  "tr_key": "201T7345"
 },
 "body": {
  "ychetime": "083256",
  "jnilysign": "3",
  "jnilchange": "0.00",
  "optcode": "201T7345",
  "yeprice": "0.00",
  "jnilydrate": "0.00",
  "expct_ccls_q": "0"
 }
}
```

---

## 🏷️ KRX야간파생 체결 (DC0)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element     | 한글명        | type   | Required   |   Length | Description   |
|:------------|:-----------|:-------|:-----------|---------:|:--------------|
| date        | 일자         | String | Y          |      8   |               |
| sign        | 전일대비구분     | String | Y          |      1   |               |
| chetime     | 체결시간       | String | Y          |      6   |               |
| change      | 전일대비       | String | Y          |      6.2 |               |
| drate       | 등락율        | String | Y          |      6.2 |               |
| price       | 현재가        | String | Y          |      6.2 |               |
| open        | 시가         | String | Y          |      6.2 |               |
| high        | 고가         | String | Y          |      6.2 |               |
| low         | 저가         | String | Y          |      6.2 |               |
| cgubun      | 체결구분       | String | Y          |      1   |               |
| cvolume     | 체결량        | String | Y          |      6   |               |
| volume      | 누적거래량      | String | Y          |     12   |               |
| value       | 누적거래대금     | String | Y          |     12   |               |
| mdvolume    | 매도누적체결량    | String | Y          |     12   |               |
| mdchecnt    | 매도누적체결건수   | String | Y          |      8   |               |
| msvolume    | 매수누적체결량    | String | Y          |     12   |               |
| mschecnt    | 매수누적체결건수   | String | Y          |      8   |               |
| cpower      | 체결강도       | String | Y          |      9.2 |               |
| offerho1    | 매도호가1      | String | Y          |      6.2 |               |
| bidho1      | 매수호가1      | String | Y          |      6.2 |               |
| openyak     | 미결제약정수량    | String | Y          |      8   |               |
| k200jisu    | KOSPI200지수 | String | Y          |      6.2 |               |
| theoryprice | 이론가        | String | Y          |      6.2 |               |
| kasis       | 괴리율        | String | Y          |      6.2 |               |
| sbasis      | 시장BASIS    | String | Y          |      6.2 |               |
| ibasis      | 이론BASIS    | String | Y          |      6.2 |               |
| openyakcha  | 미결제약정증감    | String | Y          |      8   |               |
| jgubun      | 장운영정보      | String | Y          |      2   |               |
| jnilvolume  | 전일동시간대거래량  | String | Y          |     12   |               |
| futcode     | 단축코드       | String | Y          |      8   |               |
| eqva        | KOSPI등가    | Number | Y          |      7.2 |               |
| impv        | 내재변동성      | Number | Y          |      6.2 |               |
| timevalue   | 시간가치       | Number | Y          |      6.2 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "DC0",
  "tr_key": "101W6000"
 }
}
```

### 💡 Response Example
```json
{
	"header": {
		"tr_cd": "DC0",
		"tr_key": "101W6000"
	},
	"body": {
		"date": "20250607",
		"futcode": "101W6000",
		"mdchecnt": "395",
		"sign": "2",
		"mschecnt": "618",
		"ibasis": "0.8",
		"mdvolume": "5055",
		"cpower": "298.20",
		"cvolume": "10",
		"high": "438.60",
		"low": "406.15",
		"price": "438.55",
		"kasis": "16.44",
		"cgubun": "+",
		"impv": "0",
		"bidho1": "438.20",
		"k200jisu": "376.54",
		"value": "2341307",
		"offerho1": "438.55",
		"jgubun": "40",
		"change": "32.40",
		"chetime": "163724",
		"openyak": "280027",
		"timevalue": "0",
		"alloc_gubun": "",
		"volume": "21992",
		"drate": "7.98",
		"openyakcha": "5971",
		"jnilvolume": "0",
		"msvolume": "15074",
		"eqva": "0",
		"sbasis": "62.01",
		"theoryprice": "376.62",
		"open": "406.15"
	}
}
```

---

## 🏷️ KRX야간파생 선물접수 (O02)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element        | 한글명        | type   | Required   |   Length | Description   |
|:---------------|:-----------|:-------|:-----------|---------:|:--------------|
| lineseq        | 라인일련번호     | Number | Y          |     10   |               |
| accno          | 계좌번호       | String | Y          |     11   |               |
| user           | 조작자ID      | String | Y          |      8   |               |
| len            | 헤더길이       | Number | Y          |      6   |               |
| gubun          | 헤더구분       | String | Y          |      1   |               |
| compress       | 압축구분       | String | Y          |      1   |               |
| encrypt        | 암호구분       | String | Y          |      1   |               |
| offset         | 공통시작지점     | Number | Y          |      3   |               |
| trcode         | TRCODE     | String | Y          |      8   |               |
| compid         | 이용사번호      | String | Y          |      3   |               |
| userid         | 사용자ID      | String | Y          |     16   |               |
| media          | 접속매체       | String | Y          |      2   |               |
| ifid           | I/F일련번호    | String | Y          |      3   |               |
| seq            | 전문일련번호     | String | Y          |      9   |               |
| trid           | TR추적ID     | String | Y          |     16   |               |
| pubip          | 공인IP       | String | Y          |     12   |               |
| prvip          | 사설IP       | String | Y          |     12   |               |
| pcbpno         | 처리지점번호     | String | Y          |      3   |               |
| bpno           | 지점번호       | String | Y          |      3   |               |
| termno         | 단말번호       | String | Y          |      8   |               |
| lang           | 언어구분       | String | Y          |      1   |               |
| proctm         | AP처리시간     | Number | Y          |      9   |               |
| msgcode        | 메세지코드      | String | Y          |      4   |               |
| outgu          | 메세지출력구분    | String | Y          |      1   |               |
| compreq        | 압축요청구분     | String | Y          |      1   |               |
| funckey        | 기능키        | String | Y          |      4   |               |
| reqcnt         | 요청레코드개수    | Number | Y          |      4   |               |
| filler         | 예비영역       | String | Y          |      6   |               |
| cont           | 연속구분       | String | Y          |      1   |               |
| contkey        | 연속키값       | String | Y          |     18   |               |
| varlen         | 가변시스템길이    | Number | Y          |      2   |               |
| varhdlen       | 가변해더길이     | Number | Y          |      2   |               |
| varmsglen      | 가변메시지길이    | Number | Y          |      2   |               |
| trsrc          | 조회발원지      | String | Y          |      1   |               |
| eventid        | I/F이벤트ID   | String | Y          |      4   |               |
| ifinfo         | I/F정보      | String | Y          |      4   |               |
| filler1        | 예비영역       | String | Y          |     41   |               |
| trcode1        | tr코드       | String | Y          |      4   |               |
| firmno         | 회사번호       | String | Y          |      3   |               |
| acntno         | 계좌번호       | String | Y          |     11   |               |
| acntno1        | 계좌번호       | String | Y          |      9   |               |
| acntnm         | 계좌명        | String | Y          |     40   |               |
| brnno          | 지점번호       | String | Y          |      3   |               |
| ordmktcode     | 주문시장코드     | String | Y          |      2   |               |
| ordno1         | 주문번호       | String | Y          |      3   |               |
| ordno          | 주문번호       | Number | Y          |      7   |               |
| orgordno1      | 원주문번호      | String | Y          |      3   |               |
| orgordno       | 원주문번호      | Number | Y          |      7   |               |
| prntordno      | 모주문번호      | String | Y          |      3   |               |
| prntordno1     | 모주문번호      | Number | Y          |      7   |               |
| isuno          | 종목번호       | String | Y          |     12   |               |
| fnoIsuno       | 선물옵션종목번호   | String | Y          |      8   |               |
| fnoIsunm       | 선물옵션종목명    | String | Y          |     40   |               |
| pdgrpcode      | 상품군분류코드    | String | Y          |      2   |               |
| fnoIsuptntp    | 선물옵션종목유형구분 | String | Y          |      1   |               |
| bnstp          | 매매구분       | String | Y          |      1   |               |
| mrctp          | 정정취소구분     | String | Y          |      1   |               |
| ordqty         | 주문수량       | Number | Y          |     16   |               |
| hogatype       | 호가유형코드     | String | Y          |      2   |               |
| mmgb           | 거래유형코드     | String | Y          |      2   |               |
| ordprc         | 주문가격       | Number | Y          |     13.2 |               |
| unercqty       | 미체결수량      | Number | Y          |     16   |               |
| commdacode     | 통신매체       | String | Y          |      2   |               |
| peeamtcode     | 수수료합산코드    | String | Y          |      2   |               |
| mgempno        | 관리사원       | String | Y          |      9   |               |
| fnotrdunitamt  | 선물옵션거래단위금액 | Number | Y          |     19.8 |               |
| trxtime        | 처리시각       | String | Y          |      9   |               |
| strtgcode      | 전략코드       | String | Y          |      6   |               |
| grpId          | 그룹Id       | String | Y          |     20   |               |
| ordseqno       | 주문회차       | String | Y          |     10   |               |
| ptflno         | 포트폴리오번호    | String | Y          |     10   |               |
| bskno          | 바스켓번호      | String | Y          |     10   |               |
| trchno         | 트렌치번호      | String | Y          |     10   |               |
| Itemno         | 아이템번호      | String | Y          |     10   |               |
| userId         | 주문자Id      | String | Y          |     16   |               |
| opdrtnno       | 운영지시번호     | String | Y          |     12   |               |
| rjtcode        | 부적격코드      | String | Y          |      3   |               |
| mrccnfqty      | 정정취소확인수량   | Number | Y          |     16   |               |
| orgordunercqty | 원주문미체결수량   | Number | Y          |     16   |               |
| orgordmrcqty   | 원주문정정취소수량  | Number | Y          |     16   |               |
| ctrcttime      | 약정시각(체결시각) | String | Y          |      8   |               |
| ctrctno        | 약정번호       | String | Y          |     10   |               |
| execprc        | 체결가격       | Number | Y          |     13.2 |               |
| execqty        | 체결수량       | Number | Y          |     16   |               |
| newqty         | 신규체결수량     | Number | Y          |     16   |               |
| qdtqty         | 청산체결수량     | Number | Y          |     16   |               |
| lastqty        | 최종결제수량     | Number | Y          |     16   |               |
| lallexecqty    | 전체체결수량     | Number | Y          |     16   |               |
| allexecamt     | 전체체결금액     | Number | Y          |     16   |               |
| fnobalevaltp   | 잔고평가구분     | String | Y          |      1   |               |
| bnsplamt       | 매매손익금액     | Number | Y          |     16   |               |
| fnoIsuno1      | 선물옵션종목번호1  | String | Y          |      8   |               |
| bnstp1         | 매매구분1      | String | Y          |      1   |               |
| execprc1       | 체결가1       | Number | Y          |     13.2 |               |
| newqty1        | 신규체결수량1    | Number | Y          |     16   |               |
| qdtqty1        | 청산체결수량1    | Number | Y          |     16   |               |
| allexecamt1    | 전체체결금액1    | Number | Y          |     16   |               |
| fnoIsuno2      | 선물옵션종목번호2  | String | Y          |      8   |               |
| bnstp2         | 매매구분2      | String | Y          |      1   |               |
| execprc2       | 체결가2       | Number | Y          |     13.2 |               |
| newqty2        | 신규체결수량2    | Number | Y          |     16   |               |
| lqdtqty2       | 청산체결수량2    | Number | Y          |     16   |               |
| allexecamt2    | 전체체결금액2    | Number | Y          |     16   |               |
| dps            | 예수금        | Number | Y          |     16   |               |
| ftsubtdsgnamt  | 선물대용지정금액   | Number | Y          |     16   |               |
| mgn            | 증거금        | Number | Y          |     16   |               |
| mnymgn         | 증거금현금      | Number | Y          |     16   |               |
| ordableamt     | 주문가능금액     | Number | Y          |     16   |               |
| mnyordableamt  | 주문가능현금액    | Number | Y          |     16   |               |
| fnoIsuno_1     | 잔고종목번호1    | String | Y          |      8   |               |
| bnstp_1        | 잔고매매구분1    | String | Y          |      1   |               |
| unsttqty_1     | 미결제수량1     | Number | Y          |     16   |               |
| lqdtableqty_1  | 주문가능수량1    | Number | Y          |     16   |               |
| avrprc_1       | 평균가1       | Number | Y          |     13.2 |               |
| fnoIsuno_2     | 잔고종목번호2    | String | Y          |      8   |               |
| bnstp_2        | 잔고매매구분2    | String | Y          |      1   |               |
| unsttqty_2     | 미결제수량2     | Number | Y          |     16   |               |
| lqdtableqty_2  | 주문가능수량2    | Number | Y          |     16   |               |
| avrprc_2       | 평균가2       | Number | Y          |     13.2 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "1"
 },
 "body": {
  "tr_cd": "O02",
  "tr_key": "101W6000"
 }
}
```

### 💡 Response Example
```json
{
    "header": {
        "tr_cd": "O02"
    },
    "body": {
        "grpId": "",
        "execprc2": "0.00",
        "execprc1": "0.00",
        "trchno": "0000000000",
        "acntno": "***********",
        "fnoIsuptntp": "F",
        "acntnm": "***",
        "trcode": "SONBT003",
        "userid": "*****",
        "fnobalevaltp": "2",
        "avrprc_2": "0.00",
        "avrprc_1": "0.00",
        "fnotrdunitamt": "250000.00000000",
        "len": "1106",
        "mgn": "0",
        "Itemno": "0000000000",
        "opdrtnno": "",
        "cont": "N",
        "allexecamt2": "0",
        "allexecamt1": "0",
        "compress": "0",
        "execprc": "0.00",
        "trxtime": "162043600",
        "gubun": "B",
        "trid": "dD00162043594430",
        "mnyordableamt": "0",
        "varmsglen": "0",
        "ordno": "16",
        "bnstp_2": "",
        "bnstp_1": "",
        "trsrc": "L",
        "fnoIsuno_1": "",
        "hogatype": "",
        "reqcnt": " ",
        "mmgb": "03",
        "strtgcode": "",
        "lqdtqty2": "0",
        "fnoIsuno_2": "",
        "ordseqno": "0000000000",
        "bnstp2": "",
        "bnstp1": "",
        "lastqty": "0",
        "encrypt": "0",
        "ftsubtdsgnamt": "0",
        "acntno1": "",
        "contkey": "0",
        "fnoIsuno1": "",
        "mnymgn": "0",
        "fnoIsuno2": "",
        "seq": "000000070",
        "lineseq": "300000378",
        "peeamtcode": "40",
        "varlen": "50",
        "dps": "0",
        "fnoIsunm": "F 202506",
        "newqty": "0",
        "userId": "*****",
        "fnoIsuno": "101W6000",
        "mrctp": "2",
        "isuno": "KR4101W60000",
        "firmno": "063",
        "filler": "",
        "prntordno": "000",
        "orgordno1": "000",
        "pubip": "010130001138",
        "prvip": "123456789000",
        "funckey": "C",
        "accno": "***********",
        "compreq": "0",
        "ctrcttime": "",
        "orgordmrcqty": "0",
        "termno": "",
        "qdtqty1": "0",
        "bpno": "000",
        "mgempno": "999999201",
        "offset": "212",
        "trcode1": "FO03",
        "varhdlen": "0",
        "ifinfo": "",
        "lallexecqty": "0",
        "pdgrpcode": "01",
        "ptflno": "0000000000",
        "bnsplamt": "0",
        "eventid": "",
        "lqdtableqty_1": "0",
        "pcbpno": "000",
        "lqdtableqty_2": "0",
        "orgordno": "15",
        "brnno": "201",
        "ifid": "000",
        "media": "HT",
        "filler1": "",
        "orgordunercqty": "1",
        "ordno1": "000",
        "rjtcode": "",
        "commdacode": "40",
        "newqty1": "0",
        "newqty2": "0",
        "proctm": "162043601",
        "prntordno1": "14",
        "lang": "K",
        "unercqty": "0",
        "allexecamt": "0",
        "execqty": "0",
        "qdtqty": "0",
        "bskno": "0000000000",
        "ctrctno": "0000000000",
        "ordqty": "1",
        "outgu": "1",
        "msgcode": "9999",
        "ordableamt": "0",
        "ordmktcode": "40",
        "mrccnfqty": "0",
        "comid": "063",
        "bnstp": "2",
        "unsttqty_2": "0",
        "user": "*****",
        "unsttqty_1": "0",
        "ordprc": "0.00"
    }
}
```

---

## 🏷️ KRX야간파생 선물체결 (C02)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element    | 한글명         | type   | Required   |   Length | Description   |
|:-----------|:------------|:-------|:-----------|---------:|:--------------|
| lineseq    | 라인일련번호      | String | Y          |     10   |               |
| accno      | 계좌번호        | String | Y          |     11   |               |
| user       | 조작자ID       | String | Y          |      8   |               |
| seq        | 일련번호        | String | Y          |     11   |               |
| trcode     | trcode      | String | Y          |     11   |               |
| megrpno    | 매칭그룹번호      | String | Y          |      2   |               |
| boardid    | 보드ID        | String | Y          |      2   |               |
| memberno   | 회원번호        | String | Y          |      5   |               |
| bpno       | 지점번호        | String | Y          |      5   |               |
| ordno      | 주문번호        | String | Y          |     10   |               |
| ordordno   | 원주문번호       | String | Y          |     10   |               |
| expcode    | 종목코드        | String | Y          |     12   |               |
| yakseq     | 약정번호        | String | Y          |     11   |               |
| cheprice   | 체결가격        | String | Y          |     11.2 |               |
| chevol     | 체결수량        | String | Y          |     10   |               |
| sessionid  | 세션ID        | String | Y          |      2   |               |
| chedate    | 체결일자        | String | Y          |      8   |               |
| chetime    | 체결시각        | String | Y          |      9   |               |
| spdprc1    | 최근월체결가격     | String | Y          |     11.2 |               |
| spdprc2    | 차근월체결가격     | String | Y          |     11.2 |               |
| dosugb     | 매도수구분       | String | Y          |      1   |               |
| accno1     | 계좌번호1       | String | Y          |     12   |               |
| sihogagb   | 시장조성호가구분    | String | Y          |      1   |               |
| jakino     | 위탁사번호       | String | Y          |      5   |               |
| daeyong    | 대용주권계좌번호    | String | Y          |     12   |               |
| mem_filler | mem_filler  | String | Y          |      7   |               |
| mem_accno  | mem_accno   | String | Y          |     11   |               |
| mem_filler | mem_filler1 | String | Y          |     42   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "1"
 },
 "body": {
  "tr_cd": "C02",
  "tr_key": "101W6000"
 }
}
```

### 💡 Response Example
```json
{
    "header": {
        "tr_cd": "C02"
    },
    "body": {
        "accno": "***********",
        "mem_filler": "*****",
        "accno1": "0***********",
        "sessionid": "40",
        "sihogagb": "0",
        "trcode": "TTRTDP21301",
        "megrpno": "01",
        "memberno": "00063",
        "spdprc1": "0.00",
        "boardid": "G1",
        "spdprc2": "0.00",
        "seq": "69",
        "yakseq": "00000000613",
        "lineseq": "900000129",
        "bpno": "00201",
        "chevol": "1",
        "daeyong": "",
        "chetime": "161201555",
        "chedate": "20250610",
        "ordno": "0000000013",
        "expcode": "KR4101W60000",
        "mem_accno": "***********",
        "cheprice": "415.90",
        "jakino": "",
        "user": "",
        "dosugb": "1",
        "ordordno": ""
    }
}
```

---

## 🏷️ KRX야간파생 호가 (DH0)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element     | 한글명     | type   | Required   |   Length | Description   |
|:------------|:--------|:-------|:-----------|---------:|:--------------|
| hotime      | 호가시간    | String | Y          |      6   |               |
| offerho1    | 매도호가1   | String | Y          |      6.2 |               |
| bidho1      | 매수호가1   | String | Y          |      6.2 |               |
| offerrem1   | 매도호가수량1 | String | Y          |      6   |               |
| bidrem1     | 매수호가수량1 | String | Y          |      6   |               |
| offercnt1   | 매도호가건수1 | String | Y          |      5   |               |
| bidcnt1     | 매수호가건수1 | String | Y          |      5   |               |
| offerho2    | 매도호가2   | String | Y          |      6.2 |               |
| bidho2      | 매수호가2   | String | Y          |      6.2 |               |
| offerrem2   | 매도호가수량2 | String | Y          |      6   |               |
| bidrem2     | 매수호가수량2 | String | Y          |      6   |               |
| offercnt2   | 매도호가건수2 | String | Y          |      5   |               |
| bidcnt2     | 매수호가건수2 | String | Y          |      5   |               |
| offerho3    | 매도호가3   | String | Y          |      6.2 |               |
| bidho3      | 매수호가3   | String | Y          |      6.2 |               |
| offerrem3   | 매도호가수량3 | String | Y          |      6   |               |
| bidrem3     | 매수호가수량3 | String | Y          |      6   |               |
| offercnt3   | 매도호가건수3 | String | Y          |      5   |               |
| bidcnt3     | 매수호가건수3 | String | Y          |      5   |               |
| offerho4    | 매도호가4   | String | Y          |      6.2 |               |
| bidho4      | 매수호가4   | String | Y          |      6.2 |               |
| offerrem4   | 매도호가수량4 | String | Y          |      6   |               |
| bidrem4     | 매수호가수량4 | String | Y          |      6   |               |
| offercnt4   | 매도호가건수4 | String | Y          |      5   |               |
| bidcnt4     | 매수호가건수4 | String | Y          |      5   |               |
| offerho5    | 매도호가5   | String | Y          |      6.2 |               |
| bidho5      | 매수호가5   | String | Y          |      6.2 |               |
| offerrem5   | 매도호가수량5 | String | Y          |      6   |               |
| bidrem5     | 매수호가수량5 | String | Y          |      6   |               |
| offercnt5   | 매도호가건수5 | String | Y          |      5   |               |
| bidcnt5     | 매수호가건수5 | String | Y          |      5   |               |
| totofferrem | 매도호가총수량 | String | Y          |      6   |               |
| totbidrem   | 매수호가총수량 | String | Y          |      6   |               |
| totoffercnt | 매도호가총건수 | String | Y          |      5   |               |
| totbidcnt   | 매수호가총건수 | String | Y          |      5   |               |
| futcode     | 단축코드    | String | Y          |      8   |               |
| danhochk    | 단일가호가여부 | String | Y          |      1   |               |
| alloc_gubun | 배분적용구분  | String | Y          |      1   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "DH0",
  "tr_key": "101W6000"
 }
}
```

### 💡 Response Example
```json
{
	"header": {
		"tr_cd": "DH0",
		"tr_key": "101W6000"
	},
	"body": {
		"offerrem2": "500",
		"offerho4": "438.55",
		"bidho5": "421.75",
		"offerho3": "438.50",
		"offerrem3": "5000",
		"bidho4": "421.85",
		"futcode": "101W6000",
		"offerrem4": "277",
		"offerho5": "438.60",
		"offerrem5": "112",
		"offerrem1": "825",
		"totoffercnt": "16",
		"totbidcnt": "126",
		"bidrem3": "3",
		"bidrem4": "2",
		"bidrem1": "1",
		"bidrem2": "15",
		"bidcnt5": "1",
		"bidcnt4": "2",
		"bidcnt3": "3",
		"bidcnt2": "6",
		"bidcnt1": "1",
		"danhochk": "0",
		"bidho1": "423.80",
		"hotime": "163902",
		"offerho2": "438.40",
		"bidho3": "422.00",
		"bidrem5": "1",
		"offerho1": "430.30",
		"bidho2": "423.00",
		"offercnt5": "4",
		"offercnt3": "5",
		"offercnt4": "5",
		"offercnt1": "1",
		"offercnt2": "1",
		"alloc_gubun": "",
		"totofferrem": "6714",
		"totbidrem": "3013"
	}
}
```

---

## 🏷️ KRX야간파생 선물정정취소 (H02)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element             | 한글명         | type   | Required   |   Length | Description   |
|:--------------------|:------------|:-------|:-----------|---------:|:--------------|
| lineseq             | 라인일련번호      | Number | Y          |     10   |               |
| accno               | 계좌번호        | String | Y          |     11   |               |
| user                | 조작자ID       | String | Y          |      8   |               |
| seq                 | 일련번호        | Number | Y          |     11   |               |
| trcode              | trcode      | String | Y          |     11   |               |
| megrpno             | 매칭그룹번호      | String | Y          |      2   |               |
| boardid             | 보드ID        | String | Y          |      2   |               |
| memberno            | 회원번호        | String | Y          |      5   |               |
| bpno                | 지점번호        | String | Y          |      5   |               |
| ordno               | 주문번호        | String | Y          |     10   |               |
| orgordno            | 원주문번호       | String | Y          |     10   |               |
| expcode             | 종목코드        | String | Y          |     12   |               |
| dosugb              | 매도수구분       | String | Y          |      1   |               |
| mocagb              | 정정취소구분      | String | Y          |      1   |               |
| accno1              | 계좌번호1       | String | Y          |     12   |               |
| qty2                | 호가수량        | Number | Y          |     10   |               |
| price               | 호가가격        | Number | Y          |     11.2 |               |
| ordgb               | 주문유형        | String | Y          |      1   |               |
| hogagb              | 호가구분        | String | Y          |      1   |               |
| sihogagb            | 시장조성호가구분    | String | Y          |     11   |               |
| tradid              | 자사주신고서ID    | String | Y          |      5   |               |
| treacode            | 자사주매매방법     | String | Y          |      1   |               |
| askcode             | 매도유형코드      | String | Y          |      2   |               |
| creditcode          | 신용구분코드      | String | Y          |      2   |               |
| jakigb              | 위탁자기구분      | String | Y          |      2   |               |
| trustnum            | 위탁사번호       | String | Y          |      5   |               |
| ptgb                | 프로그램구분      | String | Y          |      2   |               |
| substonum           | 대용주권계좌번호    | String | Y          |     12   |               |
| accgb               | 계좌구분코드      | String | Y          |      2   |               |
| accmarggb           | 계좌증거금코드     | String | Y          |      2   |               |
| nationcode          | 국가코드        | String | Y          |      3   |               |
| investgb            | 투자자구분       | String | Y          |      4   |               |
| forecode            | 외국인코드       | String | Y          |      2   |               |
| medcode             | 주문매체구분      | String | Y          |      1   |               |
| ordid               | 주문식별자번호     | String | Y          |     12   |               |
| macid               | MAC주소       | String | Y          |     12   |               |
| orddate             | 호가일자        | String | Y          |      8   |               |
| rcvtime             | 회원사주문시각     | String | Y          |      9   |               |
| mem_filler          | mem_filler  | String | Y          |      7   |               |
| mem_accno           | mem_accno   | String | Y          |     11   |               |
| mem_filler1         | mem_filler1 | String | Y          |     42   |               |
| ordacpttm           | 매칭접수시간      | String | Y          |      9   |               |
| qty                 | 실정정취소수량     | Number | Y          |     10   |               |
| autogb              | 자동취소구분      | String | Y          |      1   |               |
| rejcode             | 거부사유        | String | Y          |      4   |               |
| prgordde            | 프로그램호가신고    | String | Y          |      1   |               |
| trdr_id             | 거래자ID       | String | Y          |      6   |               |
| ord_grp_no          | 호가그룹번호      | String | Y          |      2   |               |
| smp_cd              | 자전거래방지코드    | String | Y          |      1   |               |
| ord_cond_prc        | 호가조건가격      | Number | Y          |     11.2 |               |
| trd_mkt_choic_tp_cd | 거래시장선택구분코드  | String | Y          |      1   |               |
| srtsell_id          | 공매도ID       | String | Y          |     10   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "1"
 },
 "body": {
  "tr_cd": "H02",
  "tr_key": "101W6000"
 }
}
```

### 💡 Response Example
```json
{
    "header": {
        "tr_cd": "H02"
    },
    "body": {
        "creditcode": "10",
        "orddate": "20250610",
        "prgordde": "1",
        "accno": "***********",
        "macid": "123456789000",
        "mem_filler": "*****",
        "qty2": "1",
        "trcode": "TTRODP11301",
        "ord_grp_no": "",
        "megrpno": "01",
        "substocnum": "",
        "memberno": "00063",
        "mocagb": "3",
        "price": "0.00",
        "boardid": "G1",
        "accgb": "31",
        "rcvtime": "162043600",
        "jakigb": "11",
        "smp_cd": "0",
        "trd_mkt_choic_tp_cd": "1",
        "ord_cond_prc": "0.00",
        "bpno": "00201",
        "medcode": "4",
        "ordgb": "2",
        "nationcode": "410",
        "accmarggb": "10",
        "ordno": "0000000016",
        "qty": "1",
        "mem_accno": "***********",
        "dosugb": "2",
        "ordordno": "0000000015",
        "trdr_id": "",
        "accno1": "0***********",
        "sihogagb": "00000000000",
        "ordacpttm": "162043608",
        "treaid": "0",
        "seq": "160",
        "lineseq": "900000200",
        "rejcode": "0000",
        "autogb": "0",
        "treacode": "0",
        "askcode": "00",
        "ptgb": "00",
        "ordid": "123456789000",
        "trustnum": "",
        "hogagb": "0",
        "forecode": "00",
        "expcode": "KR4101W60000",
        "srtsell_id": "",
        "investgb": "8000",
        "user": ""
    }
}
```

---

## 🏷️ KRX야간파생 실시간상하한가 (DD0)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| gubun         | 접속매매여부    | String | Y          |      1   |               |
| dy_gubun      | 실시간가격제한여부 | String | Y          |      1   |               |
| dy_uplmtprice | 실시간상한가    | String | Y          |      8.2 |               |
| dy_dnlmtprice | 실시간하한가    | String | Y          |      8.2 |               |
| futcode       | 단축코드      | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "DD0",
  "tr_key": "101W6000"
 }
}
```

### 💡 Response Example
```json
{
	"header": {
		"tr_cd": "DD0",
		"tr_key": "101W6000"
	},
	"body": {
		"futcode": "101W6000",
		"dy_gubun": "1",
		"dy_uplmtprice": "431.70",
		"dy_dnlmtprice": "415.50",
		"gubun": ""
	}
}
```

---

## 🏷️ KRX야간파생 가격제한폭확대 (DX0)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element    | 한글명    | type   | Required   |   Length | Description   |
|:-----------|:-------|:-------|:-----------|---------:|:--------------|
| upstep     | 적용상한단계 | String | Y          |      2   |               |
| dnstep     | 적용하한단계 | String | Y          |      2   |               |
| uplmtprice | 적용상한가  | String | Y          |      6.2 |               |
| dnlmtprice | 적용하한가  | String | Y          |      6.2 |               |
| futcode    | 단축코드   | String | Y          |      8   |               |


---

## 🏷️ KRX야간파생 예상체결 (DYC)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |
| tr_key    | 단축코드  | String | N          |        8 |               |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element      | 한글명           | type   | Required   |   Length | Description   |
|:-------------|:--------------|:-------|:-----------|---------:|:--------------|
| ychetime     | 예상체결시간        | String | Y          |      6   |               |
| yeprice      | 예상체결가격        | String | Y          |      6.2 |               |
| jnilysign    | 예상체결가전일종가대비구분 | String | Y          |      1   |               |
| jnilchange   | 예상체결가전일종가대비   | String | Y          |      6.2 |               |
| jnilydrate   | 예상체결가전일종가등락율  | String | Y          |      6.2 |               |
| futcode      | 단축코드          | String | Y          |      8   |               |
| expct_ccls_q | 예상체결수량        | String | Y          |      9   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "DYC",
  "tr_key": "101W6000"
 }
}
```

---

## 🏷️ KRX야간파생 투자자매매현황 (DBM)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                                                                                                                                                                                                                                                                                                     |
|:----------|:------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tr_cd     | 거래 CD | String | Y          |        3 |                                                                                                                                                                                                                                                                                                                                 |
| tr_key    | 단축코드  | String | N          |        5 | ※ 실시간(DBM,DBT) 키값 - 5자리- 시간대(tm_rng) + 선옵구분(fot_clsf_cd) + 기초자산(bsc_asts_id)- ex) 주간 코스피200선물 실시간키값 : DFK2I시간대(tm_rng)D : 주간N : 야간U : 통합선옵구분(fot_clsf_cd)F : 선물C : Call옵션P : Put옵션S : 스프레드기초자산ID(bsc_asts_id)K2I : KP200선물/옵션MKI : 미니KP200선물/옵션KQI : 코스닥150선물/옵션WKM : 위클리옵션-월WKI : 위클리옵션-목BM3 : 국채3년선물BMA : 국채10년선물USD : 미국달러선물 |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element    | 한글명         | type   | Required   |   Length | Description   |
|:-----------|:------------|:-------|:-----------|---------:|:--------------|
| tjjcode    | 투자자코드       | String | Y          |        4 |               |
| tjjtime    | 수신시간        | String | Y          |        8 |               |
| msvolume   | 매수거래량       | String | Y          |        8 |               |
| mdvolume   | 매도거래량       | String | Y          |        8 |               |
| msvol      | 거래량순매수      | String | Y          |        8 |               |
| p_msvol    | 거래량순매수직전대비  | String | Y          |        8 |               |
| msvalue    | 매수거래대금      | String | Y          |        6 |               |
| mdvalue    | 매도거래대금      | String | Y          |        6 |               |
| msval      | 거래대금순매수     | String | Y          |        6 |               |
| p_msval    | 거래대금순매수직전대비 | String | Y          |        6 |               |
| fottjjcode | 파생상품투자자코드   | String | Y          |        5 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "DBM",
  "tr_key": "UFK2I"
 }
}
```

### 💡 Response Example
```json
{
	"header": {
		"tr_cd": "DBM",
		"tr_key": "UFK2"
	},
	"body": {
		"p_msval": "-0",
		"tjjtime": "2003300",
		"p_msvol": "0",
		"mdvalue": "12",
		"fottjjcode": "？UFK2",
		"msvolume": "6",
		"tjjcode": "I000",
		"msvalue": "6",
		"mdvolume": "13",
		"msvol": "-6",
		"msval": "-6"
	}
}
```

---

## 🏷️ KRX야간파생 투자자별현황 (DBT)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| token     | 접근토큰    | String | Y          |     1000 |               |
| tr_type   | 거래 Type | String | Y          |        1 |               |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                                                                                                                                                                                                                                                                                                     |
|:----------|:------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| tr_cd     | 거래 CD | String | Y          |        3 |                                                                                                                                                                                                                                                                                                                                 |
| tr_key    | 단축코드  | String | N          |        5 | ※ 실시간(DBM,DBT) 키값 - 5자리- 시간대(tm_rng) + 선옵구분(fot_clsf_cd) + 기초자산(bsc_asts_id)- ex) 주간 코스피200선물 실시간키값 : DFK2I시간대(tm_rng)D : 주간N : 야간U : 통합선옵구분(fot_clsf_cd)F : 선물C : Call옵션P : Put옵션S : 스프레드기초자산ID(bsc_asts_id)K2I : KP200선물/옵션MKI : 미니KP200선물/옵션KQI : 코스닥150선물/옵션WKM : 위클리옵션-월WKI : 위클리옵션-목BM3 : 국채3년선물BMA : 국채10년선물USD : 미국달러선물 |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 |               |


### 응답 Body
| Element    | 한글명           | type   | Required   |   Length | Description   |
|:-----------|:--------------|:-------|:-----------|---------:|:--------------|
| tjjtime    | 수신시간          | String | Y          |        8 |               |
| tjjcode1   | 투자자코드1(개인)    | String | Y          |        4 |               |
| msvolume1  | 매수거래량1        | String | Y          |        8 |               |
| mdvolume1  | 매도거래량1        | String | Y          |        8 |               |
| msvol1     | 거래량순매수1       | String | Y          |        8 |               |
| msvalue1   | 매수거래대금1       | String | Y          |        6 |               |
| mdvalue1   | 매도거래대금1       | String | Y          |        6 |               |
| msval1     | 거래대금순매수1      | String | Y          |        6 |               |
| tjjcode2   | 투자자코드2(외국인)   | String | Y          |        4 |               |
| msvolume2  | 매수거래량2        | String | Y          |        8 |               |
| mdvolume2  | 매도거래량2        | String | Y          |        8 |               |
| msvol2     | 거래량순매수2       | String | Y          |        8 |               |
| msvalue2   | 매수거래대금2       | String | Y          |        6 |               |
| mdvalue2   | 매도거래대금2       | String | Y          |        6 |               |
| msval2     | 거래대금순매수2      | String | Y          |        6 |               |
| tjjcode3   | 투자자코드3(기관계)   | String | Y          |        4 |               |
| msvolume3  | 매수거래량3        | String | Y          |        8 |               |
| mdvolume3  | 매도거래량3        | String | Y          |        8 |               |
| msvol3     | 거래량순매수3       | String | Y          |        8 |               |
| msvalue3   | 매수거래대금3       | String | Y          |        6 |               |
| mdvalue3   | 매도거래대금3       | String | Y          |        6 |               |
| msval3     | 거래대금순매수3      | String | Y          |        6 |               |
| tjjcode4   | 투자자코드4(증권)    | String | Y          |        4 |               |
| msvolume4  | 매수거래량4        | String | Y          |        8 |               |
| mdvolume4  | 매도거래량4        | String | Y          |        8 |               |
| msvol4     | 거래량순매수4       | String | Y          |        8 |               |
| msvalue4   | 매수거래대금4       | String | Y          |        6 |               |
| mdvalue4   | 매도거래대금4       | String | Y          |        6 |               |
| msval4     | 거래대금순매수4      | String | Y          |        6 |               |
| tjjcode5   | 투자자코드5(투신)    | String | Y          |        4 |               |
| msvolume5  | 매수거래량5        | String | Y          |        8 |               |
| mdvolume5  | 매도거래량5        | String | Y          |        8 |               |
| msvol5     | 거래량순매수5       | String | Y          |        8 |               |
| msvalue5   | 매수거래대금5       | String | Y          |        6 |               |
| mdvalue5   | 매도거래대금5       | String | Y          |        6 |               |
| msval5     | 거래대금순매수5      | String | Y          |        6 |               |
| tjjcode6   | 투자자코드6(은행)    | String | Y          |        4 |               |
| msvolume6  | 매수거래량6        | String | Y          |        8 |               |
| mdvolume6  | 매도거래량6        | String | Y          |        8 |               |
| msvol6     | 거래량순매수6       | String | Y          |        8 |               |
| msvalue6   | 매수거래대금6       | String | Y          |        6 |               |
| mdvalue6   | 매도거래대금6       | String | Y          |        6 |               |
| msval6     | 거래대금순매수6      | String | Y          |        6 |               |
| tjjcode7   | 투자자코드7(보험)    | String | Y          |        4 |               |
| msvolume7  | 매수거래량7        | String | Y          |        8 |               |
| mdvolume7  | 매도거래량7        | String | Y          |        8 |               |
| msvol7     | 거래량순매수7       | String | Y          |        8 |               |
| msvalue7   | 매수거래대금7       | String | Y          |        6 |               |
| mdvalue7   | 매도거래대금7       | String | Y          |        6 |               |
| msval7     | 거래대금순매수7      | String | Y          |        6 |               |
| tjjcode8   | 투자자코드8(종금)    | String | Y          |        4 |               |
| msvolume8  | 매수거래량8        | String | Y          |        8 |               |
| mdvolume8  | 매도거래량8        | String | Y          |        8 |               |
| msvol8     | 거래량순매수8       | String | Y          |        8 |               |
| msvalue8   | 매수거래대금8       | String | Y          |        6 |               |
| mdvalue8   | 매도거래대금8       | String | Y          |        6 |               |
| msval8     | 거래대금순매수8      | String | Y          |        6 |               |
| tjjcode9   | 투자자코드9(기금)    | String | Y          |        4 |               |
| msvolume9  | 매수거래량9        | String | Y          |        8 |               |
| mdvolume9  | 매도거래량9        | String | Y          |        8 |               |
| msvol9     | 거래량순매수9       | String | Y          |        8 |               |
| msvalue9   | 매수거래대금9       | String | Y          |        6 |               |
| mdvalue9   | 매도거래대금9       | String | Y          |        6 |               |
| msval9     | 거래대금순매수9      | String | Y          |        6 |               |
| tjjcode10  | 투자자코드10(선물업자) | String | Y          |        4 |               |
| msvolume10 | 매수거래량10       | String | Y          |        8 |               |
| mdvolume10 | 매도거래량10       | String | Y          |        8 |               |
| msvol10    | 거래량순매수10      | String | Y          |        8 |               |
| msvalue10  | 매수거래대금10      | String | Y          |        6 |               |
| mdvalue10  | 매도거래대금10      | String | Y          |        6 |               |
| msval10    | 거래대금순매수10     | String | Y          |        6 |               |
| tjjcode11  | 투자자코드11(기타)   | String | Y          |        4 |               |
| msvolume11 | 매수거래량11       | String | Y          |        8 |               |
| mdvolume11 | 매도거래량11       | String | Y          |        8 |               |
| msvol11    | 거래량순매수11      | String | Y          |        8 |               |
| msvalue11  | 매수거래대금11      | String | Y          |        6 |               |
| mdvalue11  | 매도거래대금11      | String | Y          |        6 |               |
| msval11    | 거래대금순매수11     | String | Y          |        6 |               |
| fottjjcode | 파생상품투자자코드     | String | Y          |        5 |               |
| tjjcode0   | 투자자코드0(사모펀드)  | String | Y          |        4 |               |
| msvolume0  | 매수거래량0        | String | Y          |        8 |               |
| mdvolume0  | 매도거래량0        | String | Y          |        8 |               |
| msvol0     | 거래량순매수0       | String | Y          |        8 |               |
| msvalue0   | 매수거래대금0       | String | Y          |        6 |               |
| mdvalue0   | 매도거래대금0       | String | Y          |        6 |               |
| msval0     | 거래대금순매수0      | String | Y          |        6 |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "토큰",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "DBT",
  "tr_key": "UFK2I"
 }
}
```

### 💡 Response Example
```json
{
	"header": {
		"tr_cd": "DBT",
		"tr_key": "UFK2"
	},
	"body": {
		"mdvalue0": "0",
		"mdvalue1": "110",
		"msvolume8": "0",
		"msvolume9": "0",
		"msvolume4": "6",
		"mdvalue6": "0",
		"msvolume5": "0",
		"mdvalue7": "0",
		"msvolume6": "0",
		"mdvalue8": "0",
		"msvolume7": "0",
		"mdvalue9": "0",
		"mdvalue2": "51",
		"msvolume0": "0",
		"msvolume1": "84",
		"mdvalue3": "13",
		"msvolume2": "87",
		"mdvalue4": "13",
		"msvolume3": "6",
		"mdvalue5": "0",
		"mdvolume0": "0",
		"mdvolume9": "0",
		"mdvolume3": "13",
		"mdvolume4": "13",
		"mdvolume1": "115",
		"mdvolume2": "53",
		"mdvolume7": "0",
		"mdvolume8": "0",
		"mdvolume5": "0",
		"mdvolume6": "0",
		"msvalue1": "81",
		"msvalue2": "84",
		"msvalue0": "0",
		"msvalue5": "0",
		"msvalue6": "0",
		"msvalue3": "6",
		"msvol11": "2",
		"msvalue4": "6",
		"msvol10": "0",
		"msvalue9": "0",
		"mdvalue11": "1",
		"msvalue7": "0",
		"msvalue8": "0",
		"mdvalue10": "0",
		"tjjtime": "I2005000",
		"fottjjcode": "？UFK2",
		"tjjcode0": "000",
		"tjjcode10": "？001",
		"msvolume10": "0",
		"tjjcode11": "？000",
		"tjjcode6": "？000",
		"msval6": "0",
		"tjjcode5": "？000",
		"msval5": "0",
		"msval4": "-6",
		"tjjcode8": "？000",
		"msval3": "-6",
		"tjjcode7": "？000",
		"tjjcode2": "？001",
		"tjjcode1": "000",
		"msval9": "0",
		"tjjcode4": "？000",
		"msval8": "0",
		"tjjcode3": "？001",
		"msval7": "0",
		"msval2": "33",
		"msval1": "-29",
		"tjjcode9": "？000",
		"mdvolume10": "0",
		"msval0": "0",
		"mdvolume11": "1",
		"msvol9": "0",
		"msvol5": "0",
		"msvol6": "0",
		"msvol7": "0",
		"msvol8": "0",
		"msvol1": "-30",
		"msvol2": "34",
		"msvol3": "-6",
		"msval11": "2",
		"msvol4": "-6",
		"msval10": "0",
		"msvol0": "0",
		"msvolume11": "3",
		"msvalue10": "0",
		"msvalue11": "3"
	}
}
```

---
