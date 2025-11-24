# REST[해외선물] 차트
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=c1ef0e8b-4666-4d8c-a77f-6ab488cfdb39&api_id=906d2d0a-7a6d-4ecc-b574-ca2154a70bca

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /overseas-futureoption/chart      |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 해외선물옵션 기간별 차트를 확인할 수 있습니다.        |


## 🏷️ 해외선물차트 분봉 조회 (o3103)
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
| o3103InBlock | o3103InBlock | Object | Y          | -        |                               |
| -shcode      | 단축코드         | String | Y          | 8        | ex) ADU13                     |
| -ncnt        | N분주기         | Number | Y          | 4        | ex) 0(30초), 1(1분), 30(30분), … |
| -readcnt     | 조회건수         | Number | Y          | 4        |                               |
| -cts_date    | 연속일자         | String | Y          | 8        |                               |
| -cts_time    | 연속시간         | String | Y          | 6        |                               |


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
| o3103OutBlock  | o3103OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 8        |               |
| -timediff      | 시차             | Number       | Y          | 4        |               |
| -readcnt       | 조회건수           | Number       | Y          | 4        |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -cts_time      | 연속시간           | String       | Y          | 6        |               |
| o3103OutBlock1 | o3103OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 현지시간           | String       | Y          | 6        |               |
| -open          | 시가             | Number       | Y          | 15.9     |               |
| -high          | 고가             | Number       | Y          | 15.9     |               |
| -low           | 저가             | Number       | Y          | 15.9     |               |
| -close         | 종가             | Number       | Y          | 15.9     |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "o3103InBlock": {
    "shcode": "ADM23",
    "ncnt": 1,
    "readcnt": 20,
    "cts_date": "",
    "cts_time": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3103OutBlock": {
        "cts_date": "20230612",
        "readcnt": 20,
        "shcode": "ADM23",
        "timediff": -14,
        "cts_time": "234700"
    },
    "o3103OutBlock1": [
        {
            "date": "20230613",
            "volume": 51,
            "high": "0.67680",
            "low": "0.67670",
            "time": "000600",
            "close": "0.67670",
            "open": "0.67675"
        },
        {
            "date": "20230613",
            "volume": 49,
            "high": "0.67680",
            "low": "0.67655",
            "time": "000500",
            "close": "0.67680",
            "open": "0.67655"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물차트(일주월) 조회 (o3108)
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
| Element      | 한글명          | type   | Required   | Length   | Description          |
|:-------------|:-------------|:-------|:-----------|:---------|:---------------------|
| o3108InBlock | o3108InBlock | Object | Y          | -        |                      |
| -shcode      | 단축코드         | String | Y          | 16       | ex) ADU13            |
| -gubun       | 주기구분         | String | Y          | 1        | ex) 0(일), 1(주), 2(월) |
| -qrycnt      | 요청건수         | Number | Y          | 4        |                      |
| -sdate       | 시작일자         | String | Y          | 8        |                      |
| -edate       | 종료일자         | String | Y          | 8        | ex) 조회당일             |
| -cts_date    | 연속일자         | String | Y          | 8        |                      |


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
| o3108OutBlock  | o3108OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 16       |               |
| -jisiga        | 전일시가           | Number       | Y          | 15.9     |               |
| -jihigh        | 전일고가           | Number       | Y          | 15.9     |               |
| -jilow         | 전일저가           | Number       | Y          | 15.9     |               |
| -jiclose       | 존일종가           | Number       | Y          | 15.9     |               |
| -jivolume      | 전일거래량          | Number       | Y          | 12       |               |
| -disiga        | 당일시가           | Number       | Y          | 15.9     |               |
| -dihigh        | 당일고가           | Number       | Y          | 15.9     |               |
| -dilow         | 당일저가           | Number       | Y          | 15.9     |               |
| -diclose       | 당일종가           | Number       | Y          | 15.9     |               |
| -mk_stime      | 장시작시간          | String       | Y          | 6        |               |
| -mk_etime      | 장마감시간          | String       | Y          | 6        |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| o3108OutBlock1 | o3108OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -open          | 시가             | Number       | Y          | 15.9     |               |
| -high          | 고가             | Number       | Y          | 15.9     |               |
| -low           | 저가             | Number       | Y          | 15.9     |               |
| -close         | 종가             | Number       | Y          | 15.9     |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "o3108InBlock": {
    "shcode": "ADM23",
    "gubun": "0",
    "qrycnt": 20,
    "sdate": "20230502",
    "edate": "20230601",
    "cts_date": ""
  }
}
```

### 💡 Response Example
```json
{
    "o3108OutBlock": {
        "cts_date": null,
        "shcode": null,
        "jivolume": null,
        "mk_etime": null,
        "jisiga": null,
        "jilow": null,
        "diclose": null,
        "disiga": null,
        "dihigh": null,
        "jihigh": null,
        "rec_count": null,
        "dilow": null,
        "mk_stime": null,
        "jiclose": null
    },
    "rsp_cd": "00000",
    "o3108OutBlock1": [
        {
            "date": "20230505",
            "volume": 93733,
            "high": "0.67675",
            "low": "0.66990",
            "close": "0.67660",
            "open": "0.67035"
        },
        {
            "date": "20230601",
            "volume": 89700,
            "high": "0.65855",
            "low": "0.64880",
            "close": "0.65770",
            "open": "0.65075"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물 차트 NTick 체결 조회 (o3117)
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
| o3117InBlock | o3117InBlock | Object | Y          | -        |               |
| -shcode      | 단축코드         | String | Y          | 8        |               |
| -ncnt        | 단위           | Number | Y          | 4        |               |
| -qrycnt      | 건수           | Number | Y          | 4        |               |
| -cts_seq     | 순번CTS        | String | Y          | 10       |               |
| -cts_daygb   | 당일구분CTS      | String | Y          | 2        |               |


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
| o3117OutBlock  | o3117OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 8        |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| -cts_seq       | 순번CTS          | String       | Y          | 10       |               |
| -cts_daygb     | 당일구분CTS        | String       | Y          | 2        |               |
| o3117OutBlock1 | o3117OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -open          | 시가             | Number       | Y          | 15.9     |               |
| -high          | 고가             | Number       | Y          | 15.9     |               |
| -low           | 저가             | Number       | Y          | 15.9     |               |
| -close         | 종가             | Number       | Y          | 15.9     |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "o3117InBlock": {
    "shcode": "ADM23",
    "ncnt": 0,
    "qrycnt": 20,
    "cts_seq": "",
    "cts_daygb": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3117OutBlock": {
        "shcode": "ADM23",
        "rec_count": 20,
        "cts_daygb": "0",
        "cts_seq": "4826"
    },
    "rsp_msg": "조회완료",
    "o3117OutBlock1": [
        {
            "date": "20230613",
            "volume": 1,
            "high": "0.67670",
            "low": "0.67670",
            "time": "000533",
            "close": "0.67670",
            "open": "0.67670"
        },
        {
            "date": "20230613",
            "volume": 1,
            "high": "0.67665",
            "low": "0.67665",
            "time": "000438",
            "close": "0.67665",
            "open": "0.67665"
        }
    ]
}
```

---

## 🏷️ 해외선물옵션차트용NTick(고정형)-API용 (o3139)
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
| Element      | 한글명          | type   | Required   | Length   | Description      |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------|
| o3139InBlock | o3139InBlock | Object | Y          | -        |                  |
| -mktgb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션) |
| -shcode      | 단축코드         | String | Y          | 16       | ex) 2ESF16_1915  |
| -ncnt        | 단위           | Number | Y          | 4        |                  |
| -qrycnt      | 건수           | Number | Y          | 4        |                  |
| -cts_seq     | 순번CTS        | String | Y          | 10       |                  |
| -cts_daygb   | 당일구분CTS      | String | Y          | 2        |                  |


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
| o3139OutBlock  | o3139OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 16       |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| -cts_seq       | 연속시간           | String       | Y          | 10       |               |
| -cts_daygb     | 연속당일구분         | String       | Y          | 2        |               |
| -last_count    | 마지막Tick건수      | Number       | Y          | 4        |               |
| o3139OutBlock1 | o3139OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -open          | 시가             | Number       | Y          | 15.8     |               |
| -high          | 고가             | Number       | Y          | 15.8     |               |
| -low           | 저가             | Number       | Y          | 15.8     |               |
| -close         | 종가             | Number       | Y          | 15.8     |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "o3139InBlock": {
    "mktgb": "F",
    "shcode": "ADM23",
    "ncnt": 1,
    "qrycnt": 20,
    "cts_seq": "",
    "cts_daygb": ""
  }
}
```

### 💡 Response Example
```json
{
    "o3139OutBlock1": [
        {
            "date": "20230613",
            "volume": 1,
            "high": "0.67670",
            "low": "0.67670",
            "time": "000533",
            "close": "0.67670",
            "open": "0.67670"
        },
        {
            "date": "20230613",
            "volume": 1,
            "high": "0.67665",
            "low": "0.67665",
            "time": "000438",
            "close": "0.67665",
            "open": "0.67665"
        }
    ],
    "rsp_cd": "00000",
    "o3139OutBlock": {
        "last_count": null,
        "shcode": null,
        "rec_count": null,
        "cts_daygb": null,
        "cts_seq": null
    },
    "rsp_msg": "조회완료"
}
```

---
