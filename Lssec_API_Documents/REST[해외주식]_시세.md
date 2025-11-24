# REST[해외주식] 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=cdb7e1bc-f7c5-425c-8248-aa83dbb6919f&api_id=06f2b1bc-7f44-4368-a564-207658af552d

## 📌 기본 정보
| 항목           | 내용                                       |
|:-------------|:-----------------------------------------|
| Method       | POST                                     |
| Domain       | https://openapi.ls-sec.co.kr:8080        |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080        |
| 모의투자 도메인     |                                          |
| URL          | /overseas-stock/market-data              |
| Format       | JSON                                     |
| Content-Type | application/json; charset=UTF-8          |
| Description  | 해외주식 종목별 시세 및 차트 등 시세관련 데이터를 확인할 수 있습니다. |


## 🏷️ 해외주식 API 현재가 조회 (g3101)
### 요청 Header
| Element       | 한글명     | type   | Required   |   Length | Description                                                                     |
|:--------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰    | String | Y          |     1000 | OAuth토큰이필요한API경우발급한AccessToken을설정하기위한RequestHeaederParameter                    |
| tr_cd         | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont       | 연속거래여부  | String | Y          |        1 | 연속거래여부 Y:연속○ N:연속×                                                              |
| tr_cont_key   | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |
| mac_address   | MAC주소   | String | Y          |       12 | 법인인경우필수세팅                                                                       |


### 요청 Body
| Element       | 한글명          | type   | Required   | Length   | Description           |
|:--------------|:-------------|:-------|:-----------|:---------|:----------------------|
| -g3101InBlock | g3101InBlock | Object | Y          | -        |                       |
| -delaygb      | 지연구분         | String | Y          | 1        | R                     |
| -keysymbol    | KEY종목코드      | String | Y          | 18       | ex)82TSLA             |
| -exchcd       | 거래소코드        | String | Y          | 2        | 81 : 뉴욕/아멕스, 82 : 나스닥 |
| -symbol       | 종목코드         | String | Y          | 16       | ex)TSLA               |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부 Y:연속○ N:연속×                                                              |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element        | 한글명           | type   | Required   | Length   | Description           |
|:---------------|:--------------|:-------|:-----------|:---------|:----------------------|
| -g3101OutBlock | g3101OutBlock | Object | Y          | -        |                       |
| -delaygb       | 지연구분          | String | Y          | 1        | R                     |
| -keysymbol     | KEY종목코드       | String | Y          | 18       | ex)82TSLA             |
| -exchcd        | 거래소코드         | String | Y          | 2        | 81 : 뉴욕/아멕스, 82 : 나스닥 |
| -exchange      | 거래소ID         | String | Y          | 4        | 81 : 뉴욕/아멕스, 82 : 나스닥 |
| -suspend       | 거래상태          | String | Y          | 1        | Y:정지 N: 보통            |
| -sellonly      | 매매구분          | String | Y          | 1        | 0:매매가능1:매도만가능2:매매불가   |
| -symbol        | 종목코드          | String | Y          | 16       |                       |
| -korname       | 한글종목명         | String | Y          | 64       |                       |
| -induname      | 업종한글명         | String | Y          | 40       |                       |
| -low52p        | 52주최저가        | Number | Y          | 15.6     |                       |
| -floatpoint    | 소숫점자릿수        | String | Y          | 1        |                       |
| -currency      | 외환코드          | String | Y          | 4        |                       |
| -price         | 현재가           | Number | Y          | 15.6     |                       |
| -sign          | 전일대비구분        | String | Y          | 1        |                       |
| -diff          | 전일대비          | Number | Y          | 15.6     |                       |
| -rate          | 등락률           | Number | Y          | 6.2      |                       |
| -volume        | 거래량           | Number | Y          | 16       |                       |
| -amount        | 거래대금          | Number | Y          | 15       |                       |
| -high52p       | 52주최고가        | Number | Y          | 15.6     |                       |
| -uplimit       | 상한가           | Number | Y          | 15.6     |                       |
| -dnlimit       | 하한가           | Number | Y          | 15.6     |                       |
| -open          | 시가            | Number | Y          | 15.6     |                       |
| -high          | 고가            | Number | Y          | 15.6     |                       |
| -low           | 저가            | Number | Y          | 15.6     |                       |
| -perv          | PER           | Number | Y          | 9.2      |                       |
| -epsv          | EPS           | Number | Y          | 9.2      |                       |


### 💡 Request Example
```json
{
  "g3101InBlock": {
    "delaygb": "R",
    "keysymbol": "82TSLA",
    "exchcd": "82",
    "symbol": "TSLA"
  }
}
```

### 💡 Response Example
```json
{
	"g3101OutBlock": {
		"delaygb": "R",
		"keysymbol": "82TSLA",
		"exchcd": "82",
		"exchange": "0537",
		"suspend": "N",
		"sellonly": 0,
		"symbol": "TSLA",
		"korname": "테슬라",
		"induname": "자동차 및 부품",
		"floatpoint": "4",
		"currency": "USD",
		"price": "283.8200",
		"sign": "5",
		"diff": "1.1300",
		"rate": "-0.40",
		"volume": 414175,
		"amount": 117236758,
		"high52p": "488.5399",
		"low52p": "166.3700",
		"uplimit": "0.0000",
		"dnlimit": "0.0000",
		"open": "285.0900",
		"high": "285.3100",
		"low": "281.8400",
		"perv": "142.71",
		"epsv": "1.82"
	},
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외주식 API 시간대별 (g3102)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description                                                                     |
|:--------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| authorization | 접근토큰      | String | Y          |     1000 | OAuth 토큰이 필요한 API 경우 발급한 Access Token을 설정하기 위한 Request Heaeder Parameter        |
| tr_cd         | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부 Y:연속○ N:연속×                                                             |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |
| mac_address   | MAC 주소    | String | Y          |       12 | 법인인 경우 필수 세팅                                                                    |


### 요청 Body
| Element      | 한글명          | type   | Required   | Length   | Description           |
|:-------------|:-------------|:-------|:-----------|:---------|:----------------------|
| g3102InBlock | g3102InBlock | Object | Y          | -        |                       |
| -delaygb     | 지연구분         | String | Y          | 1        | R                     |
| -keysymbol   | KEY종목코드      | String | Y          | 18       | ex) 82TSLA            |
| -exchcd      | 거래소코드        | String | Y          | 2        | 81 : 뉴욕/아멕스, 82 : 나스닥 |
| -readcnt     | 조회갯수         | Number | Y          | 4        |                       |
| -cts_seq     | 연속시퀀스        | Number | Y          | 17       |                       |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부 Y:연속○ N:연속×                                                             |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description   |
|:---------------|:---------------|:-------------|:-----------|:---------|:--------------|
| g3102OutBlock  | g3102OutBlock  | Object       | Y          | -        |               |
| -delaygb       | 지연구분           | String       | Y          | 1        |               |
| -keysymbol     | KEY종목코드        | String       | Y          | 18       |               |
| -exchcd        | 거래소코드          | String       | Y          | 2        |               |
| -symbol        | 종목코드           | String       | Y          | 16       |               |
| -cts_seq       | 연속시퀀스          | Number       | Y          | 17       |               |
| -rec_count     | 레코드카운트         | Number       | Y          | 7        |               |
| g3102OutBlock1 | g3102OutBlock1 | Object Array | Y          | -        |               |
| -locdate       | 현지일자           | String       | Y          | 8        |               |
| -loctime       | 현지시간           | String       | Y          | 6        |               |
| -kordate       | 한국일자           | String       | Y          | 8        |               |
| -kortime       | 한국시간           | String       | Y          | 6        |               |
| -price         | 현재가            | Number       | Y          | 15.6     |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -diff          | 전일대비           | Number       | Y          | 15.6     |               |
| -rate          | 등락률            | Number       | Y          | 6.2      |               |
| -open          | 시가             | Number       | Y          | 15.6     |               |
| -high          | 고가             | Number       | Y          | 15.6     |               |
| -low           | 저가             | Number       | Y          | 15.6     |               |
| -exevol        | 체결량            | Number       | Y          | 10       |               |
| -cgubun        | 체결구분           | String       | Y          | 1        |               |
| -floatpoint    | 소숫점자릿수         | String       | Y          | 1        |               |


### 💡 Request Example
```json
{
  "g3102InBlock": {
    "delaygb": "R",
    "keysymbol": "82TSLA",
    "exchcd": "82",
    "symbol": "TSLA",
    "readcnt": 30,
    "cts_seq": 0
  }
}
```

### 💡 Response Example
```json
{
	"g3102OutBlock": {
		"delaygb": "R",
		"keysymbol": "82TSLA",
		"exchcd": "82",
		"symbol": "TSLA",
		"cts_seq": 20250428014018000,
		"rec_count": 30
	},
	"g3102OutBlock1": [
		{
			"locdate": "20250428",
			"loctime": "014101",
			"kordate": "20250428",
			"kortime": "144101",
			"price": "283.9500",
			"sign": "5",
			"diff": "1.0000",
			"rate": "-0.35",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 20,
			"cgubun": "-",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014101",
			"kordate": "20250428",
			"kortime": "144101",
			"price": "283.9900",
			"sign": "5",
			"diff": "0.9600",
			"rate": "-0.34",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 1,
			"cgubun": "-",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014055",
			"kordate": "20250428",
			"kortime": "144055",
			"price": "284.0000",
			"sign": "5",
			"diff": "0.9500",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 10,
			"cgubun": "-",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014055",
			"kordate": "20250428",
			"kortime": "144055",
			"price": "284.0300",
			"sign": "5",
			"diff": "0.9200",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 66,
			"cgubun": "-",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014050",
			"kordate": "20250428",
			"kortime": "144050",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 40,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014048",
			"kordate": "20250428",
			"kortime": "144048",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 1,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014044",
			"kordate": "20250428",
			"kortime": "144044",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014044",
			"kordate": "20250428",
			"kortime": "144044",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014043",
			"kordate": "20250428",
			"kortime": "144043",
			"price": "284.0300",
			"sign": "5",
			"diff": "0.9200",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 200,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014042",
			"kordate": "20250428",
			"kortime": "144042",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014039",
			"kordate": "20250428",
			"kortime": "144039",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 20,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014032",
			"kordate": "20250428",
			"kortime": "144032",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014032",
			"kordate": "20250428",
			"kortime": "144032",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 38,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014032",
			"kordate": "20250428",
			"kortime": "144032",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 20,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014032",
			"kordate": "20250428",
			"kortime": "144032",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 22,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014029",
			"kordate": "20250428",
			"kortime": "144029",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014029",
			"kordate": "20250428",
			"kortime": "144029",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 200,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014023",
			"kordate": "20250428",
			"kortime": "144023",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 20,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014022",
			"kordate": "20250428",
			"kortime": "144022",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014021",
			"kordate": "20250428",
			"kortime": "144021",
			"price": "284.0500",
			"sign": "5",
			"diff": "0.9000",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 80,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014021",
			"kordate": "20250428",
			"kortime": "144021",
			"price": "284.0200",
			"sign": "5",
			"diff": "0.9300",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 17,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014021",
			"kordate": "20250428",
			"kortime": "144021",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 20,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014021",
			"kordate": "20250428",
			"kortime": "144021",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 40,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014020",
			"kordate": "20250428",
			"kortime": "144020",
			"price": "284.0100",
			"sign": "5",
			"diff": "0.9400",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 2,
			"cgubun": "-",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014019",
			"kordate": "20250428",
			"kortime": "144019",
			"price": "284.0400",
			"sign": "5",
			"diff": "0.9100",
			"rate": "-0.32",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 50,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014018",
			"kordate": "20250428",
			"kortime": "144018",
			"price": "284.0000",
			"sign": "5",
			"diff": "0.9500",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 14,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014018",
			"kordate": "20250428",
			"kortime": "144018",
			"price": "284.0000",
			"sign": "5",
			"diff": "0.9500",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 36,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014018",
			"kordate": "20250428",
			"kortime": "144018",
			"price": "284.0000",
			"sign": "5",
			"diff": "0.9500",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 3,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014018",
			"kordate": "20250428",
			"kortime": "144018",
			"price": "284.0000",
			"sign": "5",
			"diff": "0.9500",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 20,
			"cgubun": "+",
			"floatpoint": "4"
		},
		{
			"locdate": "20250428",
			"loctime": "014018",
			"kordate": "20250428",
			"kortime": "144018",
			"price": "284.0000",
			"sign": "5",
			"diff": "0.9500",
			"rate": "-0.33",
			"open": "285.0900",
			"high": "285.3100",
			"low": "281.8400",
			"exevol": 10,
			"cgubun": "+",
			"floatpoint": "4"
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외주식 API 종목정보 조회 (g3104)
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
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| g3104InBlock | g3104InBlock | Object | Y          | -        |               |
| -delaygb     | 지연구분         | String | Y          | 1        |               |
| -keysymbol   | KEY종목코드      | String | Y          | 18       |               |
| -exchcd      | 거래소코드        | String | Y          | 2        |               |
| -symbol      | 종목코드         | String | Y          | 16       |               |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element        | 한글명           | type   | Required   | Length   | Description   |
|:---------------|:--------------|:-------|:-----------|:---------|:--------------|
| g3104OutBlock  | g3104OutBlock | Object | Y          | -        |               |
| -delaygb       | 지연구분          | String | Y          | 1        |               |
| -keysymbol     | KEY종목코드       | String | Y          | 18       |               |
| -exchcd        | 거래소코드         | String | Y          | 2        |               |
| -exchange      | 거래소ID         | String | Y          | 4        |               |
| -symbol        | 종목코드          | String | Y          | 16       |               |
| -korname       | 한글종목명         | String | Y          | 64       |               |
| -engname       | 영문종목명         | String | Y          | 64       |               |
| -exchange_name | 거래소명          | String | Y          | 16       |               |
| -nation_name   | 국가명           | String | Y          | 16       |               |
| -induname      | 업종명           | String | Y          | 40       |               |
| -instname      | 증권종류          | String | Y          | 16       |               |
| -floatpoint    | 소숫점자릿수        | String | Y          | 1        |               |
| -currency      | 거래통화          | String | Y          | 4        |               |
| -suspend       | 거래상태          | String | Y          | 1        |               |
| -sellonly      | 매매구분          | String | Y          | 1        |               |
| -share         | 발행주식수         | Number | Y          | 16       |               |
| -untprc        | 호가단위          | Number | Y          | 15.6     |               |
| -bidlotsize    | 매수주문단위        | String | Y          | 4        |               |
| -asklotsize    | 매도주문단위        | String | Y          | 4        |               |
| -volume        | 거래량           | Number | Y          | 16       |               |
| -amount        | 거래대금          | Number | Y          | 16       |               |
| -pcls          | 전일종가          | Number | Y          | 15.6     |               |
| -clos          | 기준가           | Number | Y          | 15.6     |               |
| -open          | 시가            | Number | Y          | 15.6     |               |
| -high          | 고가            | Number | Y          | 15.6     |               |
| -low           | 저가            | Number | Y          | 15.6     |               |
| -high52p       | 52주고가         | Number | Y          | 15.6     |               |
| -low52p        | 52주저가         | Number | Y          | 15.6     |               |
| -shareprc      | 시가총액          | Number | Y          | 16       |               |
| -perv          | PER           | Number | Y          | 9.2      |               |
| -epsv          | EPS           | Number | Y          | 9.2      |               |
| -exrate        | 환율            | Number | Y          | 15.2     |               |
| -bidlotsize2   | 매수주문단위2       | String | Y          | 8        |               |
| -asklotsize2   | 매도주문단위2       | String | Y          | 8        |               |


### 💡 Request Example
```json
{
  "g3104InBlock": {
    "delaygb": "R",
    "keysymbol": "82TSLA",
    "exchcd": "82",
    "symbol": "TSLA"
  }
}
```

### 💡 Response Example
```json
{
	"g3104OutBlock": {
		"delaygb": "R",
		"keysymbol": "82TSLA",
		"exchcd": "82",
		"exchange": "0537",
		"symbol": "TSLA",
		"korname": "테슬라",
		"engname": "TESLA INC",
		"exchange_name": "나스닥",
		"nation_name": "미국",
		"induname": "자동차 및 부품",
		"instname": "주식",
		"floatpoint": "4",
		"currency": "USD",
		"suspend": "N",
		"sellonly": "0",
		"share": 3216520000,
		"untprc": "0.0100",
		"bidlotsize": "1",
		"asklotsize": "1",
		"volume": 419973,
		"amount": 118883113,
		"pcls": "284.9500",
		"clos": "284.9500",
		"open": "285.0900",
		"high": "285.3100",
		"low": "281.8400",
		"high52p": "488.5399",
		"low52p": "166.3700",
		"shareprc": 913170027999,
		"perv": "142.71",
		"epsv": "1.82",
		"exrate": "1434.60",
		"bidlotsize2": "1",
		"asklotsize2": "1"
	},
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외주식 API 현재가호가 조회 (g3106)
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
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| g3106InBlock | g3106InBlock | Object | Y          | -        |               |
| -delaygb     | 지연구분         | String | Y          | 1        |               |
| -keysymbol   | KEY종목코드      | String | Y          | 18       |               |
| -exchcd      | 거래소코드        | String | Y          | 2        |               |
| -symbol      | 종목코드         | String | Y          | 16       |               |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element       | 한글명           | type   | Required   | Length   | Description   |
|:--------------|:--------------|:-------|:-----------|:---------|:--------------|
| g3106OutBlock | g3106OutBlock | Object | Y          | -        |               |
| -delaygb      | 지연구분          | String | Y          | 1        |               |
| -keysymbol    | KEY종목코드       | String | Y          | 18       |               |
| -exchcd       | 거래소코드         | String | Y          | 2        |               |
| -symbol       | 종목코드          | String | Y          | 16       |               |
| -korname      | 한글종목명         | String | Y          | 64       |               |
| -price        | 현재가           | Number | Y          | 15.6     |               |
| -floatpoint   | 소숫점자릿수        | String | Y          | 1        |               |
| -sign         | 전일대비구분        | String | Y          | 1        |               |
| -diff         | 전일대비          | Number | Y          | 15.6     |               |
| -rate         | 등락률           | Number | Y          | 6.2      |               |
| -volume       | 누적거래량         | Number | Y          | 16       |               |
| -amount       | 누적거래대금        | Number | Y          | 15       |               |
| -jnilclose    | 전일종가          | Number | Y          | 15.6     |               |
| -open         | 시가            | Number | Y          | 15.6     |               |
| -high         | 고가            | Number | Y          | 15.6     |               |
| -low          | 저가            | Number | Y          | 15.6     |               |
| -hotime       | 호가수신시간        | String | Y          | 6        |               |
| -offerho1     | 매도호가1         | Number | Y          | 15.6     |               |
| -bidho1       | 매수호가1         | Number | Y          | 15.6     |               |
| -offercnt1    | 매도호가건수1       | String | Y          | 10       |               |
| -bidcnt1      | 매수호가건수1       | String | Y          | 10       |               |
| -offerrem1    | 매도호가잔량1       | Number | Y          | 10       |               |
| -bidrem1      | 매수호가잔량1       | Number | Y          | 10       |               |
| -offerho2     | 매도호가2         | Number | Y          | 15.6     |               |
| -bidho2       | 매수호가2         | Number | Y          | 15.6     |               |
| -offercnt2    | 매도호가건수2       | String | Y          | 10       |               |
| -bidcnt2      | 매수호가건수2       | String | Y          | 10       |               |
| -offerrem2    | 매도호가잔량2       | Number | Y          | 10       |               |
| -bidrem2      | 매수호가잔량2       | Number | Y          | 10       |               |
| -offerho3     | 매도호가3         | Number | Y          | 15.6     |               |
| -bidho3       | 매수호가3         | Number | Y          | 15.6     |               |
| -offercnt3    | 매도호가건수3       | String | Y          | 10       |               |
| -bidcnt3      | 매수호가건수3       | String | Y          | 10       |               |
| -offerrem3    | 매도호가잔량3       | Number | Y          | 10       |               |
| -bidrem3      | 매수호가잔량3       | Number | Y          | 10       |               |
| -offerho4     | 매도호가4         | Number | Y          | 15.6     |               |
| -bidho4       | 매수호가4         | Number | Y          | 15.6     |               |
| -offercnt4    | 매도호가건수4       | String | Y          | 10       |               |
| -bidcnt4      | 매수호가건수4       | String | Y          | 10       |               |
| -offerrem4    | 매도호가잔량4       | Number | Y          | 10       |               |
| -bidrem4      | 매수호가잔량4       | Number | Y          | 10       |               |
| -offerho5     | 매도호가5         | Number | Y          | 15.6     |               |
| -bidho5       | 매수호가5         | Number | Y          | 15.6     |               |
| -offercnt5    | 매도호가건수5       | String | Y          | 10       |               |
| -bidcnt5      | 매수호가건수5       | String | Y          | 10       |               |
| -offerrem5    | 매도호가잔량5       | Number | Y          | 10       |               |
| -bidrem5      | 매수호가잔량5       | Number | Y          | 10       |               |
| -offerho6     | 매도호가6         | Number | Y          | 15.6     |               |
| -bidho6       | 매수호가6         | Number | Y          | 15.6     |               |
| -offercnt6    | 매도호가건수6       | String | Y          | 10       |               |
| -bidcnt6      | 매수호가건수6       | String | Y          | 10       |               |
| -offerrem6    | 매도호가잔량6       | Number | Y          | 10       |               |
| -bidrem6      | 매수호가잔량6       | Number | Y          | 10       |               |
| -offerho7     | 매도호가7         | Number | Y          | 15.6     |               |
| -bidho7       | 매수호가7         | Number | Y          | 15.6     |               |
| -offercnt7    | 매도호가건수7       | String | Y          | 10       |               |
| -bidcnt7      | 매수호가건수7       | String | Y          | 10       |               |
| -offerrem7    | 매도호가잔량7       | Number | Y          | 10       |               |
| -bidrem7      | 매수호가잔량7       | Number | Y          | 10       |               |
| -offerho8     | 매도호가8         | Number | Y          | 15.6     |               |
| -bidho8       | 매수호가8         | Number | Y          | 15.6     |               |
| -offercnt8    | 매도호가건수8       | String | Y          | 10       |               |
| -bidcnt8      | 매수호가건수8       | String | Y          | 10       |               |
| -offerrem8    | 매도호가잔량8       | Number | Y          | 10       |               |
| -bidrem8      | 매수호가잔량8       | Number | Y          | 10       |               |
| -offerho9     | 매도호가9         | Number | Y          | 15.6     |               |
| -bidho9       | 매수호가9         | Number | Y          | 15.6     |               |
| -offercnt9    | 매도호가건수9       | String | Y          | 10       |               |
| -bidcnt9      | 매수호가건수9       | String | Y          | 10       |               |
| -offerrem9    | 매도호가잔량9       | Number | Y          | 10       |               |
| -bidrem9      | 매수호가잔량9       | Number | Y          | 10       |               |
| -offerho10    | 매도호가10        | Number | Y          | 15.6     |               |
| -bidho10      | 매수호가10        | Number | Y          | 15.6     |               |
| -offercnt10   | 매도호가건수10      | String | Y          | 10       |               |
| -bidcnt10     | 매수호가건수10      | String | Y          | 10       |               |
| -offerrem10   | 매도호가잔량10      | Number | Y          | 10       |               |
| -bidrem10     | 매수호가잔량10      | Number | Y          | 10       |               |
| -offercnt     | 매도호가건수합       | String | Y          | 10       |               |
| -bidcnt       | 매수호가건수합       | String | Y          | 10       |               |
| -offer        | 매도호가잔량합       | Number | Y          | 10       |               |
| -bid          | 매수호가잔량합       | Number | Y          | 10       |               |


### 💡 Request Example
```json
{
  "g3106InBlock": {
    "delaygb": "R",
    "keysymbol": "82TSLA",
    "exchcd": "82",
    "symbol": "TSLA"
  }
}
```

### 💡 Response Example
```json
{
	"g3106OutBlock": {
		"delaygb": "R",
		"keysymbol": "82TSLA",
		"exchcd": "82",
		"symbol": "TSLA",
		"korname": "테슬라",
		"price": "283.0200",
		"floatpoint": "4",
		"sign": "5",
		"diff": "1.9300",
		"rate": "-0.68",
		"volume": 431173,
		"amount": 122059929,
		"jnilclose": "284.9500",
		"open": "285.0900",
		"high": "285.3100",
		"low": "281.8400",
		"hotime": "144734",
		"offerho1": "283.1100",
		"bidho1": "283.0200",
		"offercnt1": "0",
		"bidcnt1": "0",
		"offerrem1": 20,
		"bidrem1": 38,
		"offerho2": "283.1200",
		"bidho2": "283.0100",
		"offercnt2": "0",
		"bidcnt2": "0",
		"offerrem2": 524,
		"bidrem2": 120,
		"offerho3": "283.1300",
		"bidho3": "283.0000",
		"offercnt3": "0",
		"bidcnt3": "0",
		"offerrem3": 20,
		"bidrem3": 1821,
		"offerho4": "283.1400",
		"bidho4": "282.9900",
		"offercnt4": "0",
		"bidcnt4": "0",
		"offerrem4": 10,
		"bidrem4": 641,
		"offerho5": "283.1800",
		"bidho5": "282.9700",
		"offercnt5": "0",
		"bidcnt5": "0",
		"offerrem5": 2,
		"bidrem5": 1,
		"offerho6": "283.2000",
		"bidho6": "282.9600",
		"offercnt6": "0",
		"bidcnt6": "0",
		"offerrem6": 10,
		"bidrem6": 38,
		"offerho7": "283.2400",
		"bidho7": "282.9500",
		"offercnt7": "0",
		"bidcnt7": "0",
		"offerrem7": 100,
		"bidrem7": 20,
		"offerho8": "283.2500",
		"bidho8": "282.9000",
		"offercnt8": "0",
		"bidcnt8": "0",
		"offerrem8": 878,
		"bidrem8": 100,
		"offerho9": "283.2700",
		"bidho9": "282.8900",
		"offercnt9": "0",
		"bidcnt9": "0",
		"offerrem9": 156,
		"bidrem9": 1,
		"offerho10": "283.2800",
		"bidho10": "282.8500",
		"offercnt10": "0",
		"bidcnt10": "0",
		"offerrem10": 20,
		"bidrem10": 17,
		"offercnt": "0",
		"bidcnt": "0",
		"offer": 1740,
		"bid": 2797
	},
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---

## 🏷️ 해외주식 API 마스터 조회 (g3190)
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
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| g3190InBlock | g3190InBlock | Object | Y          | -        |               |
| -delaygb     | 지연구분         | String | Y          | 1        |               |
| -natcode     | 국가구분         | String | Y          | 2        |               |
| -exgubun     | 거래소구분        | String | Y          | 1        |               |
| -readcnt     | 조회갯수         | Number | Y          | 4        |               |
| -cts_value   | 연속구분         | String | Y          | 16       |               |


### 응답 Header
| Element      | 한글명     | type   | Required   |   Length | Description                                                                     |
|:-------------|:--------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입   | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래CD    | String | Y          |       10 | LS증권거래코드                                                                        |
| tr_cont      | 연속거래여부  | String | Y          |        1 | 연속거래여부Y:연속○N:연속×                                                                |
| tr_cont_key  | 연속거래Key | String | Y          |       18 | 연속일경우그전에내려온연속키값올림                                                               |


### 응답 Body
| Element         | 한글명            | type   | Required   | Length   | Description   |
|:----------------|:---------------|:-------|:-----------|:---------|:--------------|
| g3190OutBlock   | g3190OutBlock  | Object | Y          | -        |               |
| -delaygb        | 지연구분           | String | Y          | 1        |               |
| -natcode        | 국가구분           | String | Y          | 2        |               |
| -exgubun        | 거래소구분          | String | Y          | 1        |               |
| -cts_value      | 연속구분           | String | Y          | 16       |               |
| -rec_count      | 레코드카운트         | Number | Y          | 7        |               |
| -g3190OutBlock1 | g3190OutBlock1 | Object | Y          | -        |               |
| -keysymbol      | KEY종목코드        | String | Y          | 18       |               |
| -natcode        | 국가코드           | String | Y          | 2        |               |
| -exchcd         | 거래소코드          | String | Y          | 2        |               |
| -symbol         | 종목코드           | String | Y          | 16       |               |
| -seccode        | 거래소종목코드        | String | Y          | 18       |               |
| -korname        | 한글종목명          | String | Y          | 64       |               |
| -engname        | 영문종목명          | String | Y          | 64       |               |
| -currency       | 외환코드           | String | Y          | 4        |               |
| -isin           | ISIN           | String | Y          | 12       |               |
| -floatpoint     | FLOATPOINT     | String | Y          | 1        |               |
| -indusury       | 업종코드           | String | Y          | 4        |               |
| -share          | 상장주식수          | Number | Y          | 16       |               |
| -marketcap      | 자본금            | Number | Y          | 16       |               |
| -par            | 액면가            | Number | Y          | 15.6     |               |
| -parcurr        | 액면가외환코드        | String | Y          | 4        |               |
| -bidlotsize2    | 매수주문단위2        | String | Y          | 8        |               |
| -asklotsize2    | 매도주문단위2        | String | Y          | 8        |               |
| -clos           | 기준가            | Number | Y          | 15.6     |               |
| -listed_date    | 상장일자           | String | Y          | 8        |               |
| -expire_date    | 만기일자           | String | Y          | 8        |               |
| -suspend        | 거래정지여부         | String | Y          | 1        |               |
| -bymd           | 영업일자           | String | Y          | 8        |               |
| -sellonly       | SELLONLY구분     | String | Y          | 8        |               |
| -stamp          | 인지세여부          | String | Y          | 1        |               |
| -ticktype       | TICKSIZETYPE   | String | Y          | 8        |               |
| -pcls           | 전일종가           | Number | Y          | 15.6     |               |
| -vcmf           | VCM대상종목        | String | Y          | 1        |               |
| -casf           | CAS대상종목        | String | Y          | 1        |               |
| -posf           | POS대상종목        | String | Y          | 1        |               |
| -point          | 소수점매매가능종목      | String | Y          | 1        |               |


### 💡 Request Example
```json
{
  "g3190InBlock": {
    "delaygb": "R",
    "natcode": "US",
    "exgubun": "2",
    "readcnt": 10,
    "cts_value":""
  }
}
```

### 💡 Response Example
```json
{
	"g3190OutBlock": {
		"delaygb": "R",
		"natcode": "US",
		"exgubun": "2",
		"cts_value": "0000000000000011",
		"rec_count": 10
	},
	"g3190OutBlock1": [
		{
			"keysymbol": "82AACB",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AACB",
			"seccode": "82AACB",
			"korname": "ARTIUS II ACQUISITION INC",
			"engname": "ARTIUS II ACQUISITION INC",
			"currency": "USD",
			"isin": "KYG0509J1159",
			"floatpoint": "4",
			"indusury": "4530",
			"share": 22175000,
			"marketcap": 575,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "9.9200",
			"listed_date": "20250407",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "9.9200",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AACBU",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AACBU",
			"seccode": "82AACBU",
			"korname": "아티우스 애퀴지션 2 유닛",
			"engname": "ARTIUS II ACQUISITION INC UNIT 1 COM & RT (27/11/2029)",
			"currency": "USD",
			"isin": "KYG0509J1076",
			"floatpoint": "4",
			"indusury": "4530",
			"share": 22175000,
			"marketcap": 575,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "10.1099",
			"listed_date": "20250213",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "10.1099",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AACG",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AACG",
			"seccode": "82AACG",
			"korname": "ATA 크리에티비티 글로벌(ADR)",
			"engname": "ATA CREATIVITY GLOBAL SPON ADS EACH REP 2 ORD SHS",
			"currency": "USD",
			"isin": "US00211V1061",
			"floatpoint": "4",
			"indusury": "3540",
			"share": 31624548,
			"marketcap": 651522,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "0.9050",
			"listed_date": "20191017",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "0.9050",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AADR",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AADR",
			"seccode": "82AADR",
			"korname": "ADVISORSHARES DORSEY WRIGHT ADR",
			"engname": "ADVISORSHARES TRUST ADVISORSHARES DORSEY WRIGHT ADR ETF",
			"currency": "USD",
			"isin": "US00768Y2063",
			"floatpoint": "4",
			"indusury": "9010",
			"share": 510000,
			"marketcap": 0,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "73.7500",
			"listed_date": "20210603",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "73.7500",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AAL",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AAL",
			"seccode": "82AAL",
			"korname": "아메리칸 에어라인스 그룹",
			"engname": "AMERICAN AIRLINES GROUP INC",
			"currency": "USD",
			"isin": "US02376R1023",
			"floatpoint": "4",
			"indusury": "2040",
			"share": 659512000,
			"marketcap": 7000000,
			"par": "0.0100",
			"parcurr": "USD",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "9.7500",
			"listed_date": "20131210",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "9.7500",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "Y"
		},
		{
			"keysymbol": "82AAME",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AAME",
			"seccode": "82AAME",
			"korname": "애틀랜틱 아메리칸",
			"engname": "ATLANTIC AMERICAN CORP",
			"currency": "USD",
			"isin": "US0482091008",
			"floatpoint": "4",
			"indusury": "4520",
			"share": 20399800,
			"marketcap": 22401000,
			"par": "1.0000",
			"parcurr": "USD",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "1.5199",
			"listed_date": "19840907",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "1.5199",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AAOI",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AAOI",
			"seccode": "82AAOI",
			"korname": "어플라이드 옵토일렉트로닉스",
			"engname": "APPLIED OPTOELECTRONICS INC",
			"currency": "USD",
			"isin": "US03823U1025",
			"floatpoint": "4",
			"indusury": "2510",
			"share": 55342600,
			"marketcap": 49000,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "12.5600",
			"listed_date": "20130925",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "12.5600",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AAON",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AAON",
			"seccode": "82AAON",
			"korname": "에이에이온",
			"engname": "AAON INC",
			"currency": "USD",
			"isin": "US0003602069",
			"floatpoint": "4",
			"indusury": "2010",
			"share": 81317600,
			"marketcap": 326000,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "87.9400",
			"listed_date": "19910108",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "87.9400",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AAPB",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AAPB",
			"seccode": "82AAPB",
			"korname": "GRANITESHARES DAILY AAPL 2X",
			"engname": "GRANITESHARES ETF TRUST 2X LONG AAPL DAILY ETF",
			"currency": "USD",
			"isin": "US38747R8842",
			"floatpoint": "4",
			"indusury": "9010",
			"share": 810001,
			"marketcap": 0,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "21.5000",
			"listed_date": "20220809",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "21.5000",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		},
		{
			"keysymbol": "82AAPD",
			"natcode": "US",
			"exchcd": "82",
			"symbol": "AAPD",
			"seccode": "82AAPD",
			"korname": "DIREXION AAPL DAILY -1X",
			"engname": "DIREXION SHARES ETF TRUST DAILY AAPL BEAR 1X SHS",
			"currency": "USD",
			"isin": "US25461A3041",
			"floatpoint": "4",
			"indusury": "9010",
			"share": 1950000,
			"marketcap": 0,
			"par": "0.0000",
			"parcurr": "",
			"bidlotsize2": "1",
			"asklotsize2": "1",
			"clos": "17.3100",
			"listed_date": "20220809",
			"expire_date": "00000000",
			"suspend": "N",
			"bymd": "20250425",
			"sellonly": "0",
			"stamp": "",
			"ticktype": "1",
			"pcls": "17.3100",
			"vcmf": "",
			"casf": "",
			"posf": "",
			"point": "N"
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---
