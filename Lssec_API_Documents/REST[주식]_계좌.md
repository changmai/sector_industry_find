# REST[주식] 계좌
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=37d22d4d-83cd-40a4-a375-81b010a4a627

## 📌 기본 정보
| 항목           | 내용                                       |
|:-------------|:-----------------------------------------|
| Method       | POST                                     |
| Domain       | https://openapi.ls-sec.co.kr:8080        |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080        |
| 모의투자 도메인     |                                          |
| URL          | /stock/accno                             |
| Format       | JSON                                     |
| Content-Type | application/json; charset=UTF-8          |
| Description  | 계좌별 거래내역 및 잔고 등 계좌에 관련된 서비스를 확인할 수 있습니다. |


## 🏷️ 계좌 거래내역 (CDPCQ04700)
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
| Element            | 한글명                | type   | Required   | Length   | Description                                         |
|:-------------------|:-------------------|:-------|:-----------|:---------|:----------------------------------------------------|
| CDPCQ04700InBlock1 | CDPCQ04700InBlock1 | Object | Y          | -        |                                                     |
| -QryTp             | 조회구분               | String | Y          | 1        | 0@전체, 1@입출금, 2@입출고, 3@매매, 4@환전, 9@기타                |
| -QrySrtDt          | 조회시작일              | String | Y          | 8        |                                                     |
| -QryEndDt          | 조회종료일              | String | Y          | 8        |                                                     |
| -SrtNo             | 시작번호               | Number | Y          | 10       |                                                     |
| -PdptnCode         | 상품유형코드             | String | Y          | 2        | 01                                                  |
| -IsuLgclssCode     | 종목대분류코드            | String | Y          | 2        | 00@전체, 01@주식, 02@채권, 04@펀드, 03@선물, 05@해외주식, 06@해외파생 |
| -IsuNo             | 종목번호               | String | Y          | 12       |                                                     |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                | 한글명                 | type         | Required   | Length   | Description   |
|:-----------------------|:--------------------|:-------------|:-----------|:---------|:--------------|
| CDPCQ04700OutBlock1    | CDPCQ04700OutBlock1 | Object       | Y          | -        |               |
| -RecCnt                | 레코드갯수               | Number       | Y          | 5        |               |
| -QryTp                 | 조회구분                | String       | Y          | 1        |               |
| -AcntNo                | 계좌번호                | String       | Y          | 20       |               |
| -Pwd                   | 비밀번호                | String       | Y          | 8        |               |
| -QrySrtDt              | 조회시작일               | String       | Y          | 8        |               |
| -QryEndDt              | 조회종료일               | String       | Y          | 8        |               |
| -SrtNo                 | 시작번호                | Number       | Y          | 10       |               |
| -PdptnCode             | 상품유형코드              | String       | Y          | 2        |               |
| -IsuLgclssCode         | 종목대분류코드             | String       | Y          | 2        |               |
| -IsuNo                 | 종목번호                | String       | Y          | 12       |               |
| CDPCQ04700OutBlock2    | CDPCQ04700OutBlock2 | Object       | Y          | -        |               |
| -RecCnt                | 레코드갯수               | Number       | Y          | 5        |               |
| -AcntNm                | 계좌명                 | String       | Y          | 40       |               |
| CDPCQ04700OutBlock3    | CDPCQ04700OutBlock3 | Object Array | Y          | -        |               |
| -AcntNo                | 계좌번호                | String       | Y          | 20       |               |
| -TrdDt                 | 거래일자                | String       | Y          | 8        |               |
| -TrdNo                 | 거래번호                | Number       | Y          | 10       |               |
| -TpCodeNm              | 구분코드명               | String       | Y          | 50       |               |
| -SmryNo                | 적요번호                | String       | Y          | 4        |               |
| -SmryNm                | 적요명                 | String       | Y          | 40       |               |
| -CancTpNm              | 취소구분                | String       | Y          | 20       |               |
| -TrdQty                | 거래수량                | Number       | Y          | 16       |               |
| -Trtax                 | 거래세                 | Number       | Y          | 16       |               |
| -FcurrAdjstAmt         | 외화정산금액              | Number       | Y          | 25.4     |               |
| -AdjstAmt              | 정산금액                | Number       | Y          | 16       |               |
| -OvdSum                | 연체합                 | Number       | Y          | 16       |               |
| -DpsBfbalAmt           | 예수금전잔금액             | Number       | Y          | 16       |               |
| -SellPldgRfundAmt      | 매도담보상환금             | Number       | Y          | 16       |               |
| -DpspdgLoanBfbalAmt    | 예탁담보대출전잔금액          | Number       | Y          | 16       |               |
| -TrdmdaNm              | 거래매체명               | String       | Y          | 40       |               |
| -OrgTrdNo              | 원거래번호               | Number       | Y          | 10       |               |
| -IsuNm                 | 종목명                 | String       | Y          | 40       |               |
| -TrdUprc               | 거래단가                | Number       | Y          | 13.2     |               |
| -CmsnAmt               | 수수료                 | Number       | Y          | 16       |               |
| -FcurrCmsnAmt          | 외화수수료금액             | Number       | Y          | 15.2     |               |
| -RfundDiffAmt          | 상환차이금액              | Number       | Y          | 16       |               |
| -RepayAmtSum           | 변제금합계               | Number       | Y          | 16       |               |
| -SecCrbalQty           | 유가증권금잔수량            | Number       | Y          | 16       |               |
| -CslLoanRfundIntrstAmt | 매도대금담보대출상환이자금액      | Number       | Y          | 16       |               |
| -DpspdgLoanCrbalAmt    | 예탁담보대출금잔금액          | Number       | Y          | 16       |               |
| -TrxTime               | 처리시각                | String       | Y          | 9        |               |
| -Inouno                | 출납번호                | Number       | Y          | 10       |               |
| -IsuNo                 | 종목번호                | String       | Y          | 12       |               |
| -TrdAmt                | 거래금액                | Number       | Y          | 16       |               |
| -ChckAmt               | 수표금액                | Number       | Y          | 16       |               |
| -TaxSumAmt             | 세금합계금액              | Number       | Y          | 16       |               |
| -FcurrTaxSumAmt        | 외화세금합계금액            | Number       | Y          | 26.6     |               |
| -IntrstUtlfee          | 이자이용료               | Number       | Y          | 16       |               |
| -MnyDvdAmt             | 배당금액                | Number       | Y          | 16       |               |
| -RcvblOcrAmt           | 미수발생금액              | Number       | Y          | 16       |               |
| -TrxBrnNo              | 처리지점번호              | String       | Y          | 3        |               |
| -TrxBrnNm              | 처리지점명               | String       | Y          | 40       |               |
| -DpspdgLoanAmt         | 예탁담보대출금액            | Number       | Y          | 16       |               |
| -DpspdgLoanRfundAmt    | 예탁담보대출상환금액          | Number       | Y          | 16       |               |
| -BasePrc               | 기준가                 | Number       | Y          | 13.2     |               |
| -DpsCrbalAmt           | 예수금금잔금액             | Number       | Y          | 16       |               |
| -BoaAmt                | 과표                  | Number       | Y          | 16       |               |
| -MnyoutAbleAmt         | 출금가능금액              | Number       | Y          | 16       |               |
| -BcrLoanOcrAmt         | 수익증권담보대출발생금         | Number       | Y          | 16       |               |
| -BcrLoanBfbalAmt       | 수익증권담보대출전잔금         | Number       | Y          | 16       |               |
| -BnsBasePrc            | 매매기준가               | Number       | Y          | 20.1     |               |
| -TaxchrBasePrc         | 과세기준가               | Number       | Y          | 20.1     |               |
| -TrdUnit               | 거래좌수                | Number       | Y          | 16       |               |
| -BalUnit               | 잔고좌수                | Number       | Y          | 16       |               |
| -EvrTax                | 제세금                 | Number       | Y          | 16       |               |
| -EvalAmt               | 평가금액                | Number       | Y          | 16       |               |
| -BcrLoanRfundAmt       | 수익증권담보대출상환금         | Number       | Y          | 16       |               |
| -BcrLoanCrbalAmt       | 수익증권담보대출금잔금         | Number       | Y          | 16       |               |
| -AddMgnOcrTotamt       | 추가증거금발생총액           | Number       | Y          | 16       |               |
| -AddMnyMgnOcrAmt       | 추가현금증거금발생금액         | Number       | Y          | 16       |               |
| -AddMgnDfryTotamt      | 추가증거금납부총액           | Number       | Y          | 16       |               |
| -AddMnyMgnDfryAmt      | 추가현금증거금납부금액         | Number       | Y          | 16       |               |
| -BnsplAmt              | 매매손익금액              | Number       | Y          | 16       |               |
| -Ictax                 | 소득세                 | Number       | Y          | 16       |               |
| -Ihtax                 | 주민세                 | Number       | Y          | 16       |               |
| -LoanDt                | 대출일                 | String       | Y          | 8        |               |
| -CrcyCode              | 통화코드                | String       | Y          | 3        |               |
| -FcurrAmt              | 외화금액                | Number       | Y          | 24.4     |               |
| -FcurrTrdAmt           | 외화거래금액              | Number       | Y          | 24.4     |               |
| -FcurrDps              | 외화예수금               | Number       | Y          | 21.4     |               |
| -FcurrDpsBfbalAmt      | 외화예수금전잔금액           | Number       | Y          | 21.4     |               |
| -OppAcntNm             | 상대계좌명               | String       | Y          | 40       |               |
| -OppAcntNo             | 상대계좌번호              | String       | Y          | 20       |               |
| -LoanRfundAmt          | 대출상환금액              | Number       | Y          | 16       |               |
| -LoanIntrstAmt         | 대출이자금액              | Number       | Y          | 16       |               |
| -AskpsnNm              | 의뢰인명                | String       | Y          | 40       |               |
| -OrdDt                 | 주문일자                | String       | Y          | 8        |               |
| -TrdXchrat             | 거래환율                | Number       | Y          | 15.4     |               |
| -RdctCmsn              | 감면수수료               | Number       | Y          | 21.4     |               |
| -FcurrStmpTx           | 외화인지세               | Number       | Y          | 21.4     |               |
| -FcurrElecfnTrtax      | 외화전자금융거래세           | Number       | Y          | 21.4     |               |
| -FcstckTrtax           | 외화증권거래세             | Number       | Y          | 21.4     |               |
| CDPCQ04700OutBlock4    | CDPCQ04700OutBlock4 | Object       | Y          | -        |               |
| -RecCnt                | 레코드갯수               | Number       | Y          | 5        |               |
| -PnlSumAmt             | 손익합계금액              | Number       | Y          | 16       |               |
| -CtrctAsm              | 약정누계                | Number       | Y          | 16       |               |
| -CmsnAmtSumAmt         | 수수료합계금액             | Number       | Y          | 16       |               |
| CDPCQ04700OutBlock5    | CDPCQ04700OutBlock5 | Object       | Y          | -        |               |
| -RecCnt                | 레코드갯수               | Number       | Y          | 5        |               |
| -MnyinAmt              | 입금금액                | Number       | Y          | 16       |               |
| -SecinAmt              | 입고금액                | Number       | Y          | 16       |               |
| -MnyoutAmt             | 출금금액                | Number       | Y          | 16       |               |
| -SecoutAmt             | 출고금액                | Number       | Y          | 16       |               |
| -DiffAmt               | 차이금액                | Number       | Y          | 16       |               |
| -DiffAmt0              | 차이금액0               | Number       | Y          | 16       |               |
| -SellQty               | 매도수량                | Number       | Y          | 16       |               |
| -SellAmt               | 매도금액                | Number       | Y          | 16       |               |
| -SellCmsn              | 매도수수료               | Number       | Y          | 16       |               |
| -EvrTax                | 제세금                 | Number       | Y          | 19       |               |
| -FcurrSellAdjstAmt     | 외화매도정산금액            | Number       | Y          | 25.4     |               |
| -BuyQty                | 매수수량                | Number       | Y          | 16       |               |
| -BuyAmt                | 매수금액                | Number       | Y          | 16       |               |
| -BuyCmsn               | 매수수수료               | Number       | Y          | 16       |               |
| -ExecTax               | 체결세금                | Number       | Y          | 16       |               |
| -FcurrBuyAdjstAmt      | 외화매수정산금액            | Number       | Y          | 25.4     |               |


### 💡 Request Example
```json
{
  "CDPCQ04700InBlock1": {
    "RecCnt": 1,
    "QryTp": "0",
    "QrySrtDt": "20230515",
    "QryEndDt": "20230516",
    "SrtNo": 0,
    "PdptnCode": "01",
    "IsuLgclssCode": "01",
    "IsuNo": "KR7000020008"
  }
}
```

### 💡 Response Example
```json
{
  "CDPCQ04700OutBlock1": {
    "RecCnt": 1,
    "QryTp": "0",
    "AcntNo": "20277932702",
    "Pwd": "********",
    "QrySrtDt": "20230515",
    "QryEndDt": "20230516",
    "SrtNo": 0,
    "PdptnCode": "01",
    "IsuLgclssCode": "01",
    "IsuNo": "KR7000020008"
  },
  "CDPCQ04700OutBlock2": {
    "RecCnt": 1,
    "AcntNm": "충조감"
  },
  "CDPCQ04700OutBlock3": [],
  "CDPCQ04700OutBlock4": {
    "RecCnt": 1,
    "PnlSumAmt": 0,
    "CtrctAsm": 0,
    "CmsnAmtSumAmt": 0
  },
  "CDPCQ04700OutBlock5": {
    "RecCnt": 1,
    "MnyinAmt": 0,
    "SecinAmt": 0,
    "MnyoutAmt": 0,
    "SecoutAmt": 0,
    "DiffAmt": 0,
    "DiffAmt0": 0,
    "SellQty": 0,
    "SellAmt": 0,
    "SellCmsn": 0,
    "EvrTax": 0,
    "FcurrSellAdjstAmt": "0.0000",
    "BuyQty": 0,
    "BuyAmt": 0,
    "BuyCmsn": 0,
    "ExecTax": 0,
    "FcurrBuyAdjstAmt": "0.0000"
  },
  "rsp_cd": "00200",
  "rsp_msg": "조회내역이 없습니다."
}
```

---

## 🏷️ 계좌별신용한도조회 (CSPAQ00600)
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
| Element            | 한글명                | type   | Required   | Length   | Description                        |
|:-------------------|:-------------------|:-------|:-----------|:---------|:-----------------------------------|
| CSPAQ00600InBlock1 | CSPAQ00600InBlock1 | Object | Y          | -        |                                    |
| -LoanDtlClssCode   | 대출상세분류코드           | String | Y          | 2        | 01@유통융자, 03@자기융자, 05@유통대주, 07@자기대주 |
| -IsuNo             | 종목번호               | String | Y          | 12       |                                    |
| -OrdPrc            | 주문가                | Number | Y          | 13.2     |                                    |
| -CommdaCode        | 통신매체코드             | String | Y          | 2        | 41@xingAPI                         |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                 | 한글명                 | type   | Required   | Length   | Description   |
|:------------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CSPAQ00600OutBlock1     | CSPAQ00600OutBlock1 | Object | Y          | -        |               |
| -RecCnt                 | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo                 | 계좌번호                | String | Y          | 20       |               |
| -InptPwd                | 입력비밀번호              | String | Y          | 8        |               |
| -LoanDtlClssCode        | 대출상세분류코드            | String | Y          | 2        |               |
| -IsuNo                  | 종목번호                | String | Y          | 12       |               |
| -OrdPrc                 | 주문가                 | Number | Y          | 13.2     |               |
| -CommdaCode             | 통신매체코드              | String | Y          | 2        |               |
| CSPAQ00600OutBlock2     | CSPAQ00600OutBlock2 | Object | Y          | -        |               |
| -RecCnt                 | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNm                 | 계좌명                 | String | Y          | 40       |               |
| -OrdPrc                 | 주문가                 | Number | Y          | 13.2     |               |
| -SloanLmtAmt            | 대주한도                | Number | Y          | 16       |               |
| -SloanAmtSum            | 대주금액합계              | Number | Y          | 16       |               |
| -SloanNewAmt            | 대주신규금액              | Number | Y          | 16       |               |
| -SloanRfundAmt          | 대주상환금액              | Number | Y          | 16       |               |
| -MktcplMloanLmtAmt      | 유통융자한도금액            | Number | Y          | 16       |               |
| -MktcplMloanAmtSum      | 유통융자금액합계            | Number | Y          | 16       |               |
| -MktcplMloanNewAmt      | 유통융자신규금액            | Number | Y          | 16       |               |
| -MktcplMloanRfundAmt    | 유통융자상환금액            | Number | Y          | 16       |               |
| -SfaccMloanLmtAmt       | 자기융자한도금액            | Number | Y          | 16       |               |
| -SfaccMloanAmtSum       | 자기융자금액합계            | Number | Y          | 16       |               |
| -SfaccMloanNewAmt       | 자기융자신규금액            | Number | Y          | 16       |               |
| -SfaccMloanRfundAmt     | 자기융자상환금액            | Number | Y          | 16       |               |
| -BrnMktcplMloanLmtAmt   | 지점유통융자한도금액          | Number | Y          | 16       |               |
| -BrnMktcplMloanNewAmt   | 지점유통융자신규금액          | Number | Y          | 16       |               |
| -BrnMktcplMloanRfundAmt | 지점유통융자상환금액          | Number | Y          | 16       |               |
| -BrnMktcplMloanUseAmt   | 지점유통융자사용금액          | Number | Y          | 16       |               |
| -BrnSfaccMloanLmtAmt    | 지점자기융자한도금액          | Number | Y          | 16       |               |
| -BrnSfaccMloanNewAmt    | 지점자기융자신규금액          | Number | Y          | 16       |               |
| -BrnSfaccMloanRfundAmt  | 지점자기융자상환금액          | Number | Y          | 16       |               |
| -BrnSfaccMloanUseAmt    | 지점자기융자사용금액          | Number | Y          | 16       |               |
| -FirmMloanLmtMgmtYn     | 이용사융자한도관리여부         | String | Y          | 1        |               |
| -FirmCrdtIsuRestrcTp    | 이용사신용종목제한구분         | String | Y          | 1        |               |
| -PldgMaintRat           | 담보유지비율              | Number | Y          | 7.4      |               |
| -FirmNm                 | 이용사명                | String | Y          | 50       |               |
| -PldgRat                | 담보비율                | Number | Y          | 7.4      |               |
| -DpsastSum              | 예탁자산합계              | Number | Y          | 17       |               |
| -LmtChgAbleAmt          | 한도변경가능금액            | Number | Y          | 16       |               |
| -OrdAbleAmt             | 주문가능금액              | Number | Y          | 16       |               |
| -OrdAbleQty             | 주문가능수량              | Number | Y          | 16       |               |
| -RcvblUablOrdAbleQty    | 미수불가주문가능수량          | Number | Y          | 16       |               |


### 💡 Request Example
```json
{
  "CSPAQ00600InBlock1" : {
    "LoanDtlClssCode" : "01",
    "IsuNo" : "A000020",
    "OrdPrc" : 1.11,
    "CommdaCode" : "41"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00136",
    "CSPAQ00600OutBlock1": {
        "CommdaCode": "04",
        "RecCnt": 1,
        "OrdPrc": "1.11",
        "IsuNo": "A000020",
        "AcntNo": "20187511401",
        "InptPwd": "********",
        "LoanDtlClssCode": "01"
    },
    "CSPAQ00600OutBlock2": {
        "BrnMktcplMloanNewAmt": 0,
        "SloanNewAmt": 0,
        "LmtChgAbleAmt": 0,
        "SfaccMloanNewAmt": 0,
        "MktcplMloanNewAmt": 0,
        "MktcplMloanRfundAmt": 0,
        "FirmNm": "",
        "SfaccMloanLmtAmt": 999999999999999,
        "OrdAbleQty": 1638001637,
        "MktcplMloanLmtAmt": 999999999999999,
        "PldgMaintRat": "1.4000",
        "BrnMktcplMloanUseAmt": 2663782796,
        "SfaccMloanRfundAmt": 0,
        "FirmCrdtIsuRestrcTp": "",
        "DpsastSum": 100004619279,
        "MktcplMloanAmtSum": 0,
        "RcvblUablOrdAbleQty": 1638001637,
        "SfaccMloanAmtSum": 0,
        "OrdPrc": "0.00",
        "BrnSfaccMloanNewAmt": 0,
        "OrdAbleAmt": 1818181818,
        "SloanRfundAmt": 0,
        "SloanAmtSum": 0,
        "PldgRat": "0.0000",
        "BrnSfaccMloanRfundAmt": 0,
        "SloanLmtAmt": 999999999999999,
        "BrnMktcplMloanRfundAmt": 0,
        "BrnSfaccMloanUseAmt": 95819909,
        "BrnMktcplMloanLmtAmt": 42000000000,
        "RecCnt": 1,
        "BrnSfaccMloanLmtAmt": 63000000000,
        "AcntNm": "가차금",
        "FirmMloanLmtMgmtYn": ""
    },
    "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 현물계좌예수금 주문가능금액 총평가 조회 (CSPAQ12200)
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
| CSPAQ12200InBlock1 | CSPAQ12200InBlock1 | Object | Y          | -        |               |
| -BalCreTp          | 잔고생성구분             | String | Y          | 1        | 0             |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                 | 한글명                 | type   | Required   | Length   | Description   |
|:------------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CSPAQ12200OutBlock1     | CSPAQ12200OutBlock1 | Object | Y          | -        |               |
| -RecCnt                 | 레코드갯수               | Number | Y          | 5        |               |
| -MgmtBrnNo              | 관리지점번호              | String | Y          | 3        |               |
| -AcntNo                 | 계좌번호                | String | Y          | 20       |               |
| -Pwd                    | 비밀번호                | String | Y          | 8        |               |
| -BalCreTp               | 잔고생성구분              | String | Y          | 1        |               |
| CSPAQ12200OutBlock2     | CSPAQ12200OutBlock2 | Object | Y          | -        |               |
| -RecCnt                 | 레코드갯수               | Number | Y          | 5        |               |
| -BrnNm                  | 지점명                 | String | Y          | 40       |               |
| -AcntNm                 | 계좌명                 | String | Y          | 40       |               |
| -MnyOrdAbleAmt          | 현금주문가능금액            | Number | Y          | 16       |               |
| -MnyoutAbleAmt          | 출금가능금액              | Number | Y          | 16       |               |
| -SeOrdAbleAmt           | 거래소금액               | Number | Y          | 16       |               |
| -KdqOrdAbleAmt          | 코스닥금액               | Number | Y          | 16       |               |
| -BalEvalAmt             | 잔고평가금액              | Number | Y          | 16       |               |
| -RcvblAmt               | 미수금액                | Number | Y          | 16       |               |
| -DpsastTotamt           | 예탁자산총액              | Number | Y          | 16       |               |
| -PnlRat                 | 손익율                 | Number | Y          | 18.6     |               |
| -InvstOrgAmt            | 투자원금                | Number | Y          | 20       |               |
| -InvstPlAmt             | 투자손익금액              | Number | Y          | 16       |               |
| -CrdtPldgOrdAmt         | 신용담보주문금액            | Number | Y          | 16       |               |
| -Dps                    | 예수금                 | Number | Y          | 16       |               |
| -SubstAmt               | 대용금액                | Number | Y          | 16       |               |
| -D1Dps                  | D1예수금               | Number | Y          | 16       |               |
| -D2Dps                  | D2예수금               | Number | Y          | 16       |               |
| -MnyrclAmt              | 현금미수금액              | Number | Y          | 16       |               |
| -MgnMny                 | 증거금현금               | Number | Y          | 16       |               |
| -MgnSubst               | 증거금대용               | Number | Y          | 16       |               |
| -ChckAmt                | 수표금액                | Number | Y          | 16       |               |
| -SubstOrdAbleAmt        | 대용주문가능금액            | Number | Y          | 16       |               |
| -MgnRat100pctOrdAbleAmt | 증거금률100퍼센트주문가능금액    | Number | Y          | 16       |               |
| -MgnRat35ordAbleAmt     | 증거금률35%주문가능금액       | Number | Y          | 16       |               |
| -MgnRat50ordAbleAmt     | 증거금률50%주문가능금액       | Number | Y          | 16       |               |
| -PrdaySellAdjstAmt      | 전일매도정산금액            | Number | Y          | 16       |               |
| -PrdayBuyAdjstAmt       | 전일매수정산금액            | Number | Y          | 16       |               |
| -CrdaySellAdjstAmt      | 금일매도정산금액            | Number | Y          | 16       |               |
| -CrdayBuyAdjstAmt       | 금일매수정산금액            | Number | Y          | 16       |               |
| -D1ovdRepayRqrdAmt      | D1연체변제소요금액          | Number | Y          | 16       |               |
| -D2ovdRepayRqrdAmt      | D2연체변제소요금액          | Number | Y          | 16       |               |
| -D1PrsmptWthdwAbleAmt   | D1추정인출가능금액          | Number | Y          | 16       |               |
| -D2PrsmptWthdwAbleAmt   | D2추정인출가능금액          | Number | Y          | 16       |               |
| -DpspdgLoanAmt          | 예탁담보대출금액            | Number | Y          | 16       |               |
| -Imreq                  | 신용설정보증금             | Number | Y          | 16       |               |
| -MloanAmt               | 융자금액                | Number | Y          | 16       |               |
| -ChgAfPldgRat           | 변경후담보비율             | Number | Y          | 9.3      |               |
| -OrgPldgAmt             | 원담보금액               | Number | Y          | 16       |               |
| -SubPldgAmt             | 부담보금액               | Number | Y          | 16       |               |
| -RqrdPldgAmt            | 소요담보금액              | Number | Y          | 16       |               |
| -OrgPdlckAmt            | 원담보부족금액             | Number | Y          | 16       |               |
| -PdlckAmt               | 담보부족금액              | Number | Y          | 16       |               |
| -AddPldgMny             | 추가담보현금              | Number | Y          | 16       |               |
| -D1OrdAbleAmt           | D1주문가능금액            | Number | Y          | 16       |               |
| -CrdtIntdltAmt          | 신용이자미납금액            | Number | Y          | 16       |               |
| -EtclndAmt              | 기타대여금액              | Number | Y          | 16       |               |
| -NtdayPrsmptCvrgAmt     | 익일추정반대매매금액          | Number | Y          | 16       |               |
| -OrgPldgSumAmt          | 원담보합계금액             | Number | Y          | 16       |               |
| -CrdtOrdAbleAmt         | 신용주문가능금액            | Number | Y          | 16       |               |
| -SubPldgSumAmt          | 부담보합계금액             | Number | Y          | 16       |               |
| -CrdtPldgAmtMny         | 신용담보금현금             | Number | Y          | 16       |               |
| -CrdtPldgSubstAmt       | 신용담보대용금액            | Number | Y          | 16       |               |
| -AddCrdtPldgMny         | 추가신용담보현금            | Number | Y          | 16       |               |
| -CrdtPldgRuseAmt        | 신용담보재사용금액           | Number | Y          | 16       |               |
| -AddCrdtPldgSubst       | 추가신용담보대용            | Number | Y          | 16       |               |
| -CslLoanAmtdt1          | 매도대금담보대출금액          | Number | Y          | 16       |               |
| -DpslRestrcAmt          | 처분제한금액              | Number | Y          | 16       |               |


### 💡 Request Example
```json
{  
"CSPAQ12200InBlock1" : {    "RecCnt" : 1,    "MgmtBrnNo" : "1",    "BalCreTp" : "1"
 }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00136",
    "CSPAQ12200OutBlock2": {
        "KdqOrdAbleAmt": 0,
        "MloanAmt": 0,
        "ChckAmt": 0,
        "CslLoanAmtdt1": 0,
        "BrnNm": "",
        "MgnRat35ordAbleAmt": 1666666667,
        "MgnRat50ordAbleAmt": 1250000000,
        "BalEvalAmt": 0,
        "CrdayBuyAdjstAmt": 0,
        "MnyrclAmt": 0,
        "NtdayPrsmptCvrgAmt": 0,
        "PrdayBuyAdjstAmt": 0,
        "D2ovdRepayRqrdAmt": 0,
        "CrdtPldgSubstAmt": 0,
        "OrgPdlckAmt": 0,
        "AddCrdtPldgSubst": 0,
        "MnyOrdAbleAmt": 500000000,
        "ChgAfPldgRat": "0.000",
        "MgnMny": 0,
        "CrdtIntdltAmt": 0,
        "DpslRestrcAmt": 0,
        "SubPldgAmt": 0,
        "EtclndAmt": 0,
        "RqrdPldgAmt": 0,
        "MgnRat100pctOrdAbleAmt": 500000000,
        "PrdaySellAdjstAmt": 0,
        "D1PrsmptWthdwAbleAmt": 500000000,
        "InvstPlAmt": 0,
        "SeOrdAbleAmt": 0,
        "Dps": 500000000,
        "DpsastTotamt": 500000000,
        "DpspdgLoanAmt": 0,
        "OrgPldgAmt": 0,
        "D2Dps": 500000000,
        "SubstOrdAbleAmt": 0,
        "D1ovdRepayRqrdAmt": 0,
        "CrdtPldgOrdAmt": 0,
        "CrdaySellAdjstAmt": 0,
        "MgnSubst": 0,
        "PdlckAmt": 0,
        "InvstOrgAmt": 0,
        "D2PrsmptWthdwAbleAmt": 500000000,
        "CrdtPldgAmtMny": 0,
        "CrdtPldgRuseAmt": 0,
        "AddCrdtPldgMny": 0,
        "RcvblAmt": 0,
        "D1OrdAbleAmt": 500000000,
        "Imreq": 0,
        "D1Dps": 500000000,
        "RecCnt": 1,
        "PnlRat": "0.000000",
        "AcntNm": "zzin",
        "MnyoutAbleAmt": 500000000,
        "SubstAmt": 0,
        "SubPldgSumAmt": 0,
        "AddPldgMny": 0,
        "OrgPldgSumAmt": 0,
        "CrdtOrdAbleAmt": 0
    },
    "CSPAQ12200OutBlock1": {
        "MgmtBrnNo": "",
        "RecCnt": 1,
        "AcntNo": "55501780501",
        "Pwd": "0000",
        "BalCreTp": "1"
    },
    "rsp_msg": "모의투자 조회가 완료되었습니다."
}
```

---

## 🏷️ BEP단가조회 (CSPAQ12300)
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
| Element            | 한글명                | type   | Required   | Length   | Description    |
|:-------------------|:-------------------|:-------|:-----------|:---------|:---------------|
| CSPAQ12300InBlock1 | CSPAQ12300InBlock1 | Object | Y          | -        |                |
| -BalCreTp          | 잔고생성구분             | String | Y          | 1        | 0:전체           |
|                    |                    |        |            |          | 1:현물           |
|                    |                    |        |            |          | 9:선물대용         |
| -CmsnAppTpCode     | 수수료적용구분            | String | Y          | 1        | 0:평가시 수수료 미적용  |
|                    |                    |        |            |          | 1:평가시 수수료 적용   |
| -D2balBaseQryTp    | D2잔고기준조회구분         | String | Y          | 1        | 0:전부조회         |
|                    |                    |        |            |          | 1:D2잔고 0이상만 조회 |
| -UprcTpCode        | 단가구분               | String | Y          | 1        | 0:평균단가         |
|                    |                    |        |            |          | 1:BEP단가        |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                 | 한글명                 | type         | Required   | Length   | Description   |
|:------------------------|:--------------------|:-------------|:-----------|:---------|:--------------|
| CSPAQ12300OutBlock1     | CSPAQ12300OutBlock1 | Object       | Y          | -        |               |
| -RecCnt                 | 레코드갯수               | Number       | Y          | 5        |               |
| -AcntNo                 | 계좌번호                | String       | Y          | 20       |               |
| -Pwd                    | 비밀번호                | String       | Y          | 8        |               |
| -BalCreTp               | 잔고생성구분              | String       | Y          | 1        |               |
| -CmsnAppTpCode          | 수수료적용구분             | String       | Y          | 1        |               |
| -D2balBaseQryTp         | D2잔고기준조회구분          | String       | Y          | 1        |               |
| -UprcTpCode             | 단가구분                | String       | Y          | 1        |               |
| CSPAQ12300OutBlock2     | CSPAQ12300OutBlock2 | Object       | Y          | -        |               |
| -RecCnt                 | 레코드갯수               | Number       | Y          | 5        |               |
| -BrnNm                  | 지점명                 | String       | Y          | 40       |               |
| -AcntNm                 | 계좌명                 | String       | Y          | 40       |               |
| -MnyOrdAbleAmt          | 현금주문가능금액            | Number       | Y          | 16       |               |
| -MnyoutAbleAmt          | 출금가능금액              | Number       | Y          | 16       |               |
| -SeOrdAbleAmt           | 거래소금액               | Number       | Y          | 16       |               |
| -KdqOrdAbleAmt          | 코스닥금액               | Number       | Y          | 16       |               |
| -HtsOrdAbleAmt          | HTS주문가능금액           | Number       | Y          | 16       |               |
| -MgnRat100pctOrdAbleAmt | 증거금률100퍼센트주문가능금액    | Number       | Y          | 16       |               |
| -BalEvalAmt             | 잔고평가금액              | Number       | Y          | 16       |               |
| -PchsAmt                | 매입금액                | Number       | Y          | 16       |               |
| -RcvblAmt               | 미수금액                | Number       | Y          | 16       |               |
| -PnlRat                 | 손익율                 | Number       | Y          | 18.6     |               |
| -InvstOrgAmt            | 투자원금                | Number       | Y          | 20       |               |
| -InvstPlAmt             | 투자손익금액              | Number       | Y          | 16       |               |
| -CrdtPldgOrdAmt         | 신용담보주문금액            | Number       | Y          | 16       |               |
| -Dps                    | 예수금                 | Number       | Y          | 16       |               |
| -D1Dps                  | D1예수금               | Number       | Y          | 16       |               |
| -D2Dps                  | D2예수금               | Number       | Y          | 16       |               |
| -OrdDt                  | 주문일                 | String       | Y          | 8        |               |
| -MnyMgn                 | 현금증거금액              | Number       | Y          | 16       |               |
| -SubstMgn               | 대용증거금액              | Number       | Y          | 16       |               |
| -SubstAmt               | 대용금액                | Number       | Y          | 16       |               |
| -PrdayBuyExecAmt        | 전일매수체결금액            | Number       | Y          | 16       |               |
| -PrdaySellExecAmt       | 전일매도체결금액            | Number       | Y          | 16       |               |
| -CrdayBuyExecAmt        | 금일매수체결금액            | Number       | Y          | 16       |               |
| -CrdaySellExecAmt       | 금일매도체결금액            | Number       | Y          | 16       |               |
| -EvalPnlSum             | 평가손익합계              | Number       | Y          | 15       |               |
| -DpsastTotamt           | 예탁자산총액              | Number       | Y          | 16       |               |
| -Evrprc                 | 제비용                 | Number       | Y          | 19       |               |
| -RuseAmt                | 재사용금액               | Number       | Y          | 16       |               |
| -EtclndAmt              | 기타대여금액              | Number       | Y          | 16       |               |
| -PrcAdjstAmt            | 가정산금액               | Number       | Y          | 16       |               |
| -D1CmsnAmt              | D1수수료               | Number       | Y          | 16       |               |
| -D2CmsnAmt              | D2수수료               | Number       | Y          | 16       |               |
| -D1EvrTax               | D1제세금               | Number       | Y          | 16       |               |
| -D2EvrTax               | D2제세금               | Number       | Y          | 16       |               |
| -D1SettPrergAmt         | D1결제예정금액            | Number       | Y          | 16       |               |
| -D2SettPrergAmt         | D2결제예정금액            | Number       | Y          | 16       |               |
| -PrdayKseMnyMgn         | 전일KSE현금증거금          | Number       | Y          | 16       |               |
| -PrdayKseSubstMgn       | 전일KSE대용증거금          | Number       | Y          | 16       |               |
| -PrdayKseCrdtMnyMgn     | 전일KSE신용현금증거금        | Number       | Y          | 16       |               |
| -PrdayKseCrdtSubstMgn   | 전일KSE신용대용증거금        | Number       | Y          | 16       |               |
| -CrdayKseMnyMgn         | 금일KSE현금증거금          | Number       | Y          | 16       |               |
| -CrdayKseSubstMgn       | 금일KSE대용증거금          | Number       | Y          | 16       |               |
| -CrdayKseCrdtMnyMgn     | 금일KSE신용현금증거금        | Number       | Y          | 16       |               |
| -CrdayKseCrdtSubstMgn   | 금일KSE신용대용증거금        | Number       | Y          | 16       |               |
| -PrdayKdqMnyMgn         | 전일코스닥현금증거금          | Number       | Y          | 16       |               |
| -PrdayKdqSubstMgn       | 전일코스닥대용증거금          | Number       | Y          | 16       |               |
| -PrdayKdqCrdtMnyMgn     | 전일코스닥신용현금증거금        | Number       | Y          | 16       |               |
| -PrdayKdqCrdtSubstMgn   | 전일코스닥신용대용증거금        | Number       | Y          | 16       |               |
| -CrdayKdqMnyMgn         | 금일코스닥현금증거금          | Number       | Y          | 16       |               |
| -CrdayKdqSubstMgn       | 금일코스닥대용증거금          | Number       | Y          | 16       |               |
| -CrdayKdqCrdtMnyMgn     | 금일코스닥신용현금증거금        | Number       | Y          | 16       |               |
| -CrdayKdqCrdtSubstMgn   | 금일코스닥신용대용증거금        | Number       | Y          | 16       |               |
| -PrdayFrbrdMnyMgn       | 전일프리보드현금증거금         | Number       | Y          | 16       |               |
| -PrdayFrbrdSubstMgn     | 전일프리보드대용증거금         | Number       | Y          | 16       |               |
| -CrdayFrbrdMnyMgn       | 금일프리보드현금증거금         | Number       | Y          | 16       |               |
| -CrdayFrbrdSubstMgn     | 금일프리보드대용증거금         | Number       | Y          | 16       |               |
| -PrdayCrbmkMnyMgn       | 전일장외현금증거금           | Number       | Y          | 16       |               |
| -PrdayCrbmkSubstMgn     | 전일장외대용증거금           | Number       | Y          | 16       |               |
| -CrdayCrbmkMnyMgn       | 금일장외현금증거금           | Number       | Y          | 16       |               |
| -CrdayCrbmkSubstMgn     | 금일장외대용증거금           | Number       | Y          | 16       |               |
| -DpspdgQty              | 예탁담보수량              | Number       | Y          | 16       |               |
| -BuyAdjstAmtD2          | 매수정산금(D+2)          | Number       | Y          | 16       |               |
| -SellAdjstAmtD2         | 매도정산금(D+2)          | Number       | Y          | 16       |               |
| -RepayRqrdAmtD1         | 변제소요금(D+1)          | Number       | Y          | 16       |               |
| -RepayRqrdAmtD2         | 변제소요금(D+2)          | Number       | Y          | 16       |               |
| -LoanAmt                | 대출금액                | Number       | Y          | 16       |               |
| CSPAQ12300OutBlock3     | CSPAQ12300OutBlock3 | Object Array | Y          | -        |               |
| -IsuNo                  | 종목번호                | String       | Y          | 12       |               |
| -IsuNm                  | 종목명                 | String       | Y          | 40       |               |
| -SecBalPtnCode          | 유가증권잔고유형코드          | String       | Y          | 2        |               |
| -SecBalPtnNm            | 유가증권잔고유형명           | String       | Y          | 40       |               |
| -BalQty                 | 잔고수량                | Number       | Y          | 16       |               |
| -BnsBaseBalQty          | 매매기준잔고수량            | Number       | Y          | 16       |               |
| -CrdayBuyExecQty        | 금일매수체결수량            | Number       | Y          | 16       |               |
| -CrdaySellExecQty       | 금일매도체결수량            | Number       | Y          | 16       |               |
| -SellPrc                | 매도가                 | Number       | Y          | 21.4     |               |
| -BuyPrc                 | 매수가                 | Number       | Y          | 21.4     |               |
| -SellPnlAmt             | 매도손익금액              | Number       | Y          | 16       |               |
| -PnlRat                 | 손익율                 | Number       | Y          | 18.6     |               |
| -NowPrc                 | 현재가                 | Number       | Y          | 15.2     |               |
| -CrdtAmt                | 신용금액                | Number       | Y          | 16       |               |
| -DueDt                  | 만기일                 | String       | Y          | 8        |               |
| -PrdaySellExecPrc       | 전일매도체결가             | Number       | Y          | 13.2     |               |
| -PrdaySellQty           | 전일매도수량              | Number       | Y          | 16       |               |
| -PrdayBuyExecPrc        | 전일매수체결가             | Number       | Y          | 13.2     |               |
| -PrdayBuyQty            | 전일매수수량              | Number       | Y          | 16       |               |
| -LoanDt                 | 대출일                 | String       | Y          | 8        |               |
| -AvrUprc                | 평균단가                | Number       | Y          | 13.2     |               |
| -SellAbleQty            | 매도가능수량              | Number       | Y          | 16       |               |
| -SellOrdQty             | 매도주문수량              | Number       | Y          | 16       |               |
| -CrdayBuyExecAmt        | 금일매수체결금액            | Number       | Y          | 16       |               |
| -CrdaySellExecAmt       | 금일매도체결금액            | Number       | Y          | 16       |               |
| -PrdayBuyExecAmt        | 전일매수체결금액            | Number       | Y          | 16       |               |
| -PrdaySellExecAmt       | 전일매도체결금액            | Number       | Y          | 16       |               |
| -BalEvalAmt             | 잔고평가금액              | Number       | Y          | 16       |               |
| -EvalPnl                | 평가손익                | Number       | Y          | 16       |               |
| -MnyOrdAbleAmt          | 현금주문가능금액            | Number       | Y          | 16       |               |
| -OrdAbleAmt             | 주문가능금액              | Number       | Y          | 16       |               |
| -SellUnercQty           | 매도미체결수량             | Number       | Y          | 16       |               |
| -SellUnsttQty           | 매도미결제수량             | Number       | Y          | 16       |               |
| -BuyUnercQty            | 매수미체결수량             | Number       | Y          | 16       |               |
| -BuyUnsttQty            | 매수미결제수량             | Number       | Y          | 16       |               |
| -UnsttQty               | 미결제수량               | Number       | Y          | 16       |               |
| -UnercQty               | 미체결수량               | Number       | Y          | 16       |               |
| -PrdayCprc              | 전일종가                | Number       | Y          | 15.2     |               |
| -PchsAmt                | 매입금액                | Number       | Y          | 16       |               |
| -RegMktCode             | 등록시장코드              | String       | Y          | 2        |               |
| -LoanDtlClssCode        | 대출상세분류코드            | String       | Y          | 2        |               |
| -DpspdgLoanQty          | 예탁담보대출수량            | Number       | Y          | 16       |               |


### 💡 Request Example
```json
{
  "CSPAQ12300InBlock1": {
    "RecCnt": 1,
    "BalCreTp": "0",
    "CmsnAppTpCode": "0",
    "D2balBaseQryTp": "0",
    "UprcTpCode": "0"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00136",
    "CSPAQ12300OutBlock2": {
        "BuyAdjstAmtD2": 0,
        "KdqOrdAbleAmt": 0,
        "PrdayKdqMnyMgn": 0,
        "D2CmsnAmt": 0,
        "D1EvrTax": 0,
        "CrdayFrbrdMnyMgn": 0,
        "RepayRqrdAmtD2": 0,
        "D1CmsnAmt": 0,
        "CrdayCrbmkMnyMgn": 0,
        "BrnNm": "",
        "PrdayFrbrdMnyMgn": 0,
        "BalEvalAmt": 0,
        "EvalPnlSum": 0,
        "PrdayFrbrdSubstMgn": 0,
        "CrdayKdqSubstMgn": 0,
        "RepayRqrdAmtD1": 0,
        "CrdayKseCrdtMnyMgn": 0,
        "PrdayKdqSubstMgn": 0,
        "PrdayKseMnyMgn": 0,
        "D2EvrTax": 0,
        "MnyOrdAbleAmt": 0,
        "DpspdgQty": 0,
        "SellAdjstAmtD2": 0,
        "PrcAdjstAmt": 0,
        "EtclndAmt": 0,
        "Evrprc": 0,
        "CrdayKdqCrdtSubstMgn": 0,
        "PrdaySellExecAmt": 0,
        "MnyMgn": 0,
        "MgnRat100pctOrdAbleAmt": 0,
        "PrdayKseSubstMgn": 0,
        "OrdDt": "",
        "CrdayCrbmkSubstMgn": 0,
        "InvstPlAmt": 0,
        "D1SettPrergAmt": 0,
        "D2SettPrergAmt": 0,
        "SeOrdAbleAmt": 0,
        "Dps": 0,
        "DpsastTotamt": 0,
        "PrdayBuyExecAmt": 0,
        "D2Dps": 0,
        "CrdtPldgOrdAmt": 0,
        "CrdayKdqMnyMgn": 0,
        "SubstMgn": 0,
        "LoanAmt": 0,
        "PrdayKdqCrdtSubstMgn": 0,
        "PrdayKdqCrdtMnyMgn": 0,
        "InvstOrgAmt": 0,
        "PchsAmt": 0,
        "CrdayFrbrdSubstMgn": 0,
        "PrdayKseCrdtMnyMgn": 0,
        "CrdayBuyExecAmt": 0,
        "PrdayCrbmkMnyMgn": 0,
        "CrdayKdqCrdtMnyMgn": 0,
        "RcvblAmt": 0,
        "HtsOrdAbleAmt": 0,
        "PrdayCrbmkSubstMgn": 0,
        "CrdayKseCrdtSubstMgn": 0,
        "D1Dps": 0,
        "RecCnt": 1,
        "PnlRat": "0.000000",
        "PrdayKseCrdtSubstMgn": 0,
        "AcntNm": "",
        "MnyoutAbleAmt": 0,
        "CrdaySellExecAmt": 0,
        "CrdayKseMnyMgn": 0,
        "SubstAmt": 0,
        "RuseAmt": 0,
        "CrdayKseSubstMgn": 0
    },
    "CSPAQ12300OutBlock1": {
        "RecCnt": 1,
        "UprcTpCode": "0",
        "AcntNo": "20011132702",
        "D2balBaseQryTp": "0",
        "Pwd": "********",
        "CmsnAppTpCode": "0",
        "BalCreTp": "0"
    },
    "CSPAQ12300OutBlock3": [
        {
            "BuyUnercQty": 0,
            "SecBalPtnNm": "유가KSE",
            "BuyUnsttQty": 1,
            "SellUnercQty": 0,
            "UnercQty": 0,
            "SecBalPtnCode": "00",
            "PrdayBuyExecAmt": 0,
            "LoanDtlClssCode": "",
            "BalEvalAmt": 82700,
            "BuyPrc": "60000.0000",
            "SellOrdQty": 0,
            "AvrUprc": "60000.00",
            "BnsBaseBalQty": 1,
            "SellUnsttQty": 0,
            "PchsAmt": 60000,
            "PrdaySellExecPrc": "0.00",
            "PrdayCprc": "68500.00",
            "BalQty": 0,
            "PrdaySellQty": 0,
            "EvalPnl": 22700,
            "CrdayBuyExecAmt": 60000,
            "PrdayBuyExecPrc": "0.00",
            "SellAbleQty": 1,
            "OrdAbleAmt": 0,
            "MnyOrdAbleAmt": 0,
            "NowPrc": "82700.00",
            "CrdtAmt": 0,
            "SellPrc": "0.0000",
            "IsuNm": "삼성전자",
            "CrdayBuyExecQty": 1,
            "DueDt": "",
            "PnlRat": "0.378333",
            "PrdaySellExecAmt": 0,
            "IsuNo": "A005930",
            "CrdaySellExecQty": 0,
            "CrdaySellExecAmt": 0,
            "RegMktCode": "10",
            "LoanDt": "",
            "UnsttQty": 1,
            "PrdayBuyQty": 0,
            "SellPnlAmt": 22700,
            "DpspdgLoanQty": 0
        }
    ],
    "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 현물계좌 주문체결내역 조회(API) (CSPAQ13700)
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
| Element            | 한글명                | type   | Required   | Length   | Description                                                                                                                        |
|:-------------------|:-------------------|:-------|:-----------|:---------|:-----------------------------------------------------------------------------------------------------------------------------------|
| CSPAQ13700InBlock1 | CSPAQ13700InBlock1 | Object | Y          | -        |                                                                                                                                    |
| -OrdMktCode        | 주문시장코드             | String | Y          | 2        | 00.전체10.거래소20.코스닥30.프리보드                                                                                                           |
| -BnsTpCode         | 매매구분               | String | Y          | 1        | 0@전체1@매도2@매수                                                                                                                       |
| -IsuNo             | 종목번호               | String | Y          | 12       | 주식 : A+종목코드ELW : J+종목코드                                                                                                            |
| -ExecYn            | 체결여부               | String | Y          | 1        | 0.전체1.체결3.미체결                                                                                                                      |
| -OrdDt             | 주문일                | String | Y          | 8        |                                                                                                                                    |
| -SrtOrdNo2         | 시작주문번호2            | Number | Y          | 10       | 역순구분이 순 : 000000000역순구분이 역순 : 999999999                                                                                            |
| -BkseqTpCode       | 역순구분               | String | Y          | 1        | 0.역순1.정순                                                                                                                           |
| -OrdPtnCode        | 주문유형코드             | String | Y          | 2        | 00.전체98.매도전체99.매수전체01.현금매도02.현금매수05.저축매도06.저축매수09.상품매도10.상품매수03.융자매도04.융자매수07.대주매도08.대주매수11.선물대용매도13.현금매도(프)14.현금매수(프)17.대출18.대출상환 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                |
|:-------------|:----------|:-------|:-----------|---------:|:---------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API 응답 Response Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                  |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                          |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                    |


### 응답 Body
| Element             | 한글명                 | type   | Required   | Length   | Description   |
|:--------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CSPAQ13700OutBlock1 | CSPAQ13700OutBlock1 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String | Y          | 20       |               |
| -InptPwd            | 입력비밀번호              | String | Y          | 8        |               |
| -OrdMktCode         | 주문시장코드              | String | Y          | 2        |               |
| -BnsTpCode          | 매매구분                | String | Y          | 1        |               |
| -IsuNo              | 종목번호                | String | Y          | 12       |               |
| -ExecYn             | 체결여부                | String | Y          | 1        |               |
| -OrdDt              | 주문일                 | String | Y          | 8        |               |
| -SrtOrdNo2          | 시작주문번호2             | Number | Y          | 10       |               |
| -BkseqTpCode        | 역순구분                | String | Y          | 1        |               |
| -OrdPtnCode         | 주문유형코드              | String | Y          | 2        |               |
| CSPAQ13700OutBlock2 | CSPAQ13700OutBlock2 | Object | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number | Y          | 5        |               |
| -SellExecAmt        | 매도체결금액              | Number | Y          | 16       |               |
| -BuyExecAmt         | 매수체결금액              | Number | Y          | 16       |               |
| -SellExecQty        | 매도체결수량              | Number | Y          | 16       |               |
| -BuyExecQty         | 매수체결수량              | Number | Y          | 16       |               |
| -SellOrdQty         | 매도주문수량              | Number | Y          | 16       |               |
| -BuyOrdQty          | 매수주문수량              | Number | Y          | 16       |               |
| CSPAQ13700OutBlock3 | CSPAQ13700OutBlock3 | Object | Y          | -        |               |
| -OrdDt              | 주문일                 | String | Y          | 8        |               |
| -MgmtBrnNo          | 관리지점번호              | String | Y          | 3        |               |
| -OrdMktCode         | 주문시장코드              | String | Y          | 2        |               |
| -OrdNo              | 주문번호                | Number | Y          | 10       |               |
| -OrgOrdNo           | 원주문번호               | Number | Y          | 10       |               |
| -IsuNo              | 종목번호                | String | Y          | 12       |               |
| -IsuNm              | 종목명                 | String | Y          | 40       |               |
| -BnsTpCode          | 매매구분                | String | Y          | 1        |               |
| -BnsTpNm            | 매매구분                | String | Y          | 10       |               |
| -OrdPtnCode         | 주문유형코드              | String | Y          | 2        |               |
| -OrdPtnNm           | 주문유형명               | String | Y          | 40       |               |
| -OrdTrxPtnCode      | 주문처리유형코드            | Number | Y          | 9        |               |
| -OrdTrxPtnNm        | 주문처리유형명             | String | Y          | 50       |               |
| -MrcTpCode          | 정정취소구분              | String | Y          | 1        |               |
| -MrcTpNm            | 정정취소구분명             | String | Y          | 10       |               |
| -MrcQty             | 정정취소수량              | Number | Y          | 16       |               |
| -MrcAbleQty         | 정정취소가능수량            | Number | Y          | 16       |               |
| -OrdQty             | 주문수량                | Number | Y          | 16       |               |
| -OrdPrc             | 주문가격                | Number | Y          | 15.2     |               |
| -ExecQty            | 체결수량                | Number | Y          | 16       |               |
| -ExecPrc            | 체결가                 | Number | Y          | 15.2     |               |
| -ExecTrxTime        | 체결처리시각              | String | Y          | 9        |               |
| -LastExecTime       | 최종체결시각              | String | Y          | 9        |               |
| -OrdprcPtnCode      | 호가유형코드              | String | Y          | 2        |               |
| -OrdprcPtnNm        | 호가유형명               | String | Y          | 40       |               |
| -OrdCndiTpCode      | 주문조건구분              | String | Y          | 1        |               |
| -AllExecQty         | 전체체결수량              | Number | Y          | 16       |               |
| -RegCommdaCode      | 통신매체코드              | String | Y          | 2        |               |
| -CommdaNm           | 통신매체명               | String | Y          | 40       |               |
| -MbrNo              | 회원번호                | String | Y          | 3        |               |
| -RsvOrdYn           | 예약주문여부              | String | Y          | 1        |               |
| -LoanDt             | 대출일                 | String | Y          | 8        |               |
| -OrdTime            | 주문시각                | String | Y          | 9        |               |
| -OpDrtnNo           | 운용지시번호              | String | Y          | 12       |               |
| -OdrrId             | 주문자ID               | String | Y          | 16       |               |


### 💡 Request Example
```json
{
  "CSPAQ13700InBlock1" : {
    "OrdMktCode" : "00",
    "BnsTpCode" : "0",
    "IsuNo" : "A005930",
    "ExecYn" : "0",
    "OrdDt" : "20230613",
    "SrtOrdNo2" : 0,
    "BkseqTpCode" : "0", 
    "OrdPtnCode" : "00"
  }
}
```

### 💡 Response Example
```json
{
    "CSPAQ13700OutBlock2": {
        "RecCnt": 1,
        "SellOrdQty": 0,
        "BuyExecAmt": 180000,
        "BuyExecQty": 3,
        "SellExecAmt": 0,
        "SellExecQty": 0,
        "BuyOrdQty": 6
    },
    "rsp_cd": "00200",
    "CSPAQ13700OutBlock3": [
    ],
    "CSPAQ13700OutBlock1": {
        "OrdMktCode": "00",
        "BkseqTpCode": "0",
        "RecCnt": 1,
        "BnsTpCode": "0",
        "IsuNo": "A005930",
        "AcntNo": "20011132702",
        "InptPwd": "********",
        "SrtOrdNo2": 0,
        "OrdPtnCode": "00",
        "ExecYn": "0",
        "OrdDt": "20230613"
    },
    "rsp_msg": "조회내역이 없습니다."
}
```

---

## 🏷️ 현물계좌예수금 주문가능금액 총평가2 (CSPAQ22200)
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
| CSPAQ22200InBlock1 | CSPAQ22200InBlock1 | Object | Y          | -        |               |
| -BalCreTp          | 잔고생성구분             | String | Y          | 1        | 0             |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                 | 한글명                 | type   | Required   | Length   | Description                               |
|:------------------------|:--------------------|:-------|:-----------|:---------|:------------------------------------------|
| CSPAQ22200OutBlock1     | CSPAQ22200OutBlock1 | Object | Y          | -        |                                           |
| -RecCnt                 | 레코드갯수               | Number | Y          | 5        | 1                                         |
| -MgmtBrnNo              | 관리지점번호              | String | Y          | 3        | 현재 미사용                                    |
| -BalCreTp               | 잔고생성구분              | String | Y          | 1        | 0:주식잔고1:기타2:재투자잔고3:유통대주4:자기융자5:유통대주6:자기대주 |
| CSPAQ22200OutBlock2     | CSPAQ22200OutBlock2 | Object | Y          | -        |                                           |
| -RecCnt                 | 레코드갯수               | Number | Y          | 5        |                                           |
| -BrnNm                  | 지점명                 | String | Y          | 40       |                                           |
| -AcntNm                 | 계좌명                 | String | Y          | 40       |                                           |
| -MnyOrdAbleAmt          | 현금주문가능금액            | Number | Y          | 16       |                                           |
| -SubstOrdAbleAmt        | 대용주문가능금액            | Number | Y          | 16       |                                           |
| -SeOrdAbleAmt           | 거래소금액               | Number | Y          | 16       |                                           |
| -KdqOrdAbleAmt          | 코스닥금액               | Number | Y          | 16       |                                           |
| -CrdtPldgOrdAmt         | 신용담보주문금액            | Number | Y          | 16       |                                           |
| -MgnRat100pctOrdAbleAmt | 증거금률100퍼센트주문가능금액    | Number | Y          | 16       |                                           |
| -MgnRat35ordAbleAmt     | 증거금률35%주문가능금액       | Number | Y          | 16       |                                           |
| -MgnRat50ordAbleAmt     | 증거금률50%주문가능금액       | Number | Y          | 16       |                                           |
| -CrdtOrdAbleAmt         | 신용주문가능금액            | Number | Y          | 16       |                                           |
| -Dps                    | 예수금                 | Number | Y          | 16       |                                           |
| -SubstAmt               | 대용금액                | Number | Y          | 16       |                                           |
| -MgnMny                 | 증거금현금               | Number | Y          | 16       |                                           |
| -MgnSubst               | 증거금대용               | Number | Y          | 16       |                                           |
| -D1Dps                  | D1예수금               | Number | Y          | 16       |                                           |
| -D2Dps                  | D2예수금               | Number | Y          | 16       |                                           |
| -RcvblAmt               | 미수금액                | Number | Y          | 16       |                                           |
| -D1ovdRepayRqrdAmt      | D1연체변제소요금액          | Number | Y          | 16       |                                           |
| -D2ovdRepayRqrdAmt      | D2연체변제소요금액          | Number | Y          | 16       |                                           |
| -MloanAmt               | 융자금액                | Number | Y          | 16       |                                           |
| -ChgAfPldgRat           | 변경후담보비율             | Number | Y          | 9.3      |                                           |
| -RqrdPldgAmt            | 소요담보금액              | Number | Y          | 16       |                                           |
| -PdlckAmt               | 담보부족금액              | Number | Y          | 16       |                                           |
| -OrgPldgSumAmt          | 원담보합계금액             | Number | Y          | 16       |                                           |
| -SubPldgSumAmt          | 부담보합계금액             | Number | Y          | 16       |                                           |
| -CrdtPldgAmtMny         | 신용담보금현금             | Number | Y          | 16       |                                           |
| -CrdtPldgSubstAmt       | 신용담보대용금액            | Number | Y          | 16       |                                           |
| -Imreq                  | 신용설정보증금             | Number | Y          | 16       |                                           |
| -CrdtPldgRuseAmt        | 신용담보재사용금액           | Number | Y          | 16       |                                           |
| -DpslRestrcAmt          | 처분제한금액              | Number | Y          | 16       |                                           |
| -PrdaySellAdjstAmt      | 전일매도정산금액            | Number | Y          | 16       |                                           |
| -PrdayBuyAdjstAmt       | 전일매수정산금액            | Number | Y          | 16       |                                           |
| -CrdaySellAdjstAmt      | 금일매도정산금액            | Number | Y          | 16       |                                           |
| -CrdayBuyAdjstAmt       | 금일매수정산금액            | Number | Y          | 16       |                                           |
| -CslLoanAmtdt1          | 매도대금담보대출금액          | Number | Y          | 16       |                                           |


---

## 🏷️ 현물계좌증거금률별주문가능수량조회 (CSPBQ00200)
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
| CSPBQ00200InBlock1 | CSPBQ00200InBlock1 | Object | Y          | -        |               |
| -BnsTpCode         | 매매구분               | String | Y          | 1        | 1@매도, 2@매수    |
| -IsuNo             | 종목번호               | String | Y          | 12       |               |
| -OrdPrc            | 주문가격               | Number | Y          | 15.2     |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element                  | 한글명                 | type   | Required   | Length   | Description   |
|:-------------------------|:--------------------|:-------|:-----------|:---------|:--------------|
| CSPBQ00200OutBlock1      | CSPBQ00200OutBlock1 | Object | Y          | -        |               |
| -RecCnt                  | 레코드갯수               | Number | Y          | 5        |               |
| -BnsTpCode               | 매매구분                | String | Y          | 1        |               |
| -AcntNo                  | 계좌번호                | String | Y          | 20       |               |
| -InptPwd                 | 입력비밀번호              | String | Y          | 8        |               |
| -IsuNo                   | 종목번호                | String | Y          | 12       |               |
| -OrdPrc                  | 주문가격                | Number | Y          | 15.2     |               |
| -RegCommdaCode           | 통신매체코드              | String | Y          | 2        |               |
| CSPBQ00200OutBlock2      | CSPBQ00200OutBlock2 | Object | Y          | -        |               |
| -RecCnt                  | 레코드갯수               | Number | Y          | 5        |               |
| -AcntNm                  | 계좌명                 | String | Y          | 40       |               |
| -IsuNm                   | 종목명                 | String | Y          | 40       |               |
| -Dps                     | 예수금                 | Number | Y          | 16       |               |
| -SubstAmt                | 대용금액                | Number | Y          | 16       |               |
| -CrdtPldgRuseAmt         | 신용담보재사용금액           | Number | Y          | 16       |               |
| -MnyOrdAbleAmt           | 현금주문가능금액            | Number | Y          | 16       |               |
| -SubstOrdAbleAmt         | 대용주문가능금액            | Number | Y          | 16       |               |
| -MnyMgn                  | 현금증거금액              | Number | Y          | 16       |               |
| -SubstMgn                | 대용증거금액              | Number | Y          | 16       |               |
| -SeOrdAbleAmt            | 거래소금액               | Number | Y          | 16       |               |
| -KdqOrdAbleAmt           | 코스닥금액               | Number | Y          | 16       |               |
| -PrsmptDpsD1             | 추정예수금(D+1)          | Number | Y          | 16       |               |
| -PrsmptDpsD2             | 추정예수금(D+2)          | Number | Y          | 16       |               |
| -MnyoutAbleAmt           | 출금가능금액              | Number | Y          | 16       |               |
| -RcvblAmt                | 미수금액                | Number | Y          | 16       |               |
| -CmsnRat                 | 수수료율                | Number | Y          | 15.5     |               |
| -AddLevyAmt              | 추가징수금액              | Number | Y          | 16       |               |
| -RuseObjAmt              | 재사용대상금액             | Number | Y          | 16       |               |
| -MnyRuseObjAmt           | 현금재사용대상금액           | Number | Y          | 16       |               |
| -FirmMgnRat              | 이용사증거금률             | Number | Y          | 7.4      |               |
| -SubstRuseObjAmt         | 대용재사용대상금액           | Number | Y          | 16       |               |
| -IsuMgnRat               | 종목증거금률              | Number | Y          | 7.4      |               |
| -AcntMgnRat              | 계좌증거금률              | Number | Y          | 7.4      |               |
| -TrdMgnrt                | 거래증거금률              | Number | Y          | 7.4      |               |
| -Cmsn                    | 수수료                 | Number | Y          | 16       |               |
| -MgnRat20pctOrdAbleAmt   | 증거금률20퍼센트주문가능금액     | Number | Y          | 16       |               |
| -MgnRat20OrdAbleQty      | 증거금률100퍼센트현금주문가능수량  | Number | Y          | 16       |               |
| -MgnRat30pctOrdAbleAmt   | 증거금률30퍼센트주문가능금액     | Number | Y          | 16       |               |
| -MgnRat30OrdAbleQty      | 증거금률30퍼센트주문가능수량     | Number | Y          | 16       |               |
| -MgnRat40pctOrdAbleAmt   | 증거금률40퍼센트주문가능금액     | Number | Y          | 16       |               |
| -MgnRat40OrdAbleQty      | 증거금률40퍼센트주문가능수량     | Number | Y          | 16       |               |
| -MgnRat100pctOrdAbleAmt  | 증거금률100퍼센트주문가능금액    | Number | Y          | 16       |               |
| -MgnRat100OrdAbleQty     | 증거금률100퍼센트주문가능수량    | Number | Y          | 16       |               |
| -MgnRat100MnyOrdAbleAmt  | 증거금률100퍼센트현금주문가능금액  | Number | Y          | 16       |               |
| -MgnRat100MnyOrdAbleQty  | 증거금률100퍼센트현금주문가능수량  | Number | Y          | 16       |               |
| -MgnRat20pctRuseAbleAmt  | 증거금률20퍼센트재사용가능금액    | Number | Y          | 16       |               |
| -MgnRat30pctRuseAbleAmt  | 증거금률30퍼센트재사용가능금액    | Number | Y          | 16       |               |
| -MgnRat40pctRuseAbleAmt  | 증거금률40퍼센트재사용가능금액    | Number | Y          | 16       |               |
| -MgnRat100pctRuseAbleAmt | 증거금률100퍼센트재사용가능금액   | Number | Y          | 16       |               |
| -OrdAbleQty              | 주문가능수량              | Number | Y          | 16       |               |
| -OrdAbleAmt              | 주문가능금액              | Number | Y          | 16       |               |


### 💡 Request Example
```json
{
  "CSPBQ00200InBlock1": {
    "RecCnt": 1,
    "BnsTpCode": "1",
    "IsuNo": "KR7000020008",
    "OrdPrc": 0.00,
    "RegCommdaCode": "41"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00136",
    "CSPBQ00200OutBlock2": {
        "KdqOrdAbleAmt": 265866666,
        "MgnRat100OrdAbleQty": 0,
        "SeOrdAbleAmt": 265866666,
        "Cmsn": 0,
        "MgnRat100pctRuseAbleAmt": 0,
        "Dps": 80000000,
        "RuseObjAmt": 0,
        "CmsnRat": "0.00000",
        "TrdMgnrt": "0.3000",
        "MgnRat20pctRuseAbleAmt": 0,
        "SubstOrdAbleAmt": 0,
        "OrdAbleQty": 0,
        "SubstMgn": 0,
        "MgnRat100MnyOrdAbleQty": 0,
        "FirmMgnRat": "0.3000",
        "CrdtPldgRuseAmt": 0,
        "IsuMgnRat": "0.3000",
        "PrsmptDpsD2": 79879982,
        "PrsmptDpsD1": 80000000,
        "MgnRat20OrdAbleQty": 0,
        "MgnRat100MnyOrdAbleAmt": 79744009,
        "MgnRat30pctOrdAbleAmt": 265866666,
        "SubstRuseObjAmt": 0,
        "OrdAbleAmt": 0,
        "MnyOrdAbleAmt": 79760000,
        "RcvblAmt": 0,
        "MgnRat40pctRuseAbleAmt": 0,
        "AddLevyAmt": 0,
        "AcntMgnRat": "0.3000",
        "MgnRat30OrdAbleQty": 0,
        "IsuNm": "",
        "MgnRat40OrdAbleQty": 0,
        "RecCnt": 1,
        "AcntNm": "우우돌",
        "MnyoutAbleAmt": 79759742,
        "MnyMgn": 240000,
        "SubstAmt": 0,
        "MgnRat100pctOrdAbleAmt": 79744009,
        "MgnRat20pctOrdAbleAmt": 398800000,
        "MnyRuseObjAmt": 0,
        "MgnRat30pctRuseAbleAmt": 0,
        "MgnRat40pctOrdAbleAmt": 199400000
    },
    "rsp_msg": "조회가 완료되었습니다.",
    "CSPBQ00200OutBlock1": {
        "RecCnt": 1,
        "RegCommdaCode": "40",
        "BnsTpCode": "1",
        "OrdPrc": "0.00",
        "IsuNo": "KR7000020008",
        "AcntNo": "20011132702",
        "InptPwd": "********"
    }
}
```

---

## 🏷️ 주식계좌 기간별수익률 상세 (FOCCQ33600)
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
| Element            | 한글명                | type   | Required   | Length   | Description      |
|:-------------------|:-------------------|:-------|:-----------|:---------|:-----------------|
| FOCCQ33600InBlock1 | FOCCQ33600InBlock1 | Object | Y          | -        |                  |
| -QrySrtDt          | 조회시작일              | String | Y          | 8        |                  |
| -QryEndDt          | 조회종료일              | String | Y          | 8        |                  |
| -TermTp            | 기간구분               | String | Y          | 1        | 1:일별, 2:주별, 3:월별 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element             | 한글명                 | type         | Required   | Length   | Description   |
|:--------------------|:--------------------|:-------------|:-----------|:---------|:--------------|
| FOCCQ33600OutBlock1 | FOCCQ33600OutBlock1 | Object       | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number       | Y          | 5        |               |
| -AcntNo             | 계좌번호                | String       | Y          | 20       |               |
| -Pwd                | 비밀번호                | String       | Y          | 8        |               |
| -QrySrtDt           | 조회시작일               | String       | Y          | 8        |               |
| -QryEndDt           | 조회종료일               | String       | Y          | 8        |               |
| -TermTp             | 기간구분                | String       | Y          | 1        |               |
| FOCCQ33600OutBlock2 | FOCCQ33600OutBlock2 | Object       | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number       | Y          | 5        |               |
| -AcntNm             | 계좌명                 | String       | Y          | 40       |               |
| -BnsctrAmt          | 매매약정금액              | Number       | Y          | 16       |               |
| -MnyinAmt           | 입금금액                | Number       | Y          | 16       |               |
| -MnyoutAmt          | 출금금액                | Number       | Y          | 16       |               |
| -InvstAvrbalPramt   | 투자원금평잔금액            | Number       | Y          | 16       |               |
| -InvstPlAmt         | 투자손익금액              | Number       | Y          | 16       |               |
| -InvstErnrat        | 투자수익률               | Number       | Y          | 9.2      |               |
| FOCCQ33600OutBlock3 | FOCCQ33600OutBlock3 | Object Array | Y          | -        |               |
| -BaseDt             | 기준일                 | String       | Y          | 8        |               |
| -FdEvalAmt          | 기초평가금액              | Number       | Y          | 19       |               |
| -EotEvalAmt         | 기말평가금액              | Number       | Y          | 19       |               |
| -InvstAvrbalPramt   | 투자원금평잔금액            | Number       | Y          | 16       |               |
| -BnsctrAmt          | 매매약정금액              | Number       | Y          | 16       |               |
| -MnyinSecinAmt      | 입금고액                | Number       | Y          | 16       |               |
| -MnyoutSecoutAmt    | 출금고액                | Number       | Y          | 16       |               |
| -EvalPnlAmt         | 평가손익금액              | Number       | Y          | 16       |               |
| -TermErnrat         | 기간수익률               | Number       | Y          | 11.3     |               |
| -Idx                | 지수                  | Number       | Y          | 13.2     |               |


### 💡 Request Example
```json
{
  "FOCCQ33600InBlock1" : {
    "RecCnt" : 1,
    "QrySrtDt" : "20230101",
    "QryEndDt" : "20230615",
    "TermTp" : "1"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00133",
    "FOCCQ33600OutBlock3": [
        {
            "FdEvalAmt": 17176098,
            "EotEvalAmt": 17176098,
            "MnyinSecinAmt": 0,
            "InvstAvrbalPramt": 17176098,
            "BnsctrAmt": 0,
            "MnyoutSecoutAmt": 0,
            "EvalPnlAmt": 0,
            "Idx": "0.00",
            "BaseDt": "20200101",
            "TermErnrat": "0.000"
        },
        {
            "FdEvalAmt": 17176098,
            "EotEvalAmt": 17525323,
            "MnyinSecinAmt": 0,
            "InvstAvrbalPramt": 17176098,
            "BnsctrAmt": 0,
            "MnyoutSecoutAmt": 0,
            "EvalPnlAmt": 349225,
            "Idx": "0.00",
            "BaseDt": "20200102",
            "TermErnrat": "2.033"
        }
    ],
    "FOCCQ33600OutBlock2": {
        "InvstPlAmt": 10393928,
        "RecCnt": 1,
        "InvstErnrat": "38.14",
        "AcntNm": "가차금",
        "InvstAvrbalPramt": 27249892,
        "BnsctrAmt": 0,
        "MnyinAmt": 42106357,
        "MnyoutAmt": 60182733
    },
    "FOCCQ33600OutBlock1": {
        "RecCnt": 1,
        "TermTp": "1",
        "AcntNo": "10011700251",
        "QrySrtDt": "20200101",
        "Pwd": "********",
        "QryEndDt": "20230101"
    },
    "rsp_msg": "조회가 계속 됩니다. 계속하시려면 연속버튼을 누르십시오."
}
```

---

## 🏷️ 주식당일매매일지/수수료 (t0150)
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
| Element      | 한글명          | type   | Required   | Length   | Description             |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------|
| t0150InBlock | t0150InBlock | Object | Y          | -        |                         |
| -cts_medosu  | CTS_매매구분     | String | Y          | 1        | 연속조회시 OutBlock의 동일필드 입력 |
| -cts_expcode | CTS_종목번호     | String | Y          | 12       | 연속조회시 OutBlock의 동일필드 입력 |
| -cts_price   | CTS_단가       | String | Y          | 9        | 연속조회시 OutBlock의 동일필드 입력 |
| -cts_middiv  | CTS_매체       | String | Y          | 2        | 연속조회시 OutBlock의 동일필드 입력 |


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
| t0150OutBlock  | t0150OutBlock  | Object       | Y          | -        |               |
| -mdqty         | 매도수량           | Number       | Y          | 9        |               |
| -mdamt         | 매도약정금액         | Number       | Y          | 18       |               |
| -mdfee         | 매도수수료          | Number       | Y          | 18       |               |
| -mdtax         | 매도거래세          | Number       | Y          | 18       |               |
| -mdargtax      | 매도농특세          | Number       | Y          | 18       |               |
| -tmdtax        | 매도제비용합         | Number       | Y          | 18       |               |
| -mdadjamt      | 매도정산금액         | Number       | Y          | 18       |               |
| -msqty         | 매수수량           | Number       | Y          | 9        |               |
| -msamt         | 매수약정금액         | Number       | Y          | 18       |               |
| -msfee         | 매수수수료          | Number       | Y          | 18       |               |
| -tmstax        | 매수제비용합         | Number       | Y          | 18       |               |
| -msadjamt      | 매수정산금액         | Number       | Y          | 18       |               |
| -tqty          | 합계수량           | Number       | Y          | 9        |               |
| -tamt          | 합계약정금액         | Number       | Y          | 18       |               |
| -tfee          | 합계수수료          | Number       | Y          | 18       |               |
| -tottax        | 합계거래세          | Number       | Y          | 18       |               |
| -targtax       | 합계농특세          | Number       | Y          | 18       |               |
| -ttax          | 합계제비용합         | Number       | Y          | 18       |               |
| -tadjamt       | 합계정산금액         | Number       | Y          | 18       |               |
| -cts_medosu    | CTS_매매구분       | String       | Y          | 1        |               |
| -cts_expcode   | CTS_종목번호       | String       | Y          | 12       |               |
| -cts_price     | CTS_단가         | String       | Y          | 9        |               |
| -cts_middiv    | CTS_매체         | String       | Y          | 2        |               |
| t0150OutBlock1 | t0150OutBlock1 | Object Array | Y          | -        |               |
| -medosu        | 매매구분           | String       | Y          | 10       |               |
| -expcode       | 종목번호           | String       | Y          | 12       |               |
| -qty           | 수량             | Number       | Y          | 9        |               |
| -price         | 단가             | Number       | Y          | 9        |               |
| -amt           | 약정금액           | Number       | Y          | 18       |               |
| -fee           | 수수료            | Number       | Y          | 18       |               |
| -tax           | 거래세            | Number       | Y          | 18       |               |
| -argtax        | 농특세            | Number       | Y          | 18       |               |
| -adjamt        | 정산금액           | Number       | Y          | 18       |               |
| -middiv        | 매체             | String       | Y          | 20       |               |


### 💡 Request Example
```json
{
  "t0150InBlock": {
    "cts_medosu": "1",
    "cts_expcode": "1",
    "cts_price": "1",
    "cts_middiv": "1"
  }
}
```

### 💡 Response Example
```json
{
  "rsp_cd": "00000",
  "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 주식당일매매일지/수수료(전일) (t0151)
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
| Element      | 한글명          | type   | Required   | Length   | Description             |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------|
| t0151InBlock | t0151InBlock | Object | Y          | -        |                         |
| -date        | 일자           | String | Y          | 8        |                         |
| -cts_medosu  | CTS_매매구분     | String | Y          | 1        | 연속조회시 OutBlock의 동일필드 입력 |
| -cts_expcode | CTS_종목번호     | String | Y          | 12       | 연속조회시 OutBlock의 동일필드 입력 |
| -cts_price   | CTS_단가       | String | Y          | 9        | 연속조회시 OutBlock의 동일필드 입력 |
| -cts_middiv  | CTS_매체       | String | Y          | 2        | 연속조회시 OutBlock의 동일필드 입력 |


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
| t0151OutBlock  | t0151OutBlock  | Object       | Y          | -        |               |
| -mdqty         | 매도수량           | Number       | Y          | 9        |               |
| -mdamt         | 매도약정금액         | Number       | Y          | 18       |               |
| -mdfee         | 매도수수료          | Number       | Y          | 18       |               |
| -mdtax         | 매도거래세          | Number       | Y          | 18       |               |
| -mdargtax      | 매도농특세          | Number       | Y          | 18       |               |
| -tmdtax        | 매도제비용합         | Number       | Y          | 18       |               |
| -mdadjamt      | 매도정산금액         | Number       | Y          | 18       |               |
| -msqty         | 매수수량           | Number       | Y          | 9        |               |
| -msamt         | 매수약정금액         | Number       | Y          | 18       |               |
| -msfee         | 매수수수료          | Number       | Y          | 18       |               |
| -tmstax        | 매수제비용합         | Number       | Y          | 18       |               |
| -msadjamt      | 매수정산금액         | Number       | Y          | 18       |               |
| -tqty          | 합계수량           | Number       | Y          | 9        |               |
| -tamt          | 합계약정금액         | Number       | Y          | 18       |               |
| -tfee          | 합계수수료          | Number       | Y          | 18       |               |
| -tottax        | 합계거래세          | Number       | Y          | 18       |               |
| -targtax       | 합계농특세          | Number       | Y          | 18       |               |
| -ttax          | 합계제비용합         | Number       | Y          | 18       |               |
| -tadjamt       | 합계정산금액         | Number       | Y          | 18       |               |
| -cts_medosu    | CTS_매매구분       | String       | Y          | 1        |               |
| -cts_expcode   | CTS_종목번호       | String       | Y          | 12       |               |
| -cts_price     | CTS_단가         | String       | Y          | 9        |               |
| -cts_middiv    | CTS_매체         | String       | Y          | 2        |               |
| t0151OutBlock1 | t0151OutBlock1 | Object Array | Y          | -        |               |
| -medosu        | 매매구분           | String       | Y          | 10       |               |
| -expcode       | 종목번호           | String       | Y          | 12       |               |
| -qty           | 수량             | Number       | Y          | 9        |               |
| -price         | 단가             | Number       | Y          | 9        |               |
| -amt           | 약정금액           | Number       | Y          | 18       |               |
| -fee           | 수수료            | Number       | Y          | 18       |               |
| -tax           | 거래세            | Number       | Y          | 18       |               |
| -argtax        | 농특세            | Number       | Y          | 18       |               |
| -adjamt        | 정산금액           | Number       | Y          | 18       |               |
| -middiv        | 매체             | String       | Y          | 20       |               |


### 💡 Request Example
```json
{
  "t0151InBlock" : {
    "date" : "20230609",
    "cts_medosu" : "",
    "cts_expcode" : "",
    "cts_price" : "",
    "cts_middiv" : ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t0151OutBlock1": [
        {
            "price": 60000,
            "qty": 4,
            "fee": 0,
            "argtax": 0,
            "expcode": "005930",
            "amt": 240000,
            "adjamt": 240000,
            "tax": 0,
            "medosu": "매수",
            "middiv": "OPEN API"
        },
        {
            "price": 60000,
            "qty": 4,
            "fee": 36,
            "argtax": 0,
            "expcode": "",
            "amt": 240000,
            "adjamt": 240036,
            "tax": 0,
            "medosu": "종목소계",
            "middiv": ""
        }
    ],
    "rsp_msg": "조회가 완료되었습니다.",
    "t0151OutBlock": {
        "mdfee": 0,
        "mdargtax": 0,
        "tmdtax": 0,
        "ttax": 36,
        "msadjamt": 240036,
        "tamt": 240000,
        "tfee": 36,
        "msqty": 4,
        "targtax": 0,
        "cts_price": "",
        "mdqty": 0,
        "mdadjamt": 0,
        "cts_middiv": "",
        "tqty": 4,
        "cts_expcode": "",
        "msfee": 36,
        "tottax": 0,
        "msamt": 240000,
        "tmstax": 36,
        "mdtax": 0,
        "cts_medosu": "",
        "tadjamt": -240036,
        "mdamt": 0
    }
}
```

---

## 🏷️ 주식잔고2 (t0424)
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
| Element      | 한글명          | type   | Required   | Length   | Description             |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------|
| t0424InBlock | t0424InBlock | Object | Y          | -        |                         |
| -prcgb       | 단가구분         | String | Y          | 1        |                         |
| -chegb       | 체결구분         | String | Y          | 1        |                         |
| -dangb       | 단일가구분        | String | Y          | 1        |                         |
| -charge      | 제비용포함여부      | String | Y          | 1        |                         |
| -cts_expcode | CTS_종목번호     | String | Y          | 22       | 연속조회시 OutBlock의 동일필드 입력 |


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
| t0424OutBlock  | t0424OutBlock  | Object       | Y          | -        |               |
| -sunamt        | 추정순자산          | Number       | Y          | 18       |               |
| -dtsunik       | 실현손익           | Number       | Y          | 18       |               |
| -mamt          | 매입금액           | Number       | Y          | 18       |               |
| -sunamt1       | 추정D2예수금        | Number       | Y          | 18       |               |
| -cts_expcode   | CTS_종목번호       | String       | Y          | 22       |               |
| -tappamt       | 평가금액           | Number       | Y          | 18       |               |
| -tdtsunik      | 평가손익           | Number       | Y          | 18       |               |
| t0424OutBlock1 | t0424OutBlock1 | Object Array | Y          | -        |               |
| -expcode       | 종목번호           | String       | Y          | 12       |               |
| -jangb         | 잔고구분           | String       | Y          | 10       |               |
| -janqty        | 잔고수량           | Number       | Y          | 18       |               |
| -mdposqt       | 매도가능수량         | Number       | Y          | 18       |               |
| -pamt          | 평균단가           | Number       | Y          | 18       |               |
| -mamt          | 매입금액           | Number       | Y          | 18       |               |
| -sinamt        | 대출금액           | Number       | Y          | 18       |               |
| -lastdt        | 만기일자           | String       | Y          | 8        |               |
| -msat          | 당일매수금액         | Number       | Y          | 18       |               |
| -mpms          | 당일매수단가         | Number       | Y          | 18       |               |
| -mdat          | 당일매도금액         | Number       | Y          | 18       |               |
| -mpmd          | 당일매도단가         | Number       | Y          | 18       |               |
| -jsat          | 전일매수금액         | Number       | Y          | 18       |               |
| -jpms          | 전일매수단가         | Number       | Y          | 18       |               |
| -jdat          | 전일매도금액         | Number       | Y          | 18       |               |
| -jpmd          | 전일매도단가         | Number       | Y          | 18       |               |
| -sysprocseq    | 처리순번           | Number       | Y          | 10       |               |
| -loandt        | 대출일자           | String       | Y          | 8        |               |
| -hname         | 종목명            | String       | Y          | 20       |               |
| -marketgb      | 시장구분           | String       | Y          | 1        |               |
| -jonggb        | 종목구분           | String       | Y          | 1        |               |
| -janrt         | 보유비중           | Number       | Y          | 10.2     |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -appamt        | 평가금액           | Number       | Y          | 18       |               |
| -dtsunik       | 평가손익           | Number       | Y          | 18       |               |
| -sunikrt       | 수익율            | Number       | Y          | 10.2     |               |
| -fee           | 수수료            | Number       | Y          | 10       |               |
| -tax           | 제세금            | Number       | Y          | 10       |               |
| -sininter      | 신용이자           | Number       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "t0424InBlock": {
    "prcgb": "",
    "chegb": "",
    "dangb": "",
    "charge": "",
    "cts_expcode": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t0424OutBlock": {
        "dtsunik": 0,
        "cts_expcode": "",
        "mamt": 120013,
        "sunamt1": 80000000,
        "tappamt": 150283,
        "sunamt": 80030265,
        "tdtsunik": 30270
    },
    "t0424OutBlock1": [
        {
            "sininter": 0,
            "fee": 30,
            "mamt": 120000,
            "sinamt": 0,
            "mpmd": 0,
            "mdposqt": 2,
            "jsat": 0,
            "janqty": 2,
            "loandt": "",
            "sysprocseq": 4,
            "price": 75300,
            "janrt": "100.00",
            "jdat": 0,
            "jpms": 0,
            "hname": "삼성전자",
            "appamt": 150283,
            "sunikrt": "25.22",
            "jonggb": "3",
            "msat": 2,
            "tax": 300,
            "pamt": 60000,
            "jpmd": 0,
            "marketgb": "",
            "jangb": "",
            "dtsunik": 30270,
            "expcode": "005930",
            "mdat": 0,
            "mpms": 60000,
            "lastdt": ""
        }
    ],
    "rsp_msg": "조회가 완료되었습니다."
}
```

---

## 🏷️ 주식체결/미체결 (t0425)
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
| Element      | 한글명          | type   | Required   | Length   | Description             |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------|
| t0425InBlock | t0425InBlock | Object | Y          | -        |                         |
| -expcode     | 종목번호         | String | Y          | 12       |                         |
| -chegb       | 체결구분         | String | Y          | 1        | 0;전체1:체결2:미체결           |
| -medosu      | 매매구분         | String | Y          | 1        | 0:전체1:매도2:매수            |
| -sortgb      | 정렬순서         | String | Y          | 1        | 1:주문번호 역순2:주문번호 순       |
| -cts_ordno   | 주문번호         | String | Y          | 10       | 연속조회시 OutBlock의 동일필드 입력 |


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
| t0425OutBlock  | t0425OutBlock  | Object       | Y          | -        |               |
| -tqty          | 총주문수량          | Number       | Y          | 18       |               |
| -tcheqty       | 총체결수량          | Number       | Y          | 18       |               |
| -tordrem       | 총미체결수량         | Number       | Y          | 18       |               |
| -cmss          | 추정수수료          | Number       | Y          | 18       |               |
| -tamt          | 총주문금액          | Number       | Y          | 18       |               |
| -tmdamt        | 총매도체결금액        | Number       | Y          | 18       |               |
| -tmsamt        | 총매수체결금액        | Number       | Y          | 18       |               |
| -tax           | 추정제세금          | Number       | Y          | 18       |               |
| -cts_ordno     | 주문번호           | String       | Y          | 10       |               |
| t0425OutBlock1 | t0425OutBlock1 | Object Array | Y          | -        |               |
| -ordno         | 주문번호           | Number       | Y          | 10       |               |
| -expcode       | 종목번호           | String       | Y          | 12       |               |
| -medosu        | 구분             | String       | Y          | 10       |               |
| -qty           | 주문수량           | Number       | Y          | 9        |               |
| -price         | 주문가격           | Number       | Y          | 9        |               |
| -cheqty        | 체결수량           | Number       | Y          | 9        |               |
| -cheprice      | 체결가격           | Number       | Y          | 9        |               |
| -ordrem        | 미체결잔량          | Number       | Y          | 9        |               |
| -cfmqty        | 확인수량           | Number       | Y          | 9        |               |
| -status        | 상태             | String       | Y          | 20       |               |
| -orgordno      | 원주문번호          | Number       | Y          | 10       |               |
| -ordgb         | 유형             | String       | Y          | 20       |               |
| -ordtime       | 주문시간           | String       | Y          | 8        |               |
| -ordermtd      | 주문매체           | String       | Y          | 10       |               |
| -sysprocseq    | 처리순번           | Number       | Y          | 10       |               |
| -hogagb        | 호가유형           | String       | Y          | 2        |               |
| -price1        | 현재가            | Number       | Y          | 8        |               |
| -orggb         | 주문구분           | String       | Y          | 2        |               |
| -singb         | 신용구분           | String       | Y          | 2        |               |
| -loandt        | 대출일자           | String       | Y          | 8        |               |
| -exchname      | 거래소명           | String       | Y          | 3        |               |


### 💡 Request Example
```json
{
  "t0425InBlock": {
    "expcode": "005930",
    "chegb": "0",
    "medosu": "0",
    "sortgb": "2",
    "cts_ordno": " "
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t0425OutBlock1": [
        {
            "orgordno": 0,
            "ordrem": 2,
            "cfmqty": 0,
            "ordgb": "보통",
            "cheqty": 0,
            "orggb": "02",
            "ordno": 84,
            "loandt": "",
            "price": 60000,
            "sysprocseq": 88,
            "singb": "00",
            "qty": 2,
            "hogagb": "00",
            "expcode": "005930",
            "medosu": "매수",
            "cheprice": 0,
            "ordtime": "08410730",
            "ordermtd": "씽(Xing)-F",
            "price1": 71900,
            "status": "접수"
        }
    ],
    "t0425OutBlock": {
        "tcheqty": 0,
        "tamt": 0,
        "tqty": 2,
        "cmss": 0,
        "tmsamt": 0,
        "tax": 0,
        "tmdamt": 0,
        "cts_ordno": "",
        "tordrem": 2
    },
    "rsp_msg": "조회가 완료되었습니다."
}
```

---
