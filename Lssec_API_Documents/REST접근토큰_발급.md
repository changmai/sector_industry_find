# REST접근토큰 발급
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=ffd2def7-a118-40f7-a0ab-cd4c6a538a90&api_id=33bd887a-6652-4209-88cd-5324bc7c5e36

## 📌 기본 정보
| 항목           | 내용                                              |
|:-------------|:------------------------------------------------|
| Method       | POST                                            |
| Domain       | https://openapi.ls-sec.co.kr:8080               |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080               |
| 모의투자 도메인     |                                                 |
| URL          | /oauth2/token                                   |
| Format       |                                                 |
| Content-Type | application/x-www-form-urlencoded               |
| Description  | 본인을 인증하는 확인 절차로, 접근 토큰을 부여받아 오픈 API  활용이 가능합니다. |


## 🏷️ 접근토큰 발급 (token)
### 요청 Header
| Element      | 한글명   | type   | Required   |   Length | Description                                                            |
|:-------------|:------|:-------|:-----------|---------:|:-----------------------------------------------------------------------|
| content-type | 컨텐츠타입 | String | Y          |      100 | OAuth2 호출 Request Body 데이터 포맷으로 "application/x-www-form-urlencoded 설정" |


### 요청 Body
| Element      | 한글명        | type   | Required   |   Length | Description             |
|:-------------|:-----------|:-------|:-----------|---------:|:------------------------|
| grant_type   | 권한부여  Type | String | Y          |      100 | "client_credentials" 고정 |
| appkey       | 고객 앱Key    | String | Y          |       36 | 포탈에서 발급된 고객의 앱Key       |
| appsecretkey | 고객 앱 비밀Key | String | Y          |       36 | 포탈에서 발급된 고객의 앱 비밀Key    |
| scope        | scope      | String | Y          |      256 | "oob" 고정                |


### 응답 Header
| Element      | 한글명   | type   | Required   |   Length | Description                                                           |
|:-------------|:------|:-------|:-----------|---------:|:----------------------------------------------------------------------|
| content-type | 컨텐츠타입 | String | Y          |      100 | OAuth2 응답 Response Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |


### 응답 Body
| Element      | 한글명       | type   | Required   |   Length | Description      |
|:-------------|:----------|:-------|:-----------|---------:|:-----------------|
| access_token | 접근토큰      | String | Y          |     1000 | G/W 에서 발급하는 접근토큰 |
| expire_in    | 접근토큰 유효기간 | String | Y          |       10 | 유효기간(초)          |
| scope        | scope     | String | Y          |      256 | "oob" 고정         |
| token_type   | 토큰 유형     | String | Y          |      256 | Bearer           |


### 💡 Request Example
```json
appkey=BSrTOOZNoXtxt8CnaiSo1qPfzCoc0WgfP2vu&appsecretkey=d3HloL6TO7RKMVdEqf5Nhw2dnzUFAQwq&grant_type=client_credentials&scope=oob
```

### 💡 Response Example
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6IjVjNDQ0ZjI2LWZhYzUtNGJjMS1hNDhkLWMzYmI1MTg5NzM4MSIsIm5iZiI6MTY4NjYyODE1NiwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NzE0NTU2LCJpYXQiOjE2ODY2MjgxNTYsImp0aSI6IkJTclRPT1pOb1h0eHQ4Q25haVNvMXFQZnpDb2MwV2dmUDJ2dSJ9.R3M9o8u0oHg4U9uQ5YFv7cAu0JA-1V7brnkdmmmbkeRi2RM695vIgcuHnTEy5JONSLaRdKCF5L9tCYBduKRjAA",
    "scope": "oob",
    "token_type": "Bearer",
    "expires_in": 86400
}
```

---
