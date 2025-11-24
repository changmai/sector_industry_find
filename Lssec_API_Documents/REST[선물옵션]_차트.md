# REST[선물/옵션] 차트
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=2f1eea77-5606-4512-93c6-31b21d2ece90&api_id=a9b39b08-25c2-427d-848b-675c6228a92b

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /futureoption/chart               |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 주간/야간 선물옵션 기간별 차트를 확인할 수 있습니다.    |


## 🏷️ 선물옵션틱분별체결조회차트 (t2209)
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
| Element      | 한글명          | type   | Required   | Length   | Description                   |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------------|
| t2209InBlock | t2209InBlock | Object | Y          | -        |                               |
| -focode      | 단축코드         | String | Y          | 8        |                               |
| -cgubun      | 챠트구분         | String | Y          | 1        | T:틱차트B:분차트                    |
| -bgubun      | 분구분          | Object | Y          | 3        | 차트구분이 'B'일때만 체크0: 30초0초과 : n분 |
| -cnt         | 조회건수         | Object | Y          | 3        |                               |


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
| t2209OutBlock1 | t2209OutBlock1 | Object Array | Y          | -        |               |
| -chetime       | 시간             | String       | Y          | 10       |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |
| -openyak       | 미결수량           | Number       | Y          | 8        |               |
| -openupdn      | 미결증감           | Number       | Y          | 8        |               |
| -cvolume       | 체결수량           | Number       | Y          | 8        |               |
| -s_mschecnt    | 매수순간체결건수       | Number       | Y          | 8        |               |
| -s_mdchecnt    | 매도순간체결건수       | Number       | Y          | 8        |               |
| -ss_mschecnt   | 순매수순간체결건수      | Number       | Y          | 8        |               |
| -s_mschevol    | 매수순간체결량        | Number       | Y          | 12       |               |
| -s_mdchevol    | 매도순간체결량        | Number       | Y          | 12       |               |
| -ss_mschevol   | 순매수순간체결량       | Number       | Y          | 12       |               |
| -chdegvol      | 체결강도(거래량)      | Number       | Y          | 8.2      |               |
| -chdegcnt      | 체결강도(건수)       | Number       | Y          | 8.2      |               |


### 💡 Request Example
```json
{
   "t2209InBlock" :{
      "focode" : "101T6000",
      "cgubun" : "T",
      "bgubun" : 0,
      "cnt" : 0
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2209OutBlock1": [
        {
            "s_mdchecnt": 0,
            "change": "0.95",
            "sign": "5",
            "chdegcnt": "97.81",
            "ss_mschecnt": 1,
            "chetime": "151959",
            "openyak": 107170,
            "s_mschevol": "000000000013",
            "cvolume": 13,
            "volume": "000000119523",
            "high": "0",
            "chdegvol": "96.01",
            "s_mschecnt": 1,
            "low": "0",
            "openupdn": 0,
            "price": "342.30",
            "value": "010213208975",
            "s_mdchevol": "000000000000",
            "ss_mschevol": "000000000013",
            "open": "0"
        },
        {
            "s_mdchecnt": 1,
            "change": "0.95",
            "sign": "5",
            "chdegcnt": "97.80",
            "ss_mschecnt": -1,
            "chetime": "151959",
            "openyak": 107170,
            "s_mschevol": "000000000000",
            "cvolume": 2,
            "volume": "000000119510",
            "high": "0",
            "chdegvol": "95.99",
            "s_mschecnt": 0,
            "low": "0",
            "openupdn": 0,
            "price": "342.30",
            "value": "010212096500",
            "s_mdchevol": "000000000002",
            "ss_mschevol": "-00000000002",
            "open": "0"
        },
        {
            "s_mdchecnt": 0,
            "change": "0.90",
            "sign": "5",
            "chdegcnt": "97.81",
            "ss_mschecnt": 1,
            "chetime": "151959",
            "openyak": 107170,
            "s_mschevol": "000000000002",
            "cvolume": 2,
            "volume": "000000119508",
            "high": "0",
            "chdegvol": "95.99",
            "s_mschecnt": 1,
            "low": "0",
            "openupdn": 0,
            "price": "342.35",
            "value": "010211925350",
            "s_mdchevol": "000000000000",
            "ss_mschevol": "000000000002",
            "open": "0"
        },
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 선물옵션차트(틱/n틱) (t8414)
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
| Element      | 한글명                     | type   | Required   | Length   | Description                              |
|:-------------|:------------------------|:-------|:-----------|:---------|:-----------------------------------------|
| t8414InBlock | t8414InBlock            | Object | Y          | -        |                                          |
| -shcode      | 단축코드                    | String | Y          | 8        |                                          |
| -ncnt        | 단위(n틱)                  | Number | Y          | 4        |                                          |
| -qrycnt      | 요청건수(최대-압축:2000비압축:500) | Number | Y          | 4        | 요청건수                                     |
|              |                         |        |            |          |                                          |
|              |                         |        |            |          | 압축모듈인 경우 최대 2000건까지 조회가능.                |
|              |                         |        |            |          | 비압축인 경우 최대 500건까지 조회가능                   |
| -nday        | 조회영업일수(0:미사용1>=사용)      | String | Y          | 1        | 0:미사용                                    |
| -sdate       | 시작일자                    | String | Y          | 8        | 기본값 : Space                              |
|              |                         |        |            |          | (edate(필수입력) 기준으로 qrycnt 만큼 조회)          |
|              |                         |        |            |          |                                          |
|              |                         |        |            |          | 조회구간을 설정하여 필터링 하고 싶은 경우 입력               |
| -stime       | 시작시간(현재미사용)             | String | Y          | 6        |                                          |
| -edate       | 종료일자                    | String | Y          | 8        | 처음조회기준일(LE)                              |
|              |                         |        |            |          | 처음조회일 경우 이 값 기준으로 조회                     |
|              |                         |        |            |          | ("99999999" 혹은 '당일')                     |
| -etime       | 종료시간(현재미사용)             | String | Y          | 6        |                                          |
| -cts_date    | 연속일자                    | String | Y          | 8        | 처음 조회시는 Space                            |
|              |                         |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정 |
| -cts_time    | 연속시간                    | String | Y          | 10       | N:비압축                                    |
| -comp_yn     | 압축여부(Y:압축N:비압축)         | String | Y          | 1        | N:비압축 모듈                                 |
|              |                         |        |            |          | Y: 압 축 모듈                                |


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
| t8414OutBlock  | t8414OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 8        |               |
| -jisiga        | 전일시가           | Number       | Y          | 6.2      |               |
| -jihigh        | 전일고가           | Number       | Y          | 6.2      |               |
| -jilow         | 전일저가           | Number       | Y          | 6.2      |               |
| -jiclose       | 전일종가           | Number       | Y          | 6.2      |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 6.2      |               |
| -dihigh        | 당일고가           | Number       | Y          | 6.2      |               |
| -dilow         | 당일저가           | Number       | Y          | 6.2      |               |
| -diclose       | 당일종가           | Number       | Y          | 6.2      |               |
| -highend       | 상한가            | Number       | Y          | 6.2      |               |
| -lowend        | 하한가            | Number       | Y          | 6.2      |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -cts_time      | 연속시간           | String       | Y          | 10       |               |
| -s_time        | 장시작시간(HHMMSS)  | String       | Y          | 6        |               |
| -e_time        | 장종료시간(HHMMSS)  | String       | Y          | 6        |               |
| -dshmin        | 동시호가처리시간(MM:분) | String       | Y          | 2        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| t8414OutBlock1 | t8414OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 10       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -close         | 종가             | Number       | Y          | 6.2      |               |
| -jdiff_vol     | 거래량            | Number       | Y          | 12       |               |
| -openyak       | 미결제약정          | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8414InBlock": {
    "shcode": "101T6000",
    "ncnt": 1,
    "qrycnt": 20,
    "nday": "",
    "sdate": "",
    "stime": "",
    "edate": "",
    "etime": "",
    "cts_date": "",
    "cts_time": "",
    "comp_yn": "N"
  }
}
```

### 💡 Response Example
```json
{
    "t8414OutBlock1": [
    ],
    "rsp_cd": "00000",
    "t8414OutBlock": {
        "cts_date": "00000000",
        "shcode": "101T6000",
        "highend": "370.70",
        "jivolume": 165564,
        "e_time": "154500",
        "jisiga": "345.10",
        "jilow": "343.10",
        "diclose": "342.30",
        "dshmin": "10",
        "disiga": "342.15",
        "s_time": "090000",
        "lowend": "315.80",
        "dihigh": "342.75",
        "jihigh": "345.75",
        "rec_count": 0,
        "dilow": "340.65",
        "jiclose": "343.25",
        "cts_time": "0000000000"
    },
    "rsp_msg": "해당자료가 없습니다."
}
```

---

## 🏷️ 선물/옵션차트(N분) (t8415)
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
| Element      | 한글명                     | type   | Required   | Length   | Description                                                          |
|:-------------|:------------------------|:-------|:-----------|:---------|:---------------------------------------------------------------------|
| t8415InBlock | t8415InBlock            | Object | Y          | -        |                                                                      |
| -shcode      | 단축코드                    | String | Y          | 8        |                                                                      |
| -ncnt        | 단위(n분)                  | Number | Y          | 4        | 0:30초1: 1분2: 2분.....n: n분                                            |
| -qrycnt      | 요청건수(최대-압축:2000비압축:500) | Number | Y          | 4        | 요청건수압축모듈인 경우 최대 2000건까지 조회가능.비압축인 경우 최대 500건까지 조회가능                  |
| -nday        | 조회영업일수(0:미사용1>=사용)      | String | Y          | 1        | 0:미사용                                                                |
| -sdate       | 시작일자                    | String | Y          | 8        | 기본값 : Space(edate(필수입력) 기준으로 qrycnt 만큼 조회)조회구간을 설정하여 필터링 하고 싶은 경우 입력 |
| -stime       | 시작시간(현재미사용)             | String | Y          | 6        |                                                                      |
| -edate       | 종료일자                    | String | Y          | 8        | 처음조회기준일(LE)처음조회일 경우 이 값 기준으로 조회("99999999" 혹은 '당일')                  |
| -etime       | 종료시간(현재미사용)             | String | Y          | 6        |                                                                      |
| -cts_date    | 연속일자                    | String | Y          | 8        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정                |
| -cts_time    | 연속시간                    | String | Y          | 10       |                                                                      |
| -comp_yn     | 압축여부(Y:압축N:비압축)         | String | Y          | 1        | N:비압축 모듈Y: 압 축 모듈                                                    |


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
| t8415OutBlock  | t8415OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 8        |               |
| -jisiga        | 전일시가           | Number       | Y          | 6.2      |               |
| -jihigh        | 전일고가           | Number       | Y          | 6.2      |               |
| -jilow         | 전일저가           | Number       | Y          | 6.2      |               |
| -jiclose       | 전일종가           | Number       | Y          | 6.2      |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 6.2      |               |
| -dihigh        | 당일고가           | Number       | Y          | 6.2      |               |
| -dilow         | 당일저가           | Number       | Y          | 6.2      |               |
| -diclose       | 당일종가           | Number       | Y          | 6.2      |               |
| -highend       | 상한가            | Number       | Y          | 6.2      |               |
| -lowend        | 하한가            | Number       | Y          | 6.2      |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -cts_time      | 연속시간           | String       | Y          | 10       |               |
| -s_time        | 장시작시간(HHMMSS)  | String       | Y          | 6        |               |
| -e_time        | 장종료시간(HHMMSS)  | String       | Y          | 6        |               |
| -dshmin        | 동시호가처리시간(MM:분) | String       | Y          | 2        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| t8415OutBlock1 | t8415OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 10       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -close         | 종가             | Number       | Y          | 6.2      |               |
| -jdiff_vol     | 누적거래량          | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |
| -openyak       | 미결제약정          | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8415InBlock": {
    "shcode": "101T6000",
    "ncnt": 1,
    "qrycnt": 200,
    "nday": "1",
    "sdate": "20230509",
    "stime": "",
    "edate": "20230510",
    "etime": "",
    "cts_date": "",
    "cts_time": "",
    "comp_yn": "N"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8415OutBlock": {
        "cts_date": "",
        "shcode": "101T6000",
        "highend": "370.70",
        "jivolume": 165564,
        "e_time": "154500",
        "jisiga": "345.10",
        "jilow": "343.10",
        "diclose": "342.30",
        "dshmin": "10",
        "disiga": "342.15",
        "s_time": "090000",
        "lowend": "315.80",
        "dihigh": "342.75",
        "jihigh": "345.75",
        "rec_count": 396,
        "dilow": "340.65",
        "jiclose": "343.25",
        "cts_time": ""
    },
    "t8415OutBlock1": [
        {
            "date": "20230510",
            "jdiff_vol": 4566,
            "high": "328.65",
            "low": "327.90",
            "time": "090100",
            "openyak": 319869,
            "close": "327.95",
            "value": 374758,
            "open": "328.60"
        },
        {
            "date": "20230510",
            "jdiff_vol": 1837,
            "high": "328.00",
            "low": "327.80",
            "time": "090200",
            "openyak": 320161,
            "close": "327.85",
            "value": 150582,
            "open": "328.00"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 선물/옵션차트(일주월) (t8416)
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
| Element      | 한글명                     | type   | Required   | Length   | Description                                                          |
|:-------------|:------------------------|:-------|:-----------|:---------|:---------------------------------------------------------------------|
| t8416InBlock | t8416InBlock            | Object | Y          | -        |                                                                      |
| -shcode      | 단축코드                    | String | Y          | 8        |                                                                      |
| -gubun       | 주기구분(2:일3:주4:월)         | String | Y          | 1        |                                                                      |
| -qrycnt      | 요청건수(최대-압축:2000비압축:500) | Number | Y          | 4        | 요청건수압축모듈인 경우 최대 2000건까지 조회가능.비압축인 경우 최대 500건까지 조회가능                  |
| -sdate       | 시작일자                    | String | Y          | 8        | 기본값 : Space(edate(필수입력) 기준으로 qrycnt 만큼 조회)조회구간을 설정하여 필터링 하고 싶은 경우 입력 |
| -edate       | 종료일자                    | String | Y          | 8        | 처음조회기준일(LE)처음조회일 경우 이 값 기준으로 조회("99999999" 혹은 '당일')                  |
| -cts_date    | 연속일자                    | String | Y          | 8        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정                |
| -comp_yn     | 압축여부(Y:압축N:비압축)         | String | Y          | 1        | N:비압축 모듈Y: 압 축 모듈                                                    |


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
| t8416OutBlock  | t8416OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 8        |               |
| -jisiga        | 전일시가           | Number       | Y          | 6.2      |               |
| -jihigh        | 전일고가           | Number       | Y          | 6.2      |               |
| -jilow         | 전일저가           | Number       | Y          | 6.2      |               |
| -jiclose       | 전일종가           | Number       | Y          | 6.2      |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 6.2      |               |
| -dihigh        | 당일고가           | Number       | Y          | 6.2      |               |
| -dilow         | 당일저가           | Number       | Y          | 6.2      |               |
| -diclose       | 당일종가           | Number       | Y          | 6.2      |               |
| -highend       | 상한가            | Number       | Y          | 6.2      |               |
| -lowend        | 하한가            | Number       | Y          | 6.2      |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -s_time        | 장시작시간(HHMMSS)  | String       | Y          | 6        |               |
| -e_time        | 장종료시간(HHMMSS)  | String       | Y          | 6        |               |
| -dshmin        | 동시호가처리시간(MM:분) | String       | Y          | 2        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| t8416OutBlock1 | t8416OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -close         | 종가             | Number       | Y          | 6.2      |               |
| -jdiff_vol     | 누적거래량          | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |
| -openyak       | 미결제약정          | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
   "t8416InBlock" :{
      "shcode" : "101T6000",
      "gubun" : "2",
      "qrycnt" : 100,
      "sdate" : "20230502",
      "edate" : "20230602",
      "cts_date" : "",
      "comp_yn" : "N"
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t8416OutBlock": {
        "cts_date": "",
        "shcode": "101T6000",
        "highend": "370.70",
        "jivolume": 165564,
        "e_time": "154500",
        "jisiga": "345.10",
        "jilow": "343.10",
        "diclose": "342.30",
        "dshmin": "10",
        "disiga": "342.15",
        "s_time": "090000",
        "lowend": "315.80",
        "dihigh": "342.75",
        "jihigh": "345.75",
        "rec_count": 22,
        "dilow": "340.65",
        "jiclose": "343.25"
    },
    "t8416OutBlock1": [
        {
            "date": "20230502",
            "jdiff_vol": 220627,
            "high": "330.10",
            "low": "327.10",
            "openyak": 321283,
            "close": "330.00",
            "value": 18148636,
            "open": "327.75"
        },
        {
            "date": "20230503",
            "jdiff_vol": 187741,
            "high": "328.50",
            "low": "326.40",
            "openyak": 316695,
            "close": "326.80",
            "value": 15359500,
            "open": "327.90"
        }
    ]
}
```

---

## 🏷️ KRX야간파생 틱분별조회(API용) (t8461)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명          | type   | Required   | Length   | Description                   |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------------|
| t8461InBlock | t8461InBlock | Object | Y          |          |                               |
| -focode      | 단축코드         | String | Y          | 8        |                               |
| -cgubun      | 챠트구분         | String | Y          | 1        | T:틱차트B:분차트                    |
| -bgubun      | 분구분          | Object | Y          | 3        | 차트구분이 'B'일때만 체크0: 30초0초과 : n분 |
| -cnt         | 조회건수         | Object | Y          | 3        |                               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description   |
|:---------------|:---------------|:-------------|:-----------|:---------|:--------------|
| t8461OutBlock1 | t8461OutBlock1 | Object Array | Y          |          |               |
| -chetime       | 시간             | String       | Y          | 10       |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -cvolume       | 체결수량           | Number       | Y          | 8        |               |
| -s_mschecnt    | 매수순간체결건수       | Number       | Y          | 8        |               |
| -s_mdchecnt    | 매도순간체결건수       | Number       | Y          | 8        |               |
| -ss_mschecnt   | 순매수순간체결건수      | Number       | Y          | 8        |               |
| -s_mschevol    | 매수순간체결량        | Number       | Y          | 12       |               |
| -s_mdchevol    | 매도순간체결량        | Number       | Y          | 12       |               |
| -ss_mschevol   | 순매수순간체결량       | Number       | Y          | 12       |               |
| -chdegvol      | 체결강도(거래량)      | Number       | Y          | 8.2      |               |
| -chdegcnt      | 체결강도(건수)       | Number       | Y          | 8.2      |               |


### 💡 Request Example
```json
{
  "t8461InBlock": {
    "focode": "101W6000",
    "cgubun": "2",
    "bgubun": "0",
    "cnt": 20
  }
}
```

### 💡 Response Example
```json
{
	"t8461OutBlock1": [
		{
			"chetime": "161600",
			"price": "436.40",
			"sign": "2",
			"change": "30.25",
			"open": "436.00",
			"high": "436.45",
			"low": "436.00",
			"volume": "12436",
			"cvolume": 267,
			"s_mschecnt": 3,
			"s_mdchecnt": 22,
			"ss_mschecnt": -19,
			"s_mschevol": "76",
			"s_mdchevol": "191",
			"ss_mschevol": "-115",
			"chdegvol": "305.72",
			"chdegcnt": "155.87"
		},
		{
			"chetime": "161530",
			"price": "436.00",
			"sign": "2",
			"change": "29.85",
			"open": "435.85",
			"high": "436.10",
			"low": "435.40",
			"volume": "12169",
			"cvolume": 496,
			"s_mschecnt": 45,
			"s_mdchecnt": 16,
			"ss_mschecnt": 29,
			"s_mschevol": "385",
			"s_mdchevol": "111",
			"ss_mschevol": "274",
			"chdegvol": "326.75",
			"chdegcnt": "169.78"
		},
		{
			"chetime": "161500",
			"price": "435.35",
			"sign": "2",
			"change": "29.20",
			"open": "435.55",
			"high": "435.95",
			"low": "435.35",
			"volume": "11673",
			"cvolume": 228,
			"s_mschecnt": 8,
			"s_mdchecnt": 6,
			"ss_mschecnt": 2,
			"s_mschevol": "206",
			"s_mdchevol": "22",
			"ss_mschevol": "184",
			"chdegvol": "325.78",
			"chdegcnt": "161.24"
		},
		{
			"chetime": "161430",
			"price": "435.50",
			"sign": "2",
			"change": "29.35",
			"open": "435.35",
			"high": "435.50",
			"low": "435.35",
			"volume": "11445",
			"cvolume": 1127,
			"s_mschecnt": 12,
			"s_mdchecnt": 5,
			"ss_mschecnt": 7,
			"s_mschevol": "1102",
			"s_mdchevol": "25",
			"ss_mschevol": "1077",
			"chdegvol": "319.89",
			"chdegcnt": "162.07"
		},
		{
			"chetime": "161400",
			"price": "435.30",
			"sign": "2",
			"change": "29.15",
			"open": "435.25",
			"high": "435.30",
			"low": "435.25",
			"volume": "10318",
			"cvolume": 836,
			"s_mschecnt": 87,
			"s_mdchecnt": 0,
			"ss_mschecnt": 87,
			"s_mschevol": "836",
			"s_mdchevol": "0",
			"ss_mschevol": "836",
			"chdegvol": "274.61",
			"chdegcnt": "160.10"
		},
		{
			"chetime": "161330",
			"price": "435.30",
			"sign": "2",
			"change": "29.15",
			"open": "435.25",
			"high": "435.30",
			"low": "435.25",
			"volume": "9482",
			"cvolume": 172,
			"s_mschecnt": 18,
			"s_mdchecnt": 3,
			"ss_mschecnt": 15,
			"s_mschevol": "167",
			"s_mdchevol": "5",
			"ss_mschevol": "162",
			"chdegvol": "237.57",
			"chdegcnt": "116.16"
		},
		{
			"chetime": "161300",
			"price": "435.20",
			"sign": "2",
			"change": "29.05",
			"open": "435.00",
			"high": "435.20",
			"low": "434.95",
			"volume": "9310",
			"cvolume": 546,
			"s_mschecnt": 8,
			"s_mdchecnt": 3,
			"ss_mschecnt": 5,
			"s_mschevol": "536",
			"s_mdchevol": "10",
			"ss_mschevol": "526",
			"chdegvol": "230.68",
			"chdegcnt": "108.72"
		},
		{
			"chetime": "161230",
			"price": "435.00",
			"sign": "2",
			"change": "28.85",
			"open": "415.90",
			"high": "435.00",
			"low": "415.90",
			"volume": "8764",
			"cvolume": 1482,
			"s_mschecnt": 7,
			"s_mdchecnt": 1,
			"ss_mschecnt": 6,
			"s_mschevol": "1481",
			"s_mdchevol": "1",
			"ss_mschevol": "1480",
			"chdegvol": "207.81",
			"chdegcnt": "106.25"
		},
		{
			"chetime": "161200",
			"price": "424.00",
			"sign": "2",
			"change": "17.85",
			"open": "424.00",
			"high": "424.00",
			"low": "424.00",
			"volume": "7282",
			"cvolume": 0,
			"s_mschecnt": 0,
			"s_mdchecnt": 0,
			"ss_mschecnt": 0,
			"s_mschevol": "0",
			"s_mdchevol": "0",
			"ss_mschevol": "0",
			"chdegvol": "141.81",
			"chdegcnt": "103.14"
		},
		{
			"chetime": "161130",
			"price": "424.00",
			"sign": "2",
			"change": "17.85",
			"open": "424.00",
			"high": "424.00",
			"low": "423.70",
			"volume": "7282",
			"cvolume": 83,
			"s_mschecnt": 2,
			"s_mdchecnt": 8,
			"ss_mschecnt": -6,
			"s_mschevol": "9",
			"s_mdchevol": "74",
			"ss_mschevol": "-65",
			"chdegvol": "141.81",
			"chdegcnt": "103.14"
		},
		{
			"chetime": "161100",
			"price": "423.70",
			"sign": "2",
			"change": "17.55",
			"open": "424.00",
			"high": "424.00",
			"low": "423.70",
			"volume": "7199",
			"cvolume": 26,
			"s_mschecnt": 0,
			"s_mdchecnt": 4,
			"ss_mschecnt": -4,
			"s_mschevol": "0",
			"s_mdchevol": "26",
			"ss_mschevol": "-26",
			"chdegvol": "146.24",
			"chdegcnt": "106.56"
		},
		{
			"chetime": "161030",
			"price": "430.00",
			"sign": "2",
			"change": "23.85",
			"open": "423.70",
			"high": "430.00",
			"low": "423.70",
			"volume": "7173",
			"cvolume": 102,
			"s_mschecnt": 1,
			"s_mdchecnt": 2,
			"ss_mschecnt": -1,
			"s_mschevol": "100",
			"s_mdchevol": "2",
			"ss_mschevol": "98",
			"chdegvol": "148.01",
			"chdegcnt": "108.94"
		},
		{
			"chetime": "161000",
			"price": "415.60",
			"sign": "2",
			"change": "9.45",
			"open": "407.50",
			"high": "415.60",
			"low": "407.50",
			"volume": "7071",
			"cvolume": 107,
			"s_mschecnt": 2,
			"s_mdchecnt": 23,
			"ss_mschecnt": -21,
			"s_mschevol": "6",
			"s_mdchevol": "101",
			"ss_mschevol": "-95",
			"chdegvol": "143.48",
			"chdegcnt": "109.60"
		},
		{
			"chetime": "160930",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"open": "407.55",
			"high": "407.55",
			"low": "407.50",
			"volume": "6964",
			"cvolume": 39,
			"s_mschecnt": 0,
			"s_mdchecnt": 39,
			"ss_mschecnt": -39,
			"s_mschevol": "0",
			"s_mdchevol": "39",
			"ss_mschevol": "-39",
			"chdegvol": "150.29",
			"chdegcnt": "124.68"
		},
		{
			"chetime": "160900",
			"price": "414.25",
			"sign": "2",
			"change": "8.10",
			"open": "407.60",
			"high": "414.35",
			"low": "407.60",
			"volume": "6925",
			"cvolume": 91,
			"s_mschecnt": 5,
			"s_mdchecnt": 0,
			"ss_mschecnt": 5,
			"s_mschevol": "91",
			"s_mdchevol": "0",
			"ss_mschevol": "91",
			"chdegvol": "153.23",
			"chdegcnt": "166.96"
		},
		{
			"chetime": "160830",
			"price": "407.60",
			"sign": "2",
			"change": "1.45",
			"open": "407.60",
			"high": "407.60",
			"low": "407.60",
			"volume": "6834",
			"cvolume": 5,
			"s_mschecnt": 5,
			"s_mdchecnt": 0,
			"ss_mschecnt": 5,
			"s_mschevol": "5",
			"s_mdchevol": "0",
			"ss_mschevol": "5",
			"chdegvol": "148.67",
			"chdegcnt": "162.61"
		},
		{
			"chetime": "160800",
			"price": "407.60",
			"sign": "2",
			"change": "1.45",
			"open": "414.35",
			"high": "414.35",
			"low": "407.55",
			"volume": "6829",
			"cvolume": 501,
			"s_mschecnt": 6,
			"s_mdchecnt": 6,
			"ss_mschecnt": 0,
			"s_mschevol": "6",
			"s_mdchevol": "495",
			"ss_mschevol": "-489",
			"chdegvol": "148.42",
			"chdegcnt": "158.26"
		},
		{
			"chetime": "160730",
			"price": "408.25",
			"sign": "2",
			"change": "2.10",
			"open": "407.90",
			"high": "414.35",
			"low": "407.65",
			"volume": "6328",
			"cvolume": 1660,
			"s_mschecnt": 16,
			"s_mdchecnt": 5,
			"ss_mschecnt": 11,
			"s_mschevol": "1628",
			"s_mdchevol": "32",
			"ss_mschevol": "1596",
			"chdegvol": "196.88",
			"chdegcnt": "161.47"
		},
		{
			"chetime": "160700",
			"price": "407.85",
			"sign": "2",
			"change": "1.70",
			"open": "407.80",
			"high": "407.85",
			"low": "407.75",
			"volume": "4668",
			"cvolume": 231,
			"s_mschecnt": 4,
			"s_mdchecnt": 1,
			"ss_mschecnt": 3,
			"s_mschevol": "226",
			"s_mdchevol": "5",
			"ss_mschevol": "221",
			"chdegvol": "90.56",
			"chdegcnt": "153.85"
		},
		{
			"chetime": "160630",
			"price": "407.80",
			"sign": "2",
			"change": "1.65",
			"open": "407.80",
			"high": "407.80",
			"low": "407.80",
			"volume": "4437",
			"cvolume": 12,
			"s_mschecnt": 4,
			"s_mdchecnt": 0,
			"ss_mschecnt": 4,
			"s_mschevol": "12",
			"s_mdchevol": "0",
			"ss_mschevol": "12",
			"chdegvol": "75.46",
			"chdegcnt": "151.46"
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---
