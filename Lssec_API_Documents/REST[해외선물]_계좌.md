# REST[해외선물] 계좌
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=c1ef0e8b-4666-4d8c-a77f-6ab488cfdb39&api_id=44c1c082-c899-48fb-bc66-bb5be2f0ab4e

## 📌 기본 정보
| 항목           | 내용                                              |
|:-------------|:------------------------------------------------|
| Method       | POST                                            |
| Domain       | https://openapi.ls-sec.co.kr:8080               |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080               |
| 모의투자 도메인     |                                                 |
| URL          | /overseas-futureoption/accno                    |
| Format       | JSON                                            |
| Content-Type | application/json; charset=UTF-8                 |
| Description  | 해외선물옵션 계좌별 거래내역 및 잔고 등 계좌에 관련된 서비스를 확인할 수 있습니다. |


## 🏷️ 해외선물 체결내역개별 조회(주문가능수량) (CIDBQ01400)
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
| Element             | 한글명                | type   | Required   | Length   | Description    |
|:--------------------|:-------------------|:-------|:-----------|:---------|:---------------|
| CIDBQ01400InBlock1  | CIDBQ01400InBlock1 | Object | Y          | -        |                |
| -QryTpCode          | 조회구분코드             | String | Y          | 1        | 1:신규           |
|                     |                    |        |            |          | 2:청산           |
|                     |                    |        |            |          | 3:총가능          |
| -IsuCodeVal         | 종목코드값              | String | Y          | 30       |                |
| -BnsTpCode          | 매매구분코드             | String | Y          | 1        | 1:매도           |
|                     |                    |        |            |          | 2:매수           |
| -OvrsDrvtOrdPrc     | 해외파생주문가격           | Number | Y          | 30.11    | 지정가 (시장가인경우 0) |
| -AbrdFutsOrdPtnCode | 해외선물주문유형코드         | String | Y          | 1        | 1: 시장가         |
|                     |                    |        |            |          | 2: 지정가         |


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
| CIDBQ01400OutBlock1 | CIDBQ01400OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -QryTpCode          | 조회구분코드              | String | Y          | 1        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -IsuCodeVal         | 종목코드값               | String | Y          | 18       |               |
| -BnsTpCode          | 매매구분코드              | String | Y          | 1        |               |
| -OvrsDrvtOrdPrc     | 해외파생주문가격            | Number | Y          | 30.11    |               |
| -AbrdFutsOrdPtnCode | 해외선물주문유형코드          | String | Y          | 1        |               |
| CIDBQ01400OutBlock2 | CIDBQ01400OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -OrdAbleQty         | 주문가능수량              | Number | Y          | 16       |               |


### 💡 Request Example
```json
{
  "CIDBQ01400InBlock1": {
    "RecCnt": 1,
    "QryTpCode": "1",
    "IsuCodeVal": "ADM23",
    "BnsTpCode": "2",
    "OvrsDrvtOrdPrc": 1.0,
    "AbrdFutsOrdPtnCode": "1"
  }
}
```

### 💡 Response Example
```json
{
  "CIDBQ01400OutBlock1": {
    "RecCnt": 1,
    "QryTpCode": "1",
    "AcntNo": "20629783903",
    "IsuCodeVal": "ADM23",
    "BnsTpCode": "2",
    "OvrsDrvtOrdPrc": "1.00000000000",
    "AbrdFutsOrdPtnCode": "1"
  },
  "CIDBQ01400OutBlock2": {
    "RecCnt": 1,
    "OrdAbleQty": 992
  },
  "rsp_cd": "00136",
  "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 해외선물 미결제잔고내역 조회 (CIDBQ01500)
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
| CIDBQ01500InBlock1 | CIDBQ01500InBlock1 | Object | Y          | -        |               |
| -AcntTpCode        | 계좌구분코드             | String | Y          | 1        | 1:위탁          |
| -QryDt             | 조회일자               | String | Y          | 8        |               |
| -BalTpCode         | 잔고구분코드             | String | Y          | 1        | 1:합산2:건별      |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                     | 한글명                         | type         | Required   | Length   | Description   |
|:----------------------------|:----------------------------|:-------------|:-----------|:---------|:--------------|
| CIDBQ01500OutBlock1         | CIDBQ01500OutBlock1         | Object       | Y          | -        |               |
| -RecCnt                     | 레코드갯수                       | Number       | Y          | 5        |               |
| -AcntTpCode                 | 계좌구분코드                      | String       | Y          | 1        |               |
| -AcntNo                     | 계좌번호                        | String       | Y          | 20       |               |
| -FcmAcntNo                  | FCM계좌번호                     | String       | Y          | 20       |               |
| -Pwd                        | 비밀번호                        | String       | Y          | 8        |               |
| -QryDt                      | 조회일자                        | String       | Y          | 8        |               |
| -BalTpCode                  | 잔고구분코드                      | String       | Y          | 1        |               |
| CIDBQ01500OutBlock2(Occurs) | CIDBQ01500OutBlock2(Occurs) | Object Array | Y          | -        |               |
| -BaseDt                     | 기준일자                        | String       | Y          | 8        |               |
| -Dps                        | 예수금                         | Number       | Y          | 16       |               |
| -LpnlAmt                    | 청산손익금액                      | Number       | Y          | 19.2     |               |
| -FutsDueBfLpnlAmt           | 선물만기전청산손익금액                 | Number       | Y          | 23.2     |               |
| -FutsDueBfCmsn              | 선물만기전수수료                    | Number       | Y          | 23.2     |               |
| -CsgnMgn                    | 위탁증거금액                      | Number       | Y          | 16       |               |
| -MaintMgn                   | 유지증거금                       | Number       | Y          | 16       |               |
| -CtlmtAmt                   | 신용한도금액                      | Number       | Y          | 23.2     |               |
| -AddMgn                     | 추가증거금액                      | Number       | Y          | 16       |               |
| -MgnclRat                   | 마진콜율                        | Number       | Y          | 27.1     |               |
| -OrdAbleAmt                 | 주문가능금액                      | Number       | Y          | 16       |               |
| -WthdwAbleAmt               | 인출가능금액                      | Number       | Y          | 16       |               |
| -AcntNo                     | 계좌번호                        | String       | Y          | 20       |               |
| -IsuCodeVal                 | 종목코드값                       | String       | Y          | 30       |               |
| -IsuNm                      | 종목명                         | String       | Y          | 50       |               |
| -CrcyCodeVal                | 통화코드값                       | String       | Y          | 3        |               |
| -OvrsDrvtPrdtCode           | 해외파생상품코드                    | String       | Y          | 10       |               |
| -OvrsDrvtOptTpCode          | 해외파생옵션구분코드                  | String       | Y          | 1        |               |
| -DueDt                      | 만기일자                        | String       | Y          | 8        |               |
| -OvrsDrvtXrcPrc             | 해외파생행사가격                    | Number       | Y          | 30.11    |               |
| -BnsTpCode                  | 매매구분코드                      | String       | Y          | 1        |               |
| -CmnCodeNm                  | 공통코드명                       | String       | Y          | 100      |               |
| -TpCodeNm                   | 구분코드명                       | String       | Y          | 50       |               |
| -BalQty                     | 잔고수량                        | Number       | Y          | 16       |               |
| -PchsPrc                    | 매입가격                        | Number       | Y          | 30.11    |               |
| -OvrsDrvtNowPrc             | 해외파생현재가                     | Number       | Y          | 30.11    |               |
| -AbrdFutsEvalPnlAmt         | 해외선물평가손익금액                  | Number       | Y          | 19.2     |               |
| -CsgnCmsn                   | 위탁수수료                       | Number       | Y          | 19.2     |               |
| -PosNo                      | 포지션번호                       | String       | Y          | 13       |               |
| -EufOneCmsnAmt              | 거래소비용1수수료금액                 | Number       | Y          | 19.2     |               |
| -EufTwoCmsnAmt              | 거래소비용2수수료금액                 | Number       | Y          | 19.2     |               |


### 💡 Request Example
```json
{
  "CIDBQ01500InBlock1": {
    "RecCnt": 1,
    "AcntTpCode": "1",
    "FcmAcntNo": " ",
    "QryDt": "20230609",
    "BalTpCode": "1"
  }
}
```

### 💡 Response Example
```json
{
  "CIDBQ01500OutBlock1": {
    "RecCnt": 1,
    "AcntTpCode": "1",
    "AcntNo": "20629783903",
    "FcmAcntNo": "",
    "Pwd": "********",
    "QryDt": "20230609",
    "BalTpCode": "1"
  },
  "CIDBQ01500OutBlock2": [
    {
      "BaseDt": "20230609",
      "Dps": 0,
      "LpnlAmt": "0.00",
      "FutsDueBfLpnlAmt": "0.00",
      "FutsDueBfCmsn": "0.00",
      "CsgnMgn": 0,
      "MaintMgn": 0,
      "CtlmtAmt": "0.00",
      "AddMgn": 0,
      "MgnclRat": "0.0000000000",
      "OrdAbleAmt": 0,
      "WthdwAbleAmt": 0,
      "AcntNo": "20629783903",
      "IsuCodeVal": "ADM23",
      "IsuNm": "Australian Dollar(2023.06)",
      "CrcyCodeVal": "USD",
      "OvrsDrvtPrdtCode": "AD",
      "OvrsDrvtOptTpCode": "F",
      "DueDt": "20230616",
      "OvrsDrvtXrcPrc": "0.00000000000",
      "BnsTpCode": "1",
      "CmnCodeNm": "매도",
      "TpCodeNm": "일반",
      "BalQty": 2,
      "PchsPrc": "0.67130000000",
      "OvrsDrvtNowPrc": "0.67155000000",
      "AbrdFutsEvalPnlAmt": "-50.00",
      "CsgnCmsn": "15.00",
      "PosNo": "",
      "EufOneCmsnAmt": "0.00",
      "EufTwoCmsnAmt": "0.00"
    }
  ],
  "rsp_cd": "00136",
  "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 해외선물 주문내역 조회 (CIDBQ01800)
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
| Element            | 한글명                | type   | Required   | Length   | Description                   |
|:-------------------|:-------------------|:-------|:-----------|:---------|:------------------------------|
| CIDBQ01800InBlock1 | CIDBQ01800InBlock1 | Object | Y          | -        |                               |
| -IsuCodeVal        | 종목코드값              | String | Y          | 30       |                               |
| -OrdDt             | 주문일자               | String | Y          | 8        | YYYYMMDD 형식                   |
| -ThdayTpCode       | 당일구분코드             | String | Y          | 1        | SPACE                         |
| -OrdStatCode       | 주문상태코드             | String | Y          | 1        | 0:전체1:체결2:미체결                 |
| -BnsTpCode         | 매매구분코드             | String | Y          | 1        | 0:전체1:매도2:매수                  |
| -QryTpCode         | 조회구분코드             | String | Y          | 1        | 1:역순2:정순                      |
| -OrdPtnCode        | 주문유형코드             | String | Y          | 2        | 00:전체01:일반02:Average03:Spread |
| -OvrsDrvtFnoTpCode | 해외파생선물옵션구분코드       | String | Y          | 1        | A:전체F:선물O:옵션                  |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                     | 한글명                         | type         | Required   | Length   | Description                |
|:----------------------------|:----------------------------|:-------------|:-----------|:---------|:---------------------------|
| CIDBQ01800OutBlock1         | CIDBQ01800OutBlock1         | Object       | Y          | -        |                            |
| -RecCnt                     | 레코드갯수                       | Number       | Y          | 5        |                            |
| -AcntNo                     | 계좌번호                        | String       | Y          | 20       |                            |
| -Pwd                        | 비밀번호                        | String       | Y          | 8        |                            |
| -IsuCodeVal                 | 종목코드값                       | String       | Y          | 30       |                            |
| -OrdDt                      | 주문일자                        | String       | Y          | 8        |                            |
| -ThdayTpCode                | 당일구분코드                      | String       | Y          | 1        |                            |
| -OrdStatCode                | 주문상태코드                      | String       | Y          | 1        |                            |
| -BnsTpCode                  | 매매구분코드                      | String       | Y          | 1        |                            |
| -QryTpCode                  | 조회구분코드                      | String       | Y          | 1        |                            |
| -OrdPtnCode                 | 주문유형코드                      | String       | Y          | 2        |                            |
| -OvrsDrvtFnoTpCode          | 해외파생선물옵션구분코드                | String       | Y          | 1        |                            |
| CIDBQ01800OutBlock2(Occurs) | CIDBQ01800OutBlock2(Occurs) | Object Array | Y          | -        |                            |
| -OvrsFutsOrdNo              | 해외선물주문번호                    | String       | Y          | 10       |                            |
| -OvrsFutsOrgOrdNo           | 해외선물원주문번호                   | String       | Y          | 10       |                            |
| -FcmOrdNo                   | FCM주문번호                     | String       | Y          | 15       |                            |
| -IsuCodeVal                 | 종목코드값                       | String       | Y          | 30       |                            |
| -IsuNm                      | 종목명                         | String       | Y          | 50       |                            |
| -AbrdFutsXrcPrc             | 해외선물행사가격                    | Number       | Y          | 30.11    |                            |
| -FcmAcntNo                  | FCM계좌번호                     | String       | Y          | 20       |                            |
| -BnsTpCode                  | 매매구분코드                      | String       | Y          | 1        |                            |
| -BnsTpNm                    | 매매구분명                       | String       | Y          | 10       |                            |
| -FutsOrdStatCode            | 선물주문상태코드                    | String       | Y          | 1        |                            |
| -TpCodeNm                   | 구분코드명                       | String       | Y          | 50       | 주문, 접수, 확인, 체결, 소멸, 거부     |
| -FutsOrdTpCode              | 선물주문구분코드                    | String       | Y          | 1        |                            |
| -TrdTpNm                    | 거래구분명                       | String       | Y          | 20       | 신규, 정정, 취소, 이관, 수관, 소멸, 장애 |
| -AbrdFutsOrdPtnCode         | 해외선물주문유형코드                  | String       | Y          | 1        |                            |
| -OrdPtnNm                   | 주문유형명                       | String       | Y          | 40       |                            |
| -OrdPtnTermTpCode           | 주문유형기간구분코드                  | String       | Y          | 2        |                            |
| -CmnCodeNm                  | 공통코드명                       | String       | Y          | 100      |                            |
| -AppSrtDt                   | 적용시작일자                      | String       | Y          | 8        |                            |
| -AppEndDt                   | 적용종료일자                      | String       | Y          | 8        |                            |
| -OvrsDrvtOrdPrc             | 해외파생주문가격                    | Number       | Y          | 30.11    |                            |
| -OrdQty                     | 주문수량                        | Number       | Y          | 16       |                            |
| -OvrsDrvtExecIsuCode        | 해외파생체결종목코드                  | String       | Y          | 30       |                            |
| -ExecIsuNm                  | 체결종목명                       | String       | Y          | 50       |                            |
| -ExecBnsTpCode              | 체결매매구분코드                    | String       | Y          | 1        |                            |
| -ExecBnsTpNm                | 체결매매구분명                     | String       | Y          | 10       |                            |
| -AbrdFutsExecPrc            | 해외선물체결가격                    | Number       | Y          | 30.11    |                            |
| -ExecQty                    | 체결수량                        | Number       | Y          | 16       |                            |
| -OrdCndiPrc                 | 주문조건가격                      | Number       | Y          | 30.11    |                            |
| -OvrsDrvtNowPrc             | 해외파생현재가                     | Number       | Y          | 30.11    |                            |
| -MdfyQty                    | 정정수량                        | Number       | Y          | 16       |                            |
| -CancQty                    | 취소수량                        | Number       | Y          | 16       |                            |
| -RjtQty                     | 거부수량                        | Number       | Y          | 13       |                            |
| -CnfQty                     | 확인수량                        | Number       | Y          | 16       |                            |
| -UnercQty                   | 미체결수량                       | Number       | Y          | 16       |                            |
| -CvrgYn                     | 반대매매여부                      | String       | Y          | 1        |                            |
| -RegTmnlNo                  | 등록단말번호                      | String       | Y          | 3        |                            |
| -RegBrnNo                   | 등록지점번호                      | String       | Y          | 3        |                            |
| -RegUserId                  | 등록사용자ID                     | String       | Y          | 16       |                            |
| -OrdDt                      | 주문일자                        | String       | Y          | 8        |                            |
| -OrdTime                    | 주문시각                        | String       | Y          | 9        |                            |
| -OvrsOptXrcRsvTpCode        | 해외옵션행사예약구분코드                | String       | Y          | 1        | 1:만기행사                     |
| -OvrsDrvtOptTpCode          | 해외파생옵션구분코드                  | String       | Y          | 1        |                            |
| -SprdBaseIsuYn              | 스프레드기준종목여부                  | String       | Y          | 1        |                            |
| -OvrsFutsOrdDt              | 해외선물주문일자                    | String       | Y          | 8        |                            |
| -OvrsFutsOrdNo2             | 해외선물주문번호2                   | String       | Y          | 10       |                            |
| -OvrsFutsOrgOrdNo2          | 해외선물원주문번호2                  | String       | Y          | 10       |                            |
| -OvrsDrvtIsuCode2           | 해외파생종목코드2                   | String       | Y          | 30       |                            |


### 💡 Request Example
```json
{
  "CIDBQ01800InBlock1": {
    "RecCnt": 1,
    "IsuCodeVal": "ADM23",
    "OrdDt": "20230609",
    "ThdayTpCode": " ",
    "OrdStatCode": "0",
    "BnsTpCode": "0",
    "QryTpCode": "2",
    "OrdPtnCode": "00",
    "OvrsDrvtFnoTpCode": "A"
  }
}
```

### 💡 Response Example
```json
{
  "CIDBQ01800OutBlock1": {
    "RecCnt": 1,
    "AcntNo": "20629783903",
    "Pwd": "********",
    "IsuCodeVal": "ADM23",
    "OrdDt": "20230609",
    "ThdayTpCode": "",
    "OrdStatCode": "0",
    "BnsTpCode": "0",
    "QryTpCode": "2",
    "OrdPtnCode": "00",
    "OvrsDrvtFnoTpCode": "A"
  },
  "CIDBQ01800OutBlock2": [
    {
      "OvrsFutsOrdNo": "0000000087",
      "OvrsFutsOrgOrdNo": "0000000000",
      "FcmOrdNo": "0000000087",
      "IsuCodeVal": "ADM23",
      "IsuNm": "Australian Dollar(2023.06)",
      "AbrdFutsXrcPrc": "0.00000000000",
      "FcmAcntNo": "LAP18968S",
      "BnsTpCode": "1",
      "BnsTpNm": "매도",
      "FutsOrdStatCode": "4",
      "TpCodeNm": "체결",
      "FutsOrdTpCode": "1",
      "TrdTpNm": "신규",
      "AbrdFutsOrdPtnCode": "1",
      "OrdPtnNm": "시장가",
      "OrdPtnTermTpCode": "01",
      "CmnCodeNm": "일반",
      "AppSrtDt": "",
      "AppEndDt": "",
      "OvrsDrvtOrdPrc": "122.00000000000",
      "OrdQty": 1,
      "OvrsDrvtExecIsuCode": "ADM23",
      "ExecIsuNm": "Australian Dollar(2023.06)",
      "ExecBnsTpCode": "1",
      "ExecBnsTpNm": "매도",
      "AbrdFutsExecPrc": "0.67070000000",
      "ExecQty": 1,
      "OrdCndiPrc": "0.66400000000",
      "OvrsDrvtNowPrc": "0.67155000000",
      "MdfyQty": 0,
      "CancQty": 0,
      "RjtQty": 0,
      "CnfQty": 0,
      "UnercQty": 0,
      "CvrgYn": "N",
      "RegTmnlNo": "",
      "RegBrnNo": "000",
      "RegUserId": "qzvjaf",
      "OrdDt": "20230609",
      "OrdTime": "150904474",
      "OvrsOptXrcRsvTpCode": "0",
      "OvrsDrvtOptTpCode": "F",
      "SprdBaseIsuYn": "",
      "OvrsFutsOrdDt": "20230609",
      "OvrsFutsOrdNo2": "0000000087",
      "OvrsFutsOrgOrdNo2": "0000000000",
      "OvrsDrvtIsuCode2": "ADM23"
    }
  ],
  "rsp_cd": "00136",
  "rsp_msg": "조회가 완료되었습니다."
}

```

---

## 🏷️ 해외선물 주문체결내역 상세 조회 (CIDBQ02400)
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
| Element            | 한글명                | type   | Required   | Length   | Description                   |
|:-------------------|:-------------------|:-------|:-----------|:---------|:------------------------------|
| CIDBQ02400InBlock1 | CIDBQ02400InBlock1 | Object | Y          | -        |                               |
| -IsuCodeVal        | 종목코드값              | String | Y          | 30       |                               |
| -QrySrtDt          | 조회시작일자             | String | Y          | 8        | YYYYMMDD 형식과거조회시는 사용당일조회시는 공백 |
| -QryEndDt          | 조회종료일자             | String | Y          | 8        | YYYYMMDD 형식과거조회시는 사용당일조회시는 공백 |
| -ThdayTpCode       | 당일구분코드             | String | Y          | 1        | 0:과거조회1:당일조회                  |
| -OrdStatCode       | 주문상태코드             | String | Y          | 1        | 0:전체1:체결2:미체결                 |
| -BnsTpCode         | 매매구분코드             | String | Y          | 1        | 0:전체1:매도2:매수                  |
| -QryTpCode         | 조회구분코드             | String | Y          | 1        | 1:역순2:정순                      |
| -OrdPtnCode        | 주문유형코드             | String | Y          | 2        | 00:전체01:일반02:Average03:Spread |
| -OvrsDrvtFnoTpCode | 해외파생선물옵션구분코드       | String | Y          | 1        | A:전체F:선물O:옵션                  |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                     | 한글명                         | type         | Required   | Length   | Description                                                            |
|:----------------------------|:----------------------------|:-------------|:-----------|:---------|:-----------------------------------------------------------------------|
| CIDBQ02400OutBlock1         | CIDBQ02400OutBlock1         | Object       | Y          | -        |                                                                        |
| -RecCnt                     | 레코드갯수                       | Number       | Y          | 5        |                                                                        |
| -AcntNo                     | 계좌번호                        | String       | Y          | 20       |                                                                        |
| -Pwd                        | 비밀번호                        | String       | Y          | 8        |                                                                        |
| -IsuCodeVal                 | 종목코드값                       | String       | Y          | 30       |                                                                        |
| -QrySrtDt                   | 조회시작일자                      | String       | Y          | 8        |                                                                        |
| -QryEndDt                   | 조회종료일자                      | String       | Y          | 8        |                                                                        |
| -ThdayTpCode                | 당일구분코드                      | String       | Y          | 1        |                                                                        |
| -OrdStatCode                | 주문상태코드                      | String       | Y          | 1        |                                                                        |
| -BnsTpCode                  | 매매구분코드                      | String       | Y          | 1        |                                                                        |
| -QryTpCode                  | 조회구분코드                      | String       | Y          | 1        |                                                                        |
| -OrdPtnCode                 | 주문유형코드                      | String       | Y          | 2        |                                                                        |
| -OvrsDrvtFnoTpCode          | 해외파생선물옵션구분코드                | String       | Y          | 1        |                                                                        |
| CIDBQ02400OutBlock2(Occurs) | CIDBQ02400OutBlock2(Occurs) | Object Array | Y          | -        |                                                                        |
| -OrdDt                      | 주문일자                        | String       | Y          | 8        |                                                                        |
| -OvrsFutsOrdNo              | 해외선물주문번호                    | String       | Y          | 10       |                                                                        |
| -OvrsFutsOrgOrdNo           | 해외선물원주문번호                   | String       | Y          | 10       |                                                                        |
| -FcmOrdNo                   | FCM주문번호                     | String       | Y          | 15       |                                                                        |
| -ExecDt                     | 체결일자                        | String       | Y          | 8        |                                                                        |
| -OvrsFutsExecNo             | 해외선물체결번호                    | String       | Y          | 10       |                                                                        |
| -FcmAcntNo                  | FCM계좌번호                     | String       | Y          | 20       |                                                                        |
| -IsuCodeVal                 | 종목코드값                       | String       | Y          | 30       |                                                                        |
| -IsuNm                      | 종목명                         | String       | Y          | 50       |                                                                        |
| -AbrdFutsXrcPrc             | 해외선물행사가격                    | Number       | Y          | 30.11    |                                                                        |
| -BnsTpCode                  | 매매구분코드                      | String       | Y          | 1        | 0:전체1:매도2:매수                                                           |
| -BnsTpNm                    | 매매구분명                       | String       | Y          | 10       |                                                                        |
| -FutsOrdStatCode            | 선물주문상태코드                    | String       | Y          | 1        | 0:전체1:체결2:미체결                                                          |
| -TpCodeNm                   | 구분코드명                       | String       | Y          | 50       | 신규, 정정, 취소, 이관, 수관, 소멸, 장애                                             |
| -FutsOrdTpCode              | 선물주문구분코드                    | String       | Y          | 1        | 공백                                                                     |
| -TrdTpNm                    | 거래구분명                       | String       | Y          | 20       | 주문, 접수, 확인, 체결, 소멸, 거부                                                 |
| -AbrdFutsOrdPtnCode         | 해외선물주문유형코드                  | String       | Y          | 1        | 공백                                                                     |
| -OrdPtnNm                   | 주문유형명                       | String       | Y          | 40       | 시장가, 지정가, Stop Market, Stop Limit                                      |
| -OrdPtnTermTpCode           | 주문유형기간구분코드                  | String       | Y          | 2        | 공백                                                                     |
| -CmnCodeNm                  | 공통코드명                       | String       | Y          | 100      | 일반, Spread                                                             |
| -AppSrtDt                   | 적용시작일자                      | String       | Y          | 8        |                                                                        |
| -AppEndDt                   | 적용종료일자                      | String       | Y          | 8        |                                                                        |
| -OrdQty                     | 주문수량                        | Number       | Y          | 16       |                                                                        |
| -OvrsDrvtOrdPrc             | 해외파생주문가격                    | Number       | Y          | 30.11    |                                                                        |
| -OvrsDrvtExecIsuCode        | 해외파생체결종목코드                  | String       | Y          | 30       |                                                                        |
| -ExecIsuNm                  | 체결종목명                       | String       | Y          | 50       |                                                                        |
| -ExecBnsTpCode              | 체결매매구분코드                    | String       | Y          | 1        |                                                                        |
| -ExecBnsTpNm                | 체결매매구분명                     | String       | Y          | 10       |                                                                        |
| -ExecQty                    | 체결수량                        | Number       | Y          | 16       |                                                                        |
| -AbrdFutsExecPrc            | 해외선물체결가격                    | Number       | Y          | 30.11    |                                                                        |
| -OrdCndiPrc                 | 주문조건가격                      | Number       | Y          | 30.11    |                                                                        |
| -OvrsDrvtNowPrc             | 해외파생현재가                     | Number       | Y          | 30.11    |                                                                        |
| -UnercQty                   | 미체결수량                       | Number       | Y          | 16       |                                                                        |
| -TrxStatCode                | 처리상태코드                      | String       | Y          | 2        |                                                                        |
| -TrxStatCodeNm              | 처리상태코드명                     | String       | Y          | 40       | 체결, 체결취소                                                               |
| -CsgnCmsn                   | 위탁수수료                       | Number       | Y          | 19.2     |                                                                        |
| -FcmCmsn                    | FCM수수료                      | Number       | Y          | 21.4     |                                                                        |
| -ThcoCmsn                   | 당사수수료                       | Number       | Y          | 19.2     |                                                                        |
| -MdaCode                    | 매체코드                        | String       | Y          | 2        | 00 창구22 아이폰23 안드로이드41 API43 로보API85 HTS96 최종결제LP 로스컷SK CashCallSO 조건주문 |
| -MdaCodeNm                  | 매체코드명                       | String       | Y          | 40       |                                                                        |
| -RegTmnlNo                  | 등록단말번호                      | String       | Y          | 3        |                                                                        |
| -RegUserId                  | 등록사용자ID                     | String       | Y          | 16       |                                                                        |
| -OrdSndDttm                 | 주문발송일시                      | String       | Y          | 17       |                                                                        |
| -ExecDttm                   | 체결일시                        | String       | Y          | 17       |                                                                        |
| -EufOneCmsnAmt              | 거래소비용1수수료금액                 | Number       | Y          | 19.2     |                                                                        |
| -EufTwoCmsnAmt              | 거래소비용2수수료금액                 | Number       | Y          | 19.2     |                                                                        |
| -LchOneCmsnAmt              | 런던청산소1수수료금액                 | Number       | Y          | 19.2     |                                                                        |
| -LchTwoCmsnAmt              | 런던청산소2수수료금액                 | Number       | Y          | 19.2     |                                                                        |
| -TrdOneCmsnAmt              | 거래1수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -TrdTwoCmsnAmt              | 거래2수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -TrdThreeCmsnAmt            | 거래3수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -StrmOneCmsnAmt             | 단기1수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -StrmTwoCmsnAmt             | 단기2수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -StrmThreeCmsnAmt           | 단기3수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -TransOneCmsnAmt            | 전달1수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -TransTwoCmsnAmt            | 전달2수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -TransThreeCmsnAmt          | 전달3수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -TransFourCmsnAmt           | 전달4수수료금액                    | Number       | Y          | 19.2     |                                                                        |
| -OvrsOptXrcRsvTpCode        | 해외옵션행사예약구분코드                | String       | Y          | 1        | 1:만기행사                                                                 |
| -OvrsDrvtOptTpCode          | 해외파생옵션구분코드                  | String       | Y          | 1        |                                                                        |
| -SprdBaseIsuYn              | 스프레드기준종목여부                  | String       | Y          | 1        |                                                                        |
| -OvrsDrvtIsuCode2           | 해외파생종목코드2                   | String       | Y          | 30       |                                                                        |


### 💡 Request Example
```json
{
  "CIDBQ02400InBlock1": {
    "RecCnt": 1,
    "IsuCodeVal": "ADM23",
    "QrySrtDt": "20230516",
    "QryEndDt": "20230609",
    "ThdayTpCode": "1",
    "OrdStatCode": "0",
    "BnsTpCode": "0",
    "QryTpCode": "2",
    "OrdPtnCode": "00",
    "OvrsDrvtFnoTpCode": "A"
  }
}
```

### 💡 Response Example
```json
{
  "CIDBQ02400OutBlock1": {
    "RecCnt": 1,
    "AcntNo": "20629783903",
    "Pwd": "********",
    "IsuCodeVal": "ADM23",
    "QrySrtDt": "20230516",
    "QryEndDt": "20230609",
    "ThdayTpCode": "1",
    "OrdStatCode": "0",
    "BnsTpCode": "0",
    "QryTpCode": "2",
    "OrdPtnCode": "00",
    "OvrsDrvtFnoTpCode": "A"
  },
  "CIDBQ02400OutBlock2": [
    {
      "OrdDt": "20230609",
      "OvrsFutsOrdNo": "0000000087",
      "OvrsFutsOrgOrdNo": "0000000000",
      "FcmOrdNo": "0000000087",
      "ExecDt": "20230609",
      "OvrsFutsExecNo": "0000000048",
      "FcmAcntNo": "LAP18968S",
      "IsuCodeVal": "ADM23",
      "IsuNm": "Australian Dollar(2023.06)",
      "AbrdFutsXrcPrc": "0.00000000000",
      "BnsTpCode": "1",
      "BnsTpNm": "매도",
      "FutsOrdStatCode": "4",
      "TpCodeNm": "신규",
      "FutsOrdTpCode": "1",
      "TrdTpNm": "체결",
      "AbrdFutsOrdPtnCode": "1",
      "OrdPtnNm": "시장가",
      "OrdPtnTermTpCode": "01",
      "CmnCodeNm": "일반",
      "AppSrtDt": "",
      "AppEndDt": "",
      "OrdQty": 1,
      "OvrsDrvtOrdPrc": "122.00000000000",
      "OvrsDrvtExecIsuCode": "ADM23",
      "ExecIsuNm": "Australian Dollar(2023.06)",
      "ExecBnsTpCode": "1",
      "ExecBnsTpNm": "매도",
      "ExecQty": 1,
      "AbrdFutsExecPrc": "0.67070000000",
      "OrdCndiPrc": "0.66400000000",
      "OvrsDrvtNowPrc": "0.67070000000",
      "UnercQty": 0,
      "TrxStatCode": "1",
      "TrxStatCodeNm": "체결",
      "CsgnCmsn": "7.50",
      "FcmCmsn": "0.0000",
      "ThcoCmsn": "0.00",
      "MdaCode": "40",
      "MdaCodeNm": "40",
      "RegTmnlNo": "",
      "RegUserId": "qzvjaf",
      "OrdSndDttm": "20230609150904474",
      "ExecDttm": "20230609150904559",
      "EufOneCmsnAmt": "0.00",
      "EufTwoCmsnAmt": "0.00",
      "LchOneCmsnAmt": "0.00",
      "LchTwoCmsnAmt": "0.00",
      "TrdOneCmsnAmt": "0.00",
      "TrdTwoCmsnAmt": "0.00",
      "TrdThreeCmsnAmt": "0.00",
      "StrmOneCmsnAmt": "0.00",
      "StrmTwoCmsnAmt": "0.00",
      "StrmThreeCmsnAmt": "0.00",
      "TransOneCmsnAmt": "0.00",
      "TransTwoCmsnAmt": "0.00",
      "TransThreeCmsnAmt": "0.00",
      "TransFourCmsnAmt": "0.00",
      "OvrsOptXrcRsvTpCode": "0",
      "OvrsDrvtOptTpCode": "F",
      "SprdBaseIsuYn": "",
      "OvrsDrvtIsuCode2": "ADM23"
    }
  ],
  "rsp_cd": "00136",
  "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 해외선물 예수금/잔고현황 (CIDBQ03000)
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
| CIDBQ03000InBlock1 | CIDBQ03000InBlock1 | Object | Y          | -        |               |
| -AcntTpCode        | 계좌구분코드             | String | Y          | 1        | 1 : 위탁계좌      |
|                    |                    |        |            |          | 2 : 중개계좌      |
| -TrdDt             | 거래일자               | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element               | 한글명                 | type   | Required   | Length   | Description   |
|:----------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CIDBQ03000OutBlock1   | CIDBQ03000OutBlock1 | Object | Y          | -        |               |
| -RecCnt               | 레코드갯수               | Number | Y          | 5        |               |
| -AcntTpCode           | 계좌구분코드              | String | Y          | 1        |               |
| -AcntNo               | 계좌번호                | String | Y          | 20       |               |
| -AcntPwd              | 계좌비밀번호              | String | Y          | 8        |               |
| -TrdDt                | 거래일자                | String | Y          | 8        |               |
| CIDBQ03000OutBlock2   | CIDBQ03000OutBlock2 | Object | Y          | -        |               |
| -AcntNo               | 계좌번호                | String | Y          | 20       |               |
| -TrdDt                | 거래일자                | String | Y          | 8        |               |
| -CrcyObjCode          | 통화대상코드              | String | Y          | 12       |               |
| -OvrsFutsDps          | 해외선물예수금             | Number | Y          | 23.2     |               |
| -CustmMnyioAmt        | 고객입출금금액             | Number | Y          | 19.2     |               |
| -AbrdFutsLqdtPnlAmt   | 해외선물청산손익금액          | Number | Y          | 19.2     |               |
| -AbrdFutsCmsnAmt      | 해외선물수수료금액           | Number | Y          | 19.2     |               |
| -PrexchDps            | 가환전예수금              | Number | Y          | 19.2     |               |
| -EvalAssetAmt         | 평가자산금액              | Number | Y          | 19.2     |               |
| -AbrdFutsCsgnMgn      | 해외선물위탁증거금액          | Number | Y          | 19.2     |               |
| -AbrdFutsAddMgn       | 해외선물추가증거금액          | Number | Y          | 19.2     |               |
| -AbrdFutsWthdwAbleAmt | 해외선물인출가능금액          | Number | Y          | 19.2     |               |
| -AbrdFutsOrdAbleAmt   | 해외선물주문가능금액          | Number | Y          | 19.2     |               |
| -AbrdFutsEvalPnlAmt   | 해외선물평가손익금액          | Number | Y          | 19.2     |               |
| -LastSettPnlAmt       | 최종결제손익금액            | Number | Y          | 19.2     |               |
| -OvrsOptSettAmt       | 해외옵션결제금액            | Number | Y          | 19.2     |               |
| -OvrsOptBalEvalAmt    | 해외옵션잔고평가금액          | Number | Y          | 19.2     |               |


### 💡 Request Example
```json
{
  "CIDBQ03000InBlock1": {
    "RecCnt": 1,
    "AcntTpCode": "1",
    "TrdDt": "20230609"
  }
}
```

### 💡 Response Example
```json
{
  "CIDBQ03000OutBlock1": {
    "RecCnt": 1,
    "AcntTpCode": "1",
    "AcntNo": "20629783903",
    "AcntPwd": "********",
    "TrdDt": "20230609"
  },
  "CIDBQ03000OutBlock2": [
    {
      "AcntNo": "20629783903",
      "TrdDt": "20230609",
      "CrcyObjCode": "TOT(USD)",
      "OvrsFutsDps": "0.00",
      "CustmMnyioAmt": "0.00",
      "AbrdFutsLqdtPnlAmt": "0.00",
      "AbrdFutsCmsnAmt": "15.00",
      "PrexchDps": "2296914.47",
      "EvalAssetAmt": "2296849.47",
      "AbrdFutsCsgnMgn": "4400.00",
      "AbrdFutsAddMgn": "4465.00",
      "AbrdFutsWthdwAbleAmt": "2187537.60",
      "AbrdFutsOrdAbleAmt": "2183072.60",
      "AbrdFutsEvalPnlAmt": "-50.00",
      "LastSettPnlAmt": "-65.00",
      "OvrsOptSettAmt": "0.00",
      "OvrsOptBalEvalAmt": "0.00"
    }
  ],
  "rsp_cd": "00136",
  "rsp_msg": "조회가 완료되었습니다."
}

```

---

## 🏷️ 해외선물 예탁자산 조회 (CIDBQ05300)
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
| CIDBQ05300InBlock1 | CIDBQ05300InBlock1 | Object | Y          | -        |               |
| -OvrsAcntTpCode    | 해외계좌구분코드           | String | Y          | 1        | 1:위탁          |
| -CrcyCode          | 통화코드               | String | Y          | 3        | ALL:전체        |
|                    |                    |        |            |          | CAD:캐나다 달러    |
|                    |                    |        |            |          | CHF:스위스 프랑    |
|                    |                    |        |            |          | EUR:유럽연합 유로   |
|                    |                    |        |            |          | GBP:영국 파운드    |
|                    |                    |        |            |          | HKD:홍콩 달러     |
|                    |                    |        |            |          | JPY:일본 엔      |
|                    |                    |        |            |          | SGD:싱가포르 달러   |
|                    |                    |        |            |          | USD:미국 달러     |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                  | 한글명                 | type         | Required   | Length   | Description   |
|:-------------------------|:--------------------|:-------------|:-----------|:---------|:--------------|
| CIDBQ05300OutBlock1      | CIDBQ05300OutBlock1 | Object       | Y          | -        |               |
| -RecCnt                  | 레코드갯수               | Number       | Y          | 5        |               |
| -OvrsAcntTpCode          | 해외계좌구분코드            | String       | Y          | 1        |               |
| -FcmAcntNo               | FCM계좌번호             | String       | Y          | 20       |               |
| -AcntNo                  | 계좌번호                | String       | Y          | 20       |               |
| -AcntPwd                 | 계좌비밀번호              | String       | Y          | 8        |               |
| -CrcyCode                | 통화코드                | String       | Y          | 3        |               |
| CIDBQ05300OutBlock2      | CIDBQ05300OutBlock2 | Object Array | Y          | -        |               |
| (Occurs)                 | (Occurs)            |              |            |          |               |
| -AcntNo                  | 계좌번호                | String       | Y          | 20       |               |
| -CrcyCode                | 통화코드                | String       | Y          | 3        |               |
| -OvrsFutsDps             | 해외선물예수금             | Number       | Y          | 23.2     |               |
| -AbrdFutsCsgnMgn         | 해외선물위탁증거금액          | Number       | Y          | 19.2     |               |
| -OvrsFutsSplmMgn         | 해외선물추가증거금           | Number       | Y          | 23.2     |               |
| -CustmLpnlAmt            | 고객청산손익금액            | Number       | Y          | 19.2     |               |
| -AbrdFutsEvalPnlAmt      | 해외선물평가손익금액          | Number       | Y          | 19.2     |               |
| -AbrdFutsCmsnAmt         | 해외선물수수료금액           | Number       | Y          | 19.2     |               |
| -AbrdFutsEvalDpstgTotAmt | 해외선물평가예탁총금액         | Number       | Y          | 19.2     |               |
| -Xchrat                  | 환율                  | Number       | Y          | 15.4     |               |
| -FcurrRealMxchgAmt       | 외화실환전금액             | Number       | Y          | 19.2     |               |
| -AbrdFutsWthdwAbleAmt    | 해외선물인출가능금액          | Number       | Y          | 19.2     |               |
| -AbrdFutsOrdAbleAmt      | 해외선물주문가능금액          | Number       | Y          | 19.2     |               |
| -FutsDueNarrvLqdtPnlAmt  | 선물만기미도래청산손익금액       | Number       | Y          | 19.2     |               |
| -FutsDueNarrvCmsn        | 선물만기미도래수수료          | Number       | Y          | 19.2     |               |
| -AbrdFutsLqdtPnlAmt      | 해외선물청산손익금액          | Number       | Y          | 19.2     |               |
| -OvrsFutsDueCmsn         | 해외선물만기수수료           | Number       | Y          | 19.2     |               |
| -OvrsFutsOptBuyAmt       | 해외선물옵션매수금액          | Number       | Y          | 23.2     |               |
| -OvrsFutsOptSellAmt      | 해외선물옵션매도금액          | Number       | Y          | 23.2     |               |
| -OptBuyMktWrthAmt        | 옵션매수시장가치금액          | Number       | Y          | 19.2     |               |
| -OptSellMktWrthAmt       | 옵션매도시장가치금액          | Number       | Y          | 19.2     |               |
| CIDBQ05300OutBlock3      | CIDBQ05300OutBlock3 | Object       | Y          | -        |               |
| -RecCnt                  | 레코드갯수               | Number       | Y          | 5        |               |
| -OvrsFutsDps             | 해외선물예수금             | Number       | Y          | 23.2     |               |
| -AbrdFutsLqdtPnlAmt      | 해외선물청산손익금액          | Number       | Y          | 19.2     |               |
| -FutsDueNarrvLqdtPnlAmt  | 선물만기미도래청산손익금액       | Number       | Y          | 19.2     |               |
| -AbrdFutsEvalPnlAmt      | 해외선물평가손익금액          | Number       | Y          | 19.2     |               |
| -AbrdFutsEvalDpstgTotAmt | 해외선물평가예탁총금액         | Number       | Y          | 19.2     |               |
| -CustmLpnlAmt            | 고객청산손익금액            | Number       | Y          | 19.2     |               |
| -OvrsFutsDueCmsn         | 해외선물만기수수료           | Number       | Y          | 19.2     |               |
| -FcurrRealMxchgAmt       | 외화실환전금액             | Number       | Y          | 19.2     |               |
| -AbrdFutsCmsnAmt         | 해외선물수수료금액           | Number       | Y          | 19.2     |               |
| -FutsDueNarrvCmsn        | 선물만기미도래수수료          | Number       | Y          | 19.2     |               |
| -AbrdFutsCsgnMgn         | 해외선물위탁증거금액          | Number       | Y          | 19.2     |               |
| -OvrsFutsMaintMgn        | 해외선물유지증거금           | Number       | Y          | 19.2     |               |
| -OvrsFutsOptBuyAmt       | 해외선물옵션매수금액          | Number       | Y          | 23.2     |               |
| -OvrsFutsOptSellAmt      | 해외선물옵션매도금액          | Number       | Y          | 23.2     |               |
| -CtlmtAmt                | 신용한도금액              | Number       | Y          | 23.2     |               |
| -OvrsFutsSplmMgn         | 해외선물추가증거금           | Number       | Y          | 23.2     |               |
| -MgnclRat                | 마진콜율                | Number       | Y          | 27.1     |               |
| -AbrdFutsOrdAbleAmt      | 해외선물주문가능금액          | Number       | Y          | 19.2     |               |
| -AbrdFutsWthdwAbleAmt    | 해외선물인출가능금액          | Number       | Y          | 19.2     |               |
| -OptBuyMktWrthAmt        | 옵션매수시장가치금액          | Number       | Y          | 19.2     |               |
| -OptSellMktWrthAmt       | 옵션매도시장가치금액          | Number       | Y          | 19.2     |               |
| -OvrsOptSettAmt          | 해외옵션결제금액            | Number       | Y          | 19.2     |               |
| -OvrsOptBalEvalAmt       | 해외옵션잔고평가금액          | Number       | Y          | 19.2     |               |


### 💡 Request Example
```json
{
  "CIDBQ05300InBlock1": {
    "RecCnt": 1,
    "OvrsAcntTpCode": "1",
    "FcmAcntNo": " ",
    "CrcyCode": "ALL"
  }
}
```

### 💡 Response Example
```json
{
  "CIDBQ05300OutBlock1": {
    "RecCnt": 1,
    "OvrsAcntTpCode": "1",
    "FcmAcntNo": "",
    "AcntNo": "20629783903",
    "AcntPwd": "********",
    "CrcyCode": "ALL"
  },
  "CIDBQ05300OutBlock2": [
    {
      "AcntNo": "20629783903",
      "CrcyCode": "KRW",
      "OvrsFutsDps": "3000000000.00",
      "AbrdFutsCsgnMgn": "0.00",
      "OvrsFutsSplmMgn": "0.00",
      "CustmLpnlAmt": "0.00",
      "AbrdFutsEvalPnlAmt": "0.00",
      "AbrdFutsCmsnAmt": "0.00",
      "AbrdFutsEvalDpstgTotAmt": "0.00",
      "Xchrat": "0.0000",
      "FcurrRealMxchgAmt": "2187537.60",
      "AbrdFutsWthdwAbleAmt": "2993876677.00",
      "AbrdFutsOrdAbleAmt": "3000000000.00",
      "FutsDueNarrvLqdtPnlAmt": "0.00",
      "FutsDueNarrvCmsn": "0.00",
      "AbrdFutsLqdtPnlAmt": "0.00",
      "OvrsFutsDueCmsn": "0.00",
      "OvrsFutsOptBuyAmt": "0.00",
      "OvrsFutsOptSellAmt": "0.00",
      "OptBuyMktWrthAmt": "0.00",
      "OptSellMktWrthAmt": "0.00"
    },
    {
      "AcntNo": "20629783903",
      "CrcyCode": "USD",
      "OvrsFutsDps": "0.00",
      "AbrdFutsCsgnMgn": "4400.00",
      "OvrsFutsSplmMgn": "4465.00",
      "CustmLpnlAmt": "0.00",
      "AbrdFutsEvalPnlAmt": "-50.00",
      "AbrdFutsCmsnAmt": "15.00",
      "AbrdFutsEvalDpstgTotAmt": "-65.00",
      "Xchrat": "0.0000",
      "FcurrRealMxchgAmt": "0.00",
      "AbrdFutsWthdwAbleAmt": "0.00",
      "AbrdFutsOrdAbleAmt": "2183072.60",
      "FutsDueNarrvLqdtPnlAmt": "0.00",
      "FutsDueNarrvCmsn": "0.00",
      "AbrdFutsLqdtPnlAmt": "0.00",
      "OvrsFutsDueCmsn": "0.00",
      "OvrsFutsOptBuyAmt": "0.00",
      "OvrsFutsOptSellAmt": "0.00",
      "OptBuyMktWrthAmt": "0.00",
      "OptSellMktWrthAmt": "0.00"
    }
  ],
  "CIDBQ05300OutBlock3": {
    "RecCnt": 1,
    "OvrsFutsDps": "0.00",
    "AbrdFutsLqdtPnlAmt": "0.00",
    "FutsDueNarrvLqdtPnlAmt": "0.00",
    "AbrdFutsEvalPnlAmt": "-50.00",
    "AbrdFutsEvalDpstgTotAmt": "-65.00",
    "CustmLpnlAmt": "0.00",
    "OvrsFutsDueCmsn": "0.00",
    "FcurrRealMxchgAmt": "0.00",
    "AbrdFutsCmsnAmt": "15.00",
    "FutsDueNarrvCmsn": "0.00",
    "AbrdFutsCsgnMgn": "4400.00",
    "OvrsFutsMaintMgn": "4400.00",
    "OvrsFutsOptBuyAmt": "0.00",
    "OvrsFutsOptSellAmt": "0.00",
    "CtlmtAmt": "0.00",
    "OvrsFutsSplmMgn": "4465.00",
    "MgnclRat": "0.0000000000",
    "AbrdFutsOrdAbleAmt": "2183072.60",
    "AbrdFutsWthdwAbleAmt": "0.00",
    "OptBuyMktWrthAmt": "0.00",
    "OptSellMktWrthAmt": "0.00",
    "OvrsOptSettAmt": "0.00",
    "OvrsOptBalEvalAmt": "0.00"
  },
  "rsp_cd": "00136",
  "rsp_msg": "조회가 완료되었습니다."
}

```

---

## 🏷️ 일자별 미결제 잔고내역 (CIDEQ00800)
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
| CIDEQ00800InBlock1 | CIDEQ00800InBlock1 | Object | Y          | -        |               |
| -RecCnt            | 레코드갯수              | Number | Y          | 5        |               |
| -TrdDt             | 거래일자               | String | Y          | 8        |               |


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
| CIDEQ00800OutBlock1 | CIDEQ00800OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -AcntPwd            | 계좌비밀번호              | String | Y          | 8        |               |
| -TrdDt              | 거래일자                | String | Y          | 8        |               |
| CIDEQ00800OutBlock2 | CIDEQ00800OutBlock2 | Object | Y          | -        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -TrdDt              | 거래일자                | String | Y          | 8        |               |
| -IsuCodeVal         | 종목코드값               | String | Y          | 30       |               |
| -BnsTpNm            | 매매구분명               | String | Y          | 10       |               |
| -BalQty             | 잔고수량                | Number | Y          | 16       |               |
| -LqdtAbleQty        | 청산가능수량              | Number | Y          | 16       |               |
| -PchsPrc            | 매입가격                | Number | Y          | 30.11    |               |
| -OvrsDrvtNowPrc     | 해외파생현재가             | Number | Y          | 30.11    |               |
| -AbrdFutsEvalPnlAmt | 해외선물평가손익금액          | Number | Y          | 19.2     |               |
| -CustmBalAmt        | 고객잔고금액              | Number | Y          | 19.2     |               |
| -FcurrEvalAmt       | 외화평가금액              | Number | Y          | 21.4     |               |
| -IsuNm              | 종목명                 | String | Y          | 50       |               |
| -CrcyCodeVal        | 통화코드값               | String | Y          | 3        |               |
| -OvrsDrvtPrdtCode   | 해외파생상품코드            | String | Y          | 10       |               |
| -DueDt              | 만기일자                | String | Y          | 8        |               |
| -PrcntrAmt          | 계약당금액               | Number | Y          | 19.2     |               |
| -FcurrEvalPnlAmt    | 외화평가손익금액            | Number | Y          | 21.4     |               |


### 💡 Request Example
```json
{
  "CIDEQ00800InBlock1": {
    "RecCnt": 1,
    "TrdDt": "20241004"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00136",
    "CIDEQ00800OutBlock2": [
        {
            "BalQty": 4,
            "TrdDt": "20230609",
            "LqdtAbleQty": 4,
            "PrcntrAmt": "100000.00",
            "OvrsDrvtPrdtCode": "AD",
            "FcurrEvalPnlAmt": "12131775.0000",
            "OvrsDrvtNowPrc": "0.67410000000",
            "BnsTpNm": "매도",
            "IsuNm": "Australian Dollar(2023.06)",
            "DueDt": "20230616",
            "PchsPrc": "31.00353750000",
            "FcurrEvalAmt": "1078560.0000",
            "CustmBalAmt": "12401415.00",
            "AcntNo": "20629783903",
            "AbrdFutsEvalPnlAmt": "12131775.00",
            "IsuCodeVal": "ADM23",
            "CrcyCodeVal": "USD"
        }
    ],
    "CIDEQ00800OutBlock1": {
        "RecCnt": 1,
        "TrdDt": "20230609",
        "AcntNo": "20629783903",
        "AcntPwd": "********"
    },
    "rsp_msg": "조회가 완료되었습니다."
}
```

---
