# REST[업종] 차트
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=f82999f4-eb1a-4ead-a0b1-a4386e8721ab&api_id=5b483d74-407c-4760-8452-1b2b1dc1dcde

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /indtp/chart                      |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 업종 기간별 차트를 확인할 수 있는 서비스입니다.       |


## 🏷️ 업종차트(종합) (t4203)
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
| Element      | 한글명                          | type   | Required   | Length   | Description                                            |
|:-------------|:-----------------------------|:-------|:-----------|:---------|:-------------------------------------------------------|
| t4203InBlock | t4203InBlock                 | Object | Y          | -        |                                                        |
| -shcode      | 단축코드                         | String | Y          | 3        |                                                        |
| -gubun       | 주기구분(0:틱1:분2:일3:주4:월)        | String | Y          | 1        | 0:틱1:분2:일3:주4:월                                        |
| -ncnt        | 틱개수                          | Number | Y          | 4        |                                                        |
| -qrycnt      | 건수                           | Number | Y          | 4        | 1 이상 500 이하값만 유효                                       |
| -tdgb        | 당일구분(0:전체1:당일만)              | String | Y          | 1        | 0:전체1:당일만                                              |
| -sdate       | 시작일자                         | String | Y          | 8        | 조회구간종료일Space:기본값                                       |
| -edate       | 종료일자                         | String | Y          | 8        | 처음조회기준일(LE)처음조회일 경우 이 값 기준으로 조회                        |
| -cts_date    | 연속일자                         | String | Y          | 8        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 cts_date 값으로 설정  |
| -cts_time    | 연속시간                         | String | Y          | 10       | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정  |
| -cts_daygb   | 연속당일구분(0:연속전체1:연속당일만2:연속전일만) | String | Y          | 1        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 cts_daygb 값으로 설정 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                                   |
|:---------------|:---------------|:-------------|:-----------|:---------|:----------------------------------------------|
| t4203OutBlock  | t4203OutBlock  | Object       | Y          | -        |                                               |
| -shcode        | 단축코드           | String       | Y          | 3        |                                               |
| -jisiga        | 전일시가           | Number       | Y          | 7.2      |                                               |
| -jihigh        | 전일고가           | Number       | Y          | 7.2      |                                               |
| -jilow         | 전일저가           | Number       | Y          | 7.2      |                                               |
| -jiclose       | 전일종가           | Number       | Y          | 7.2      |                                               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |                                               |
| -disiga        | 당일시가           | Number       | Y          | 7.2      |                                               |
| -dihigh        | 당일고가           | Number       | Y          | 7.2      |                                               |
| -dilow         | 당일저가           | Number       | Y          | 7.2      |                                               |
| -diclose       | 당일종가           | Number       | Y          | 7.2      |                                               |
| -disvalue      | 당일거래대금         | Number       | Y          | 12       |                                               |
| -cts_date      | 연속일자           | String       | Y          | 8        | 연속조회키연속 조회시 이 값을 InBlock의 cts_date 필드에 넣어준다.  |
| -cts_time      | 연속시간           | String       | Y          | 10       | 연속조회키연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다.  |
| -cts_daygb     | 연속당일구분         | String       | Y          | 1        | 연속조회키연속 조회시 이 값을 InBlock의 cts_daygb 필드에 넣어준다. |
| t4203OutBlock1 | t4203OutBlock1 | Object Array | Y          | -        |                                               |
| -date          | 날짜             | String       | Y          | 8        |                                               |
| -time          | 시간             | String       | Y          | 6        |                                               |
| -open          | 시가             | Number       | Y          | 7.2      |                                               |
| -high          | 고가             | Number       | Y          | 7.2      |                                               |
| -low           | 저가             | Number       | Y          | 7.2      |                                               |
| -close         | 종가             | Number       | Y          | 7.2      |                                               |
| -jdiff_vol     | 거래량            | Number       | Y          | 12       |                                               |
| -value         | 거래대금           | Number       | Y          | 12       |                                               |


### 💡 Request Example
```json
{
  "t4203InBlock": {
    "shcode": "001",
    "gubun": "1",
    "ncnt": 1,
    "qrycnt": 1,
    "tdgb": "1",
    "sdate": " ",
    "edate": "",
    "cts_date": " ",
    "cts_time": " ",
    "cts_daygb": " "
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t4203OutBlock": {
        "cts_date": "20230605",
        "shcode": "001",
        "jivolume": 569620,
        "cts_daygb": "1",
        "disvalue": 3886266,
        "jisiga": "2586.27",
        "jilow": "2583.88",
        "diclose": "2610.85",
        "disiga": "2617.43",
        "dihigh": "2617.58",
        "jihigh": "2601.38",
        "dilow": "2610.40",
        "jiclose": "2601.36",
        "cts_time": "102700 026"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t4203OutBlock1": [
        {
            "date": "20230605",
            "jdiff_vol": 0,
            "high": "2610.85",
            "low": "2610.85",
            "time": "102800",
            "close": "2610.85",
            "value": 0,
            "open": "2610.85"
        }
    ]
}
```

---

## 🏷️ 업종차트(틱/n틱) (t8417)
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
| t8417InBlock | t8417InBlock            | Object | Y          | -        |                                          |
| -shcode      | 단축코드                    | String | Y          | 3        |                                          |
| -ncnt        | 단위(n틱)                  | Number | Y          | 4        |                                          |
| -qrycnt      | 요청건수(최대-압축:2000비압축:500) | Number | Y          | 4        | 요청건수                                     |
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
| -cts_time    | 연속시간                    | String | Y          | 10       |                                          |
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
| t8417OutBlock  | t8417OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 3        |               |
| -jisiga        | 전일시가           | Number       | Y          | 7.2      |               |
| -jihigh        | 전일고가           | Number       | Y          | 7.2      |               |
| -jilow         | 전일저가           | Number       | Y          | 7.2      |               |
| -jiclose       | 전일종가           | Number       | Y          | 7.2      |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 7.2      |               |
| -dihigh        | 당일고가           | Number       | Y          | 7.2      |               |
| -dilow         | 당일저가           | Number       | Y          | 7.2      |               |
| -diclose       | 당일종가           | Number       | Y          | 7.2      |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -cts_time      | 연속시간           | String       | Y          | 10       |               |
| -s_time        | 장시작시간(HHMMSS)  | String       | Y          | 6        |               |
| -e_time        | 장종료시간(HHMMSS)  | String       | Y          | 6        |               |
| -dshmin        | 동시호가처리시간(MM:분) | String       | Y          | 2        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| t8417OutBlock1 | t8417OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -open          | 시가             | Number       | Y          | 7.2      |               |
| -high          | 고가             | Number       | Y          | 7.2      |               |
| -low           | 저가             | Number       | Y          | 7.2      |               |
| -close         | 종가             | Number       | Y          | 7.2      |               |
| -jdiff_vol     | 거래량            | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8417InBlock": {
    "shcode": "001",
    "ncnt": 1,
    "qrycnt": 1,
    "nday": "0",
    "sdate": " ",
    "stime": "",
    "edate": "99999999",
    "etime": "",
    "cts_date": " ",
    "cts_time": "",
    "comp_yn": "N"
  }
}
```

### 💡 Response Example
```json
{
    "t8417OutBlock1": [
        {
            "date": "20230605",
            "jdiff_vol": 215,
            "high": "2610.85",
            "low": "2610.85",
            "time": "102700",
            "close": "2610.85",
            "open": "2610.85"
        }
    ],
    "rsp_cd": "00000",
    "t8417OutBlock": {
        "cts_date": "20230605",
        "shcode": "001",
        "jivolume": 569620,
        "e_time": "153000",
        "jisiga": "2586.27",
        "jilow": "2583.88",
        "diclose": "2610.85",
        "dshmin": "10",
        "disiga": "2617.43",
        "s_time": "090000",
        "dihigh": "2617.58",
        "jihigh": "2601.38",
        "rec_count": 1,
        "dilow": "2610.40",
        "jiclose": "2601.36",
        "cts_time": "102650"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 업종차트(N분) (t8418)
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
| t8418InBlock | t8418InBlock            | Object | Y          | -        |                                                                      |
| -shcode      | 단축코드                    | String | Y          | 3        |                                                                      |
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
| t8418OutBlock  | t8418OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 3        |               |
| -jisiga        | 전일시가           | Number       | Y          | 7.2      |               |
| -jihigh        | 전일고가           | Number       | Y          | 7.2      |               |
| -jilow         | 전일저가           | Number       | Y          | 7.2      |               |
| -jiclose       | 전일종가           | Number       | Y          | 7.2      |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 7.2      |               |
| -dihigh        | 당일고가           | Number       | Y          | 7.2      |               |
| -dilow         | 당일저가           | Number       | Y          | 7.2      |               |
| -diclose       | 당일종가           | Number       | Y          | 7.2      |               |
| -disvalue      | 당일거래대금         | Number       | Y          | 12       |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -cts_time      | 연속시간           | String       | Y          | 10       |               |
| -s_time        | 업종시작시간(HHMMSS) | String       | Y          | 6        |               |
| -e_time        | 업종종료시간(HHMMSS) | String       | Y          | 6        |               |
| -dshmin        | 동시호가처리시간(MM:분) | String       | Y          | 2        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| t8418OutBlock1 | t8418OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -open          | 시가             | Number       | Y          | 7.2      |               |
| -high          | 고가             | Number       | Y          | 7.2      |               |
| -low           | 저가             | Number       | Y          | 7.2      |               |
| -close         | 종가             | Number       | Y          | 7.2      |               |
| -jdiff_vol     | 거래량            | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8418InBlock": {
    "shcode": "001",
    "ncnt": 0,
    "qrycnt": 5,
    "nday": "0",
    "sdate": " ",
    "stime": "",
    "edate": "99999999",
    "etime": "",
    "cts_date": " ",
    "cts_time": "",
    "comp_yn": "N"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8418OutBlock": {
        "cts_date": "20230605",
        "shcode": "001",
        "jivolume": 569620,
        "e_time": "153000",
        "disvalue": 3886266,
        "jisiga": "2586.27",
        "jilow": "2583.88",
        "diclose": "2610.85",
        "dshmin": "10",
        "disiga": "2617.43",
        "s_time": "090000",
        "dihigh": "2617.58",
        "jihigh": "2601.38",
        "rec_count": 5,
        "dilow": "2610.40",
        "jiclose": "2601.36",
        "cts_time": "102300"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t8418OutBlock1": [
        {
            "date": "20230605",
            "jdiff_vol": 1673,
            "high": "2611.59",
            "low": "2610.75",
            "time": "102400",
            "close": "2610.97",
            "value": 19176,
            "open": "2611.42"
        },
        {
            "date": "20230605",
            "jdiff_vol": 1509,
            "high": "2611.75",
            "low": "2610.70",
            "time": "102500",
            "close": "2611.50",
            "value": 15544,
            "open": "2610.70"
        },
        {
            "date": "20230605",
            "jdiff_vol": 1316,
            "high": "2611.97",
            "low": "2610.80",
            "time": "102600",
            "close": "2610.80",
            "value": 18831,
            "open": "2611.97"
        },
        {
            "date": "20230605",
            "jdiff_vol": 1418,
            "high": "2611.45",
            "low": "2610.53",
            "time": "102700",
            "close": "2610.85",
            "value": 15265,
            "open": "2611.30"
        },
        {
            "date": "20230605",
            "jdiff_vol": 0,
            "high": "2610.85",
            "low": "2610.85",
            "time": "102800",
            "close": "2610.85",
            "value": 0,
            "open": "2610.85"
        }
    ]
}
```

---

## 🏷️ 업종차트(일주월) (t8419)
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
| t8419InBlock | t8419InBlock            | Object | Y          | -        |                                                                      |
| -shcode      | 단축코드                    | String | Y          | 3        |                                                                      |
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
| t8419OutBlock  | t8419OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 3        |               |
| -jisiga        | 전일시가           | Number       | Y          | 7.2      |               |
| -jihigh        | 전일고가           | Number       | Y          | 7.2      |               |
| -jilow         | 전일저가           | Number       | Y          | 7.2      |               |
| -jiclose       | 전일종가           | Number       | Y          | 7.2      |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 7.2      |               |
| -dihigh        | 당일고가           | Number       | Y          | 7.2      |               |
| -dilow         | 당일저가           | Number       | Y          | 7.2      |               |
| -diclose       | 당일종가           | Number       | Y          | 7.2      |               |
| -disvalue      | 당일거래대금         | Number       | Y          | 12       |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -s_time        | 업종시작시간         | String       | Y          | 6        |               |
| -e_time        | 업종종료시간         | String       | Y          | 6        |               |
| -dshmin        | 동시호가처리시간(MM:분) | String       | Y          | 2        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| t8419OutBlock1 | t8419OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -open          | 시가             | Number       | Y          | 7.2      |               |
| -high          | 고가             | Number       | Y          | 7.2      |               |
| -low           | 저가             | Number       | Y          | 7.2      |               |
| -close         | 종가             | Number       | Y          | 7.2      |               |
| -jdiff_vol     | 거래량            | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8419InBlock": {
    "shcode": "001",
    "gubun": "2",
    "qrycnt": 5,
    "sdate": " ",
    "edate": "99999999",
    "cts_date": " ",
    "comp_yn": "N"
  }
}
```

### 💡 Response Example
```json
{
    "t8419OutBlock": {
        "cts_date": "20230526",
        "shcode": "001",
        "jivolume": 569620,
        "e_time": "153000",
        "disvalue": 3886266,
        "jisiga": "2586.27",
        "jilow": "2583.88",
        "diclose": "2610.85",
        "dshmin": "10",
        "disiga": "2617.43",
        "s_time": "090000",
        "dihigh": "2617.58",
        "jihigh": "2601.38",
        "rec_count": 5,
        "dilow": "2610.40",
        "jiclose": "2601.36"
    },
    "rsp_cd": "00000",
    "t8419OutBlock1": [
        {
            "date": "20230530",
            "jdiff_vol": 641647,
            "high": "2586.22",
            "low": "2574.82",
            "close": "2585.52",
            "value": 11066254,
            "open": "2582.41"
        },
        {
            "date": "20230531",
            "jdiff_vol": 686187,
            "high": "2596.31",
            "low": "2575.98",
            "close": "2577.12",
            "value": 15135111,
            "open": "2586.03"
        },
        {
            "date": "20230601",
            "jdiff_vol": 675233,
            "high": "2580.15",
            "low": "2565.00",
            "close": "2569.17",
            "value": 9168502,
            "open": "2572.56"
        },
        {
            "date": "20230602",
            "jdiff_vol": 569620,
            "high": "2601.38",
            "low": "2583.88",
            "close": "2601.36",
            "value": 9383535,
            "open": "2586.27"
        },
        {
            "date": "20230605",
            "jdiff_vol": 263380,
            "high": "2617.58",
            "low": "2610.40",
            "close": "2610.85",
            "value": 3886266,
            "open": "2617.43"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---
