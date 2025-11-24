# REST[주식] 섹터
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=8f027fa6-4177-43e3-9a7a-a76873efd47c

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /stock/sector                     |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 섹터별 종목조회 및 시세를 확인할 수 있는 서비스입니다.   |


## 🏷️ 테마별종목 (t1531)
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
| Element      | 한글명          | type   | Required   | Length   | Description       |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------|
| t1531InBlock | t1531InBlock | Object | Y          | -        |                   |
| -tmname      | 테마명          | String | Y          | 36       | t8425조회하여 확인 후 입력 |
| -tmcode      | 테마코드         | String | Y          | 4        | t8425조회하여 확인 후 입력 |


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
| t1531OutBlock | t1531OutBlock | Object Array | Y          | -        |               |
| -tmname       | 테마명           | String       | Y          | 36       |               |
| -avgdiff      | 평균등락율         | Number       | Y          | 6.2      |               |
| -tmcode       | 테마코드          | String       | Y          | 4        |               |


### 💡 Request Example
```json
{
   "t1531InBlock" :{
      "tmname" : "",
      "tmcode" : ""
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1531OutBlock": [
        {
            "tmname": "화폐\/금융자동화기기(디지털화폐 등)",
            "avgdiff": "0.49",
            "tmcode": "0008"
        },
        {
            "tmname": "OLED(유기 발광 다이오드)",
            "avgdiff": "-0.13",
            "tmcode": "0009"
        },
        {
            "tmname": "반도체 장비",
            "avgdiff": "-0.59",
            "tmcode": "0012"
        },
        {
            "tmname": "페라이트",
            "avgdiff": "0.74",
            "tmcode": "0534"
        }
    ],
    "rsp_msg": "조회완료"
}

```

---

## 🏷️ 종목별테마 (t1532)
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
| t1532InBlock | t1532InBlock | Object | Y          | -        |               |
| -shcode      | 종목코드         | String | Y          | 6        |               |


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
| t1532OutBlock | t1532OutBlock | Object Array | Y          | -        |               |
| -tmname       | 테마명           | String       | Y          | 36       |               |
| -avgdiff      | 평균등락율         | Number       | Y          | 6.2      |               |
| -tmcode       | 테마코드          | String       | Y          | 4        |               |


### 💡 Request Example
```json


{
  "t1532InBlock" : {
    "shcode" : "078020"
  }
}



```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1532OutBlock": [
        {
            "tmname": "증권",
            "avgdiff": "000.65",
            "tmcode": "0151"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 특이테마 (t1533)
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
| t1533InBlock | t1533InBlock | Object | Y          | -        |               |
| -gubun       | 구분           | String | Y          | 1        | 1@상승율 상위      |
|              |              |        |            |          | 2@하락율 상위      |
|              |              |        |            |          | 3@거래증가율 상위    |
|              |              |        |            |          | 4@거래증가율 하위    |
|              |              |        |            |          | 5@상승종목비율 상위   |
|              |              |        |            |          | 6@상승종목비율 하위   |
|              |              |        |            |          | 7@기준대비 상승율 상위 |
|              |              |        |            |          | 8@기준대비 하락율 상위 |
| -chgdate     | 대비일자         | Number | Y          | 2        |               |


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
| t1533OutBlock  | t1533OutBlock  | Object       | Y          | -        |               |
| -bdate         | 일자             | String       | Y          | 8        |               |
| t1533OutBlock1 | t1533OutBlock1 | Object Array | Y          | -        |               |
| -tmname        | 테마명            | String       | Y          | 36       |               |
| -totcnt        | 전체             | Number       | Y          | 4        |               |
| -upcnt         | 상승             | Number       | Y          | 4        |               |
| -dncnt         | 하락             | Number       | Y          | 4        |               |
| -uprate        | 상승비율           | Number       | Y          | 6.2      |               |
| -diff_vol      | 거래증가율          | Number       | Y          | 10.2     |               |
| -avgdiff       | 평균등락율          | Number       | Y          | 6.2      |               |
| -chgdiff       | 대비등락율          | Number       | Y          | 6.2      |               |
| -tmcode        | 테마코드           | String       | Y          | 4        |               |


### 💡 Request Example
```json
{
  "t1533InBlock" : {
    "gubun" : "1",
    "chgdate" : 0
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1533OutBlock1": [
        {
            "tmname": "조선",
            "totcnt": 6,
            "diff_vol": "287.29",
            "avgdiff": "4.10",
            "tmcode": "0030",
            "upcnt": 6,
            "dncnt": 0,
            "chgdiff": "0.00",
            "uprate": "100.00"
        },
        {
            "tmname": "치아 치료(임플란트 등)",
            "totcnt": 12,
            "diff_vol": "-46.37",
            "avgdiff": "-1.56",
            "tmcode": "0174",
            "upcnt": 1,
            "dncnt": 11,
            "chgdiff": "0.00",
            "uprate": "8.33"
        }
    ],
    "rsp_msg": "조회완료",
    "t1533OutBlock": {
        "bdate": "20230605"
    }
}

```

---

## 🏷️ 테마종목별시세조회 (t1537)
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
| Element      | 한글명          | type   | Required   | Length   | Description       |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------|
| t1537InBlock | t1537InBlock | Object | Y          | -        |                   |
| -tmcode      | 테마코드         | String | Y          | 4        | t8425조회하여 확인 후 입력 |


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
| t1537OutBlock  | t1537OutBlock  | Object       | Y          | -        |               |
| -upcnt         | 상승종목수          | Number       | Y          | 4        |               |
| -tmcnt         | 테마종목수          | Number       | Y          | 4        |               |
| -uprate        | 상승종목비율         | Number       | Y          | 4        |               |
| -tmname        | 테마명            | String       | Y          | 36       |               |
| t1537OutBlock1 | t1537OutBlock1 | Object Array | Y          | -        |               |
| -hname         | 종목명            | String       | Y          | 20       |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 8        |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 누적거래량          | Number       | Y          | 12       |               |
| -jniltime      | 전일동시간          | Number       | Y          | 9.2      |               |
| -shcode        | 종목코드           | String       | Y          | 6        |               |
| -yeprice       | 예상체결가          | Number       | Y          | 8        |               |
| -open          | 시가             | Number       | Y          | 8        |               |
| -high          | 고가             | Number       | Y          | 8        |               |
| -low           | 저가             | Number       | Y          | 8        |               |
| -value         | 누적거래대금(단위:백만)  | Number       | Y          | 12       |               |
| -marketcap     | 시가총액(단위:백만)    | Number       | Y          | 12       |               |


### 💡 Request Example
```json


{
  "t1537InBlock" : {
    "tmcode" : "0151"
  }
}



```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1537OutBlock": {
        "tmname": "증권",
        "tmcnt": 21,
        "upcnt": 17,
        "uprate": 80
    },
    "t1537OutBlock1": [
        {
            "marketcap": 355984,
            "change": 15,
            "shcode": "001200",
            "sign": "2",
            "diff": "000.41",
            "jniltime": "000045.92",
            "volume": 585074,
            "high": 3750,
            "low": 3645,
            "price": 3675,
            "yeprice": 0,
            "value": 2160,
            "hname": "유진투자증권",
            "open": 3660
        },
        {
            "marketcap": 47080,
            "change": 0,
            "shcode": "190650",
            "sign": "3",
            "diff": "000.00",
            "jniltime": "000275.66",
            "volume": 11018,
            "high": 7380,
            "low": 7250,
            "price": 7370,
            "yeprice": 0,
            "value": 81,
            "hname": "코리아에셋투자증권",
            "open": 7370
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 전체테마 (t8425)
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
| t8425InBlock | t8425InBlock | Object | Y          | -        |               |
| -dummy       | Dummy        | String | Y          | 1        |               |


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
| t8425OutBlock | t8425OutBlock | Object Array | Y          | -        |               |
| -tmname       | 테마명           | String       | Y          | 36       |               |
| -tmcode       | 테마코드          | String       | Y          | 4        |               |


### 💡 Request Example
```json
{
   "t8425InBlock" :{
      "dummy" : ""
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t8425OutBlock": [
        {
            "tmname": "화폐\/금융자동화기기(디지털화폐 등)",
            "tmcode": "0008"
        },
        {
            "tmname": "OLED(유기 발광 다이오드)",
            "tmcode": "0009"
        },
        {
            "tmname": "STO(증권형 토큰 발행)",
            "tmcode": "0531"
        },
        {
            "tmname": "페라이트",
            "tmcode": "0534"
        }
    ]
}
```

---
