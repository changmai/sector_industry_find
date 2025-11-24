# REST[해외주식] 주문
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=cdb7e1bc-f7c5-425c-8248-aa83dbb6919f&api_id=6bafc43c-6080-4541-bfc2-c2608b269ca0

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /overseas-stock/order             |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 해외주식 주문서비스를 확인할 수 있습니다            |


## 🏷️ 미국시장주문 API (COSAT00301)
### 요청 Header
| Element       | 한글명     | type   | Required   |   Length | Description                                                                     |
|:--------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰    | String | Y          |     1000 | OAuth토큰이필요한API경우발급한AccessToken을설정하기위한RequestHeaederParameter                    |
| tr_cd         | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont       | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key   | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |
| mac_address   | MAC주소   | String | Y          |       12 | 법인인경우필수세팅                                                                       |


### 요청 Body
| Element            | 한글명                | type   | Required   | Length   | Description                                       |
|:-------------------|:-------------------|:-------|:-----------|:---------|:--------------------------------------------------|
| COSAT00301InBlock1 | COSAT00301InBlock1 | Object | Y          | -        |                                                   |
| -RecCnt            | 레코드갯수              | Number | Y          | 5        | 00001                                             |
| -OrdPtnCode        | 주문유형코드             | String | Y          | 2        | 01 : 매도주문02 : 매수주문08 : 취소주문                       |
| -OrgOrdNo          | 원주문번호              | Number | Y          | 10       | 취소주문인 경우만 필수 입력                                   |
| -OrdMktCode        | 주문시장코드             | String | Y          | 2        | 81 : 뉴욕거래소82 : NASDAQ                             |
| -IsuNo             | 종목번호               | String | Y          | 12       | 단축종목코드ex.TSLA                                     |
| -OrdQty            | 주문수량               | Number | Y          | 16       |                                                   |
| -OvrsOrdPrc        | 해외주문가              | Number | Y          | 28.7     |                                                   |
| -OrdprcPtnCode     | 호가유형코드             | String | Y          | 2        | 00@지정가M1@LOOM2@LOC매도인경우 호가유형 확대03@시장가M3@MOOM4@MOC |
| -BrkTpCode         | 중개인구분코드            | String | Y          | 2        |                                                   |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element             | 한글명                 | type   | Required   | Length   | Description   |
|:--------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| COSAT00301OutBlock1 | COSAT00301OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdPtnCode         | 주문유형코드              | String | Y          | 2        |               |
| -OrgOrdNo           | 원주문번호               | Number | Y          | 10       |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -InptPwd            | 입력비밀번호              | String | Y          | 8        |               |
| -OrdMktCode         | 주문시장코드              | String | Y          | 2        |               |
| -IsuNo              | 종목번호                | String | Y          | 12       |               |
| -OrdQty             | 주문수량                | Number | Y          | 16       |               |
| -OvrsOrdPrc         | 해외주문가               | Number | Y          | 28.7     |               |
| -OrdprcPtnCode      | 호가유형코드              | String | Y          | 2        |               |
| -RegCommdaCode      | 등록통신매체코드            | String | Y          | 2        |               |
| -BrkTpCode          | 중개인구분코드             | String | Y          | 2        |               |
| COSAT00301OutBlock2 | COSAT00301OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdNo              | 주문번호                | Number | Y          | 10       |               |
| -AcntNm             | 계좌명                 | String | Y          | 40       |               |
| -IsuNm              | 종목명                 | String | Y          | 40       |               |


### 💡 Request Example
```json
{
  "COSAT00301InBlock1": {
    "RecCnt": 1,
    "OrdPtnCode": "02",
    "OrdMktCode": "82",
    "IsuNo": "PLTR",
    "OrdQty": 5,
    "OvrsOrdPrc": 70,
    "OrdprcPtnCode": "00",
    "BrkTpCode": ""
  }
}
```

---

## 🏷️ 미국시장정정주문 API (COSAT00311)
### 요청 Header
| Element       | 한글명     | type   | Required   |   Length | Description                                                                     |
|:--------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰    | String | Y          |     1000 | OAuth토큰이필요한API경우발급한AccessToken을설정하기위한RequestHeaederParameter                    |
| tr_cd         | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont       | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key   | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |
| mac_address   | MAC주소   | String | Y          |       12 | 법인인경우필수세팅                                                                       |


### 요청 Body
| Element            | 한글명                | type   | Required   | Length   | Description       |
|:-------------------|:-------------------|:-------|:-----------|:---------|:------------------|
| COSAT00311InBlock1 | COSAT00311InBlock1 | Object | Y          | -        |                   |
| -RecCnt            | 레코드갯수              | Number | Y          | 5        | 00001             |
| -OrdPtnCode        | 주문유형코드             | String | Y          | 2        | 07@정정주문           |
| -OrgOrdNo          | 원주문번호              | Number | Y          | 10       |                   |
| -OrdMktCode        | 주문시장코드             | String | Y          | 2        | 81@뉴욕거래소82@NASDAQ |
| -IsuNo             | 종목번호               | String | Y          | 12       |                   |
| -OrdQty            | 주문수량               | Number | Y          | 16       | 0 입력              |
| -OvrsOrdPrc        | 해외주문가              | Number | Y          | 28.7     |                   |
| -OrdprcPtnCode     | 호가유형코드             | String | Y          | 2        |                   |
| -BrkTpCode         | 중개인구분코드            | String | Y          | 2        |                   |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element              | 한글명                 | type   | Required   | Length   | Description   |
|:---------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| -COSAT00311OutBlock1 | COSAT00311OutBlock1 | Object | Y          | -        |               |
| -RecCnt              | 레코드갯수               | Object | Y          | 5        |               |
| -OrdPtnCode          | 주문유형코드              | String | Y          | 2        |               |
| -OrgOrdNo            | 원주문번호               | Object | Y          | 10       |               |
| -AcntNo              | 계좌번호                | String | Y          | 20       |               |
| -InptPwd             | 입력비밀번호              | String | Y          | 8        |               |
| -OrdMktCode          | 주문시장코드              | String | Y          | 2        |               |
| -IsuNo               | 종목번호                | String | Y          | 12       |               |
| -OrdQty              | 주문수량                | Object | Y          | 16       |               |
| -OvrsOrdPrc          | 해외주문가               | Object | Y          | 28.7     |               |
| -OrdprcPtnCode       | 호가유형코드              | String | Y          | 2        |               |
| -RegCommdaCode       | 등록통신매체코드            | String | Y          | 2        |               |
| -BrkTpCode           | 중개인구분코드             | String | Y          | 2        |               |
| -COSAT00311OutBlock2 | COSAT00311OutBlock2 | Object | Y          | -        |               |
| -RecCnt              | 레코드갯수               | Object | Y          | 5        |               |
| -OrdNo               | 주문번호                | Object | Y          | 10       |               |
| -AcntNm              | 계좌명                 | String | Y          | 40       |               |
| -IsuNm               | 종목명                 | String | Y          | 40       |               |


---

## 🏷️ 해외증권 매도상환주문(미국) (COSMT00300)
### 요청 Header
| Element       | 한글명     | type   | Required   |   Length | Description                                                                     |
|:--------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰    | String | Y          |     1000 | OAuth토큰이필요한API경우발급한AccessToken을설정하기위한RequestHeaederParameter                    |
| tr_cd         | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont       | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key   | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |
| mac_address   | MAC주소   | String | Y          |       12 | 법인인경우필수세팅                                                                       |


### 요청 Body
| Element             | 한글명                | type   | Required   | Length   | Description   |
|:--------------------|:-------------------|:-------|:-----------|:---------|:--------------|
| -COSMT00300InBlock1 | COSMT00300InBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수              | Object | Y          | 5        |               |
| -OrdPtnCode         | 주문유형코드             | String | Y          | 2        |               |
| -OrgOrdNo           | 원주문번호              | Object | Y          | 10       |               |
| -AcntNo             | 계좌번호               | String | Y          | 20       |               |
| -InptPwd            | 입력비밀번호             | String | Y          | 8        |               |
| -OrdMktCode         | 주문시장코드             | String | Y          | 2        |               |
| -IsuNo              | 종목번호               | String | Y          | 12       |               |
| -OrdQty             | 주문수량               | Object | Y          | 16       |               |
| -OvrsOrdPrc         | 해외주문가              | Object | Y          | 28.7     |               |
| -OrdprcPtnCode      | 호가유형코드             | String | Y          | 2        |               |
| -BrkTpCode          | 중개인구분코드            | String | Y          | 2        |               |
| -MgntrnCode         | 신용거래코드             | String | Y          | 3        |               |
| -LoanDt             | 대출일자               | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element              | 한글명                 | type   | Required   | Length   | Description   |
|:---------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| -LoanDtlClssCode     | 대출상세분류코드            | String | Y          | 2        |               |
| -COSMT00300OutBlock1 | COSMT00300OutBlock1 | Object | Y          | -        |               |
| -RecCnt              | 레코드갯수               | Object | Y          | 5        |               |
| -OrdPtnCode          | 주문유형코드              | String | Y          | 2        |               |
| -OrgOrdNo            | 원주문번호               | Object | Y          | 10       |               |
| -AcntNo              | 계좌번호                | String | Y          | 20       |               |
| -InptPwd             | 입력비밀번호              | String | Y          | 8        |               |
| -OrdMktCode          | 주문시장코드              | String | Y          | 2        |               |
| -IsuNo               | 종목번호                | String | Y          | 12       |               |
| -OrdQty              | 주문수량                | Object | Y          | 16       |               |
| -OvrsOrdPrc          | 해외주문가               | Object | Y          | 28.7     |               |
| -OrdprcPtnCode       | 호가유형코드              | String | Y          | 2        |               |
| -RegCommdaCode       | 등록통신매체코드            | String | Y          | 2        |               |
| -BrkTpCode           | 중개인구분코드             | String | Y          | 2        |               |
| -MgntrnCode          | 신용거래코드              | String | Y          | 3        |               |
| -LoanDt              | 대출일자                | String | Y          | 8        |               |
| -LoanDtlClssCode     | 대출상세분류코드            | String | Y          | 2        |               |
| -COSMT00300OutBlock2 | COSMT00300OutBlock2 | Object | Y          | -        |               |
| -RecCnt              | 레코드갯수               | Object | Y          | 5        |               |
| -OrdNo               | 주문번호                | Object | Y          | 10       |               |
| -AcntNm              | 계좌명                 | String | Y          | 40       |               |
| -IsuNm               | 종목명                 | String | Y          | 40       |               |


---

## 🏷️ 해외주식 예약주문 등록 및 취소 (COSAT00400)
### 요청 Header
| Element       | 한글명     | type   | Required   |   Length | Description                                                                     |
|:--------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰    | String | Y          |     1000 | OAuth토큰이필요한API경우발급한AccessToken을설정하기위한RequestHeaederParameter                    |
| tr_cd         | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont       | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key   | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |
| mac_address   | MAC주소   | String | Y          |       12 | 법인인경우필수세팅                                                                       |


### 요청 Body
| Element             | 한글명                | type   | Required   | Length   | Description   |
|:--------------------|:-------------------|:-------|:-----------|:---------|:--------------|
| -COSAT00400InBlock1 | COSAT00400InBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수              | Object | Y          | 5        |               |
| -TrxTpCode          | 처리구분코드             | String | Y          | 1        |               |
| -CntryCode          | 국가코드               | String | Y          | 3        |               |
| -RsvOrdInptDt       | 예약주문입력일자           | String | Y          | 8        |               |
| -RsvOrdNo           | 예약주문번호             | Object | Y          | 10       |               |
| -BnsTpCode          | 매매구분코드             | String | Y          | 1        |               |
| -AcntNo             | 계좌번호               | String | Y          | 20       |               |
| -Pwd                | 비밀번호               | String | Y          | 8        |               |
| -FcurrMktCode       | 외화시장코드             | String | Y          | 2        |               |
| -IsuNo              | 종목번호               | String | Y          | 12       |               |
| -OrdQty             | 주문수량               | Object | Y          | 16       |               |
| -OvrsOrdPrc         | 해외주문가              | Object | Y          | 28.7     |               |
| -OrdprcPtnCode      | 호가유형코드             | String | Y          | 2        |               |
| -RsvOrdSrtDt        | 예약주문시작일자           | String | Y          | 8        |               |
| -RsvOrdEndDt        | 예약주문종료일자           | String | Y          | 8        |               |
| -RsvOrdCndiCode     | 예약주문조건코드           | String | Y          | 2        |               |
| -MgntrnCode         | 신용거래코드             | String | Y          | 3        |               |
| -LoanDt             | 대출일자               | String | Y          | 8        |               |
| -LoanDtlClssCode    | 대출상세분류코드           | String | Y          | 2        |               |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element              | 한글명                 | type   | Required   | Length   | Description   |
|:---------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| -COSAT00400OutBlock1 | COSAT00400OutBlock1 | Object | Y          | -        |               |
| -RecCnt              | 레코드갯수               | Object | Y          | 5        |               |
| -TrxTpCode           | 처리구분코드              | String | Y          | 1        |               |
| -CntryCode           | 국가코드                | String | Y          | 3        |               |
| -RsvOrdInptDt        | 예약주문입력일자            | String | Y          | 8        |               |
| -RsvOrdNo            | 예약주문번호              | Object | Y          | 10       |               |
| -BnsTpCode           | 매매구분코드              | String | Y          | 1        |               |
| -AcntNo              | 계좌번호                | String | Y          | 20       |               |
| -Pwd                 | 비밀번호                | String | Y          | 8        |               |
| -FcurrMktCode        | 외화시장코드              | String | Y          | 2        |               |
| -IsuNo               | 종목번호                | String | Y          | 12       |               |
| -OrdQty              | 주문수량                | Object | Y          | 16       |               |
| -OvrsOrdPrc          | 해외주문가               | Object | Y          | 28.7     |               |
| -RegCommdaCode       | 등록통신매체코드            | String | Y          | 2        |               |
| -OrdprcPtnCode       | 호가유형코드              | String | Y          | 2        |               |
| -RsvOrdSrtDt         | 예약주문시작일자            | String | Y          | 8        |               |
| -RsvOrdEndDt         | 예약주문종료일자            | String | Y          | 8        |               |
| -RsvOrdCndiCode      | 예약주문조건코드            | String | Y          | 2        |               |
| -MgntrnCode          | 신용거래코드              | String | Y          | 3        |               |
| -LoanDt              | 대출일자                | String | Y          | 8        |               |
| -LoanDtlClssCode     | 대출상세분류코드            | String | Y          | 2        |               |
| -COSAT00400OutBlock2 | COSAT00400OutBlock2 | Object | Y          | -        |               |
| -RecCnt              | 레코드갯수               | Object | Y          | 5        |               |
| -RsvOrdNo            | 예약주문번호              | Object | Y          | 10       |               |


---
