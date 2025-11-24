# REST[선물/옵션] 기타
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=2f1eea77-5606-4512-93c6-31b21d2ece90&api_id=98373ce4-042a-4fc8-85ef-b9b8f64101ce

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /futureoption/etc                 |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 파생증거금율에 대해 확인할 수 있습니다.            |


## 🏷️ 파생상품증거금율조회 (MMDAQ91200)
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
| MMDAQ91200InBlock1 | MMDAQ91200InBlock1 | Object | Y          | -        |               |
| -IsuLgclssCode     | 종목대분류코드            | String | Y          | 2        |               |
| -IsuMdclssCode     | 종목중분류코드            | String | Y          | 2        |               |


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
| MMDAQ91200OutBlock1 | MMDAQ91200OutBlock1 | Object       | Y          | -        |               |
| -RecCnt             | 레코드갯수               | Number       | Y          | 5        |               |
| -IsuLgclssCode      | 종목대분류코드             | String       | Y          | 2        |               |
| -IsuMdclssCode      | 종목중분류코드             | String       | Y          | 2        |               |
| MMDAQ91200OutBlock2 | MMDAQ91200OutBlock2 | Object Array | Y          | -        |               |
| -IsuSmclssCode      | 종목소분류코드             | String       | Y          | 3        |               |
| -IsuMdclssCode      | 종목중분류코드             | String       | Y          | 2        |               |
| -IsuLrgMdclssNm     | 종목대중분류명             | String       | Y          | 40       |               |
| -IsuLrgMidSmclssNm  | 종목대중소분류명            | String       | Y          | 40       |               |
| -ShtnHanglIsuNm     | 단축한글종목명             | String       | Y          | 40       |               |
| -CsgnMgnrt          | 위탁증거금율              | Number       | Y          | 26.9     |               |
| -MaintMgnrt         | 유지증거금율              | Number       | Y          | 26.9     |               |
| -MnyMgnrt           | 현금증거금율              | Number       | Y          | 26.9     |               |
| -RmndDays           | 잔여일수                | Number       | Y          | 6        |               |
| -OnePrcntrOrdMgn    | 1계약당주문증거금           | Number       | Y          | 17       |               |


### 💡 Request Example
```json
{
  "MMDAQ91200InBlock1": {
    "RecCnt": 1,
    "IsuLgclssCode": "",
    "IsuMdclssCode": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00133",
    "MMDAQ91200OutBlock1": {
        "IsuLgclssCode": "",
        "IsuMdclssCode": "00",
        "RecCnt": 1
    },
    "MMDAQ91200OutBlock2": [
        {
            "IsuSmclssCode": "501",
            "IsuMdclssCode": "01",
            "MnyMgnrt": "+000000000000003.900000000",
            "OnePrcntrOrdMgn": 6559020,
            "MaintMgnrt": "+000000000000005.200000000",
            "RmndDays": 999999,
            "IsuLrgMidSmclssNm": "옵션_지수옵션_KOSPI200",
            "ShtnHanglIsuNm": "KOSPI200",
            "IsuLrgMdclssNm": "지수옵션",
            "CsgnMgnrt": "+000000000000007.800000000"
        },
        {
            "IsuSmclssCode": "5C8",
            "IsuMdclssCode": "02",
            "MnyMgnrt": "+000000000000008.100000000",
            "OnePrcntrOrdMgn": 174636,
            "MaintMgnrt": "+000000000000010.800000000",
            "RmndDays": 999999,
            "IsuLrgMidSmclssNm": "옵션_주식옵션_삼성물산",
            "ShtnHanglIsuNm": "삼성물산",
            "IsuLrgMdclssNm": "주식옵션",
            "CsgnMgnrt": "+000000000000016.200000000"
        }
    ],
    "rsp_msg": "조회가 계속 됩니다. 계속하시려면 연속버튼을 누르십시오."
}
```

---
