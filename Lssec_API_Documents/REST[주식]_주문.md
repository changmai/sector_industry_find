# REST[주식] 주문
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=d0e216e0-10d9-479f-8a4d-e175b8bae307

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /stock/order                      |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 주문과 관련된 서비스를 확인할 수 있습니다.          |


## 🏷️ 현물주문 (CSPAT00601)
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
| Element            | 한글명                | type   | Required   | Length   | Description                                                                                     |
|:-------------------|:-------------------|:-------|:-----------|:---------|:------------------------------------------------------------------------------------------------|
| CSPAT00601InBlock1 | CSPAT00601InBlock1 | Object | Y          | -        |                                                                                                 |
| -IsuNo             | 종목번호               | String | Y          | 12       | 주식/ETF : 종목코드 or A+종목코드(모의투자는 A+종목코드)ELW : J+종목코드ETN : Q+종목코드                                   |
| -OrdQty            | 주문수량               | Number | Y          | 16       |                                                                                                 |
| -OrdPrc            | 주문가                | Number | Y          | 13.2     |                                                                                                 |
| -BnsTpCode         | 매매구분               | String | Y          | 1        | 1:매도, 2:매수                                                                                      |
| -OrdprcPtnCode     | 호가유형코드             | String | Y          | 2        | 00@지정가03@시장가05@조건부지정가06@최유리지정가07@최우선지정가12@중간가61@장개시전시간외종가81@시간외종가82@시간외단일가                      |
| -MgntrnCode        | 신용거래코드             | String | Y          | 3        | 000:보통003:유통/자기융자신규005:유통대주신규007:자기대주신규101:유통융자상환103:자기융자상환105:유통대주상환107:자기대주상환180:예탁담보대출상환(신용) |
| -LoanDt            | 대출일                | String | Y          | 8        |                                                                                                 |
| -OrdCndiTpCode     | 주문조건구분             | String | Y          | 1        | 0:없음,1:IOC,2:FOK                                                                                |
| -MbrNo             | 회원사번호              | String | Y          | 3        | KRX: KRXNXT: NXT공백을 포함한 그외 입력값은 KRX로 처리                                                         |


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
| CSPAT00601OutBlock1 | CSPAT00601OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -InptPwd            | 입력비밀번호              | String | Y          | 8        |               |
| -IsuNo              | 종목번호                | String | Y          | 12       |               |
| -OrdQty             | 주문수량                | Number | Y          | 16       |               |
| -OrdPrc             | 주문가                 | Number | Y          | 13.2     |               |
| -BnsTpCode          | 매매구분                | String | Y          | 1        |               |
| -OrdprcPtnCode      | 호가유형코드              | String | Y          | 2        |               |
| -PrgmOrdprcPtnCode  | 프로그램호가유형코드          | String | Y          | 2        |               |
| -StslAbleYn         | 공매도가능여부             | String | Y          | 1        |               |
| -StslOrdprcTpCode   | 공매도호가구분             | String | Y          | 1        |               |
| -CommdaCode         | 통신매체코드              | String | Y          | 2        |               |
| -MgntrnCode         | 신용거래코드              | String | Y          | 3        |               |
| -LoanDt             | 대출일                 | String | Y          | 8        |               |
| -MbrNo              | 회원번호                | String | Y          | 3        |               |
| -OrdCndiTpCode      | 주문조건구분              | String | Y          | 1        |               |
| -StrtgCode          | 전략코드                | String | Y          | 6        |               |
| -GrpId              | 그룹ID                | String | Y          | 20       |               |
| -OrdSeqNo           | 주문회차                | Number | Y          | 10       |               |
| -PtflNo             | 포트폴리오번호             | Number | Y          | 10       |               |
| -BskNo              | 바스켓번호               | Number | Y          | 10       |               |
| -TrchNo             | 트렌치번호               | Number | Y          | 10       |               |
| -ItemNo             | 아이템번호               | Number | Y          | 10       |               |
| -OpDrtnNo           | 운용지시번호              | String | Y          | 12       |               |
| -LpYn               | 유동성공급자여부            | String | Y          | 1        |               |
| -CvrgTpCode         | 반대매매구분              | String | Y          | 1        |               |
| CSPAT00601OutBlock2 | CSPAT00601OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdNo              | 주문번호                | Number | Y          | 10       |               |
| -OrdTime            | 주문시각                | String | Y          | 9        |               |
| -OrdMktCode         | 주문시장코드              | String | Y          | 2        |               |
| -OrdPtnCode         | 주문유형코드              | String | Y          | 2        |               |
| -ShtnIsuNo          | 단축종목번호              | String | Y          | 9        |               |
| -MgempNo            | 관리사원번호              | String | Y          | 9        |               |
| -OrdAmt             | 주문금액                | Number | Y          | 16       |               |
| -SpareOrdNo         | 예비주문번호              | Number | Y          | 10       |               |
| -CvrgSeqno          | 반대매매일련번호            | Number | Y          | 10       |               |
| -RsvOrdNo           | 예약주문번호              | Number | Y          | 10       |               |
| -SpotOrdQty         | 실물주문수량              | Number | Y          | 16       |               |
| -RuseOrdQty         | 재사용주문수량             | Number | Y          | 16       |               |
| -MnyOrdAmt          | 현금주문금액              | Number | Y          | 16       |               |
| -SubstOrdAmt        | 대용주문금액              | Number | Y          | 16       |               |
| -RuseOrdAmt         | 재사용주문금액             | Number | Y          | 16       |               |
| -AcntNm             | 계좌명                 | String | Y          | 40       |               |
| -IsuNm              | 종목명                 | String | Y          | 40       |               |


### 💡 Request Example
```json
{
  "CSPAT00601InBlock1" : {
    "IsuNo" : "A272210",
    "OrdQty" : 1,
    "OrdPrc" : 35000,
    "BnsTpCode" : "2",
    "OrdprcPtnCode" : "00",
    "MgntrnCode" : "000",
    "LoanDt" : "",
    "OrdCndiTpCode" : "0",
    "MbrNo" : "NXT"
  }
}
```

### 💡 Response Example
```json
{
    "CSPAT00601OutBlock1": {
        "RecCnt": 1,
        "AcntNo": "20*********",
        "InptPwd": "********",
        "IsuNo": "A272210",
        "OrdQty": 1,
        "OrdPrc": "35000.00",
        "BnsTpCode": "2",
        "OrdprcPtnCode": "00",
        "PrgmOrdprcPtnCode": "00",
        "StslAbleYn": "0",
        "StslOrdprcTpCode": "0",
        "CommdaCode": "40",
        "MgntrnCode": "000",
        "LoanDt": "",
        "MbrNo": "NXT",
        "OrdCndiTpCode": "0",
        "StrtgCode": "",
        "GrpId": "",
        "OrdSeqNo": 0,
        "PtflNo": 0,
        "BskNo": 0,
        "TrchNo": 0,
        "ItemNo": 0,
        "OpDrtnNo": "0",
        "LpYn": "0",
        "CvrgTpCode": "0"
    },
    "CSPAT00601OutBlock2": {
        "RecCnt": 1,
        "OrdNo": 32004,
        "OrdTime": "153257702",
        "OrdMktCode": "10",
        "OrdPtnCode": "02",
        "ShtnIsuNo": "A272210",
        "MgempNo": "999999209",
        "OrdAmt": 35000,
        "SpareOrdNo": 32004,
        "CvrgSeqno": 0,
        "RsvOrdNo": 0,
        "SpotOrdQty": 0,
        "RuseOrdQty": 0,
        "MnyOrdAmt": 35000,
        "SubstOrdAmt": 0,
        "RuseOrdAmt": 0,
        "AcntNm": "***",
        "IsuNm": "한화시스템"
    },
    "rsp_cd": "00040",
    "rsp_msg": "매수 주문이 완료되었습니다."
}
```

---

## 🏷️ 현물정정주문 (CSPAT00701)
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
| Element            | 한글명                | type   | Required   | Length   | Description                                                          |
|:-------------------|:-------------------|:-------|:-----------|:---------|:---------------------------------------------------------------------|
| CSPAT00701InBlock1 | CSPAT00701InBlock1 | Object | Y          | -        |                                                                      |
| -OrgOrdNo          | 원주문번호              | Number | Y          | 10       |                                                                      |
| -IsuNo             | 종목번호               | String | Y          | 12       | 주식 : 종목코드 or A+종목코드(모의투자는 A+종목코드)ELW : J+종목코드ETN : Q+종목코드            |
| -OrdQty            | 주문수량               | Number | Y          | 16       |                                                                      |
| -OrdprcPtnCode     | 호가유형코드             | String | Y          | 2        | 00@지정가03@시장가05@조건부지정가06@최유리지정가07@최우선지정가61@장개시전시간외종가81@시간외종가82@시간외단일가 |
| -OrdCndiTpCode     | 주문조건구분             | String | Y          | 1        | 0:없음, 1:IOC, 2:FOK                                                   |
| -OrdPrc            | 주문가                | Number | Y          | 13.2     |                                                                      |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element             | 한글명                 | type   | Required   | Length   | Description                                                                |
|:--------------------|:--------------------|:-------|:-----------|:---------|:---------------------------------------------------------------------------|
| CSPAT00701OutBlock1 | CSPAT00701OutBlock1 | Object | Y          | -        |                                                                            |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |                                                                            |
| -OrgOrdNo           | 원주문번호               | Number | Y          | 10       |                                                                            |
| -AcntNo             | 계좌번호                | String | Y          | 20       |                                                                            |
| -InptPwd            | 입력비밀번호              | String | Y          | 8        |                                                                            |
| -IsuNo              | 종목번호                | String | Y          | 12       |                                                                            |
| -OrdQty             | 주문수량                | Number | Y          | 16       |                                                                            |
| -OrdprcPtnCode      | 호가유형코드              | String | Y          | 2        | 00@지정가03@시장가05@조건부지정가06@최유리지정가07@최우선지정가12@중간가61@장개시전시간외종가81@시간외종가82@시간외단일가 |
| -OrdCndiTpCode      | 주문조건구분              | String | Y          | 1        |                                                                            |
| -OrdPrc             | 주문가                 | Number | Y          | 13.2     |                                                                            |
| -CommdaCode         | 통신매체코드              | String | Y          | 2        |                                                                            |
| -StrtgCode          | 전략코드                | String | Y          | 6        |                                                                            |
| -GrpId              | 그룹ID                | String | Y          | 20       |                                                                            |
| -OrdSeqNo           | 주문회차                | Number | Y          | 10       |                                                                            |
| -PtflNo             | 포트폴리오번호             | Number | Y          | 10       |                                                                            |
| -BskNo              | 바스켓번호               | Number | Y          | 10       |                                                                            |
| -TrchNo             | 트렌치번호               | Number | Y          | 10       |                                                                            |
| -ItemNo             | 아이템번호               | Number | Y          | 10       |                                                                            |
| CSPAT00701OutBlock2 | CSPAT00701OutBlock2 | Object | Y          | -        |                                                                            |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |                                                                            |
| -OrdNo              | 주문번호                | Number | Y          | 10       |                                                                            |
| -PrntOrdNo          | 모주문번호               | Number | Y          | 10       |                                                                            |
| -OrdTime            | 주문시각                | String | Y          | 9        |                                                                            |
| -OrdMktCode         | 주문시장코드              | String | Y          | 2        |                                                                            |
| -OrdPtnCode         | 주문유형코드              | String | Y          | 2        |                                                                            |
| -ShtnIsuNo          | 단축종목번호              | String | Y          | 9        |                                                                            |
| -PrgmOrdprcPtnCode  | 프로그램호가유형코드          | String | Y          | 2        |                                                                            |
| -StslOrdprcTpCode   | 공매도호가구분             | String | Y          | 1        |                                                                            |
| -StslAbleYn         | 공매도가능여부             | String | Y          | 1        |                                                                            |
| -MgntrnCode         | 신용거래코드              | String | Y          | 3        |                                                                            |
| -LoanDt             | 대출일                 | String | Y          | 8        |                                                                            |
| -CvrgOrdTp          | 반대매매주문구분            | String | Y          | 1        |                                                                            |
| -LpYn               | 유동성공급자여부            | String | Y          | 1        |                                                                            |
| -MgempNo            | 관리사원번호              | String | Y          | 9        |                                                                            |
| -OrdAmt             | 주문금액                | Number | Y          | 16       |                                                                            |
| -BnsTpCode          | 매매구분                | String | Y          | 1        |                                                                            |
| -SpareOrdNo         | 예비주문번호              | Number | Y          | 10       |                                                                            |
| -CvrgSeqno          | 반대매매일련번호            | Number | Y          | 10       |                                                                            |
| -RsvOrdNo           | 예약주문번호              | Number | Y          | 10       |                                                                            |
| -MnyOrdAmt          | 현금주문금액              | Number | Y          | 16       |                                                                            |
| -SubstOrdAmt        | 대용주문금액              | Number | Y          | 16       |                                                                            |
| -RuseOrdAmt         | 재사용주문금액             | Number | Y          | 16       |                                                                            |
| -AcntNm             | 계좌명                 | String | Y          | 40       |                                                                            |
| -IsuNm              | 종목명                 | String | Y          | 40       |                                                                            |


### 💡 Request Example
```json
{
  "CSPAT00701InBlock1" : {
    "OrgOrdNo" : 171011,
    "IsuNo" : "A005930",
    "OrdQty" : 1,
    "OrdprcPtnCode" : "00",
    "OrdCndiTpCode" : "0",
    "OrdPrc" : 8350.0
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "03181",
    "rsp_msg": "주문가격이 하한가 미달입니다.",
    "CSPAT00701OutBlock2": {
        "OrdAmt": 0,
        "BnsTpCode": "",
        "CvrgSeqno": 0,
        "SpareOrdNo": 0,
        "OrdMktCode": "",
        "ShtnIsuNo": "",
        "OrdTime": "",
        "StslAbleYn": "",
        "StslOrdprcTpCode": "",
        "OrdPtnCode": "",
        "CvrgOrdTp": "",
        "MgntrnCode": "",
        "MgempNo": "",
        "OrdNo": 0,
        "PrntOrdNo": 0,
        "PrgmOrdprcPtnCode": "",
        "SubstOrdAmt": 0,
        "IsuNm": "",
        "RuseOrdAmt": 0,
        "RecCnt": 1,
        "MnyOrdAmt": 0,
        "AcntNm": "",
        "LoanDt": "",
        "RsvOrdNo": 0,
        "LpYn": ""
    },
    "CSPAT00701OutBlock1": {
        "OrdPrc": "8350.00",
        "InptPwd": "********",
        "TrchNo": 0,
        "OrgOrdNo": 84005,
        "BskNo": 0,
        "StrtgCode": "",
        "OrdQty": 1,
        "CommdaCode": "40",
        "RecCnt": 1,
        "OrdprcPtnCode": "00",
        "IsuNo": "A005930",
        "OrdSeqNo": 0,
        "ItemNo": 0,
        "AcntNo": "20011132702",
        "OrdCndiTpCode": "0",
        "PtflNo": 0,
        "GrpId": ""
    }
}
```

---

## 🏷️ 현물취소주문 (CSPAT00801)
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
| Element            | 한글명                | type   | Required   | Length   | Description                                               |
|:-------------------|:-------------------|:-------|:-----------|:---------|:----------------------------------------------------------|
| CSPAT00801InBlock1 | CSPAT00801InBlock1 | Object | Y          | -        |                                                           |
| -OrgOrdNo          | 원주문번호              | Number | Y          | 10       |                                                           |
| -IsuNo             | 종목번호               | String | Y          | 12       | 주식 : 종목코드 or A+종목코드(모의투자는 A+종목코드)ELW : J+종목코드ETN : Q+종목코드 |
| -OrdQty            | 주문수량               | Number | Y          | 16       |                                                           |


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
| CSPAT00801OutBlock1 | CSPAT00801OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrgOrdNo           | 원주문번호               | Number | Y          | 10       |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -InptPwd            | 입력비밀번호              | String | Y          | 8        |               |
| -IsuNo              | 종목번호                | String | Y          | 12       |               |
| -OrdQty             | 주문수량                | Number | Y          | 16       |               |
| -CommdaCode         | 통신매체코드              | String | Y          | 2        |               |
| -GrpId              | 그룹ID                | String | Y          | 20       |               |
| -StrtgCode          | 전략코드                | String | Y          | 6        |               |
| -OrdSeqNo           | 주문회차                | Number | Y          | 10       |               |
| -PtflNo             | 포트폴리오번호             | Number | Y          | 10       |               |
| -BskNo              | 바스켓번호               | Number | Y          | 10       |               |
| -TrchNo             | 트렌치번호               | Number | Y          | 10       |               |
| -ItemNo             | 아이템번호               | Number | Y          | 10       |               |
| CSPAT00801OutBlock2 | CSPAT00801OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdNo              | 주문번호                | Number | Y          | 10       |               |
| -PrntOrdNo          | 모주문번호               | Number | Y          | 10       |               |
| -OrdTime            | 주문시각                | String | Y          | 9        |               |
| -OrdMktCode         | 주문시장코드              | String | Y          | 2        |               |
| -OrdPtnCode         | 주문유형코드              | String | Y          | 2        |               |
| -ShtnIsuNo          | 단축종목번호              | String | Y          | 9        |               |
| -PrgmOrdprcPtnCode  | 프로그램호가유형코드          | String | Y          | 2        |               |
| -StslOrdprcTpCode   | 공매도호가구분             | String | Y          | 1        |               |
| -StslAbleYn         | 공매도가능여부             | String | Y          | 1        |               |
| -MgntrnCode         | 신용거래코드              | String | Y          | 3        |               |
| -LoanDt             | 대출일                 | String | Y          | 8        |               |
| -CvrgOrdTp          | 반대매매주문구분            | String | Y          | 1        |               |
| -LpYn               | 유동성공급자여부            | String | Y          | 1        |               |
| -MgempNo            | 관리사원번호              | String | Y          | 9        |               |
| -BnsTpCode          | 매매구분                | String | Y          | 1        |               |
| -SpareOrdNo         | 예비주문번호              | Number | Y          | 10       |               |
| -CvrgSeqno          | 반대매매일련번호            | Number | Y          | 10       |               |
| -RsvOrdNo           | 예약주문번호              | Number | Y          | 10       |               |
| -AcntNm             | 계좌명                 | String | Y          | 40       |               |
| -IsuNm              | 종목명                 | String | Y          | 40       |               |


### 💡 Request Example
```json
{
  "CSPAT00801InBlock1" : {
    "OrgOrdNo" : 171011,
    "IsuNo" : "A005930",
    "OrdQty" : 1
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00156",
    "CSPAT00801OutBlock2": {
        "MgntrnCode": "000",
        "BnsTpCode": "2",
        "CvrgSeqno": 0,
        "MgempNo": "999999106",
        "SpareOrdNo": 0,
        "OrdNo": 84006,
        "PrntOrdNo": 84005,
        "PrgmOrdprcPtnCode": "00",
        "OrdMktCode": "10",
        "IsuNm": "삼성전자",
        "ShtnIsuNo": "A005930",
        "RecCnt": 1,
        "OrdTime": "133018980",
        "StslAbleYn": "0",
        "AcntNm": "우우돌",
        "StslOrdprcTpCode": "0",
        "LoanDt": "00000000",
        "RsvOrdNo": 0,
        "OrdPtnCode": "02",
        "LpYn": "0",
        "CvrgOrdTp": "0"
    },
    "CSPAT00801OutBlock1": {
        "InptPwd": "********",
        "TrchNo": 0,
        "OrgOrdNo": 84005,
        "BskNo": 0,
        "StrtgCode": "",
        "OrdQty": 1,
        "CommdaCode": "40",
        "RecCnt": 1,
        "IsuNo": "A005930",
        "OrdSeqNo": 0,
        "ItemNo": 0,
        "AcntNo": "20011132702",
        "PtflNo": 0,
        "GrpId": ""
    },
    "rsp_msg": "취소주문이 완료되었습니다."
}
```

---
