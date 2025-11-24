# WEBSOCKET[실시간 시세 투자정보] 투자정보
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=cd909627-82e5-40c9-b313-1a8fd2d7b119&api_id=d67d0790-4b26-447b-82eb-e9642f66057c

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
| Description  | 투자정보를  실시간으로 확인할 수 있습니다.         |


## 🏷️ 시간대별투자자매매추이 (BMT)
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
| upcode     | 업종코드          | String | Y          |        3 |               |
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
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjY2NDVmOGU0LTRkYzEtNDk4ZS05MjEzLTJlYTU5YjNmYjk2MyIsIm5iZiI6MTY4NjY5NjA3MCwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzgyNDcwLCJpYXQiOjE2ODY2OTYwNzAsImp0aSI6IlBTRU1CcWF5Q1N6QmxnTjZ3SlRkUTV5dkRNdjllWjlNZWJ2UCJ9.0roE4en_J2M3PDFr8xrZK4l0pw4uz5-kIc7I_w-E2gXlfMvIdIYqTn3LH_kr-V_iOhiOU-dLRrRbbavzNHJX3Q",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "BMT",
  "tr_key": "001"
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "BMT",
  "tr_key": "001"
 },
 "body": {
  "mdvalue0": "177",
  "mdvalue1": "26157",
  "msvolume8": "28",
  "msvolume9": "4294",
  "msvolume4": "1751",
  "mdvalue6": "4",
  "msvolume5": "562",
  "mdvalue7": "24",
  "msvolume6": "7",
  "mdvalue8": "1",
  "msvolume7": "277",
  "mdvalue9": "3430",
  "mdvalue2": "7432",
  "msvolume0": "1134",
  "msvolume1": "162016",
  "mdvalue3": "5963",
  "msvolume2": "26797",
  "mdvalue4": "2218",
  "msvolume3": "8054",
  "mdvalue5": "110",
  "mdvolume0": "318",
  "mdvolume9": "4372",
  "mdvolume3": "9338",
  "mdvolume4": "4204",
  "mdvolume1": "155078",
  "mdvolume2": "30775",
  "mdvolume7": "59",
  "mdvolume8": "6",
  "mdvolume5": "333",
  "mdvolume6": "47",
  "msvalue1": "26664",
  "msvalue2": "7893",
  "msvalue0": "464",
  "msvalue5": "274",
  "msvalue6": "6",
  "msvalue3": "5208",
  "msvol11": "-1676",
  "msvalue4": "710",
  "msvol10": "0",
  "msvalue9": "3658",
  "mdvalue11": "440",
  "msvalue7": "84",
  "msvalue8": "12",
  "mdvalue10": "0",
  "tjjtime": "09510001",
  "tjjcode0": "0000",
  "tjjcode10": "0011",
  "msvolume10": "0",
  "tjjcode11": "0007",
  "tjjcode6": "0004",
  "msval6": "1",
  "tjjcode5": "0003",
  "msval5": "165",
  "msval4": "-1508",
  "tjjcode8": "0005",
  "msval3": "-755",
  "tjjcode7": "0002",
  "tjjcode2": "0017",
  "tjjcode1": "0008",
  "msval9": "228",
  "tjjcode4": "0001",
  "msval8": "11",
  "tjjcode3": "0018",
  "msval7": "60",
  "msval2": "461",
  "msval1": "507",
  "tjjcode9": "0006",
  "mdvolume10": "0",
  "msval0": "287",
  "mdvolume11": "2939",
  "msvol9": "-78",
  "msvol5": "229",
  "msvol6": "-39",
  "msvol7": "219",
  "msvol8": "22",
  "msvol1": "6938",
  "msvol2": "-3978",
  "msvol3": "-1284",
  "msval11": "-212",
  "msvol4": "-2453",
  "msval10": "0",
  "msvol0": "817",
  "msvolume11": "1263",
  "msvalue10": "0",
  "msvalue11": "228",
  "upcode": "001"
 }
}
```

---

## 🏷️ 현물정보USD실시간 (CUR)
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
| Element   | 한글명     | type   | Required   |   Length | Description   |
|:----------|:--------|:-------|:-----------|---------:|:--------------|
| time      | 전송시간    | String | Y          |      6   |               |
| offer     | 매도호가    | String | Y          |      7.2 |               |
| bid       | 매수호가    | String | Y          |      7.2 |               |
| open      | 시가      | String | Y          |      7.2 |               |
| high      | 고가      | String | Y          |      7.2 |               |
| low       | 저가      | String | Y          |      7.2 |               |
| price     | 체결가     | String | Y          |      7.2 |               |
| sign      | 전일대비구분  | String | Y          |      1   |               |
| change    | 전일대비    | String | Y          |      7.2 |               |
| drate     | 등락율     | String | Y          |      7.2 |               |
| ctime     | 데이타발생시간 | String | Y          |      6   |               |
| base_id   | 기초자산ID  | String | Y          |      6   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImRmYzQ2NThiLTQ3NmItNGQ4MS05OGM3LTI3NzlmNDhjMGZkZiIsIm5iZiI6MTY4NzM5MTEwOSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg3NDcxMTk5LCJpYXQiOjE2ODczOTExMDksImp0aSI6IlBTMzA3em5Jd2ZMSWxXR1Bhbm1SN2ZtMzl2NXRDbWYydWFPWCJ9.mZK8YsM8NNT-5-1Q7uPi1Xjnx9J-P_eRgn2fHCpMtT5CaXK7fu94xeR5iMGqhhTCW3W08IUUG0ixH01IOULtkg",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "CUR",
  "tr_key": "USD   "
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "CUR",
  "tr_key": "USD   "
 },
 "body": {
  "offer": "1318.40",
  "high": "1326.40",
  "drate": "-0.64",
  "low": "1315.50",
  "base_id": "USD",
  "price": "1318.20",
  "change": "-8.50",
  "sign": "5",
  "ctime": "152956",
  "time": "152959",
  "bid": "1318.30",
  "open": "1326.00"
 }
}
```

---

## 🏷️ US지수 (MK2)
### 요청 Header
| Element   | 한글명     | type   | Required   |   Length | Description                                  |
|:----------|:--------|:-------|:-----------|---------:|:---------------------------------------------|
| token     | 접근토큰    | String | Y          |     1000 | Access Token을 설정하기 위한 Header Parameter       |
| tr_type   | 거래 Type | String | Y          |        1 | 1: 계좌등록, 2: 계좌해제, 3: 실시간 시세 등록, 4: 실시간 시세 해제 |


### 요청 Body
| Element   | 한글명   | type   | Required   |   Length | Description                                                                                  |
|:----------|:------|:-------|:-----------|---------:|:---------------------------------------------------------------------------------------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드                                                                                    |
| tr_key    | 심볼코드  | String | N          |       16 | DJI@DJI         : 다우산업NAS@IXIC      : 나스닥 종합SPI@SPX       : S&P 500USI@SOXX      : 필라델피아 반도체 |


### 응답 Header
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| tr_cd     | 거래 CD | String | Y          |        3 | LS증권 거래코드     |


### 응답 Body
| Element   | 한글명    | type   | Required   |   Length | Description   |
|:----------|:-------|:-------|:-----------|---------:|:--------------|
| date      | 일자     | String | Y          |      8   |               |
| time      | 시간     | String | Y          |      6   |               |
| kodate    | 한국일자   | String | Y          |      8   |               |
| kotime    | 한국시간   | String | Y          |      6   |               |
| open      | 시가     | String | Y          |      9.2 |               |
| high      | 고가     | String | Y          |      9.2 |               |
| low       | 저가     | String | Y          |      9.2 |               |
| price     | 현재가    | String | Y          |      9.2 |               |
| sign      | 전일대비구분 | String | Y          |      1   |               |
| change    | 전일대비   | String | Y          |      9.2 |               |
| uprate    | 등락율    | String | Y          |      9.2 |               |
| bidho     | 매수호가   | String | Y          |      9.2 |               |
| bidrem    | 매수잔량   | String | Y          |      9   |               |
| offerho   | 매도호가   | String | Y          |      9.2 |               |
| offerrem  | 매도잔량   | String | Y          |      9   |               |
| volume    | 누적거래량  | String | Y          |     12   |               |
| xsymbol   | 심벌     | String | Y          |     16   |               |
| cvolume   | 체결거래량  | String | Y          |      8   |               |


### 💡 Request Example
```json
{
 "header": {
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImRmYzQ2NThiLTQ3NmItNGQ4MS05OGM3LTI3NzlmNDhjMGZkZiIsIm5iZiI6MTY4NzM5MTEwOSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg3NDcxMTk5LCJpYXQiOjE2ODczOTExMDksImp0aSI6IlBTMzA3em5Jd2ZMSWxXR1Bhbm1SN2ZtMzl2NXRDbWYydWFPWCJ9.mZK8YsM8NNT-5-1Q7uPi1Xjnx9J-P_eRgn2fHCpMtT5CaXK7fu94xeR5iMGqhhTCW3W08IUUG0ixH01IOULtkg",
  "tr_type": "3"
 },
 "body": {
  "tr_cd": "MK2",
  "tr_key": "NII@NI225       "
 }
}
```

### 💡 Response Example
```json
{
 "header": {
  "tr_cd": "MK2",
  "tr_key": "N"
 },
 "body": {
  "date": "II@NI225",
  "change": "10？ 334.49",
  "sign": "8",
  "bidrem": ".38",
  "offerho": "0.00",
  "cvolume": "I@NI225",
  "offerrem": " ",
  "volume": "0.00",
  "high": "20  3.34",
  "bidho": "6.14",
  "kodate": "0230622",
  "low": "8.01？ 336",
  "xsymbol": "0            0 N",
  "price": "1.46？ 333",
  "kotime": "40020",
  "time": "",
  "uprate": "5.-1",
  "open": "230622. 1"
 }
}
```

---
