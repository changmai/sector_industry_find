# REST[주식] 프로그램
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=6b554636-7b2a-4e1a-a615-54b0c131a558

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /stock/program                    |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 프로그램매매 추이에  관한 정보를 확인할 수 있습니다.    |


## 🏷️ 프로그램매매종합조회 (t1631)
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
| Element      | 한글명          | type   | Required   | Length   | Description                     |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------------------|
| t1631InBlock | t1631InBlock | Object | Y          | -        |                                 |
| -gubun       | 구분           | String | Y          | 1        | 1:거래소2:코스닥                      |
| -dgubun      | 일자구분         | String | Y          | 1        | 1:당일조회2:기간조회                    |
| -sdate       | 시작일자         | String | Y          | 8        |                                 |
| -edate       | 종료일자         | String | Y          | 8        |                                 |
| -exchgubun   | 거래소구분코드      | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리 |


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
| t1631OutBlock  | t1631OutBlock  | Object       | Y          | -        |               |
| -cdhrem        | 매도차익미체결잔량      | Number       | Y          | 8        |               |
| -bdhrem        | 매도비차익미체결잔량     | Number       | Y          | 8        |               |
| -tcdrem        | 매도차익주문수량       | Number       | Y          | 8        |               |
| -tbdrem        | 매도비차익주문수량      | Number       | Y          | 8        |               |
| -cshrem        | 매수차익미체결잔량      | Number       | Y          | 8        |               |
| -bshrem        | 매수비차익미체결잔량     | Number       | Y          | 8        |               |
| -tcsrem        | 매수차익주문수량       | Number       | Y          | 8        |               |
| -tbsrem        | 매수비차익주문수량      | Number       | Y          | 8        |               |
| t1631OutBlock1 | t1631OutBlock1 | Object Array | Y          | -        |               |
| -offervolume   | 매도수량           | Number       | Y          | 8        |               |
| -offervalue    | 매도금액           | Number       | Y          | 12       |               |
| -bidvolume     | 매수수량           | Number       | Y          | 8        |               |
| -bidvalue      | 매수금액           | Number       | Y          | 12       |               |
| -volume        | 순매수수량          | Number       | Y          | 8        |               |
| -value         | 순매수금액          | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1631InBlock" : {
    "gubun" : "1",
    "dgubun" : "1",
    "sdate" : "",
    "edate" : ""
  }
}
```

### 💡 Response Example
```json
{
    "t1631OutBlock1": [
        {
            "bidvolume": 102,
            "volume": 99,
            "bidvalue": 6919,
            "offervalue": 479,
            "value": 6440,
            "offervolume": 3
        },
        {
            "bidvolume": 0,
            "volume": 0,
            "bidvalue": 1,
            "offervalue": 1,
            "value": 1,
            "offervolume": 0
        },
        {
            "bidvolume": 102,
            "volume": 99,
            "bidvalue": 6921,
            "offervalue": 480,
            "value": 6441,
            "offervolume": 3
        }
    ],
    "rsp_cd": "00000",
    "t1631OutBlock": {
        "tcdrem": 0,
        "cdhrem": 0,
        "tbdrem": 5,
        "bshrem": 149,
        "cshrem": 0,
        "tbsrem": 251,
        "bdhrem": 2,
        "tcsrem": 0
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 시간대별프로그램매매추이 (t1632)
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
| Element      | 한글명          | type   | Required   | Length   | Description                                       |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------------------------------------|
| t1632InBlock | t1632InBlock | Object | Y          | -        |                                                   |
| -gubun       | 구분           | String | Y          | 1        | 0@거래소1@코스닥                                        |
| -gubun1      | 금액수량구분       | String | Y          | 1        | 0:금액1:수량                                          |
| -gubun2      | 직전대비증감       | String | Y          | 1        | 1:직전대비증감                                          |
| -gubun3      | 전일구분         | String | Y          | 1        | 1:전일분                                             |
| -date        | 일자           | String | Y          | 8        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정 |
| -time        | 시간           | String | Y          | 6        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 time 값으로 설정 |
| -exchgubun   | 거래소구분코드      | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리                   |


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
| t1632OutBlock  | t1632OutBlock  | Object       | Y          | -        |               |
| -date          | 날짜CTS          | String       | Y          | 8        |               |
| -time          | 시간CTS          | String       | Y          | 6        |               |
| -idx           | IDX            | Number       | Y          | 4        |               |
| -ex_gubun      | 거래소별구분코드       | String       | Y          | 2        |               |
| t1632OutBlock1 | t1632OutBlock1 | Object Array | Y          | -        |               |
| -time          | 시간             | String       | Y          | 8        |               |
| -k200jisu      | KP200          | Number       | Y          | 6.2      |               |
| -sign          | 대비구분           | String       | Y          | 1        |               |
| -change        | 대비             | Number       | Y          | 6.2      |               |
| -k200basis     | BASIS          | Number       | Y          | 6.2      |               |
| -tot3          | 전체순매수          | Number       | Y          | 12       |               |
| -tot1          | 전체매수           | Number       | Y          | 12       |               |
| -tot2          | 전체매도           | Number       | Y          | 12       |               |
| -cha3          | 차익순매수          | Number       | Y          | 12       |               |
| -cha1          | 차익매수           | Number       | Y          | 12       |               |
| -cha2          | 차익매도           | Number       | Y          | 12       |               |
| -bcha3         | 비차익순매수         | Number       | Y          | 12       |               |
| -bcha1         | 비차익매수          | Number       | Y          | 12       |               |
| -bcha2         | 비차익매도          | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1632InBlock" : {
    "gubun" : "0",
    "gubun1" : "0",
    "gubun2" : "1",
    "gubun3" : "1",
    "date" : " ",
    "time" : " " 
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1632OutBlock": {
        "date": "20230602",
        "time": "175811",
        "idx": 19
    },
    "t1632OutBlock1": [
        {
            "bcha1": 0,
            "change": "004.59",
            "sign": "2",
            "bcha3": 0,
            "bcha2": 0,
            "k200basis": "000.28",
            "tot3": 0,
            "tot1": 0,
            "tot2": 0,
            "cha2": 0,
            "cha3": 0,
            "time": "180518",
            "cha1": 0,
            "k200jisu": "342.67"
        },
        {
            "bcha1": 0,
            "change": "004.59",
            "sign": "2",
            "bcha3": 0,
            "bcha2": 0,
            "k200basis": "000.28",
            "tot3": 0,
            "tot1": 0,
            "tot2": 0,
            "cha2": 0,
            "cha3": 0,
            "time": "175928",
            "cha1": 0,
            "k200jisu": "342.67"
        }
    ]
}

```

---

## 🏷️ 기간별프로그램매매추이 (t1633)
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
| Element      | 한글명          | type   | Required   | Length   | Description                                       |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------------------------------------|
| t1633InBlock | t1633InBlock | Object | Y          | -        |                                                   |
| -gubun       | 시장구분         | String | Y          | 1        | 0@거래소1@코스닥                                        |
| -gubun1      | 금액수량구분       | String | Y          | 1        | 0:금액1:수량                                          |
| -gubun2      | 수치누적구분       | String | Y          | 1        | 0@수치1@누적                                          |
| -gubun3      | 일주월구분        | String | Y          | 1        | 1@일2@주3@월                                         |
| -fdate       | from일자       | String | Y          | 8        |                                                   |
| -tdate       | to일자         | String | Y          | 8        |                                                   |
| -gubun4      | 직전대비증감구분     | String | Y          | 1        | 0:Default1:직전대비증감                                 |
| -date        | 날짜           | String | Y          | 8        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정 |
| -exchgubun   | 거래소구분코드      | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리                   |


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
| t1633OutBlock  | t1633OutBlock  | Object       | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -idx           | IDX            | Number       | Y          | 4        |               |
| t1633OutBlock1 | t1633OutBlock1 | Object Array | Y          | -        |               |
| -date          | 일자             | String       | Y          | 8        |               |
| -jisu          | KP200          | Number       | Y          | 6.2      |               |
| -sign          | 대비구분           | String       | Y          | 1        |               |
| -change        | 대비             | Number       | Y          | 6.2      |               |
| -tot3          | 전체순매수          | Number       | Y          | 12       |               |
| -tot1          | 전체매수           | Number       | Y          | 12       |               |
| -tot2          | 전체매도           | Number       | Y          | 12       |               |
| -cha3          | 차익순매수          | Number       | Y          | 12       |               |
| -cha1          | 차익매수           | Number       | Y          | 12       |               |
| -cha2          | 차익매도           | Number       | Y          | 12       |               |
| -bcha3         | 비차익순매수         | Number       | Y          | 12       |               |
| -bcha1         | 비차익매수          | Number       | Y          | 12       |               |
| -bcha2         | 비차익매도          | Number       | Y          | 12       |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1633InBlock" : {
    "gubun" : "0",
    "gubun1" : "0",
    "gubun2" : "0",
    "gubun3" : "1",
    "fdate" : "20230101",
    "tdate" : "20230619",
    "gubun4" : "0",
    "date" : " "
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1633OutBlock1": [
        {
            "date": "20230619",
            "bcha1": 6921,
            "change": "16.32",
            "sign": "2",
            "bcha3": 6441,
            "bcha2": 480,
            "tot3": 6441,
            "tot1": 6921,
            "tot2": 480,
            "jisu": "329.85",
            "volume": 245,
            "cha2": 0,
            "cha3": 0,
            "cha1": 0
        },
        {
            "date": "20230616",
            "bcha1": 808,
            "change": "1.98",
            "sign": "2",
            "bcha3": 282,
            "bcha2": 526,
            "tot3": 391,
            "tot1": 917,
            "tot2": 526,
            "jisu": "345.17",
            "volume": 153589,
            "cha2": 0,
            "cha3": 109,
            "cha1": 109
        }
    ],
    "t1633OutBlock": {
        "date": "20230102",
        "idx": 115
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 종목별프로그램매매동향 (t1636)
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
| Element      | 한글명          | type   | Required   | Length   | Description                                          |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------------------------|
| t1636InBlock | t1636InBlock | Object | Y          | -        |                                                      |
| -gubun       | 구분           | String | Y          | 1        | 0:코스피1:코스닥                                           |
| -gubun1      | 금액수량구분       | String | Y          | 1        | 0:수량1:금액                                             |
| -gubun2      | 정렬기준         | String | Y          | 1        | 0:시가총액비중1:순매수상위2:순매도상위3:매도상위4:매수상위                   |
| -shcode      | 종목코드         | String | Y          | 6        |                                                      |
| -cts_idx     | IDXCTS       | Number | Y          | 4        | 처음 조회시는 Space연속 조회시에 이전 조회한 OutBlock의 cts_idx 값으로 설정 |
| -exchgubun   | 거래소구분코드      | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리                      |


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
| t1636OutBlock  | t1636OutBlock  | Object       | Y          | -        |               |
| -cts_idx       | IDXCTS         | Number       | Y          | 4        |               |
| t1636OutBlock1 | t1636OutBlock1 | Object Array | Y          | -        |               |
| -rank          | 순위             | Number       | Y          | 8        |               |
| -hname         | 종목명            | String       | Y          | 20       |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 대비구분           | String       | Y          | 1        |               |
| -change        | 대비             | Number       | Y          | 8        |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -svalue        | 순매수금액          | Number       | Y          | 12       |               |
| -offervalue    | 매도금액           | Number       | Y          | 12       |               |
| -stksvalue     | 매수금액           | Number       | Y          | 12       |               |
| -svolume       | 순매수수량          | Number       | Y          | 12       |               |
| -offervolume   | 매도수량           | Number       | Y          | 12       |               |
| -stksvolume    | 매수수량           | Number       | Y          | 12       |               |
| -sgta          | 시가총액           | Number       | Y          | 15       |               |
| -rate          | 비중             | Number       | Y          | 6.2      |               |
| -shcode        | 종목코드           | String       | Y          | 6        |               |
| -ex_shcode     | 거래소별단축코드       | String       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "t1636InBlock" : {
    "gubun":"0",
    "gubun1":"0",
    "gubun2":"0",
    "shcode":"001200",
    "cts_idx": 0
  }
}
```

### 💡 Response Example
```json
{
    "t1636OutBlock": {
        "cts_idx": 312
    },
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1636OutBlock1": [
        {
            "stksvalue": 0,
            "change": 25,
            "shcode": "001200",
            "sign": "2",
            "diff": "0.68",
            "offervalue": 0,
            "offervolume": 74893,
            "volume": 322192,
            "sgta": 356952750330,
            "rate": "000.02",
            "price": 3685,
            "stksvolume": 124828,
            "svalue": 0,
            "rank": 293,
            "svolume": 49935,
            "hname": "유진투자증권"
        },
        {
            "stksvalue": 0,
            "change": 20,
            "shcode": "003610",
            "sign": "5",
            "diff": "-0.27",
            "offervalue": 0,
            "offervolume": 1532,
            "volume": 76162,
            "sgta": 311431702400,
            "rate": "000.02",
            "price": 7360,
            "stksvolume": 7949,
            "svalue": 0,
            "rank": 312,
            "svolume": 6417,
            "hname": "방림"
        }
    ]
}
```

---

## 🏷️ 종목별프로그램매매추이 (t1637)
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
| Element      | 한글명              | type   | Required   | Length   | Description                                        |
|:-------------|:-----------------|:-------|:-----------|:---------|:---------------------------------------------------|
| t1637InBlock | t1637InBlock     | Object | Y          | -        |                                                    |
| -gubun1      | 수량금액구분(0:수량1:금액) | String | Y          | 1        |                                                    |
| -gubun2      | 시간일별구분(0:시간1:일자) | String | Y          | 1        |                                                    |
| -shcode      | 종목코드             | String | Y          | 6        |                                                    |
| -date        | 일자               | String | Y          | 8        | 일별 연속 조회시에 이전 조회한 OutBlock1의 마지막 Row의 date 값으로 설정  |
| -time        | 시간               | String | Y          | 6        | 시간별 연속 조회시에 이전 조회한 OutBlock1의 마지막 Row의 time 값으로 설정 |
| -cts_idx     | IDXCTS(9999:차트)  | Number | Y          | 4        | 차트 조회시에만 9999로 입력                                  |
| -exchgubun   | 거래소구분코드          | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리                    |


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
| t1637OutBlock  | t1637OutBlock  | Object       | Y          | -        |               |
| -cts_idx       | IDXCTS         | Number       | Y          | 4        |               |
| t1637OutBlock1 | t1637OutBlock1 | Object Array | Y          | -        |               |
| -date          | 일자             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 대비구분           | String       | Y          | 1        |               |
| -change        | 대비             | Number       | Y          | 8        |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -svalue        | 순매수금액          | Number       | Y          | 15       |               |
| -offervalue    | 매도금액           | Number       | Y          | 15       |               |
| -stksvalue     | 매수금액           | Number       | Y          | 15       |               |
| -svolume       | 순매수수량          | Number       | Y          | 12       |               |
| -offervolume   | 매도수량           | Number       | Y          | 12       |               |
| -stksvolume    | 매수수량           | Number       | Y          | 12       |               |
| -shcode        | 종목코드           | String       | Y          | 6        |               |
| -ex_shcode     | 거래소별단축코드       | String       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "t1637InBlock" : {
    "gubun1" : "0",
    "gubun2" : "0",
    "shcode" : "001200",
    "date" : "",
    "time" : "",
    "cts_idx" : 9999
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1637OutBlock": {
        "cts_idx": 0
    },
    "t1637OutBlock1": [
        {
            "date": "20230605",
            "stksvalue": 0,
            "change": 0,
            "shcode": "A00120",
            "sign": "",
            "diff": "0",
            "offervalue": 0,
            "offervolume": 0,
            "volume": 0,
            "price": 3685,
            "stksvolume": 0,
            "svalue": 188914,
            "svolume": 49935,
            "time": "102700"
        },
        {
            "date": "20230605",
            "stksvalue": 0,
            "change": 0,
            "shcode": "A00120",
            "sign": "",
            "diff": "0",
            "offervalue": 0,
            "offervolume": 0,
            "volume": 0,
            "price": 3645,
            "stksvolume": 0,
            "svalue": -74311,
            "svolume": -20307,
            "time": "090100"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 프로그램매매종합조회(미니) (t1640)
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
| Element      | 한글명          | type   | Required   | Length   | Description                                        |
|:-------------|:-------------|:-------|:-----------|:---------|:---------------------------------------------------|
| t1640InBlock | t1640InBlock | Object | Y          | -        |                                                    |
| -gubun       | 구분           | String | Y          | 2        | 11@거래소전체12@거래소차익13@거래소비차익21@코스닥전체22@코스닥차익23@코스닥비차익 |
| -exchgubun   | 거래소구분코드      | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리                    |


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
| t1640OutBlock | t1640OutBlock | Object | Y          | -        |               |
| -offervolume  | 매도수량          | Number | Y          | 8        |               |
| -bidvolume    | 매수수량          | Number | Y          | 8        |               |
| -volume       | 순매수수량         | Number | Y          | 8        |               |
| -offerdiff    | 매도증감          | Number | Y          | 8        |               |
| -biddiff      | 매수증감          | Number | Y          | 8        |               |
| -sundiff      | 순매수증감         | Number | Y          | 8        |               |
| -basis        | 베이시스          | Number | Y          | 6.2      |               |
| -offervalue   | 매도금액          | Number | Y          | 12       |               |
| -bidvalue     | 매수금액          | Number | Y          | 12       |               |
| -value        | 순매수금액         | Number | Y          | 12       |               |
| -offervaldiff | 매도금액증감        | Number | Y          | 12       |               |
| -bidvaldiff   | 매수금액증감        | Number | Y          | 12       |               |
| -sunvaldiff   | 순매수증감         | Number | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1640InBlock" : {
    "gubun" : "11"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "조회완료",
    "t1640OutBlock": {
        "sundiff": 6,
        "bidvaldiff": "000000000250",
        "bidvalue": "000000786684",
        "offervalue": "000000758788",
        "basis": "000.01",
        "offervolume": 36452,
        "offerdiff": 10,
        "bidvolume": 39833,
        "volume": 3381,
        "sunvaldiff": "-00000000100",
        "biddiff": 16,
        "value": "000000027896",
        "offervaldiff": "000000000350"
    }
}
```

---

## 🏷️ 시간대별프로그램매매추이(차트) (t1662)
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
| Element      | 한글명          | type   | Required   | Length   | Description                     |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------------------|
| t1662InBlock | t1662InBlock | Object | Y          | -        |                                 |
| -gubun       | 구분           | String | Y          | 1        | 0@코스피1@코스닥                      |
| -gubun1      | 금액수량구분       | String | Y          | 1        | 0:금액1:수량                        |
| -gubun3      | 전일구분         | String | Y          | 1        | 0:당일1:전일                        |
| -exchgubun   | 거래소구분코드      | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리 |


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
| t1662OutBlock | t1662OutBlock | Object Array | Y          | -        |               |
| -time         | 시간            | String       | Y          | 6        |               |
| -k200jisu     | KP200         | Number       | Y          | 6.2      |               |
| -sign         | 대비구분          | String       | Y          | 1        |               |
| -change       | 대비            | Number       | Y          | 6.2      |               |
| -k200basis    | BASIS         | Number       | Y          | 6.2      |               |
| -tot3         | 전체순매수         | Number       | Y          | 12       |               |
| -tot1         | 전체매수          | Number       | Y          | 12       |               |
| -tot2         | 전체매도          | Number       | Y          | 12       |               |
| -cha3         | 차익순매수         | Number       | Y          | 12       |               |
| -cha1         | 차익매수          | Number       | Y          | 12       |               |
| -cha2         | 차익매도          | Number       | Y          | 12       |               |
| -bcha3        | 비차익순매수        | Number       | Y          | 12       |               |
| -bcha1        | 비차익매수         | Number       | Y          | 12       |               |
| -bcha2        | 비차익매도         | Number       | Y          | 12       |               |
| -volume       | 거래량           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t1662InBlock" : {
    "gubun" : "0",
    "gubun1" : "0",
    "gubun3" : "0"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1662OutBlock": [
        {
            "bcha1": 768966,
            "change": "001.08",
            "sign": "2",
            "bcha3": 15815,
            "bcha2": 753151,
            "k200basis": "000.27",
            "tot3": 27896,
            "tot1": 786684,
            "tot2": 758788,
            "volume": 24,
            "cha2": 5637,
            "cha3": 12081,
            "time": "102600",
            "cha1": 17718,
            "k200jisu": "343.75"
        },
        {
            "bcha1": 12327,
            "change": "000.00",
            "sign": "3",
            "bcha3": -7637,
            "bcha2": 19964,
            "k200basis": "002.08",
            "tot3": -7637,
            "tot1": 12327,
            "tot2": 19964,
            "volume": 0,
            "cha2": 0,
            "cha3": 0,
            "time": "090000",
            "cha1": 0,
            "k200jisu": "342.67"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}

```

---
