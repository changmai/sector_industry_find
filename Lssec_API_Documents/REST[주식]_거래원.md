# REST[주식] 거래원
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=3dbce945-a73c-475c-9758-88d9922ab94e

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /stock/exchange                   |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 종목별 거래 회원사를 호출하여 거래원을 확인할 수 있습니다. |


## 🏷️ 종목별상위회원사 (t1752)
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
| t1752InBlock | t1752InBlock | Object | Y          | -        |                                 |
| -shcode      | 종목코드         | String | Y          | 6        |                                 |
| -traddate1   | 조회날짜1        | String | Y          | 8        | 기간 조회시 시작일(YYYYMMDD)            |
| -traddate2   | 조회날짜2        | String | Y          | 8        | 기간 조회시 종료일(YYYYMMDD)            |
| -fwgubun1    | 외국계구분        | String | Y          | 1        | 0 : 전체1 : 외국계 회원사만 조회           |
| -cts_idx     | CTSIDX       | Number | Y          | 4        | OutBlock 동일필드 연속조회시 입력          |
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
| t1752OutBlock  | t1752OutBlock  | Object       | Y          | -        |               |
| -fwdvl         | 외국계매도          | Number       | Y          | 12       |               |
| -fwsvl         | 외국계매수          | Number       | Y          | 12       |               |
| -cts_idx       | CTSIDX         | Number       | Y          | 4        |               |
| t1752OutBlock1 | t1752OutBlock1 | Object Array | Y          | -        |               |
| -tradname      | 회원사            | String       | Y          | 20       |               |
| -tradmdvol     | 매도수량           | Number       | Y          | 12       |               |
| -tradmsvol     | 매수수량           | Number       | Y          | 12       |               |
| -tradmssvol    | 순매수            | Number       | Y          | 12       |               |
| -wintrd        | 창구거래           | Number       | Y          | 12       |               |
| -winrat        | 비중             | Number       | Y          | 6.1      |               |
| -tradno        | 회원사코드          | String       | Y          | 3        |               |
| -wgubun        | 외국계여부          | String       | Y          | 1        |               |
| -swinrat       | 순비중            | Number       | Y          | 6.1      |               |


### 💡 Request Example
```json
{
  "t1752InBlock" : {
    "shcode" : "005930",
    "traddate1" : "20230502",
    "traddate2" : "20230601",
    "fwgubun1" : "0",
    "cts_idx" : 0
  }
}

```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1752OutBlock1": [
        {
            "tradmdvol": 10485472,
            "tradmsvol": 18297639,
            "tradno": "033",
            "wgubun": "1",
            "swinrat": "27.0",
            "tradname": "JP모간",
            "winrat": "51.0",
            "wintrd": 28783111,
            "tradmssvol": 7812167
        },
        {
            "tradmdvol": 10025294,
            "tradmsvol": 9401013,
            "tradno": "021",
            "wgubun": "0",
            "swinrat": "-2.0",
            "tradname": "한화투자",
            "winrat": "34.0",
            "wintrd": 19426307,
            "tradmssvol": -624281
        }
    ],
    "t1752OutBlock": {
        "cts_idx": 40,
        "fwdvl": 65771261,
        "fwsvl": 94034201
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 회원사리스트 (t1764)
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
| t1764InBlock | t1764InBlock | Object | Y          | -        |                                                   |
| -shcode      | 종목코드         | String | Y          | 6        |                                                   |
| -gubun1      | 구분1          | String | Y          | 1        | 0 or 1 : 전회원사조회                                   |
|              |              |        |            |          | 0,1 이외의 값 입력시 InBlock.shcode 종목으로 거래가 있는 회원사만 조회됨 |


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
| t1764OutBlock | t1764OutBlock | Object Array | Y          | -        |               |
| -rank         | 순위            | Number       | Y          | 4        |               |
| -tradno       | 거래원번호         | String       | Y          | 3        |               |
| -tradname     | 거래원이름         | String       | Y          | 20       |               |


### 💡 Request Example
```json
{
  "t1764InBlock" : {
    "shcode" : "001200",
    "gubun1" : "0"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1764OutBlock": [
        {
            "tradno": "000",
            "tradname": "외국계회원사전체",
            "rank": 0
        },
        {
            "tradno": "086",
            "tradname": "BNK 증권",
            "rank": 1
        },
        {
            "tradno": "067",
            "tradname": "BNP 파리바",
            "rank": 2
        },
        {
            "tradno": "066",
            "tradname": "흥국증권",
            "rank": 63
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}

```

---

## 🏷️ 종목별회원사추이 (t1771)
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
| t1771InBlock | t1771InBlock | Object | Y          | -        |                                                   |
| -shcode      | 종목코드         | String | Y          | 6        |                                                   |
| -tradno      | 거래원코드        | String | Y          | 3        | 거래원코드t1764 를 조회한 후 t1764OutBlock 의 tradno 의 값을 사용 |
| -gubun1      | 구분1          | String | Y          | 1        | 0 : 시간별1 : 일별                                     |
| -traddate1   | 거래원날짜1       | String | Y          | 8        | 일별 조회시 사용OutBlock1.traddate >= InBlock.traddate1  |
| -traddate2   | 거래원날짜2       | String | Y          | 8        | 일별 조회시 사용OutBlock1.traddate <= InBlock.traddate2  |
| -cts_idx     | CTSIDX       | Number | Y          | 4        | 처음 조회시 Space 입력다음 조회시 OutBlock의 cts_idx 값을 입력     |
| -cnt         | 요청건수         | Object | Y          | 3        |                                                   |
| -exchgubun   | 거래소구분        | String | Y          | 1        | K: KRXN: NXTU:통합그외 입력값은 KRX로 처리                   |


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
| t1771OutBlock  | t1771OutBlock  | Object       | Y          | -        |               |
| -cts_idx       | CTSIDX         | Number       | Y          | 4        |               |
| t1771OutBlock2 | t1771OutBlock2 | Object Array | Y          | -        |               |
| -traddate      | 날짜             | String       | Y          | 8        |               |
| -tradtime      | 시간             | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 대비구분           | String       | Y          | 1        |               |
| -change        | 대비             | Number       | Y          | 8        |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -tradmdcha     | 매도             | Number       | Y          | 12       |               |
| -tradmscha     | 매수             | Number       | Y          | 12       |               |
| -tradmdval     | 매도대금           | Number       | Y          | 18       |               |
| -tradmsval     | 매수대금           | Number       | Y          | 18       |               |
| -tradmsscha    | 순매수            | Number       | Y          | 12       |               |
| -tradmttvolume | 누적순매수          | Number       | Y          | 12       |               |
| -tradavg       | 평균단가           | Number       | Y          | 8        |               |
| -tradmttavg    | 누적평균단가         | Number       | Y          | 8        |               |


### 💡 Request Example
```json
{
  "t1771InBlock" : {
    "shcode" : "005930",
    "tradno" : "086",
    "gubun1" : "1",
    "traddate1" : "20230101",
    "traddate2" : "20230619",
    "cts_idx" : 0,
    "cnt" : 100
  }
}
```

### 💡 Response Example
```json
{
    "t1771OutBlock2": [
        {
            "tradtime": "",
            "tradmsval": 105447198900,
            "change": 0,
            "sign": "3",
            "diff": "0.00",
            "tradmscha": 1483138,
            "traddate": "20230619",
            "volume": 0,
            "tradavg": 71110,
            "tradmdval": 108970167900,
            "price": 65100,
            "tradmdcha": 1532140,
            "tradmsscha": -49002,
            "tradmttavg": 64759,
            "tradmttvolume": -1721142
        },
        {
            "tradtime": "",
            "tradmsval": 0,
            "change": 15000,
            "sign": "1",
            "diff": "2994.00",
            "tradmscha": 0,
            "traddate": "20230619",
            "volume": 205461,
            "tradavg": 0,
            "tradmdval": 0,
            "price": 65100,
            "tradmdcha": 0,
            "tradmsscha": 0,
            "tradmttavg": 64675,
            "tradmttvolume": -1672140
        }
    ],
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1771OutBlock": {
        "cts_idx": 100
    }
}
```

---
