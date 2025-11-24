# REST[주식] 외인/기관
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=90378c39-f93e-4f95-9670-f76e5c924cc6

## 📌 기본 정보
| 항목           | 내용                                         |
|:-------------|:-------------------------------------------|
| Method       | POST                                       |
| Domain       | https://openapi.ls-sec.co.kr:8080          |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080          |
| 모의투자 도메인     |                                            |
| URL          | /stock/frgr-itt                            |
| Format       | JSON                                       |
| Content-Type | application/json; charset=UTF-8            |
| Description  | 종목별 외인/기관 거래현황을 추정할 수 있는 서비스입니다.(실시간정보 아님) |


## 🏷️ 외인기관종목별동향 (t1702)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description                                                                     |
|:--------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰      | String | Y          |     1000 | OAuth 토큰이 필요한 API 경우 발급한 Access Token을 설정하기 위한 Request Heaeder Parameter        |
| tr_cd         | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |
| mac_address   | MAC 주소    | String | Y          |       12 | 법인인 경우 필수 세팅                                                                    |


### 요청 Body
| Element      | 한글명                   | type   | Required   | Length   | Description                              |
|:-------------|:----------------------|:-------|:-----------|:---------|:-----------------------------------------|
| t1702InBlock | t1702InBlock          | Object | Y          | -        |                                          |
| -shcode      | 종목코드                  | String | Y          | 6        |                                          |
| -fromdt      | 시작일자                  | String | Y          | 8        |                                          |
| -todt        | 종료일자                  | String | Y          | 8        | t1702OutBlock1.date <= t1702InBlock.todt |
| -volvalgb    | 금액수량구분(0:금액1:수량2:단가)  | String | Y          | 1        |                                          |
| -msmdgb      | 매수매도구분(0:순매수1:매수2:매도) | String | Y          | 1        |                                          |
| -gubun       | 누적구분(0:일간1:누적)        | String | Y          | 1        |                                          |
| -exchgubun   | 거래소구분코드               | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리          |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description   |
|:---------------|:---------------|:-------------|:-----------|:---------|:--------------|
| t1702OutBlock1 | t1702OutBlock1 | Object Array | Y          | -        |               |
| -date          | 일자             | String       | Y          | 8        |               |
| -close         | 종가             | Number       | Y          | 8        |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 8        |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 누적거래량          | Number       | Y          | 12       |               |
| -tjj0000       | 사모펀드           | Number       | Y          | 12       |               |
| -tjj0001       | 증권             | Number       | Y          | 12       |               |
| -tjj0002       | 보험             | Number       | Y          | 12       |               |
| -tjj0003       | 투신             | Number       | Y          | 12       |               |
| -tjj0004       | 은행             | Number       | Y          | 12       |               |
| -tjj0005       | 종금             | Number       | Y          | 12       |               |
| -tjj0006       | 기금             | Number       | Y          | 12       |               |
| -tjj0007       | 기타법인           | Number       | Y          | 12       |               |
| -tjj0008       | 개인             | Number       | Y          | 12       |               |
| -tjj0009       | 등록외국인          | Number       | Y          | 12       |               |
| -tjj0010       | 미등록외국인         | Number       | Y          | 12       |               |
| -tjj0011       | 국가외            | Number       | Y          | 12       |               |
| -tjj0018       | 기관             | Number       | Y          | 12       |               |
| -tjj0016       | 외인계(등록+미등록)    | Number       | Y          | 12       |               |
| -amt0017       | 기타계(기타+국가)     | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1702InBlock" : {
    "shcode" : "001200",
    "fromdt" : "20250801",
    "todt" : "20250805",
    "volvalgb" : "0",
    "msmdgb" : "0",
    "gubun" : "0",
    "exchgubun" : "U"
  }
}
```

### 💡 Response Example
```json
{
  "t1702OutBlock1": [
    {
      "date": "20250805",
      "close": 3280,
      "sign": "2",
      "change": 60,
      "diff": "1.86",
      "volume": 887335,
      "tjj0000": -1,
      "tjj0001": 83,
      "tjj0002": 0,
      "tjj0003": 0,
      "tjj0004": 0,
      "tjj0005": 0,
      "tjj0006": 89,
      "tjj0007": -4,
      "tjj0008": -554,
      "tjj0009": 385,
      "tjj0010": 1,
      "tjj0011": 0,
      "tjj0018": 171,
      "tjj0016": 387,
      "tjj0017": -4,
      "value": 2922
    },
    {
      "date": "20250804",
      "close": 3220,
      "sign": "2",
      "change": 65,
      "diff": "2.06",
      "volume": 814070,
      "tjj0000": -158,
      "tjj0001": -18,
      "tjj0002": 0,
      "tjj0003": 0,
      "tjj0004": 0,
      "tjj0005": 0,
      "tjj0006": -10,
      "tjj0007": 24,
      "tjj0008": -68,
      "tjj0009": 232,
      "tjj0010": -2,
      "tjj0011": 0,
      "tjj0018": -186,
      "tjj0016": 230,
      "tjj0017": 24,
      "value": 2603
    },
    {
      "date": "20250801",
      "close": 3155,
      "sign": "5",
      "change": -225,
      "diff": "-6.66",
      "volume": 1810509,
      "tjj0000": 0,
      "tjj0001": -140,
      "tjj0002": 0,
      "tjj0003": 0,
      "tjj0004": 0,
      "tjj0005": 0,
      "tjj0006": 0,
      "tjj0007": 20,
      "tjj0008": -1023,
      "tjj0009": 1143,
      "tjj0010": -1,
      "tjj0011": 0,
      "tjj0018": -140,
      "tjj0016": 1143,
      "tjj0017": 20,
      "value": 5815
    }
  ],
  "rsp_cd": "00000",
  "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 외인기관종목별동향 (t1716)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description                                                                     |
|:--------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰      | String | Y          |     1000 | OAuth 토큰이 필요한 API 경우 발급한 Access Token을 설정하기 위한 Request Heaeder Parameter        |
| tr_cd         | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |
| mac_address   | MAC 주소    | String | Y          |       12 | 법인인 경우 필수 세팅                                                                    |


### 요청 Body
| Element      | 한글명                  | type   | Required   | Length   | Description         |
|:-------------|:---------------------|:-------|:-----------|:---------|:--------------------|
| t1716InBlock | t1716InBlock         | Object | Y          | -        |                     |
| -shcode      | 종목코드                 | String | Y          | 6        |                     |
| -gubun       | 구분(0:일간순매수1:기간누적순매수) | String | Y          | 1        | 0:일간순매수1:기간내누적순매수   |
| -fromdt      | 시작일자                 | String | Y          | 8        | YYYYMMDD            |
| -todt        | 종료일자                 | String | Y          | 8        | YYYYMMDD            |
| -prapp       | PR감산적용율              | Number | Y          | 3        | 프로그램매매 감산 적용율 - %단위 |
| -prgubun     | PR적용구분(0:적용안함1:적용)   | String | Y          | 1        | 0:미적용1:적용           |
| -orggubun    | 기관적용                 | String | Y          | 1        | 0:미적용1:적용           |
| -frggubun    | 외인적용                 | String | Y          | 1        | 0:미적용1:적용           |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element       | 한글명           | type         | Required   | Length   | Description   |
|:--------------|:--------------|:-------------|:-----------|:---------|:--------------|
| t1716OutBlock | t1716OutBlock | Object Array | Y          | -        |               |
| -date         | 일자            | String       | Y          | 8        |               |
| -close        | 종가            | Number       | Y          | 8        |               |
| -sign         | 전일대비구분        | String       | Y          | 1        |               |
| -change       | 전일대비          | Number       | Y          | 8        |               |
| -diff         | 등락율           | Number       | Y          | 6.2      |               |
| -volume       | 누적거래량         | Number       | Y          | 12       |               |
| -krx_0008     | 거래소_개인        | Number       | Y          | 12       |               |
| -krx_0018     | 거래소_기관        | Number       | Y          | 12       |               |
| -krx_0009     | 거래소_외국인       | Number       | Y          | 12       |               |
| -pgmvol       | 프로그램          | Number       | Y          | 12       |               |
| -fsc_listing  | 금감원_외인보유주식수   | Number       | Y          | 12       |               |
| -fsc_sjrate   | 금감원_소진율       | Number       | Y          | 6.2      |               |
| -fsc_0009     | 금감원_외국인       | Number       | Y          | 12       |               |
| -gm_volume    | 공매도수량         | Number       | Y          | 12       |               |
| -gm_value     | 공매도대금         | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1716InBlock" : {
    "shcode" : "005930",
    "gubun" : "0",
    "fromdt" : "20230101",
    "todt" : "20230619",
    "prapp" : 0,
    "prgubun" : "0",
    "orggubun" : "0",
    "frggubun" : "0"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1716OutBlock": [
        {
            "date": "20230619",
            "pgmvol": 100000,
            "change": 0,
            "fsc_listing": 3134788284,
            "sign": "3",
            "diff": "0.00",
            "krx_0008": 3267,
            "krx_0009": 139,
            "fsc_sjrate": "5251.00",
            "krx_0018": -3407,
            "volume": 0,
            "gm_volume": 0,
            "gm_value": 0,
            "fsc_0009": -70,
            "close": 65100
        },
        {
            "date": "20230616",
            "pgmvol": 2076,
            "change": -21400,
            "fsc_listing": 3134788354,
            "sign": "4",
            "diff": "-2993.00",
            "krx_0008": 267859,
            "krx_0009": 3317,
            "fsc_sjrate": "5251.00",
            "krx_0018": -273453,
            "volume": 441652,
            "gm_volume": 0,
            "gm_value": 0,
            "fsc_0009": 70,
            "close": 50100
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 외인기관종목별동향 (t1717)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description                                                                     |
|:--------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰      | String | Y          |     1000 | OAuth 토큰이 필요한 API 경우 발급한 Access Token을 설정하기 위한 Request Heaeder Parameter        |
| tr_cd         | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |
| mac_address   | MAC 주소    | String | Y          |       12 | 법인인 경우 필수 세팅                                                                    |


### 요청 Body
| Element      | 한글명                  | type   | Required   | Length   | Description                     |
|:-------------|:---------------------|:-------|:-----------|:---------|:--------------------------------|
| t1717InBlock | t1717InBlock         | Object | Y          | -        |                                 |
| -shcode      | 종목코드                 | String | Y          | 6        |                                 |
| -gubun       | 구분(0:일간순매수1:기간누적순매수) | String | Y          | 1        |                                 |
| -fromdt      | 시작일자(일간조회일경우는space)  | String | Y          | 8        | OutBlock.date >= fromdt         |
| -todt        | 종료일자                 | String | Y          | 8        | OutBlock.date <= todt           |
| -exchgubun   | 거래소구분코드              | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element       | 한글명               | type         | Required   | Length   | Description   |
|:--------------|:------------------|:-------------|:-----------|:---------|:--------------|
| t1717OutBlock | t1717OutBlock     | Object Array | Y          | -        |               |
| -date         | 일자                | String       | Y          | 8        |               |
| -close        | 종가                | Number       | Y          | 8        |               |
| -sign         | 전일대비구분            | String       | Y          | 1        |               |
| -change       | 전일대비              | Number       | Y          | 8        |               |
| -diff         | 등락율               | Number       | Y          | 6.2      |               |
| -volume       | 누적거래량             | Number       | Y          | 12       |               |
| -tjj0000_vol  | 사모펀드(순매수량)        | Number       | Y          | 12       |               |
| -tjj0001_vol  | 증권(순매수량)          | Number       | Y          | 12       |               |
| -tjj0002_vol  | 보험(순매수량)          | Number       | Y          | 12       |               |
| -tjj0003_vol  | 투신(순매수량)          | Number       | Y          | 12       |               |
| -tjj0004_vol  | 은행(순매수량)          | Number       | Y          | 12       |               |
| -tjj0005_vol  | 종금(순매수량)          | Number       | Y          | 12       |               |
| -tjj0006_vol  | 기금(순매수량)          | Number       | Y          | 12       |               |
| -tjj0007_vol  | 기타법인(순매수량)        | Number       | Y          | 12       |               |
| -tjj0008_vol  | 개인(순매수량)          | Number       | Y          | 12       |               |
| -tjj0009_vol  | 등록외국인(순매수량)       | Number       | Y          | 12       |               |
| -tjj0010_vol  | 미등록외국인(순매수량)      | Number       | Y          | 12       |               |
| -tjj0011_vol  | 국가외(순매수량)         | Number       | Y          | 12       |               |
| -tjj0018_vol  | 기관(순매수량)          | Number       | Y          | 12       |               |
| -tjj0016_vol  | 외인계(순매수량)(등록+미등록) | Number       | Y          | 12       |               |
| -tjj0017_vol  | 기타계(순매수량)(기타+국가)  | Number       | Y          | 12       |               |
| -tjj0000_dan  | 사모펀드(단가)          | Number       | Y          | 12       |               |
| -tjj0001_dan  | 증권(단가)            | Number       | Y          | 12       |               |
| -tjj0002_dan  | 보험(단가)            | Number       | Y          | 12       |               |
| -tjj0003_dan  | 투신(단가)            | Number       | Y          | 12       |               |
| -tjj0004_dan  | 은행(단가)            | Number       | Y          | 12       |               |
| -tjj0005_dan  | 종금(단가)            | Number       | Y          | 12       |               |
| -tjj0006_dan  | 기금(단가)            | Number       | Y          | 12       |               |
| -tjj0007_dan  | 기타법인(단가)          | Number       | Y          | 12       |               |
| -tjj0008_dan  | 개인(단가)            | Number       | Y          | 12       |               |
| -tjj0009_dan  | 등록외국인(단가)         | Number       | Y          | 12       |               |
| -tjj0010_dan  | 미등록외국인(단가)        | Number       | Y          | 12       |               |
| -tjj0011_dan  | 국가외(단가)           | Number       | Y          | 12       |               |
| -tjj0018_dan  | 기관(단가)            | Number       | Y          | 12       |               |
| -tjj0016_dan  | 외인계(단가)(등록+미등록)   | Number       | Y          | 12       |               |
| -tjj0017_dan  | 기타계(단가)(기타+국가)    | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1717InBlock" : {
    "shcode" : "001200",
    "gubun" : "1",
    "fromdt" : "",
    "todt" : ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1717OutBlock": [
        {
            "date": "20230605",
            "tjj0001_vol": 0,
            "sign": "2",
            "tjj0005_dan": 0,
            "tjj0001_dan": 0,
            "tjj0018_vol": 0,
            "tjj0005_vol": 0,
            "tjj0018_dan": 0,
            "tjj0007_vol": 0,
            "tjj0002_dan": 0,
            "tjj0007_dan": 0,
            "tjj0002_vol": 0,
            "tjj0010_dan": 0,
            "tjj0010_vol": 0,
            "tjj0011_dan": 0,
            "close": 3685,
            "tjj0006_dan": 0,
            "tjj0006_vol": 0,
            "tjj0008_dan": 0,
            "change": 25,
            "tjj0011_vol": 0,
            "diff": "0.68",
            "tjj0016_vol": 0,
            "tjj0003_vol": 0,
            "tjj0009_vol": 0,
            "tjj0016_dan": 0,
            "tjj0003_dan": 0,
            "volume": 322192,
            "tjj0009_dan": 0,
            "tjj0000_vol": 0,
            "tjj0017_dan": 0,
            "tjj0004_vol": 0,
            "tjj0017_vol": 0,
            "tjj0000_dan": 0,
            "tjj0008_vol": 0,
            "tjj0004_dan": 0
        }
    ]
}
```

---
