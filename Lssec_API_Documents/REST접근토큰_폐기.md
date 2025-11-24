# REST접근토큰 폐기
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=ffd2def7-a118-40f7-a0ab-cd4c6a538a90&api_id=2d923333-f816-4df9-932d-ad390437b66f

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /oauth2/revoke                    |
| Format       |                                   |
| Content-Type | application/x-www-form-urlencoded |
| Description  | 발급받은 접근토큰을 더 이상  활용하지 않을 때 사용합니다. |


## 🏷️ 접근토큰 폐기 (revoke)
### 요청 Header
| Element      | 한글명   | type   | Required   |   Length | Description                                                            |
|:-------------|:------|:-------|:-----------|---------:|:-----------------------------------------------------------------------|
| content-type | 컨텐츠타입 | String | Y          |      100 | OAuth2 호출 Request Body 데이터 포맷으로 "application/x-www-form-urlencoded 설정" |


### 요청 Body
| Element         | 한글명        | type   | Required   |   Length | Description                       |
|:----------------|:-----------|:-------|:-----------|---------:|:----------------------------------|
| appkey          | 고객 앱Key    | String | Y          |      100 | 포탈에서 발급된 고객의 앱Key                 |
| appsecretkey    | 고객 앱 비밀Key | String | Y          |       36 | 포탈에서 발급된 고객의 앱 비밀Key              |
| token_type_hint | 토큰 유형 hint | String | Y          |       36 | access_token, refresh_token 토큰 타입 |
| token           | 접근토큰       | String | Y          |      256 | G/W 에서 발급하는 접근토큰                  |


### 응답 Header
| Element      | 한글명   | type   | Required   |   Length | Description                                                           |
|:-------------|:------|:-------|:-----------|---------:|:----------------------------------------------------------------------|
| content-type | 컨텐츠타입 | String | Y          |      100 | OAuth2 응답 Response Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |


### 응답 Body
| Element   | 한글명   | type   | Required   |   Length | Description   |
|:----------|:------|:-------|:-----------|---------:|:--------------|
| code      | 응답코드  | String | Y          |        3 |               |
| message   | 응답메시지 | String | Y          |      100 | 응답메시지         |


### 💡 Request Example
```json
appkey=PSd7orrAJnAfr202g4MpbzVxwqPBjjkvjLf2&appsecretkey=puQoMSRYZwOHt8goiEHbOazdBqLRUyYA&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6ImZhNDQ5NzBmLTVjNmQtNGNlZi1iNTc4LTVhNjViZjBiOTE1YyIsIm5iZiI6MTY4NjYyODQwMSwiZ3JhbnRfdHlwZSI6IkNsaWVudCIsImlzcyI6InVub2d3IiwiZXhwIjoxNjg2NjkzNjAxLCJpYXQiOjE2ODY2Mjg0MDEsImp0aSI6IlBTZDdvcnJBSm5BZnIyMDJnNE1wYnpWeHdxUEJqamt2akxmMiJ9.tP3WswPL-FAGdJBTVn6geHALK90i2zRQWZpqPIHRK09SOiP_sd8qJZeosoXFqZdfTqisXlAgwOjXcSvAR0V0lg&token_type_hint=access_token
```

### 💡 Response Example
```json
{
    "code": 200,
    "message": "접근토큰 폐기에 성공하였습니다."
}
```

---
