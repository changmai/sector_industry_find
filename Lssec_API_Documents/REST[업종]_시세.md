# REST[업종] 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=f82999f4-eb1a-4ead-a0b1-a4386e8721ab&api_id=88a7c0d3-fb4f-48ef-bc9b-4c47ac72a87b

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /indtp/market-data                |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 업종별 시세 및 기간별 추이를 확인할 수 있는 서비스입니다. |


## 🏷️ 업종기간별추이 (t1514)
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
| Element      | 한글명          | type   | Required   | Length   | Description                            |
|:-------------|:-------------|:-------|:-----------|:---------|:---------------------------------------|
| t1514InBlock | t1514InBlock | Object | Y          | -        |                                        |
| -upcode      | 업종코드         | String | Y          | 3        |                                        |
| -gubun1      | 구분1          | String | Y          | 1        | 미사용항목임 - 스페이스설정                        |
| -gubun2      | 구분2          | String | Y          | 1        | 일@1                                    |
|              |              |        |            |          | 주@2                                    |
|              |              |        |            |          | 월@3                                    |
|              |              |        |            |          | 분                                      |
| -cts_date    | CTS_일자       | String | Y          | 8        | 연속조회기준일(LT)                            |
|              |              |        |            |          | - 연속조회일 경우 이 값 기준으로 조회(cont:1일때)       |
|              |              |        |            |          | (이전 조회한 t1514OutBlock.cts_date 값으로 설정) |
|              |              |        |            |          | -처음조회시 스페이스설정.                         |
| -cnt         | 조회건수         | Object | Y          | 4        |                                        |
| -rate_gbn    | 비중구분         | String | Y          | 1        | 비중구분                                   |
|              |              |        |            |          | - 1:거래량비중                              |
|              |              |        |            |          | - 2:거래대금비중                             |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                               |
|:---------------|:---------------|:-------------|:-----------|:---------|:------------------------------------------|
| t1514OutBlock  | t1514OutBlock  | Object       | Y          | -        |                                           |
| -cts_date      | CTS_일자         | String       | Y          | 8        | 연속조회키값(다음데이타가 있을 경우에 한해서 세팅 됨)            |
|                |                |              |            |          | 이 필드의 데이터를 다음 조회시 InBlock의 date 필드에 넣어준다. |
| t1514OutBlock1 | t1514OutBlock1 | Object Array | Y          | -        |                                           |
| -date          | 일자             | String       | Y          | 8        |                                           |
| -jisu          | 지수             | Number       | Y          | 12.2     |                                           |
| -sign          | 전일대비구분         | String       | Y          | 1        |                                           |
| -change        | 전일대비           | Number       | Y          | 7.2      |                                           |
| -diff          | 등락율            | Number       | Y          | 6.2      |                                           |
| -volume        | 거래량            | Number       | Y          | 12       |                                           |
| -diff_vol      | 거래증가율          | Number       | Y          | 12.2     |                                           |
| -value1        | 거래대금1          | Number       | Y          | 12       |                                           |
| -high          | 상승             | Number       | Y          | 4        |                                           |
| -unchg         | 보합             | Number       | Y          | 4        |                                           |
| -low           | 하락             | Number       | Y          | 4        |                                           |
| -uprate        | 상승종목비율         | Number       | Y          | 6.2      |                                           |
| -frgsvolume    | 외인순매수          | Number       | Y          | 8        |                                           |
| -openjisu      | 시가             | Number       | Y          | 12.2     |                                           |
| -highjisu      | 고가             | Number       | Y          | 12.2     |                                           |
| -lowjisu       | 저가             | Number       | Y          | 12.2     |                                           |
| -value2        | 거래대금2          | Number       | Y          | 12       |                                           |
| -up            | 상한             | Number       | Y          | 4        |                                           |
| -down          | 하한             | Number       | Y          | 4        |                                           |
| -totjo         | 종목수            | Number       | Y          | 4        |                                           |
| -orgsvolume    | 기관순매수          | Number       | Y          | 8        |                                           |
| -upcode        | 업종코드           | String       | Y          | 3        |                                           |
| -rate          | 거래비중           | Number       | Y          | 7.2      |                                           |
| -divrate       | 업종배당수익률        | Number       | Y          | 7.2      |                                           |


### 💡 Request Example
```json
{
  "t1514InBlock": {
    "upcode": "001",
    "gubun1": " ",
    "gubun2": "1",
    "cts_date": " ",
    "cnt": 1,
    "rate_gbn": "1"
  }
}
```

### 💡 Response Example
```json
{
    "t1514OutBlock": {
        "cts_date": "20230605"
    },
    "rsp_cd": "00000",
    "t1514OutBlock1": [
        {
            "date": "20230605",
            "divrate": "0.00",
            "value2": 3884240,
            "diff_vol": "46.20",
            "value1": 3884240,
            "change": "9.26",
            "sign": "2",
            "totjo": 950,
            "diff": "0.36",
            "orgsvolume": 1210,
            "unchg": 91,
            "down": 0,
            "jisu": "2610.62",
            "volume": 263165,
            "high": 606,
            "highjisu": "2617.58",
            "low": 253,
            "rate": "0.00",
            "upcode": "001",
            "up": 0,
            "lowjisu": "2610.40",
            "uprate": "63.79",
            "openjisu": "2617.43",
            "frgsvolume": 351
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 전체업종 (t8424)
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
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| t8424InBlock | t8424InBlock | Object | Y          | -        |               |
| -gubun1      | 구분1          | String | Y          | 1        |               |


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
| t8424OutBlock | t8424OutBlock | Object Array | Y          | -        |               |
| -hname        | 업종명           | String       | Y          | 20       |               |
| -upcode       | 업종코드          | String       | Y          | 3        |               |


### 💡 Request Example
```json
{
  "t8424InBlock": {
    "gubun1": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8424OutBlock": [
        {
            "upcode": "001",
            "hname": "종       합"
        },
        {
            "upcode": "002",
            "hname": "대   형  주"
        },
        {
            "upcode": "820",
            "hname": "KQ150 L KP200 0.5 S"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 예상지수 (t1485)
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
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| t1485InBlock | t1485InBlock | Object | Y          | -        |               |
| -upcode      | 업종코드         | String | Y          | 3        | 코스피@001       |
|              |              |        |            |          | 코스닥@301       |
|              |              |        |            |          | KRX100@501    |
|              |              |        |            |          | KP200@101     |
|              |              |        |            |          | SRI@515       |
|              |              |        |            |          | 코스닥프리미어@404   |
|              |              |        |            |          | KRX 보험@516    |
|              |              |        |            |          | KRX 운송@517    |
| -gubun       | 조회구분         | String | Y          | 1        | 1:장전          |
|              |              |        |            |          | 2:장후          |


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
| t1485OutBlock  | t1485OutBlock  | Object       | Y          | -        |               |
| -pricejisu     | 현재지수           | Number       | Y          | 10.2     |               |
| -sign          | 지수전일대비구분       | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 10.2     |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -yhighjo       | 상승종목수          | Number       | Y          | 4        |               |
| -yupjo         | 상한종목수          | Number       | Y          | 4        |               |
| -yunchgjo      | 보합종목수          | Number       | Y          | 4        |               |
| -ylowjo        | 하락종목수          | Number       | Y          | 4        |               |
| -ydownjo       | 하한종목수          | Number       | Y          | 4        |               |
| -ytrajo        | 거래형성수          | Number       | Y          | 4        |               |
| t1485OutBlock1 | t1485OutBlock1 | Object Array | Y          | -        |               |
| -chetime       | 시간             | String       | Y          | 6        |               |
| -jisu          | 예상지수           | Number       | Y          | 10.2     |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 10.2     |               |
| -volume        | 예상체결량          | Number       | Y          | 12       |               |
| -volcha        | 예상체결량직전대비      | Number       | Y          | 12       |               |
| -diff          | 예상등락율          | Number       | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t1485InBlock" : {
    "upcode" : "001",
    "gubun" : "1"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1485OutBlock1": [
        {
            "jisu": "2617.03",
            "volume": 7372,
            "volcha": 810,
            "change": "15.67",
            "sign": "2",
            "diff": "0.60",
            "chetime": "장  전"
        },
        {
            "jisu": "2601.36",
            "volume": 488,
            "volcha": 0,
            "change": "0.00",
            "sign": "3",
            "diff": "0.00",
            "chetime": "084000"
        }
    ],
    "rsp_msg": "조회완료",
    "t1485OutBlock": {
        "volume": 263165,
        "ylowjo": 1,
        "yhighjo": 5,
        "yunchgjo": 944,
        "yupjo": 0,
        "change": "9.26",
        "sign": "2",
        "ydownjo": 0,
        "ytrajo": 7,
        "pricejisu": "2610.62"
    }
}
```

---

## 🏷️ 업종현재가 (t1511)
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
| Element      | 한글명          | type   | Required   | Length   | Description                        |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------|
| t1511InBlock | t1511InBlock | Object | Y          | -        |                                    |
| -upcode      | 업종코드         | String | Y          | 3        | 코스피@001코스피200@101KRX100@501코스닥@301 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element       | 한글명           | type   | Required   | Length   | Description   |
|:--------------|:--------------|:-------|:-----------|:---------|:--------------|
| t1511OutBlock | t1511OutBlock | Object | Y          | -        |               |
| -gubun        | 업종구분          | String | Y          | 1        |               |
| -hname        | 업종명           | String | Y          | 20       |               |
| -pricejisu    | 현재지수          | Number | Y          | 7.2      |               |
| -jniljisu     | 전일지수          | Number | Y          | 7.2      |               |
| -sign         | 전일대비구분        | String | Y          | 1        |               |
| -change       | 전일대비          | Number | Y          | 7.2      |               |
| -diffjisu     | 지수등락율         | Number | Y          | 6.2      |               |
| -jnilvolume   | 전일거래량         | Number | Y          | 12       |               |
| -volume       | 당일거래량         | Number | Y          | 12       |               |
| -volumechange | 거래량전일대비       | Number | Y          | 12       |               |
| -volumerate   | 거래량비율         | Number | Y          | 6.2      |               |
| -jnilvalue    | 전일거래대금        | Number | Y          | 12       |               |
| -value        | 당일거래대금        | Number | Y          | 12       |               |
| -valuechange  | 거래대금전일대비      | Number | Y          | 12       |               |
| -valuerate    | 거래대금비율        | Number | Y          | 6.2      |               |
| -openjisu     | 시가지수          | Number | Y          | 7.2      |               |
| -opendiff     | 시가등락율         | Number | Y          | 6.2      |               |
| -opentime     | 시가시간          | String | Y          | 6        |               |
| -highjisu     | 고가지수          | Number | Y          | 7.2      |               |
| -highdiff     | 고가등락율         | Number | Y          | 6.2      |               |
| -hightime     | 고가시간          | String | Y          | 6        |               |
| -lowjisu      | 저가지수          | Number | Y          | 7.2      |               |
| -lowdiff      | 저가등락율         | Number | Y          | 6.2      |               |
| -lowtime      | 저가시간          | String | Y          | 6        |               |
| -whjisu       | 52주최고지수       | Number | Y          | 7.2      |               |
| -whchange     | 52주최고현재가대비    | Number | Y          | 7.2      |               |
| -whjday       | 52주최고지수일자     | String | Y          | 8        |               |
| -wljisu       | 52주최저지수       | Number | Y          | 7.2      |               |
| -wlchange     | 52주최저현재가대비    | Number | Y          | 7.2      |               |
| -wljday       | 52주최저지수일자     | String | Y          | 8        |               |
| -yhjisu       | 연중최고지수        | Number | Y          | 7.2      |               |
| -yhchange     | 연중최고현재가대비     | Number | Y          | 7.2      |               |
| -yhjday       | 연중최고지수일자      | String | Y          | 8        |               |
| -yljisu       | 연중최저지수        | Number | Y          | 7.2      |               |
| -ylchange     | 연중최저현재가대비     | Number | Y          | 7.2      |               |
| -yljday       | 연중최저지수일자      | String | Y          | 8        |               |
| -firstjcode   | 첫번째지수코드       | String | Y          | 3        |               |
| -firstjname   | 첫번째지수명        | String | Y          | 20       |               |
| -firstjisu    | 첫번째지수         | Number | Y          | 7.2      |               |
| -firsign      | 첫번째대비구분       | String | Y          | 1        |               |
| -firchange    | 첫번째전일대비       | Number | Y          | 7.2      |               |
| -firdiff      | 첫번째등락율        | Number | Y          | 6.2      |               |
| -secondjcode  | 두번째지수코드       | String | Y          | 3        |               |
| -secondjname  | 두번째지수명        | String | Y          | 20       |               |
| -secondjisu   | 두번째지수         | Number | Y          | 7.2      |               |
| -secsign      | 두번째대비구분       | String | Y          | 1        |               |
| -secchange    | 두번째전일대비       | Number | Y          | 7.2      |               |
| -secdiff      | 두번째등락율        | Number | Y          | 6.2      |               |
| -thirdjcode   | 세번째지수코드       | String | Y          | 3        |               |
| -thirdjname   | 세번째지수명        | String | Y          | 20       |               |
| -thirdjisu    | 세번째지수         | Number | Y          | 7.2      |               |
| -thrsign      | 세번째대비구분       | String | Y          | 1        |               |
| -thrchange    | 세번째전일대비       | Number | Y          | 7.2      |               |
| -thrdiff      | 세번째등락율        | Number | Y          | 6.2      |               |
| -fourthjcode  | 네번째지수코드       | String | Y          | 3        |               |
| -fourthjname  | 네번째지수명        | String | Y          | 20       |               |
| -fourthjisu   | 네번째지수         | Number | Y          | 7.2      |               |
| -forsign      | 네번째대비구분       | String | Y          | 1        |               |
| -forchange    | 네번째전일대비       | Number | Y          | 7.2      |               |
| -fordiff      | 네번째등락율        | Number | Y          | 6.2      |               |
| -highjo       | 상승종목수         | Number | Y          | 4        |               |
| -upjo         | 상한종목수         | Number | Y          | 4        |               |
| -unchgjo      | 보합종목수         | Number | Y          | 4        |               |
| -lowjo        | 하락종목수         | Number | Y          | 4        |               |
| -downjo       | 하한종목수         | Number | Y          | 4        |               |


### 💡 Request Example
```json
{
  "t1511InBlock" : {
    "upcode" : "001"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1511OutBlock": {
        "wljisu": "2134.77",
        "firchange": "9.26",
        "secondjcode": "002",
        "sign": "2",
        "volumechange": -306455,
        "highjisu": "2617.58",
        "yhjisu": "2601.38",
        "upjo": 0,
        "jnilvalue": 9383535,
        "highjo": 606,
        "secondjisu": "2611.97",
        "yljday": "20230103",
        "hname": "종       합",
        "lowdiff": "0.35",
        "downjo": 0,
        "diffjisu": "0.36",
        "forsign": "2",
        "firsign": "2",
        "fourthjcode": "004",
        "gubun": "1",
        "volume": 263165,
        "jniljisu": "2601.36",
        "yhchange": "0.36",
        "highdiff": "0.62",
        "secchange": "7.26",
        "jnilvolume": 569620,
        "valuerate": "41.39",
        "whjday": "20220607",
        "opendiff": "0.62",
        "secdiff": "0.28",
        "lowjo": 253,
        "thrdiff": "0.83",
        "fourthjname": "소   형  주",
        "firstjname": "종       합",
        "fourthjisu": "2393.35",
        "firdiff": "0.03",
        "whchange": "-1.93",
        "thirdjname": "중   형  주",
        "whjisu": "2662.04",
        "thirdjcode": "003",
        "valuechange": -5499295,
        "fordiff": "0.59",
        "firstjcode": "001",
        "value": 3884240,
        "openjisu": "2617.43",
        "secsign": "2",
        "yhjday": "20230602",
        "ylchange": "19.72",
        "wlchange": "22.29",
        "firstjisu": "2610.62",
        "change": "9.26",
        "yljisu": "2180.67",
        "secondjname": "대   형  주",
        "opentime": "090030",
        "thirdjisu": "2760.88",
        "lowtime": "090740",
        "wljday": "20220930",
        "hightime": "090040",
        "thrchange": "22.71",
        "volumerate": "46.20",
        "lowjisu": "2610.40",
        "thrsign": "2",
        "unchgjo": 91,
        "forchange": "14.01",
        "pricejisu": "2610.62"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 업종별종목시세 (t1516)
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
| Element      | 한글명          | type   | Required   | Length   | Description                            |
|:-------------|:-------------|:-------|:-----------|:---------|:---------------------------------------|
| t1516InBlock | t1516InBlock | Object | Y          | -        |                                        |
| -upcode      | 업종코드         | String | Y          | 3        |                                        |
| -gubun       | 구분           | String | Y          | 1        | 1:코스피업종                                |
|              |              |        |            |          | 2:코스닥업종                                |
|              |              |        |            |          | 3:섹터지수                                 |
| -shcode      | 종목코드         | String | Y          | 6        | 처음 조회시는 Space                          |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 shcode 값으로 설정 |


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
| t1516OutBlock  | t1516OutBlock  | Object       | Y          | -        |               |
| -shcode        | 종목코드           | String       | Y          | 6        |               |
| -pricejisu     | 지수             | Number       | Y          | 12.2     |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 7.2      |               |
| -jdiff         | 등락율            | Number       | Y          | 6.2      |               |
| t1516OutBlock1 | t1516OutBlock1 | Object Array | Y          | -        |               |
| -hname         | 종목명            | String       | Y          | 20       |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 8        |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 누적거래량          | Number       | Y          | 12       |               |
| -open          | 시가             | Number       | Y          | 8        |               |
| -high          | 고가             | Number       | Y          | 8        |               |
| -low           | 저가             | Number       | Y          | 8        |               |
| -sojinrate     | 소진율            | Number       | Y          | 6.2      |               |
| -beta          | 베타계수           | Number       | Y          | 6.5      |               |
| -perx          | PER            | Number       | Y          | 8.2      |               |
| -frgsvolume    | 외인순매수          | Number       | Y          | 12       |               |
| -orgsvolume    | 기관순매수          | Number       | Y          | 12       |               |
| -diff_vol      | 거래증가율          | Number       | Y          | 10.2     |               |
| -shcode        | 종목코드           | String       | Y          | 6        |               |
| -total         | 시가총액           | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1516InBlock" : {
    "upcode" : "001",
    "gubun" : "1",
    "shcode" : ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1516OutBlock1": [
        {
            "diff_vol": "-000052.61",
            "change": 30,
            "shcode": "000020",
            "sign": "5",
            "diff": "-00.30",
            "orgsvolume": 0,
            "perx": "015.40",
            "volume": 80350,
            "high": 10150,
            "total": 2804,
            "low": 9870,
            "price": 10040,
            "sojinrate": "004.02",
            "value": 799,
            "hname": "동화약품",
            "open": 10130,
            "beta": "0.0000",
            "frgsvolume": 0
        },
        {
            "diff_vol": "-000082.37",
            "change": 0,
            "shcode": "000640",
            "sign": "3",
            "diff": "000.00",
            "orgsvolume": 0,
            "perx": "064.07",
            "volume": 1326,
            "high": 89800,
            "total": 5695,
            "low": 88700,
            "price": 89700,
            "sojinrate": "012.68",
            "value": 118,
            "hname": "동아쏘시오홀딩스",
            "open": 88800,
            "beta": "0.0000",
            "frgsvolume": 0
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1516OutBlock": {
        "shcode": "000640",
        "change": "0009.26",
        "sign": "2",
        "jdiff": "000.36",
        "pricejisu": "000002610.62"
    }
}

```

---
