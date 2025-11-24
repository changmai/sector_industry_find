# REST[기타] 시간조회
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=6ad419a5-f0ce-47c2-a52a-91685fa86a31&api_id=3c452f0d-715e-43b5-a140-3e26f73dec76

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /etc/time-search                  |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | 현재 시간조회가 가능합니다.                   |


## 🏷️ 서버시간조회 (t0167)
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
| t0167InBlock | t0167InBlock | Object | Y          | -        |               |
| -id          | id           | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element       | 한글명              | type   | Required   | Length   | Description   |
|:--------------|:-----------------|:-------|:-----------|:---------|:--------------|
| t0167OutBlock | t0167OutBlock    | Object | Y          | -        |               |
| -dt           | 일자(YYYYMMDD)     | String | Y          | 8        |               |
| -time         | 시간(HHMMSSssssss) | String | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t0167InBlock": {
    "id": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t0167OutBlock": {
        "dt": "20230605",
        "time": "102652926435"
    },
    "rsp_msg": "조회완료"
}
```

---
