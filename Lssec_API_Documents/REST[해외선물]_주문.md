# REST[해외선물] 주문
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=c1ef0e8b-4666-4d8c-a77f-6ab488cfdb39&api_id=b820f925-e189-4553-a7d1-8e5f2750fe08

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /overseas-futureoption/order      |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 해외선물옵션 주문서비스를 확인할 수 있습니다          |


## 🏷️ 해외선물 신규주문 (CIDBT00100)
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
| Element             | 한글명                | type   | Required   | Length   | Description   |
|:--------------------|:-------------------|:-------|:-----------|:---------|:--------------|
| CIDBT00100InBlock1  | CIDBT00100InBlock1 | Object | Y          | -        |               |
| -OrdDt              | 주문일자               | String | Y          | 8        | YYYYMMDD 형식   |
| -IsuCodeVal         | 종목코드값              | String | Y          | 30       |               |
| -FutsOrdTpCode      | 선물주문구분코드           | String | Y          | 1        | 1:신규          |
| -BnsTpCode          | 매매구분코드             | String | Y          | 1        | 1:매도2:매수      |
| -AbrdFutsOrdPtnCode | 해외선물주문유형코드         | String | Y          | 1        | 1:시장가2:지정가    |
| -CrcyCode           | 통화코드               | String | Y          | 3        | SPACE         |
| -OvrsDrvtOrdPrc     | 해외파생주문가격           | Number | Y          | 30.11    |               |
| -CndiOrdPrc         | 조건주문가격             | Number | Y          | 30.11    |               |
| -OrdQty             | 주문수량               | Number | Y          | 16       |               |
| -PrdtCode           | 상품코드               | String | Y          | 6        | SPACE         |
| -DueYymm            | 만기년월               | String | Y          | 6        | SPACE         |
| -ExchCode           | 거래소코드              | String | Y          | 10       | SPACE         |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element             | 한글명                 | type   | Required   | Length   | Description   |
|:--------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CIDBT00100OutBlock1 | CIDBT00100OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdDt              | 주문일자                | String | Y          | 8        |               |
| -BrnCode            | 지점코드                | String | Y          | 7        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -Pwd                | 비밀번호                | String | Y          | 8        |               |
| -IsuCodeVal         | 종목코드값               | String | Y          | 30       |               |
| -FutsOrdTpCode      | 선물주문구분코드            | String | Y          | 1        |               |
| -BnsTpCode          | 매매구분코드              | String | Y          | 1        |               |
| -AbrdFutsOrdPtnCode | 해외선물주문유형코드          | String | Y          | 1        |               |
| -CrcyCode           | 통화코드                | String | Y          | 3        |               |
| -OvrsDrvtOrdPrc     | 해외파생주문가격            | Number | Y          | 30.11    |               |
| -CndiOrdPrc         | 조건주문가격              | Number | Y          | 30.11    |               |
| -OrdQty             | 주문수량                | Number | Y          | 16       |               |
| -PrdtCode           | 상품코드                | String | Y          | 6        |               |
| -DueYymm            | 만기년월                | String | Y          | 6        |               |
| -ExchCode           | 거래소코드               | String | Y          | 10       |               |
| CIDBT00100OutBlock2 | CIDBT00100OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -OvrsFutsOrdNo      | 해외선물주문번호            | String | Y          | 10       |               |


### 💡 Request Example
```json
{
  "CIDBT00100InBlock1" : {
    "RecCnt" : 1,
    "OrdDt" : "20230609",
    "BrnCode" : "100",
    "IsuCodeVal" : "ADM23",
    "FutsOrdTpCode" : "1",
    "BnsTpCode" : "1",
    "AbrdFutsOrdPtnCode" : "2",
    "CrcyCode" : " ",
    "OvrsDrvtOrdPrc" : 122.0,
    "CndiOrdPrc" : 0.664,
    "OrdQty" : 1,
    "PrdtCode" : "000000",
    "DueYymm" : "000001",
    "ExchCode" : " "
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "CIDBT00100OutBlock1": {
        "ExchCode": "",
        "FutsOrdTpCode": "1",
        "BnsTpCode": "1",
        "OrdQty": 1,
        "RecCnt": 1,
        "PrdtCode": "000000",
        "AcntNo": "20629783903",
        "CndiOrdPrc": "0.66400000000",
        "BrnCode": "",
        "Pwd": "********",
        "CrcyCode": "",
        "DueYymm": "000001",
        "IsuCodeVal": "ADM23",
        "AbrdFutsOrdPtnCode": "2",
        "OrdDt": "20230609",
        "OvrsDrvtOrdPrc": "122.00000000000"
    },
    "CIDBT00100OutBlock2": {
        "RecCnt": 1,
        "AcntNo": "20629783903",
        "OvrsFutsOrdNo": "0000000136"
    },
    "rsp_msg": "정상 처리되었습니다."
}
```

---

## 🏷️ 해외선물 정정주문 (CIDBT00900)
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
| Element            | 한글명                | type   | Required   | Length   | Description   |
|:-------------------|:-------------------|:-------|:-----------|:---------|:--------------|
| CIDBT00900InBlock1 | CIDBT00900InBlock1 | Object | Y          | -        |               |
| -OrdDt             | 주문일자               | String | Y          | 8        | YYYYMMDD 형식   |
| -OvrsFutsOrgOrdNo  | 해외선물원주문번호          | String | Y          | 10       |               |
| -IsuCodeVal        | 종목코드값              | String | Y          | 30       |               |
| -FutsOrdTpCode     | 선물주문구분코드           | String | Y          | 1        | 2:정정          |
| -BnsTpCode         | 매매구분코드             | String | Y          | 1        | 1:매도2:매수      |
| -FutsOrdPtnCode    | 선물주문유형코드           | String | Y          | 1        | 2:지정가         |
| -CrcyCodeVal       | 통화코드값              | String | Y          | 3        | SPACE         |
| -OvrsDrvtOrdPrc    | 해외파생주문가격           | Number | Y          | 30.11    |               |
| -CndiOrdPrc        | 조건주문가격             | Number | Y          | 30.11    |               |
| -OrdQty            | 주문수량               | Number | Y          | 16       |               |
| -OvrsDrvtPrdtCode  | 해외파생상품코드           | String | Y          | 10       | SPACE         |
| -DueYymm           | 만기년월               | String | Y          | 6        | SPACE         |
| -ExchCode          | 거래소코드              | String | Y          | 10       | SPACE         |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element             | 한글명                 | type   | Required   | Length   | Description   |
|:--------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CIDBT00900OutBlock1 | CIDBT00900OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdDt              | 주문일자                | String | Y          | 8        |               |
| -RegBrnNo           | 등록지점번호              | String | Y          | 3        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -Pwd                | 비밀번호                | String | Y          | 8        |               |
| -OvrsFutsOrgOrdNo   | 해외선물원주문번호           | String | Y          | 10       |               |
| -IsuCodeVal         | 종목코드값               | String | Y          | 30       |               |
| -FutsOrdTpCode      | 선물주문구분코드            | String | Y          | 1        |               |
| -BnsTpCode          | 매매구분코드              | String | Y          | 1        |               |
| -FutsOrdPtnCode     | 선물주문유형코드            | String | Y          | 1        |               |
| -CrcyCodeVal        | 통화코드값               | String | Y          | 3        |               |
| -OvrsDrvtOrdPrc     | 해외파생주문가격            | Number | Y          | 30.11    |               |
| -CndiOrdPrc         | 조건주문가격              | Number | Y          | 30.11    |               |
| -OrdQty             | 주문수량                | Number | Y          | 16       |               |
| -OvrsDrvtPrdtCode   | 해외파생상품코드            | String | Y          | 10       |               |
| -DueYymm            | 만기년월                | String | Y          | 6        |               |
| -ExchCode           | 거래소코드               | String | Y          | 10       |               |
| CIDBT00900OutBlock2 | CIDBT00900OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -OvrsFutsOrdNo      | 해외선물주문번호            | String | Y          | 10       |               |
| -InnerMsgCnts       | 내부메시지내용             | String | Y          | 80       |               |


### 💡 Request Example
```json
{
  "CIDBT00900InBlock1" : {
    "RecCnt" : 1,
    "OrdDt" : "20230609",
    "RegBrnNo" : " ",
    "OvrsFutsOrgOrdNo" : "0000000029",
    "IsuCodeVal" : "ADM23",
    "FutsOrdTpCode" : "2",
    "BnsTpCode" : "1",
    "FutsOrdPtnCode" : "2",
    "CrcyCodeVal" : " ",
    "OvrsDrvtOrdPrc" : 122.0,
    "CndiOrdPrc" : 0.66400000000,
    "OrdQty" : 1,
    "OvrsDrvtPrdtCode" : "",
    "DueYymm" : "",
    "ExchCode" : " "
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00131",
    "rsp_msg": "정정이 완료되었습니다.",
    "CIDBT00900OutBlock2": {
        "RecCnt": 1,
        "AcntNo": "20629783903",
        "OvrsFutsOrdNo": "0000000030",
        "InnerMsgCnts": ""
    },
    "CIDBT00900OutBlock1": {
        "ExchCode": "",
        "FutsOrdTpCode": "2",
        "BnsTpCode": "1",
        "OvrsDrvtPrdtCode": "",
        "FutsOrdPtnCode": "2",
        "OvrsFutsOrgOrdNo": "0000000029",
        "OrdQty": 1,
        "RecCnt": 1,
        "AcntNo": "20629783903",
        "CndiOrdPrc": "0.66700000000",
        "RegBrnNo": "",
        "Pwd": "********",
        "DueYymm": "",
        "IsuCodeVal": "ADM23",
        "OrdDt": "20230609",
        "CrcyCodeVal": "",
        "OvrsDrvtOrdPrc": "122.50000000000"
    }
}
```

---

## 🏷️ 해외선물 취소주문 (CIDBT01000)
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
| Element            | 한글명                | type   | Required   | Length   | Description   |
|:-------------------|:-------------------|:-------|:-----------|:---------|:--------------|
| CIDBT01000InBlock1 | CIDBT01000InBlock1 | Object | Y          | -        |               |
| -OrdDt             | 주문일자               | String | Y          | 8        | YYYYMMDD 형식   |
| -IsuCodeVal        | 종목코드값              | String | Y          | 30       |               |
| -OvrsFutsOrgOrdNo  | 해외선물원주문번호          | String | Y          | 10       |               |
| -FutsOrdTpCode     | 선물주문구분코드           | String | Y          | 1        | 3:취소          |
| -PrdtTpCode        | 상품구분코드             | String | Y          | 2        | SPACE         |
| -ExchCode          | 거래소코드              | String | Y          | 10       | SPACE         |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element             | 한글명                 | type   | Required   | Length   | Description   |
|:--------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CIDBT01000OutBlock1 | CIDBT01000OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdDt              | 주문일자                | String | Y          | 8        |               |
| -BrnNo              | 지점번호                | String | Y          | 3        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -Pwd                | 비밀번호                | String | Y          | 8        |               |
| -IsuCodeVal         | 종목코드값               | String | Y          | 30       |               |
| -OvrsFutsOrgOrdNo   | 해외선물원주문번호           | String | Y          | 10       |               |
| -FutsOrdTpCode      | 선물주문구분코드            | String | Y          | 1        |               |
| -PrdtTpCode         | 상품구분코드              | String | Y          | 2        |               |
| -ExchCode           | 거래소코드               | String | Y          | 10       |               |
| CIDBT01000OutBlock2 | CIDBT01000OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -OvrsFutsOrdNo      | 해외선물주문번호            | String | Y          | 10       |               |
| -InnerMsgCnts       | 내부메시지내용             | String | Y          | 80       |               |


### 💡 Request Example
```json
{
  "CIDBT01000InBlock1" : {
    "RecCnt" : 1,
    "OrdDt" : "20230609",
    "BrnNo" : " ",
    "IsuCodeVal" : "ADM23",
    "OvrsFutsOrgOrdNo" : "0000000030",
    "FutsOrdTpCode" : "3",
    "PrdtTpCode" : " ",
    "ExchCode" : " "
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00156",
    "CIDBT01000OutBlock1": {
        "RecCnt": 1,
        "ExchCode": "",
        "FutsOrdTpCode": "3",
        "BrnNo": "",
        "AcntNo": "20629783903",
        "Pwd": "********",
        "IsuCodeVal": "ADM23",
        "OvrsFutsOrgOrdNo": "0000000030",
        "PrdtTpCode": "",
        "OrdDt": "20230609"
    },
    "rsp_msg": "취소주문이 완료되었습니다.",
    "CIDBT01000OutBlock2": {
        "RecCnt": 1,
        "AcntNo": "20629783903",
        "OvrsFutsOrdNo": "0000000031",
        "InnerMsgCnts": ""
    }
}
```

---
