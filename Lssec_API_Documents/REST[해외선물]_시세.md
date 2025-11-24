# REST[해외선물] 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=c1ef0e8b-4666-4d8c-a77f-6ab488cfdb39&api_id=d61d4f85-9845-41ef-b915-4efa8fd0aad1

## 📌 기본 정보
| 항목           | 내용                                 |
|:-------------|:-----------------------------------|
| Method       | POST                               |
| Domain       | https://openapi.ls-sec.co.kr:8080  |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080  |
| 모의투자 도메인     |                                    |
| URL          | /overseas-futureoption/market-data |
| Format       | JSON                               |
| Content-Type | application/json; charset=UTF-8    |
| Description  | 해외선물옵션 종목별 시세 및 차트 등               |
|              | 시세관련 데이터를 확인할 수 있습니다.              |


## 🏷️ 해외선물마스터조회 (o3101)
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
| o3101InBlock | o3101InBlock | Object | Y          | -        |               |
| -gubun       | 입력구분(예비)     | String | Y          | 1        |               |


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
| o3101OutBlock | o3101OutBlock | Object | Y          | -        |               |
| -Symbol       | 종목코드          | String | Y          | 8        |               |
| -SymbolNm     | 종목명           | String | Y          | 50       |               |
| -ApplDate     | 종목배치수신일(한국일자) | String | Y          | 8        |               |
| -BscGdsCd     | 기초상품코드        | String | Y          | 10       |               |
| -BscGdsNm     | 기초상품명         | String | Y          | 40       |               |
| -ExchCd       | 거래소코드         | String | Y          | 10       |               |
| -ExchNm       | 거래소명          | String | Y          | 40       |               |
| -CrncyCd      | 기준통화코드        | String | Y          | 3        |               |
| -NotaCd       | 진법구분코드        | String | Y          | 3        |               |
| -UntPrc       | 호가단위가격        | Number | Y          | 15.9     |               |
| -MnChgAmt     | 최소가격변동금액      | Number | Y          | 15.9     |               |
| -RgltFctr     | 가격조정계수        | Number | Y          | 15.10    |               |
| -CtrtPrAmt    | 계약당금액         | Number | Y          | 15.2     |               |
| -GdsCd        | 상품구분코드        | String | Y          | 3        |               |
| -LstngYr      | 월물(년)         | String | Y          | 4        |               |
| -LstngM       | 월물(월)         | String | Y          | 1        |               |
| -EcPrc        | 정산가격          | Number | Y          | 15.9     |               |
| -DlStrtTm     | 거래시작시간        | String | Y          | 6        |               |
| -DlEndTm      | 거래종료시간        | String | Y          | 6        |               |
| -DlPsblCd     | 거래가능구분코드      | String | Y          | 1        |               |
| -MgnCltCd     | 증거금징수구분코드     | String | Y          | 1        |               |
| -OpngMgn      | 개시증거금         | Number | Y          | 15.2     |               |
| -MntncMgn     | 유지증거금         | Number | Y          | 15.2     |               |
| -OpngMgnR     | 개시증거금율        | Number | Y          | 7.3      |               |
| -MntncMgnR    | 유지증거금율        | Number | Y          | 7.3      |               |
| -DotGb        | 유효소수점자리수      | Number | Y          | 2        |               |


### 💡 Request Example
```json
{
  "o3101InBlock": {
    "gubun": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3101OutBlock": [
        {
            "GdsCd": "002",
            "MnChgAmt": "5.000000000",
            "BscGdsCd": "AD",
            "Symbol": "ADM23",
            "UntPrc": "0.000050000",
            "ApplDate": "20230608",
            "ExchNm": "시카고상업거래소",
            "MntncMgnR": "0.000",
            "OpngMgn": "2035.00",
            "CtrtPrAmt": "100000.00",
            "DotGb": 5,
            "LstngM": "M",
            "DlEndTm": "060000",
            "DlPsblCd": "1",
            "BscGdsNm": "Australian Dollar",
            "NotaCd": "10",
            "OpngMgnR": "0.000",
            "RgltFctr": "1.0000000000",
            "MgnCltCd": "1",
            "DlStrtTm": "070000",
            "CrncyCd": "USD",
            "LstngYr": "2023",
            "EcPrc": "0.665750000",
            "MntncMgn": "2035.00",
            "SymbolNm": "Australian Dollar(2023.06)",
            "ExchCd": "CME"
        },
        {
            "GdsCd": "002",
            "MnChgAmt": "1.250000000",
            "BscGdsCd": "M6E",
            "Symbol": "M6EZ23",
            "UntPrc": "0.000100000",
            "ApplDate": "20230608",
            "ExchNm": "시카고상업거래소",
            "MntncMgnR": "0.000",
            "OpngMgn": "292.00",
            "CtrtPrAmt": "12500.00",
            "DotGb": 5,
            "LstngM": "Z",
            "DlEndTm": "060000",
            "DlPsblCd": "1",
            "BscGdsNm": "E-micro EUR\/USD",
            "NotaCd": "10",
            "OpngMgnR": "0.000",
            "RgltFctr": "1.0000000000",
            "MgnCltCd": "1",
            "DlStrtTm": "070000",
            "CrncyCd": "USD",
            "LstngYr": "2023",
            "EcPrc": "1.081150000",
            "MntncMgn": "292.00",
            "SymbolNm": "E-micro EUR\/USD(2023.12)",
            "ExchCd": "CME"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물 일별체결 조회 (o3104)
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
| o3104InBlock | o3104InBlock | Object | Y          | -        |               |
| -gubun       | 조회구분         | String | Y          | 1        | 0:일별          |
|              |              |        |            |          | 1:주별          |
|              |              |        |            |          | 2:월별          |
| -shcode      | 단축코드         | String | Y          | 8        |               |
| -date        | 조회일자         | String | Y          | 8        | YYYYMMDD      |


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
| o3104OutBlock1 | o3104OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -chedate       | 일자             | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 15.9     |               |
| -sign          | 대비구분           | String       | Y          | 1        |               |
| -change        | 대비             | Number       | Y          | 15.9     |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -open          | 시가             | Number       | Y          | 15.9     |               |
| -high          | 고가             | Number       | Y          | 15.9     |               |
| -low           | 저가             | Number       | Y          | 15.9     |               |
| -cgubun        | 체결구분           | String       | Y          | 1        |               |
| -volume        | 누적거래량          | Number       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3104InBlock": {
    "gubun": "0",
    "shcode": "ADM23",
    "date": "20230608"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3104OutBlock1": [
        {
            "volume": 57123,
            "chedate": "20230501",
            "high": "0.66820",
            "low": "0.66215",
            "price": "0.66435",
            "change": "0.00150",
            "sign": "2",
            "diff": "0.23",
            "cgubun": "",
            "open": "0.66300"
        },
        {
            "volume": 78764,
            "chedate": "20230428",
            "high": "0.66555",
            "low": "0.65820",
            "price": "0.66285",
            "change": "-0.00160",
            "sign": "5",
            "diff": "-0.24",
            "cgubun": "",
            "open": "0.66435"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물 현재가(종목정보) 조회 (o3105)
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
| o3105InBlock | o3105InBlock | Object | Y          | -        |               |
| -symbol      | 종목심볼         | String | Y          | 8        |               |


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
| o3105OutBlock | o3105OutBlock | Object | Y          | -        |               |
| -Symbol       | 종목코드          | String | Y          | 8        |               |
| -SymbolNm     | 종목명           | String | Y          | 50       |               |
| -ApplDate     | 종목배치수신일       | String | Y          | 8        |               |
| -BscGdsCd     | 기초상품코드        | String | Y          | 10       |               |
| -BscGdsNm     | 기초상품명         | String | Y          | 40       |               |
| -ExchCd       | 거래소코드         | String | Y          | 10       |               |
| -ExchNm       | 거래소명          | String | Y          | 40       |               |
| -EcCd         | 정산구분코드        | String | Y          | 1        |               |
| -CrncyCd      | 기준통화코드        | String | Y          | 3        |               |
| -NotaCd       | 진법구분코드        | String | Y          | 3        |               |
| -UntPrc       | 호가단위가격        | Number | Y          | 15.9     |               |
| -MnChgAmt     | 최소가격변동금액      | Number | Y          | 15.9     |               |
| -RgltFctr     | 가격조정계수        | Number | Y          | 15.10    |               |
| -CtrtPrAmt    | 계약당금액         | Number | Y          | 15.2     |               |
| -LstngMCnt    | 상장개월수         | Number | Y          | 2        |               |
| -GdsCd        | 상품구분코드        | String | Y          | 3        |               |
| -MrktCd       | 시장구분코드        | String | Y          | 3        |               |
| -EminiCd      | Emini구분코드     | String | Y          | 1        |               |
| -LstngYr      | 상장년           | String | Y          | 4        |               |
| -LstngM       | 상장월           | String | Y          | 1        |               |
| -SeqNo        | 월물순서          | Number | Y          | 5        |               |
| -LstngDt      | 상장일자          | String | Y          | 8        |               |
| -MtrtDt       | 만기일자          | String | Y          | 8        |               |
| -FnlDlDt      | 최종거래일         | String | Y          | 8        |               |
| -FstTrsfrDt   | 최초인도통지일자      | String | Y          | 8        |               |
| -EcPrc        | 정산가격          | Number | Y          | 15.9     |               |
| -DlDt         | 거래시작일자(한국)    | String | Y          | 8        |               |
| -DlStrtTm     | 거래시작시간(한국)    | String | Y          | 6        |               |
| -DlEndTm      | 거래종료시간(한국)    | String | Y          | 6        |               |
| -OvsStrDay    | 거래시작일자(현지)    | String | Y          | 8        |               |
| -OvsStrTm     | 거래시작시간(현지)    | String | Y          | 6        |               |
| -OvsEndDay    | 거래종료일자(현지)    | String | Y          | 8        |               |
| -OvsEndTm     | 거래종료시간(현지)    | String | Y          | 6        |               |
| -DlPsblCd     | 거래가능구분코드      | String | Y          | 1        |               |
| -MgnCltCd     | 증거금징수구분코드     | String | Y          | 1        |               |
| -OpngMgn      | 개시증거금         | Number | Y          | 15.2     |               |
| -MntncMgn     | 유지증거금         | Number | Y          | 15.2     |               |
| -OpngMgnR     | 개시증거금율        | Number | Y          | 7.3      |               |
| -MntncMgnR    | 유지증거금율        | Number | Y          | 7.3      |               |
| -DotGb        | 유효소수점자리수      | Number | Y          | 2        |               |
| -TimeDiff     | 시차            | Number | Y          | 5        |               |
| -OvsDate      | 현지체결일자        | String | Y          | 8        |               |
| -KorDate      | 한국체결일자        | String | Y          | 8        |               |
| -TrdTm        | 현지체결시간        | String | Y          | 6        |               |
| -RcvTm        | 한국체결시각        | String | Y          | 6        |               |
| -TrdP         | 체결가격          | Number | Y          | 15.9     |               |
| -TrdQ         | 체결수량          | Number | Y          | 10       |               |
| -TotQ         | 누적거래량         | Number | Y          | 15       |               |
| -TrdAmt       | 체결거래대금        | Number | Y          | 15.2     |               |
| -TotAmt       | 누적거래대금        | Number | Y          | 15.2     |               |
| -OpenP        | 시가            | Number | Y          | 15.9     |               |
| -HighP        | 고가            | Number | Y          | 15.9     |               |
| -LowP         | 저가            | Number | Y          | 15.9     |               |
| -CloseP       | 전일종가          | Number | Y          | 15.9     |               |
| -YdiffP       | 전일대비          | Number | Y          | 15.9     |               |
| -YdiffSign    | 전일대비구분        | String | Y          | 1        |               |
| -Cgubun       | 체결구분          | String | Y          | 1        |               |
| -Diff         | 등락율           | Number | Y          | 6.2      |               |


### 💡 Request Example
```json
{
   "o3105InBlock" :{
      "symbol" : "CUSN23  "
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3105OutBlock": {
        "GdsCd": "002",
        "MnChgAmt": "10.000000000",
        "CloseP": "7.2081",
        "Diff": "-0.10",
        "UntPrc": "0.0001",
        "OvsEndTm": "163000",
        "TimeDiff": -1,
        "EminiCd": "0",
        "CtrtPrAmt": "100000.00",
        "DotGb": 4,
        "OvsStrDay": "20230625",
        "DlEndTm": "173000",
        "EcCd": "1",
        "TotQ": 1011,
        "SeqNo": 1,
        "BscGdsNm": "Renminbi_USD\/CNH",
        "YdiffP": "-0.0070",
        "RgltFctr": "1.0000000000",
        "OpenP": "7.2081",
        "MgnCltCd": "1",
        "RcvTm": "103710",
        "TrdQ": 1,
        "TrdP": "7.2011",
        "TrdAmt": "7.20",
        "DlStrtTm": "181500",
        "CrncyCd": "CNY",
        "MrktCd": "001",
        "LowP": "7.1907",
        "YdiffSign": "5",
        "OvsStrTm": "171500",
        "BscGdsCd": "CUS",
        "MtrtDt": "20230717",
        "Symbol": "CUSN23",
        "OvsDate": "20230626",
        "TrdTm": "093710",
        "LstngMCnt": 12,
        "ApplDate": "20230626",
        "ExchNm": "홍콩거래소",
        "MntncMgnR": "0",
        "OpngMgn": "14084.00",
        "LstngM": "N",
        "Cgubun": "",
        "DlPsblCd": "1",
        "NotaCd": "10",
        "OpngMgnR": "0",
        "TotAmt": "0.00",
        "FnlDlDt": "20230717",
        "HighP": "7.2081",
        "LstngYr": "2023",
        "DlDt": "20230626",
        "KorDate": "20230626",
        "FstTrsfrDt": "",
        "EcPrc": "7.2081",
        "MntncMgn": "14084.00",
        "SymbolNm": "Renminbi_USD\/CNH(2023.07)",
        "LstngDt": "20230116",
        "OvsEndDay": "20230626",
        "ExchCd": "HKEX"
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물 현재가호가 조회 (o3106)
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
| o3106InBlock | o3106InBlock | Object | Y          | -        |               |
| -symbol      | 종목심볼         | String | Y          | 8        |               |


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
| o3106OutBlock | o3106OutBlock | Object | Y          | -        |               |
| -symbol       | 종목코드          | String | Y          | 8        |               |
| -symbolname   | 종목명           | String | Y          | 50       |               |
| -price        | 현재가           | Number | Y          | 15.9     |               |
| -sign         | 전일대비구분        | String | Y          | 1        |               |
| -change       | 전일대비          | Number | Y          | 15.9     |               |
| -diff         | 등락율           | Number | Y          | 6.2      |               |
| -volume       | 누적거래량         | Number | Y          | 10       |               |
| -jnilclose    | 전일종가          | Number | Y          | 15.9     |               |
| -open         | 시가            | Number | Y          | 15.9     |               |
| -high         | 고가            | Number | Y          | 15.9     |               |
| -low          | 저가            | Number | Y          | 15.9     |               |
| -hotime       | 호가수신시간        | String | Y          | 6        |               |
| -offerho1     | 매도호가1         | Number | Y          | 15.9     |               |
| -bidho1       | 매수호가1         | Number | Y          | 15.9     |               |
| -offercnt1    | 매도호가건수1       | Number | Y          | 10       |               |
| -bidcnt1      | 매수호가건수1       | Number | Y          | 10       |               |
| -offerrem1    | 매도호가수량1       | Number | Y          | 10       |               |
| -bidrem1      | 매수호가수량1       | Number | Y          | 10       |               |
| -offerho2     | 매도호가2         | Number | Y          | 15.9     |               |
| -bidho2       | 매수호가2         | Number | Y          | 15.9     |               |
| -offercnt2    | 매도호가건수2       | Number | Y          | 10       |               |
| -bidcnt2      | 매수호가건수2       | Number | Y          | 10       |               |
| -offerrem2    | 매도호가수량2       | Number | Y          | 10       |               |
| -bidrem2      | 매수호가수량2       | Number | Y          | 10       |               |
| -offerho3     | 매도호가3         | Number | Y          | 15.9     |               |
| -bidho3       | 매수호가3         | Number | Y          | 15.9     |               |
| -offercnt3    | 매도호가건수3       | Number | Y          | 10       |               |
| -bidcnt3      | 매수호가건수3       | Number | Y          | 10       |               |
| -offerrem3    | 매도호가수량3       | Number | Y          | 10       |               |
| -bidrem3      | 매수호가수량3       | Number | Y          | 10       |               |
| -offerho4     | 매도호가4         | Number | Y          | 15.9     |               |
| -bidho4       | 매수호가4         | Number | Y          | 15.9     |               |
| -offercnt4    | 매도호가건수4       | Number | Y          | 10       |               |
| -bidcnt4      | 매수호가건수4       | Number | Y          | 10       |               |
| -offerrem4    | 매도호가수량4       | Number | Y          | 10       |               |
| -bidrem4      | 매수호가수량4       | Number | Y          | 10       |               |
| -offerho5     | 매도호가5         | Number | Y          | 15.9     |               |
| -bidho5       | 매수호가5         | Number | Y          | 15.9     |               |
| -offercnt5    | 매도호가건수5       | Number | Y          | 10       |               |
| -bidcnt5      | 매수호가건수5       | Number | Y          | 10       |               |
| -offerrem5    | 매도호가수량5       | Number | Y          | 10       |               |
| -bidrem5      | 매수호가수량5       | Number | Y          | 10       |               |
| -offercnt     | 매도호가건수합       | Number | Y          | 10       |               |
| -bidcnt       | 매수호가건수합       | Number | Y          | 10       |               |
| -offer        | 매도호가수량합       | Number | Y          | 10       |               |
| -bid          | 매수호가수량합       | Number | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3106InBlock": {
    "symbol": "ADM23"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3106OutBlock": {
        "offerrem2": 19,
        "offerho4": "0.67685",
        "bidho5": "0.67645",
        "symbol": "ADM23",
        "offerho3": "0.67680",
        "offerrem3": 30,
        "bidho4": "0.67650",
        "offerrem4": 43,
        "offerho5": "0.67690",
        "offerrem5": 53,
        "jnilclose": "0.67535",
        "offerrem1": 4,
        "sign": "2",
        "symbolname": "Australian Dollar(2023.06)",
        "bidrem3": 52,
        "offer": 149,
        "bidrem4": 55,
        "high": "0.67680",
        "bidrem1": 21,
        "bidrem2": 38,
        "low": "0.67395",
        "price": "0.67670",
        "bidcnt5": 20,
        "bidcnt4": 18,
        "bidcnt3": 20,
        "bidcnt2": 16,
        "bidcnt1": 12,
        "bidho1": "0.67665",
        "hotime": "000533",
        "offerho2": "0.67675",
        "bidho3": "0.67655",
        "bidrem5": 54,
        "offerho1": "0.67670",
        "bidho2": "0.67660",
        "offercnt5": 16,
        "change": "0.00135",
        "offercnt3": 16,
        "offercnt4": 21,
        "diff": "0.20",
        "offercnt1": 2,
        "offercnt2": 12,
        "volume": 18844,
        "bid": 220,
        "offercnt": 67,
        "bidcnt": 86,
        "open": "0.67510"
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물 관심종목 조회 (o3107)
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
| Element      | 한글명          | type         | Required   | Length   | Description   |
|:-------------|:-------------|:-------------|:-----------|:---------|:--------------|
| o3107InBlock | o3107InBlock | Object Array | Y          | -        |               |
| (Occurs)     | (Occurs)     |              |            |          |               |
| -symbol      | 종목심볼         | String       | Y          | 8        |               |


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
| o3107OutBlock | o3107OutBlock | Object Array | Y          | -        |               |
| (Occurs)      | (Occurs)      |              |            |          |               |
| -symbol       | 종목코드          | String       | Y          | 8        |               |
| -symbolname   | 종목명           | String       | Y          | 50       |               |
| -price        | 현재가           | Number       | Y          | 15.9     |               |
| -sign         | 전일대비구분        | String       | Y          | 1        |               |
| -change       | 전일대비          | Number       | Y          | 15.9     |               |
| -diff         | 등락율           | Number       | Y          | 6.2      |               |
| -volume       | 누적거래량         | Number       | Y          | 10       |               |
| -jnilclose    | 전일종가          | Number       | Y          | 15.9     |               |
| -open         | 시가            | Number       | Y          | 15.9     |               |
| -high         | 고가            | Number       | Y          | 15.9     |               |
| -low          | 저가            | Number       | Y          | 15.9     |               |
| -offerho1     | 매도호가1         | Number       | Y          | 15.9     |               |
| -bidho1       | 매수호가1         | Number       | Y          | 15.9     |               |
| -offercnt1    | 매도호가건수1       | Number       | Y          | 10       |               |
| -bidcnt1      | 매수호가건수1       | Number       | Y          | 10       |               |
| -offerrem1    | 매도호가수량1       | Number       | Y          | 10       |               |
| -bidrem1      | 매수호가수량1       | Number       | Y          | 10       |               |
| -offercnt     | 매도호가건수합       | Number       | Y          | 10       |               |
| -bidcnt       | 매수호가건수합       | Number       | Y          | 10       |               |
| -offer        | 매도호가수량합       | Number       | Y          | 10       |               |
| -bid          | 매수호가수량합       | Number       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3107InBlock": {
    "symbol": "ADM23"
  }
}
```

### 💡 Response Example
```json
{
  "o3107OutBlock": [],
  "rsp_cd": "00000",
  "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물 시간대별(Tick)체결 조회 (o3116)
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
| o3116InBlock | o3116InBlock | Object | Y          | -        |               |
| -gubun       | 조회구분         | String | Y          | 1        | 0:당일 만 사용가능   |
| -shcode      | 단축코드         | String | Y          | 8        |               |
| -readcnt     | 조회갯수         | Number | Y          | 4        |               |
| -cts_seq     | 순번CTS        | Number | Y          | 8        |               |


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
| o3116OutBlock  | o3116OutBlock  | Object       | Y          | -        |               |
| -cts_seq       | 순번CTS          | Number       | Y          | 8        |               |
| o3116OutBlock1 | o3116OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -ovsdate       | 현지일자           | String       | Y          | 8        |               |
| -ovstime       | 현지시간           | String       | Y          | 6        |               |
| -price         | 현재가            | Number       | Y          | 15.9     |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 15.9     |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -cvolume       | 체결수량           | Number       | Y          | 10       |               |
| -volume        | 누적거래량          | Number       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3116InBlock": {
    "gubun": "0",
    "shcode": "ADM23",
    "readcnt": 20,
    "cts_seq": 0
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3116OutBlock": {
        "cts_seq": 4826
    },
    "o3116OutBlock1": [
        {
            "volume": 18844,
            "ovstime": "000533",
            "price": "0.67670",
            "change": "0.00135",
            "sign": "2",
            "ovsdate": "20230613",
            "diff": "0.20",
            "cvolume": 1
        },
        {
            "volume": 18771,
            "ovstime": "000438",
            "price": "0.67665",
            "change": "0.00130",
            "sign": "2",
            "ovsdate": "20230613",
            "diff": "0.19",
            "cvolume": 1
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물옵션 마스터 조회 (o3121)
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
| Element      | 한글명          | type   | Required   | Length   | Description            |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------|
| o3121InBlock | o3121InBlock | Object | Y          | -        |                        |
| -MktGb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션)       |
| -BscGdsCd    | 옵션기초상품코드     | String | Y          | 10       | ex) ['시장구분' 옵션의 경우]    |
|              |              |        |            |          |      공란(옵션상품 목록),      |
|              |              |        |            |          |      O_ES(ES상품옵션종목 목록) |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element           | 한글명           | type   | Required   | Length   | Description              |
|:------------------|:--------------|:-------|:-----------|:---------|:-------------------------|
| o3121OutBlock     | o3121OutBlock | Object | Y          | -        |                          |
| -Symbol           | 종목코드          | String | Y          | 16       |                          |
| -SymbolNm         | 종목명           | String | Y          | 50       |                          |
| -ApplDate         | 종목배치수신일(한국일자) | String | Y          | 8        |                          |
| -BscGdsCd         | 기초상품코드        | String | Y          | 10       | 시장구분 공란 시 옵션기초상품코드 받는 필드 |
| -BscGdsNm         | 기초상품명         | String | Y          | 40       |                          |
| -ExchCd           | 거래소코드         | String | Y          | 10       |                          |
| -ExchNm           | 거래소명          | String | Y          | 40       |                          |
| -CrncyCd          | 기준통화코드        | String | Y          | 3        |                          |
| -NotaCd           | 진법구분코드        | String | Y          | 3        |                          |
| -UntPrc           | 호가단위가격        | Number | Y          | 15.9     |                          |
| -MnChgAmt         | 최소가격변동금액      | Number | Y          | 15.9     |                          |
| -RgltFctr         | 가격조정계수        | Number | Y          | 15.10    |                          |
| -CtrtPrAmt        | 계약당금액         | Number | Y          | 15.2     |                          |
| -GdsCd            | 상품구분코드        | String | Y          | 3        |                          |
| -LstngYr          | 월물(년)         | String | Y          | 4        |                          |
| -LstngM           | 월물(월)         | String | Y          | 1        |                          |
| -EcPrc            | 정산가격          | Number | Y          | 15.9     |                          |
| -DlStrtTm         | 거래시작시간        | String | Y          | 6        |                          |
| -DlEndTm          | 거래종료시간        | String | Y          | 6        |                          |
| -DlPsblCd         | 거래가능구분코드      | String | Y          | 1        |                          |
| -MgnCltCd         | 증거금징수구분코드     | String | Y          | 1        |                          |
| -OpngMgn          | 개시증거금         | Number | Y          | 15.2     |                          |
| -MntncMgn         | 유지증거금         | Number | Y          | 15.2     |                          |
| -OpngMgnR         | 개시증거금율        | Number | Y          | 7.3      |                          |
| -MntncMgnR        | 유지증거금율        | Number | Y          | 7.3      |                          |
| -DotGb            | 유효소수점자리수      | Number | Y          | 2        |                          |
| -XrcPrc           | 옵션행사가         | String | Y          | 15       |                          |
| -FdasBasePrc      | 기초자산기준가격      | String | Y          | 15       |                          |
| -OptTpCode        | 옵션콜풋구분        | String | Y          | 1        |                          |
| -RgtXrcPtnCode    | 권리행사구분코드      | String | Y          | 1        |                          |
| -Moneyness        | ATM구분         | String | Y          | 1        |                          |
| -LastSettPtnCode  | 해외파생기초자산종목코드  | String | Y          | 30       |                          |
| -OptMinOrcPrc     | 해외옵션최소호가      | String | Y          | 15       |                          |
| -OptMinBaseOrcPrc | 해외옵션최소기준호가    | String | Y          | 15       |                          |


### 💡 Request Example
```json
{
  "o3121InBlock": {
    "MktGb": "O",
    "BscGdsCd": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3121OutBlock": [
        {
            "GdsCd": "001",
            "MnChgAmt": "0",
            "BscGdsCd": "O_E1A",
            "Symbol": "",
            "XrcPrc": "",
            "UntPrc": "0",
            "OptMinOrcPrc": "",
            "ApplDate": "20230608",
            "ExchNm": "시카고상업거래소",
            "MntncMgnR": "0",
            "OpngMgn": "0",
            "FdasBasePrc": "",
            "CtrtPrAmt": "0",
            "DotGb": 0,
            "OptMinBaseOrcPrc": "",
            "LstngM": "",
            "DlEndTm": "",
            "RgtXrcPtnCode": "",
            "DlPsblCd": "",
            "BscGdsNm": "W1 Monday E-mini S&P 500 Option",
            "NotaCd": "",
            "OpngMgnR": "0",
            "RgltFctr": "0",
            "OptTpCode": "",
            "LastSettPtnCode": "",
            "MgnCltCd": "",
            "Moneyness": "",
            "DlStrtTm": "",
            "CrncyCd": "",
            "LstngYr": "",
            "EcPrc": "0",
            "MntncMgn": "0",
            "SymbolNm": "",
            "ExchCd": "CME"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물옵션 차트 분봉 조회 (o3123)
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
| o3123InBlock | o3123InBlock | Object | Y          | -        |                               |
| -mktgb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션)              |
| -shcode      | 단축코드         | String | Y          | 16       | ex) ADU13,2ESF16_1915         |
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
| o3123OutBlock  | o3123OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 16       |               |
| -timediff      | 시차             | Number       | Y          | 4        |               |
| -readcnt       | 조회건수           | Number       | Y          | 4        |               |
| -cts_date      | 연속일자           | String       | Y          | 8        |               |
| -cts_time      | 연속시간           | String       | Y          | 6        |               |
| o3123OutBlock1 | o3123OutBlock1 | Object Array | Y          | -        |               |
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
  "o3123InBlock": {
    "mktgb": "F",
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
    "o3123OutBlock1": [
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
            "date": "20230612",
            "volume": 12,
            "high": "0.67650",
            "low": "0.67640",
            "time": "234700",
            "close": "0.67640",
            "open": "0.67650"
        }
    ],
    "rsp_msg": "조회완료",
    "o3123OutBlock": {
        "cts_date": "20230612",
        "readcnt": 20,
        "shcode": "ADM23",
        "timediff": -14,
        "cts_time": "234700"
    }
}
```

---

## 🏷️ 해외선물옵션 현재가(종목정보) 조회 (o3125)
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
| o3125InBlock | o3125InBlock | Object | Y          | -        |                  |
| -mktgb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션) |
| -symbol      | 종목심볼         | String | Y          | 16       | ex) 2ESF16_1915  |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명           | type   | Required   | Length   | Description   |
|:---------------|:--------------|:-------|:-----------|:---------|:--------------|
| o3125OutBlock  | o3125OutBlock | Object | Y          | -        |               |
| -Symbol        | 종목코드          | String | Y          | 16       |               |
| -SymbolNm      | 종목명           | String | Y          | 50       |               |
| -ApplDate      | 종목배치수신일       | String | Y          | 8        |               |
| -BscGdsCd      | 기초상품코드        | String | Y          | 10       |               |
| -BscGdsNm      | 기초상품명         | String | Y          | 40       |               |
| -ExchCd        | 거래소코드         | String | Y          | 10       |               |
| -ExchNm        | 거래소명          | String | Y          | 40       |               |
| -EcCd          | 정산구분코드        | String | Y          | 1        |               |
| -CrncyCd       | 기준통화코드        | String | Y          | 3        |               |
| -NotaCd        | 진법구분코드        | String | Y          | 3        |               |
| -UntPrc        | 호가단위가격        | Number | Y          | 15.9     |               |
| -MnChgAmt      | 최소가격변동금액      | Number | Y          | 15.9     |               |
| -RgltFctr      | 가격조정계수        | Number | Y          | 15.10    |               |
| -CtrtPrAmt     | 계약당금액         | Number | Y          | 15.2     |               |
| -LstngMCnt     | 상장개월수         | Number | Y          | 2        |               |
| -GdsCd         | 상품구분코드        | String | Y          | 3        |               |
| -MrktCd        | 시장구분코드        | String | Y          | 3        |               |
| -EminiCd       | Emini구분코드     | String | Y          | 1        |               |
| -LstngYr       | 상장년           | String | Y          | 4        |               |
| -LstngM        | 상장월           | String | Y          | 1        |               |
| -SeqNo         | 월물순서          | Number | Y          | 5        |               |
| -LstngDt       | 상장일자          | String | Y          | 8        |               |
| -MtrtDt        | 만기일자          | String | Y          | 8        |               |
| -FnlDlDt       | 최종거래일         | String | Y          | 8        |               |
| -FstTrsfrDt    | 최초인도통지일자      | String | Y          | 8        |               |
| -EcPrc         | 정산가격          | Number | Y          | 15.9     |               |
| -DlDt          | 거래시작일자(한국)    | String | Y          | 8        |               |
| -DlStrtTm      | 거래시작시간(한국)    | String | Y          | 6        |               |
| -DlEndTm       | 거래종료시간(한국)    | String | Y          | 6        |               |
| -OvsStrDay     | 거래시작일자(현지)    | String | Y          | 8        |               |
| -OvsStrTm      | 거래시작시간(현지)    | String | Y          | 6        |               |
| -OvsEndDay     | 거래종료일자(현지)    | String | Y          | 8        |               |
| -OvsEndTm      | 거래종료시간(현지)    | String | Y          | 6        |               |
| -DlPsblCd      | 거래가능구분코드      | String | Y          | 1        |               |
| -MgnCltCd      | 증거금징수구분코드     | String | Y          | 1        |               |
| -OpngMgn       | 개시증거금         | Number | Y          | 15.2     |               |
| -MntncMgn      | 유지증거금         | Number | Y          | 15.2     |               |
| -OpngMgnR      | 개시증거금율        | Number | Y          | 7.3      |               |
| -MntncMgnR     | 유지증거금율        | Number | Y          | 7.3      |               |
| -DotGb         | 유효소수점자리수      | Number | Y          | 2        |               |
| -TimeDiff      | 시차            | Number | Y          | 5        |               |
| -OvsDate       | 현지체결일자        | String | Y          | 8        |               |
| -KorDate       | 한국체결일자        | String | Y          | 8        |               |
| -TrdTm         | 현지체결시간        | String | Y          | 6        |               |
| -RcvTm         | 한국체결시각        | String | Y          | 6        |               |
| -TrdP          | 체결가격          | Number | Y          | 15.9     |               |
| -TrdQ          | 체결수량          | Number | Y          | 10       |               |
| -TotQ          | 누적거래량         | Number | Y          | 15       |               |
| -TrdAmt        | 체결거래대금        | Number | Y          | 15.2     |               |
| -TotAmt        | 누적거래대금        | Number | Y          | 15.2     |               |
| -OpenP         | 시가            | Number | Y          | 15.9     |               |
| -HighP         | 고가            | Number | Y          | 15.9     |               |
| -LowP          | 저가            | Number | Y          | 15.9     |               |
| -CloseP        | 전일종가          | Number | Y          | 15.9     |               |
| -YdiffP        | 전일대비          | Number | Y          | 15.9     |               |
| -YdiffSign     | 전일대비구분        | String | Y          | 1        |               |
| -Cgubun        | 체결구분          | String | Y          | 1        |               |
| -Diff          | 등락율           | Number | Y          | 6.2      |               |
| -MinOrcPrc     | 최소호가          | Number | Y          | 15.9     |               |
| -MinBaseOrcPrc | 최소기준호가        | Number | Y          | 15.9     |               |


### 💡 Request Example
```json
{
   "o3125InBlock" :{
      "mktgb" : "F",
      "symbol" : "HSIM23          "
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3125OutBlock": {
        "GdsCd": "001",
        "MnChgAmt": "50.000000000",
        "CloseP": "18875.0",
        "MinBaseOrcPrc": "0",
        "Diff": "0.25",
        "UntPrc": "1.0",
        "OvsEndTm": "163000",
        "TimeDiff": -1,
        "EminiCd": "0",
        "CtrtPrAmt": "50.00",
        "DotGb": 0,
        "OvsStrDay": "20230625",
        "DlEndTm": "173000",
        "EcCd": "1",
        "TotQ": 93965,
        "SeqNo": 1,
        "BscGdsNm": "Hang Seng",
        "YdiffP": "47.0",
        "RgltFctr": "1.0000000000",
        "OpenP": "18877.0",
        "MgnCltCd": "1",
        "RcvTm": "122002",
        "TrdQ": 3,
        "TrdP": "18922.0",
        "TrdAmt": "56766.00",
        "DlStrtTm": "181500",
        "CrncyCd": "HKD",
        "MrktCd": "001",
        "LowP": "18676.0",
        "YdiffSign": "2",
        "OvsStrTm": "171500",
        "BscGdsCd": "HSI",
        "MtrtDt": "20230629",
        "Symbol": "HSIM23",
        "OvsDate": "20230626",
        "TrdTm": "112002",
        "LstngMCnt": 12,
        "ApplDate": "20230626",
        "ExchNm": "홍콩거래소",
        "MntncMgnR": "0",
        "MinOrcPrc": "0",
        "OpngMgn": "101944.00",
        "LstngM": "M",
        "Cgubun": "",
        "DlPsblCd": "1",
        "NotaCd": "10",
        "OpngMgnR": "0",
        "TotAmt": "0.00",
        "FnlDlDt": "20230629",
        "HighP": "19022.0",
        "LstngYr": "2023",
        "DlDt": "20230626",
        "KorDate": "20230626",
        "FstTrsfrDt": "",
        "EcPrc": "18875.0",
        "MntncMgn": "101944.00",
        "SymbolNm": "Hang Seng(2023.06)",
        "LstngDt": "20221226",
        "OvsEndDay": "20230626",
        "ExchCd": "HKEX"
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물옵션 현재가호가 조회 (o3126)
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
| o3126InBlock | o3126InBlock | Object | Y          | -        |                  |
| -mktgb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션) |
| -symbol      | 종목심볼         | String | Y          | 16       | ex) 2ESF16_1915  |


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
| o3126OutBlock | o3126OutBlock | Object | Y          | -        |               |
| -symbol       | 종목코드          | String | Y          | 16       |               |
| -symbolname   | 종목명           | String | Y          | 50       |               |
| -price        | 현재가           | Number | Y          | 15.9     |               |
| -sign         | 전일대비구분        | String | Y          | 1        |               |
| -change       | 전일대비          | Number | Y          | 15.9     |               |
| -diff         | 등락율           | Number | Y          | 6.2      |               |
| -volume       | 누적거래량         | Number | Y          | 10       |               |
| -jnilclose    | 전일종가          | Number | Y          | 15.9     |               |
| -open         | 시가            | Number | Y          | 15.9     |               |
| -high         | 고가            | Number | Y          | 15.9     |               |
| -low          | 저가            | Number | Y          | 15.9     |               |
| -hotime       | 호가수신시간        | String | Y          | 6        |               |
| -offerho1     | 매도호가1         | Number | Y          | 15.9     |               |
| -bidho1       | 매수호가1         | Number | Y          | 15.9     |               |
| -offercnt1    | 매도호가건수1       | Number | Y          | 10       |               |
| -bidcnt1      | 매수호가건수1       | Number | Y          | 10       |               |
| -offerrem1    | 매도호가수량1       | Number | Y          | 10       |               |
| -bidrem1      | 매수호가수량1       | Number | Y          | 10       |               |
| -offerho2     | 매도호가2         | Number | Y          | 15.9     |               |
| -bidho2       | 매수호가2         | Number | Y          | 15.9     |               |
| -offercnt2    | 매도호가건수2       | Number | Y          | 10       |               |
| -bidcnt2      | 매수호가건수2       | Number | Y          | 10       |               |
| -offerrem2    | 매도호가수량2       | Number | Y          | 10       |               |
| -bidrem2      | 매수호가수량2       | Number | Y          | 10       |               |
| -offerho3     | 매도호가3         | Number | Y          | 15.9     |               |
| -bidho3       | 매수호가3         | Number | Y          | 15.9     |               |
| -offercnt3    | 매도호가건수3       | Number | Y          | 10       |               |
| -bidcnt3      | 매수호가건수3       | Number | Y          | 10       |               |
| -offerrem3    | 매도호가수량3       | Number | Y          | 10       |               |
| -bidrem3      | 매수호가수량3       | Number | Y          | 10       |               |
| -offerho4     | 매도호가4         | Number | Y          | 15.9     |               |
| -bidho4       | 매수호가4         | Number | Y          | 15.9     |               |
| -offercnt4    | 매도호가건수4       | Number | Y          | 10       |               |
| -bidcnt4      | 매수호가건수4       | Number | Y          | 10       |               |
| -offerrem4    | 매도호가수량4       | Number | Y          | 10       |               |
| -bidrem4      | 매수호가수량4       | Number | Y          | 10       |               |
| -offerho5     | 매도호가5         | Number | Y          | 15.9     |               |
| -bidho5       | 매수호가5         | Number | Y          | 15.9     |               |
| -offercnt5    | 매도호가건수5       | Number | Y          | 10       |               |
| -bidcnt5      | 매수호가건수5       | Number | Y          | 10       |               |
| -offerrem5    | 매도호가수량5       | Number | Y          | 10       |               |
| -bidrem5      | 매수호가수량5       | Number | Y          | 10       |               |
| -offercnt     | 매도호가건수합       | Number | Y          | 10       |               |
| -bidcnt       | 매수호가건수합       | Number | Y          | 10       |               |
| -offer        | 매도호가수량합       | Number | Y          | 10       |               |
| -bid          | 매수호가수량합       | Number | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3126InBlock": {
    "mktgb": "F",
    "symbol": "ADM23"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "조회완료",
    "o3126OutBlock": {
        "offerrem2": 20,
        "offerho4": "0.67685",
        "bidho5": "0.67645",
        "symbol": "ADM23",
        "offerho3": "0.67680",
        "offerrem3": 30,
        "bidho4": "0.67650",
        "offerrem4": 43,
        "offerho5": "0.67690",
        "offerrem5": 53,
        "jnilclose": "0.67535",
        "offerrem1": 4,
        "sign": "2",
        "symbolname": "Australian Dollar(2023.06)",
        "bidrem3": 52,
        "offer": 150,
        "bidrem4": 55,
        "high": "0.67680",
        "bidrem1": 21,
        "bidrem2": 38,
        "low": "0.67395",
        "price": "0.67670",
        "bidcnt5": 20,
        "bidcnt4": 18,
        "bidcnt3": 20,
        "bidcnt2": 16,
        "bidcnt1": 12,
        "bidho1": "0.67665",
        "hotime": "000534",
        "offerho2": "0.67675",
        "bidho3": "0.67655",
        "bidrem5": 54,
        "offerho1": "0.67670",
        "bidho2": "0.67660",
        "offercnt5": 16,
        "change": "0.00135",
        "offercnt3": 16,
        "offercnt4": 21,
        "diff": "0.20",
        "offercnt1": 2,
        "offercnt2": 13,
        "volume": 18844,
        "bid": 220,
        "offercnt": 68,
        "bidcnt": 86,
        "open": "0.67510"
    }
}
```

---

## 🏷️ 해외선물옵션 관심종목 조회 (o3127)
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
| Element       | 한글명           | type         | Required   | Length   | Description      |
|:--------------|:--------------|:-------------|:-----------|:---------|:-----------------|
| o3127InBlock  | o3127InBlock  | Object       | Y          | -        |                  |
| -nrec         | 건수            | Number       | Y          | 4        |                  |
| o3127InBlock1 | o3127InBlock1 | Object Array | Y          | -        |                  |
| (Occurs)      | (Occurs)      |              |            |          |                  |
| -mktgb        | 기본입력          | String       | Y          | 1        | ex) F(선물), O(옵션) |
| -symbol       | 종목심볼          | String       | Y          | 16       | ex) 2ESF16_1915  |


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
| o3127OutBlock | o3127OutBlock | Object Array | Y          | -        |               |
| (Occurs)      | (Occurs)      |              |            |          |               |
| -symbol       | 종목코드          | String       | Y          | 16       |               |
| -symbolname   | 종목명           | String       | Y          | 50       |               |
| -price        | 현재가           | Number       | Y          | 15.9     |               |
| -sign         | 전일대비구분        | String       | Y          | 1        |               |
| -change       | 전일대비          | Number       | Y          | 15.9     |               |
| -diff         | 등락율           | Number       | Y          | 6.2      |               |
| -volume       | 누적거래량         | Number       | Y          | 10       |               |
| -jnilclose    | 전일종가          | Number       | Y          | 15.9     |               |
| -open         | 시가            | Number       | Y          | 15.9     |               |
| -high         | 고가            | Number       | Y          | 15.9     |               |
| -low          | 저가            | Number       | Y          | 15.9     |               |
| -offerho1     | 매도호가1         | Number       | Y          | 15.9     |               |
| -bidho1       | 매수호가1         | Number       | Y          | 15.9     |               |
| -offercnt1    | 매도호가건수1       | Number       | Y          | 10       |               |
| -bidcnt1      | 매수호가건수1       | Number       | Y          | 10       |               |
| -offerrem1    | 매도호가수량1       | Number       | Y          | 10       |               |
| -bidrem1      | 매수호가수량1       | Number       | Y          | 10       |               |
| -offercnt     | 매도호가건수합       | Number       | Y          | 10       |               |
| -bidcnt       | 매수호가건수합       | Number       | Y          | 10       |               |
| -offer        | 매도호가수량합       | Number       | Y          | 10       |               |
| -bid          | 매수호가수량합       | Number       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3127InBlock": {
    "nrec": 20
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3127OutBlock": [
        {
            "symbol": "",
            "change": "0",
            "jnilclose": "0",
            "offerrem1": 0,
            "sign": "",
            "diff": "0",
            "offercnt1": 0,
            "symbolname": "",
            "volume": 0,
            "offer": 0,
            "high": "0",
            "bidrem1": 0,
            "low": "0",
            "price": "0",
            "bidcnt1": 0,
            "bidho1": "0",
            "bid": 0,
            "offercnt": 0,
            "bidcnt": 0,
            "open": "0",
            "offerho1": "0"
        }
    ],
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물옵션 차트 일주월 조회 (o3128)
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
| Element      | 한글명          | type   | Required   | Length   | Description           |
|:-------------|:-------------|:-------|:-----------|:---------|:----------------------|
| o3128InBlock | o3128InBlock | Object | Y          | -        |                       |
| -mktgb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션)      |
| -shcode      | 단축코드         | String | Y          | 16       | ex) ADU13,2ESF16_1915 |
| -gubun       | 주기구분         | String | Y          | 1        | ex) 0(일), 1(주), 2(월)  |
| -qrycnt      | 요청건수         | Number | Y          | 4        |                       |
| -sdate       | 시작일자         | String | Y          | 8        |                       |
| -edate       | 종료일자         | String | Y          | 8        | ex) 조회당일              |
| -cts_date    | 연속일자         | String | Y          | 8        |                       |


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
| o3128OutBlock  | o3128OutBlock  | Object       | Y          | -        |               |
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
| o3128OutBlock1 | o3128OutBlock1 | Object Array | Y          | -        |               |
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
  "o3128InBlock": {
    "mktgb": "F",
    "shcode": "ADM23",
    "gubun": "1",
    "qrycnt": 20,
    "sdate": "20230525",
    "edate": "20230609",
    "cts_date": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3128OutBlock": {
        "cts_date": "00000000",
        "shcode": "ADM23",
        "jivolume": 0,
        "mk_etime": "160000",
        "jisiga": "0",
        "jilow": "0",
        "diclose": "0.67670",
        "disiga": "0.67510",
        "dihigh": "0.67680",
        "jihigh": "0",
        "rec_count": 6,
        "dilow": "0.67395",
        "mk_stime": "170000",
        "jiclose": "0"
    },
    "rsp_msg": "조회완료",
    "o3128OutBlock1": [
        {
            "date": "20230505",
            "volume": 412248,
            "high": "0.67675",
            "low": "0.66215",
            "close": "0.67660",
            "open": "0.66300"
        }
    ]
}
```

---

## 🏷️ 해외선물옵션 시간대별 Tick 체결 조회 (o3136)
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
| o3136InBlock | o3136InBlock | Object | Y          | -        |                  |
| -gubun       | 조회구분         | String | Y          | 1        | ex) 0(당일), 1(전일) |
| -mktgb       | 시장구분         | String | Y          | 1        | ex) F(선물), O(옵션) |
| -shcode      | 단축코드         | String | Y          | 16       | ex) 2ESF16_1915  |
| -readcnt     | 조회갯수         | Number | Y          | 4        |                  |
| -cts_seq     | 순번CTS        | Number | Y          | 8        |                  |


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
| o3136OutBlock  | o3136OutBlock  | Object       | Y          | -        |               |
| -cts_seq       | 순번CTS          | Number       | Y          | 8        |               |
| o3136OutBlock1 | o3136OutBlock1 | Object Array | Y          | -        |               |
| (Occurs)       | (Occurs)       |              |            |          |               |
| -ovsdate       | 현지일자           | String       | Y          | 8        |               |
| -ovstime       | 현지시간           | String       | Y          | 6        |               |
| -price         | 현재가            | Number       | Y          | 15.9     |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 15.9     |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -cvolume       | 체결수량           | Number       | Y          | 10       |               |
| -volume        | 누적거래량          | Number       | Y          | 10       |               |


### 💡 Request Example
```json
{
  "o3136InBlock": {
    "gubun": "0",
    "mktgb": "F",
    "shcode": "ADM23",
    "readcnt": 20,
    "cts_seq": 0
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "o3136OutBlock1": [
        {
            "volume": 18844,
            "ovstime": "000533",
            "price": "0.67670",
            "change": "0.00135",
            "sign": "2",
            "ovsdate": "20230613",
            "diff": "0.20",
            "cvolume": 1
        },
        {
            "volume": 18771,
            "ovstime": "000438",
            "price": "0.67665",
            "change": "0.00130",
            "sign": "2",
            "ovsdate": "20230613",
            "diff": "0.19",
            "cvolume": 1
        }
    ],
    "o3136OutBlock": {
        "cts_seq": 4826
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외선물옵션 차트 NTick 체결 조회 (o3137)
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
| o3137InBlock | o3137InBlock | Object | Y          | -        |                  |
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
| o3137OutBlock  | o3137OutBlock  | Object       | Y          | -        |               |
| -shcode        | 단축코드           | String       | Y          | 16       |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| -cts_seq       | 연속시간           | String       | Y          | 10       |               |
| -cts_daygb     | 연속당일구분         | String       | Y          | 2        |               |
| o3137OutBlock1 | o3137OutBlock1 | Object Array | Y          | -        |               |
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
  "o3137InBlock": {
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
    "rsp_cd": "00000",
    "rsp_msg": "조회완료",
    "o3137OutBlock": {
        "shcode": null,
        "rec_count": null,
        "cts_daygb": null,
        "cts_seq": null
    },
    "o3137OutBlock1": [
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
