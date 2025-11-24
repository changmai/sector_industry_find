# REST[선물/옵션] 시세
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=2f1eea77-5606-4512-93c6-31b21d2ece90&api_id=9f467798-6ce6-4d31-ab93-5a0e2860f89f

## 📌 기본 정보
| 항목           | 내용                                               |
|:-------------|:-------------------------------------------------|
| Method       | POST                                             |
| Domain       | https://openapi.ls-sec.co.kr:8080                |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080                |
| 모의투자 도메인     |                                                  |
| URL          | /futureoption/market-data                        |
| Format       | JSON                                             |
| Content-Type | application/json; charset=UTF-8                  |
| Description  | 주간/야간 선물옵션 종목별 시세 및 미결제약정 등시세관련 데이터를 확인할 수 있습니다. |


## 🏷️ 선물/옵션현재가(시세)조회 (t2101)
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
| t2101InBlock | t2101InBlock | Object | Y          | -        |               |
| -focode      | 단축코드         | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element         | 한글명                                | type   | Required   | Length   | Description              |
|:----------------|:-----------------------------------|:-------|:-----------|:---------|:-------------------------|
| t2101OutBlock   | t2101OutBlock                      | Object | Y          | -        |                          |
| -hname          | 한글명                                | String | Y          | 20       |                          |
| -price          | 현재가                                | Number | Y          | 6.2      |                          |
| -sign           | 전일대비구분                             | String | Y          | 1        | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| -change         | 전일대비                               | Number | Y          | 6.2      |                          |
| -jnilclose      | 전일종가                               | Number | Y          | 6.2      |                          |
| -diff           | 등락율                                | Number | Y          | 6.2      |                          |
| -volume         | 거래량                                | Number | Y          | 12       |                          |
| -value          | 거래대금                               | Number | Y          | 12       |                          |
| -mgjv           | 미결제량                               | Number | Y          | 8        |                          |
| -mgjvdiff       | 미결제증감                              | Number | Y          | 8        |                          |
| -open           | 시가                                 | Number | Y          | 6.2      |                          |
| -high           | 고가                                 | Number | Y          | 6.2      |                          |
| -low            | 저가                                 | Number | Y          | 6.2      |                          |
| -uplmtprice     | 상한가                                | Number | Y          | 6.2      |                          |
| -dnlmtprice     | 하한가                                | Number | Y          | 6.2      |                          |
| -high52w        | 52최고가                              | Number | Y          | 6.2      |                          |
| -low52w         | 52최저가                              | Number | Y          | 6.2      |                          |
| -basis          | 베이시스                               | Number | Y          | 6.2      |                          |
| -recprice       | 기준가                                | Number | Y          | 6.2      |                          |
| -theoryprice    | 이론가                                | Number | Y          | 6.2      |                          |
| -glyl           | 괴리율                                | Number | Y          | 6.3      |                          |
| -cbhprice       | CB상한가                              | Number | Y          | 6.2      |                          |
| -cblprice       | CB하한가                              | Number | Y          | 6.2      |                          |
| -lastmonth      | 만기일                                | String | Y          | 8        |                          |
| -jandatecnt     | 잔여일                                | Number | Y          | 8        |                          |
| -pricejisu      | 종합지수                               | Number | Y          | 6.2      |                          |
| -jisusign       | 종합지수전일대비구분                         | String | Y          | 1        | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| -jisuchange     | 종합지수전일대비                           | Number | Y          | 6.2      |                          |
| -jisudiff       | 종합지수등락율                            | Number | Y          | 6.2      |                          |
| -kospijisu      | KOSPI200지수                         | Number | Y          | 6.2      |                          |
| -kospisign      | KOSPI200전일대비구분                     | String | Y          | 1        | 1:상한 2:상승 3:보합 4:하한 5:하락 |
| -kospichange    | KOSPI200전일대비                       | Number | Y          | 6.2      |                          |
| -kospidiff      | KOSPI200등락율                        | Number | Y          | 6.2      |                          |
| -listhprice     | 상장최고가                              | Number | Y          | 6.2      |                          |
| -listlprice     | 상장최저가                              | Number | Y          | 6.2      |                          |
| -delt           | 델타                                 | Number | Y          | 6.4      |                          |
| -gama           | 감마                                 | Number | Y          | 6.4      |                          |
| -ceta           | 세타                                 | Number | Y          | 6.4      |                          |
| -vega           | 베가                                 | Number | Y          | 6.4      |                          |
| -rhox           | 로우                                 | Number | Y          | 6.4      |                          |
| -gmprice        | 근월물현재가                             | Number | Y          | 6.2      |                          |
| -gmsign         | 근월물전일대비구분                          | String | Y          | 1        |                          |
| -gmchange       | 근월물전일대비                            | Number | Y          | 6.2      |                          |
| -gmdiff         | 근월물등락율                             | Number | Y          | 6.2      |                          |
| -theorypriceg   | 이론가                                | Number | Y          | 6.2      |                          |
| -histimpv       | 역사적변동성                             | Number | Y          | 6.2      |                          |
| -impv           | 내재변동성                              | Number | Y          | 6.2      |                          |
| -sbasis         | 시장BASIS                            | Number | Y          | 6.2      |                          |
| -ibasis         | 이론BASIS                            | Number | Y          | 6.2      |                          |
| -gmfutcode      | 근월물종목코드                            | String | Y          | 8        |                          |
| -actprice       | 행사가                                | Number | Y          | 6.2      |                          |
| -greeks_time    | 거래소민감도수신시간                         | String | Y          | 6        |                          |
| -greeks_confirm | 거래소민감도확정여부                         | String | Y          | 8        |                          |
| -danhochk       | 단일가호가여부                            | String | Y          | 1        |                          |
| -yeprice        | 예상체결가                              | Number | Y          | 6.2      |                          |
| -jnilysign      | 예상체결가전일종가대비구분                      | String | Y          | 1        |                          |
| -jnilychange    | 예상체결가전일종가대비                        | Number | Y          | 6.2      |                          |
| -jnilydrate     | 예상체결가전일종가등락율                       | Number | Y          | 6.2      |                          |
| -alloc_gubun    | 배분구분(1:배분개시2:배분해제0:미발생)            | String | Y          | 1        |                          |
| -bjandatecnt    | 잔여일(영업일)                           | Number | Y          | 8        |                          |
| -focode         | 종목코드                               | String | Y          | 8        |                          |
| -dy_gubun       | 실시간가격제한여부(0:대상아님1:적용중2:미적용중3:일시해제) | String | Y          | 1        |                          |
| -dy_uplmtprice  | 실시간상한가                             | Number | Y          | 6.2      |                          |
| -dy_dnlmtprice  | 실시간하한가                             | Number | Y          | 6.2      |                          |
| -updnstep_gubun | 가격제한폭확대(0:미확대1:확대2:대상아님)           | String | Y          | 1        |                          |
| -upstep         | 상한적용단계                             | String | Y          | 2        |                          |
| -dnstep         | 하한적용단계                             | String | Y          | 2        |                          |
| -uplmtprice_3rd | 3단계상한가                             | Number | Y          | 6.2      |                          |
| -dnlmtprice_3rd | 3단계하한가                             | Number | Y          | 6.2      |                          |
| -expct_ccls_q   | 예상체결수량                             | Number | Y          | 9        |                          |


### 💡 Request Example
```json
{
  "t2101InBlock" : {
    "focode" : "101T6000"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2101OutBlock": {
        "jnilysign": "5",
        "jnilclose": "343.25",
        "sign": "5",
        "high52w": "0",
        "glyl": "-0.142",
        "kospichange": "0.47",
        "cbhprice": "0.00",
        "uplmtprice_3rd": "411.90",
        "jisusign": "5",
        "gmfutcode": "",
        "high": "342.75",
        "price": "342.30",
        "gmdiff": "0",
        "danhochk": "0",
        "jandatecnt": 1,
        "impv": "0",
        "hname": "코스피200 F 202306",
        "cblprice": "0.00",
        "listhprice": "405.70",
        "gmprice": "0",
        "diff": "-0.28",
        "rhox": "0",
        "basis": "0",
        "volume": 119523,
        "yeprice": "342.15",
        "low52w": "0",
        "dnstep": "01",
        "kospisign": "5",
        "dy_uplmtprice": "345.70",
        "listlprice": "281.25",
        "ibasis": "0.04",
        "bjandatecnt": 1,
        "dnlmtprice": "315.80",
        "recprice": "343.25",
        "mgjv": 0,
        "low": "340.65",
        "updnstep_gubun": "0",
        "theorypriceg": "0",
        "jnilychange": "1.10",
        "gmsign": "",
        "actprice": "0",
        "value": 10213209,
        "gama": "0",
        "dnlmtprice_3rd": "274.60",
        "jisuchange": "4.75",
        "upstep": "01",
        "jisudiff": "-0.18",
        "ceta": "0",
        "gmchange": "0",
        "greeks_confirm": "",
        "dy_gubun": "1",
        "change": "0.95",
        "delt": "0",
        "uplmtprice": "370.70",
        "kospijisu": "342.75",
        "lastmonth": "20230608",
        "greeks_time": "",
        "jnilydrate": "-0.32",
        "alloc_gubun": "",
        "focode": "101T6000",
        "kospidiff": "-0.14",
        "histimpv": "0",
        "dy_dnlmtprice": "338.90",
        "mgjvdiff": -144557,
        "sbasis": "-0.45",
        "theoryprice": "342.79",
        "open": "342.15",
        "vega": "0",
        "pricejisu": "2610.85",
        "expct_ccls_q": 0
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 선물/옵션현재가호가조회 (t2105)
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
| t2105InBlock | t2105InBlock | Object | Y          | -        |               |
| -shcode      | 단축코드         | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element       | 한글명           | type   | Required   | Length   | Description          |
|:--------------|:--------------|:-------|:-----------|:---------|:---------------------|
| t2105OutBlock | t2105OutBlock | Object | Y          | -        |                      |
| -hname        | 종목명           | String | Y          | 20       |                      |
| -price        | 현재가           | Number | Y          | 6.2      |                      |
| -sign         | 전일대비구분        | String | Y          | 1        | 1:상한2:상승3:보합4:하한5:하락 |
| -change       | 전일대비          | Number | Y          | 6.2      |                      |
| -diff         | 등락율           | Number | Y          | 6.2      |                      |
| -volume       | 거래량           | Number | Y          | 12       |                      |
| -stimeqrt     | 거래량전일동시간비율    | Number | Y          | 6.2      |                      |
| -jnilclose    | 전일종가          | Number | Y          | 6.2      |                      |
| -offerho1     | 매도호가1         | Number | Y          | 6.2      |                      |
| -bidho1       | 매수호가1         | Number | Y          | 6.2      |                      |
| -offerrem1    | 매도호가수량1       | Number | Y          | 8        |                      |
| -bidrem1      | 매수호가수량1       | Number | Y          | 8        |                      |
| -dcnt1        | 매도호가건수1       | Number | Y          | 8        |                      |
| -scnt1        | 매수호가건수1       | Number | Y          | 8        |                      |
| -offerho2     | 매도호가2         | Number | Y          | 6.2      |                      |
| -bidho2       | 매수호가2         | Number | Y          | 6.2      |                      |
| -offerrem2    | 매도호가수량2       | Number | Y          | 8        |                      |
| -bidrem2      | 매수호가수량2       | Number | Y          | 8        |                      |
| -dcnt2        | 매도호가건수2       | Number | Y          | 8        |                      |
| -scnt2        | 매수호가건수2       | Number | Y          | 8        |                      |
| -offerho3     | 매도호가3         | Number | Y          | 6.2      |                      |
| -bidho3       | 매수호가3         | Number | Y          | 6.2      |                      |
| -offerrem3    | 매도호가수량3       | Number | Y          | 8        |                      |
| -bidrem3      | 매수호가수량3       | Number | Y          | 8        |                      |
| -dcnt3        | 매도호가건수3       | Number | Y          | 8        |                      |
| -scnt3        | 매수호가건수3       | Number | Y          | 8        |                      |
| -offerho4     | 매도호가4         | Number | Y          | 6.2      |                      |
| -bidho4       | 매수호가4         | Number | Y          | 6.2      |                      |
| -offerrem4    | 매도호가수량4       | Number | Y          | 8        |                      |
| -bidrem4      | 매수호가수량4       | Number | Y          | 8        |                      |
| -dcnt4        | 매도호가건수4       | Number | Y          | 8        |                      |
| -scnt4        | 매수호가건수4       | Number | Y          | 8        |                      |
| -offerho5     | 매도호가5         | Number | Y          | 6.2      |                      |
| -bidho5       | 매수호가5         | Number | Y          | 6.2      |                      |
| -offerrem5    | 매도호가수량5       | Number | Y          | 8        |                      |
| -bidrem5      | 매수호가수량5       | Number | Y          | 8        |                      |
| -dcnt5        | 매도호가건수5       | Number | Y          | 8        |                      |
| -scnt5        | 매수호가건수5       | Number | Y          | 8        |                      |
| -dvol         | 매도호가총수량       | Number | Y          | 8        |                      |
| -svol         | 매수호가총수량       | Number | Y          | 8        |                      |
| -toffernum    | 총매도호가건수       | Number | Y          | 8        |                      |
| -tbidnum      | 총매수호가건수       | Number | Y          | 8        |                      |
| -time         | 수신시간          | String | Y          | 6        |                      |
| -shcode       | 단축코드          | String | Y          | 8        |                      |


### 💡 Request Example
```json
{
   "t2105InBlock" :{
      "shcode" : "101T6000"
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2105OutBlock": {
        "offerrem2": 179,
        "offerho4": "342.50",
        "bidho5": "342.10",
        "dvol": 6245,
        "offerho3": "342.45",
        "offerrem3": 171,
        "bidho4": "342.15",
        "offerrem4": 202,
        "offerho5": "342.55",
        "offerrem5": 136,
        "jnilclose": "343.25",
        "offerrem1": 36,
        "sign": "5",
        "bidrem3": 54,
        "bidrem4": 48,
        "bidrem1": 2,
        "bidrem2": 41,
        "price": "342.30",
        "scnt1": 1,
        "tbidnum": 931,
        "bidho1": "342.30",
        "scnt5": 15,
        "scnt4": 19,
        "hname": "코스피200 F 202306",
        "offerho2": "342.40",
        "bidho3": "342.20",
        "scnt3": 18,
        "bidrem5": 60,
        "offerho1": "342.35",
        "bidho2": "342.25",
        "scnt2": 9,
        "dcnt4": 40,
        "dcnt3": 26,
        "dcnt2": 30,
        "dcnt1": 4,
        "stimeqrt": "77.11",
        "change": "0.95",
        "shcode": "101T6000",
        "diff": "-0.28",
        "toffernum": 672,
        "volume": 119523,
        "svol": 5732,
        "time": "152000",
        "dcnt5": 21
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 선물/옵션현재가시세메모 (t2106)
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
| Element       | 한글명           | type         | Required   | Length   | Description                       |
|:--------------|:--------------|:-------------|:-----------|:---------|:----------------------------------|
| t2106InBlock  | t2106InBlock  | Object       | Y          | -        |                                   |
| -code         | 종목코드          | String       | Y          | 8        |                                   |
| -nrec         | 건수            | String       | Y          | 2        | t2106InBlock1 의 개수                |
| t2106InBlock1 | t2106InBlock1 | Object Array | Y          | -        |                                   |
| -indx         | 인덱스           | String       | Y          | 1        | t2106InBlock1 의 Occurs 순서(0부터 시작) |
| -gubn         | 조건구분          | String       | Y          | 1        | 1:시세                              |
|               |               |              |            |          | 2:최고저가                            |
|               |               |              |            |          | 3:Pivot                           |
|               |               |              |            |          | 4:이동평균선                           |
| -dat1         | 데이타1          | String       | Y          | 1        | 1:시가                              |
|               |               |              |            |          | 2:고가                              |
|               |               |              |            |          | 3:저가                              |
|               |               |              |            |          | 4:가중평균가                           |
| -dat2         | 데이타2          | String       | Y          | 8        | 1:당일                              |
|               |               |              |            |          | 2:전일                              |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description              |
|:---------------|:---------------|:-------------|:-----------|:---------|:-------------------------|
| t2106OutBlock  | t2106OutBlock  | Object       | Y          | -        |                          |
| -nrec          | 출력건수           | String       | Y          | 2        | t2106OutBlock1 의 개수      |
| t2106OutBlock1 | t2106OutBlock1 | Object Array | Y          | -        |                          |
| -indx          | 인덱스            | String       | Y          | 1        | t2106InBlock1 의 indx와 동일 |
| -gubn          | 조건구분           | String       | Y          | 1        | 1:시세                     |
|                |                |              |            |          | 2:최고저가                   |
|                |                |              |            |          | 3:Pivot                  |
|                |                |              |            |          | 4:이동평균선                  |
|                |                |              |            |          | t2106InBlock1의 gubn과 동일  |
| -vals          | 출력값            | String       | Y          | 8        |                          |


### 💡 Request Example
```json
{
  "t2106InBlock": {
    "code": "101T6000",
    "nrec": ""
  }
}
```

### 💡 Response Example
```json
{
  "rsp_cd": "00000",
  "rsp_msg": "입력조건을 확인하세요"
}
```

---

## 🏷️ 선물옵션시간대별체결조회 (t2201)
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
| Element      | 한글명          | type   | Required   | Length   | Description                              |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------------|
| t2201InBlock | t2201InBlock | Object | Y          | -        |                                          |
| -focode      | 단축코드         | String | Y          | 8        |                                          |
| -cvolume     | 특이거래량        | Number | Y          | 12       | 체결수량 >= cvolume                          |
| -stime       | 시작시간         | String | Y          | 4        | 체결시간 >= stime(hhmm)                      |
| -etime       | 종료시간         | String | Y          | 4        | 체결시간 <= etime(hhmm)                      |
| -cts_time    | 시간CTS        | String | Y          | 10       | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                             |
|:---------------|:---------------|:-------------|:-----------|:---------|:----------------------------------------|
| t2201OutBlock  | t2201OutBlock  | Object       | Y          | -        |                                         |
| -cts_time      | 시간CTS          | String       | Y          | 10       | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다. |
| t2201OutBlock1 | t2201OutBlock1 | Object Array | Y          | -        |                                         |
| -chetime       | 시간             | String       | Y          | 10       |                                         |
| -price         | 현재가            | Number       | Y          | 6.2      |                                         |
| -sign          | 전일대비구분         | String       | Y          | 1        |                                         |
| -change        | 전일대비           | Number       | Y          | 6.2      |                                         |
| -cvolume       | 체결수량           | Number       | Y          | 8        |                                         |
| -chdegree      | 체결강도           | Number       | Y          | 8.2      |                                         |
| -offerho       | 매도호가           | Number       | Y          | 6.2      |                                         |
| -bidho         | 매수호가           | Number       | Y          | 6.2      |                                         |
| -volume        | 거래량            | Number       | Y          | 12       |                                         |
| -openyak       | 미결수량           | Number       | Y          | 8        |                                         |
| -jnilopenupdn  | 미결전일증감         | Number       | Y          | 8        |                                         |
| -ibasis        | 이론BASIS        | Number       | Y          | 6.2      |                                         |
| -sbasis        | 시장BASIS        | Number       | Y          | 6.2      |                                         |
| -kasis         | 괴리율            | Number       | Y          | 6.2      |                                         |
| -value         | 거래대금           | Number       | Y          | 12       |                                         |
| -j_openupdn    | 미결직전증감         | Number       | Y          | 8        |                                         |
| -n_msvolume    | 누적매수체결량        | Number       | Y          | 12       |                                         |
| -n_mdvolume    | 누적매도체결량        | Number       | Y          | 12       |                                         |
| -s_msvolume    | 누적순매수체결량       | Number       | Y          | 12       |                                         |
| -n_mschecnt    | 누적매수체결건수       | Number       | Y          | 8        |                                         |
| -n_mdchecnt    | 누적매도체결건수       | Number       | Y          | 8        |                                         |
| -s_mschecnt    | 누적순매수체결건수      | Number       | Y          | 8        |                                         |


### 💡 Request Example
```json
{
  "t2201InBlock": {
    "focode": "101T6000",
    "cvolume": 0,
    "stime": "0900",
    "etime": "1600",
    "cts_time": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2201OutBlock": {
        "cts_time": "1519336905"
    },
    "t2201OutBlock1": [
        {
            "change": "0.95",
            "sign": "5",
            "ibasis": "0.04",
            "n_mdchecnt": 26165,
            "chetime": "1519599311",
            "offerho": "342.35",
            "openyak": 107170,
            "j_openupdn": 0,
            "cvolume": 13,
            "n_mdvolume": "60493",
            "volume": "119523",
            "chdegree": "96.01",
            "bidho": "342.25",
            "s_mschecnt": -574,
            "price": "342.30",
            "kasis": "0.05",
            "s_msvolume": "-2413",
            "n_mschecnt": 25591,
            "jnilopenupdn": -37387,
            "n_msvolume": "58080",
            "sbasis": "0.21",
            "value": "10213209"
        },
        {
            "change": "0.95",
            "sign": "5",
            "ibasis": "0.04",
            "n_mdchecnt": 26165,
            "chetime": "1519599299",
            "offerho": "342.30",
            "openyak": 107170,
            "j_openupdn": 0,
            "cvolume": 2,
            "n_mdvolume": "60493",
            "volume": "119510",
            "chdegree": "95.99",
            "bidho": "342.25",
            "s_mschecnt": -575,
            "price": "342.30",
            "kasis": "0.05",
            "s_msvolume": "-2426",
            "n_mschecnt": 25590,
            "jnilopenupdn": -37387,
            "n_msvolume": "58067",
            "sbasis": "0.21",
            "value": "10212096"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 기간별주가 (t2203)
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
| Element      | 한글명          | type   | Required   | Length   | Description                              |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------------|
| t2203InBlock | t2203InBlock | Object | Y          | -        |                                          |
| -shcode      | 단축코드         | String | Y          | 8        |                                          |
| -futcheck    | 선물최근월물       | String | Y          | 1        | 0:default                                |
|              |              |        |            |          | 1:최근월물만연결                                |
| -date        | 날짜           | String | Y          | 8        | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정     |
| -cts_code    | CTS종목코드      | String | Y          | 8        | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 cts_code 값으로 설정 |
| -lastdate    | 전종목만기일       | String | Y          | 8        |                                          |
| -cnt         | 조회요청건수       | Object | Y          | 3        |                                          |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                             |
|:---------------|:---------------|:-------------|:-----------|:---------|:----------------------------------------|
| t2203OutBlock  | t2203OutBlock  | Object       | Y          | -        |                                         |
| -date          | 날짜             | String       | Y          | 8        | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 date 필드에 넣어준다.     |
| -cts_code      | CTS종목코드        | String       | Y          | 8        | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 cts_code 필드에 넣어준다. |
| -lastdate      | 전종목만기일         | String       | Y          | 8        |                                         |
| -nowfutyn      | 최근월선물여부        | String       | Y          | 1        |                                         |
| t2203OutBlock1 | t2203OutBlock1 | Object Array | Y          | -        |                                         |
| -date          | 날짜             | String       | Y          | 8        |                                         |
| -open          | 시가             | Number       | Y          | 6.2      |                                         |
| -high          | 고가             | Number       | Y          | 6.2      |                                         |
| -low           | 저가             | Number       | Y          | 6.2      |                                         |
| -close         | 종가             | Number       | Y          | 6.2      |                                         |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한                                    |
|                |                |              |            |          | 2:상승                                    |
|                |                |              |            |          | 3:보합                                    |
|                |                |              |            |          | 4:하한                                    |
|                |                |              |            |          | 5:하락                                    |
| -change        | 전일대비           | Number       | Y          | 6.2      |                                         |
| -diff          | 등락율            | Number       | Y          | 6.2      |                                         |
| -volume        | 거래량            | Number       | Y          | 12       |                                         |
| -diff_vol      | 거래증가율          | Number       | Y          | 10.2     |                                         |
| -openyak       | 미결수량           | Number       | Y          | 8        |                                         |
| -openyakupdn   | 미결증감           | Number       | Y          | 8        |                                         |
| -value         | 거래대금           | Number       | Y          | 12       |                                         |


### 💡 Request Example
```json
{
   "t2203InBlock" :{
      "shcode" : "101T6000",
      "futcheck" : "0",
      "date" : "",
      "cts_code" : "",
      "lastdate" : "",
      "cnt" : 20
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2203OutBlock": {
        "date": "20230602",
        "cts_code": "101T6000",
        "nowfutyn": "Y",
        "lastdate": ""
    },
    "t2203OutBlock1": [
        {
            "date": "20230608",
            "openyakupdn": -144557,
            "diff_vol": "-27.81",
            "change": "0.95",
            "sign": "5",
            "diff": "-0.28",
            "openyak": 0,
            "volume": 119523,
            "high": "342.75",
            "low": "340.65",
            "close": "342.30",
            "value": "000010213209",
            "open": "342.15"
        },
        {
            "date": "20230607",
            "openyakupdn": -80170,
            "diff_vol": "1.32",
            "change": "0.75",
            "sign": "5",
            "diff": "-0.22",
            "openyak": 144557,
            "volume": 165564,
            "high": "345.75",
            "low": "343.10",
            "close": "343.25",
            "value": "000014265463",
            "open": "345.10"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 선물옵션시간대별체결조회(단일출력용) (t2210)
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
| Element      | 한글명          | type   | Required   | Length   | Description         |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------|
| t2210InBlock | t2210InBlock | Object | Y          | -        |                     |
| -focode      | 단축코드         | String | Y          | 8        |                     |
| -cvolume     | 특이거래량        | Number | Y          | 12       | 체결수량 >= cvolume     |
| -stime       | 시작시간         | String | Y          | 4        | 체결시간 >= stime(hhmm) |
| -etime       | 종료시간         | String | Y          | 4        | 체결시간 <= etime(hhmm) |


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
| t2210OutBlock | t2210OutBlock | Object | Y          | -        |               |
| -mdvolume     | 매도체결수량        | Number | Y          | 8        |               |
| -mdchecnt     | 매도체결건수        | Number | Y          | 8        |               |
| -msvolume     | 매수체결수량        | Number | Y          | 8        |               |
| -mschecnt     | 매수체결건수        | Number | Y          | 8        |               |


### 💡 Request Example
```json
{
   "t2210InBlock" :{
      "focode" : "101T6000",
      "cvolume" : 0,
      "stime" : "0900",
      "etime" : "1600"
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t2210OutBlock": {
        "mdchecnt": 26165,
        "msvolume": 58080,
        "mschecnt": 25591,
        "mdvolume": 60493
    }
}
```

---

## 🏷️ 옵션전광판 (t2301)
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
| Element      | 한글명            | type   | Required   | Length   | Description          |
|:-------------|:---------------|:-------|:-----------|:---------|:---------------------|
| t2301InBlock | t2301InBlock   | Object | Y          | -        |                      |
| -yyyymm      | 월물             | String | Y          | 6        | ex) 미니,정규 : '200604' |
|              |                |        |            |          |     위클리 : 'W1    '   |
| -gubun       | 미니구분(M:미니G:정규) | String | Y          | 1        | M: 미니                |
|              |                |        |            |          | G: 정규                |
|              |                |        |            |          | W: 위클리               |


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
| t2301OutBlock  | t2301OutBlock  | Object       | Y          | -        |               |
| -histimpv      | 역사적변동성         | Number       | Y          | 4        |               |
| -jandatecnt    | 옵션잔존일          | Number       | Y          | 4        |               |
| -cimpv         | 콜옵션대표IV        | Number       | Y          | 6.3      |               |
| -pimpv         | 풋옵션대표IV        | Number       | Y          | 6.3      |               |
| -gmprice       | 근월물현재가         | Number       | Y          | 6.2      |               |
| -gmsign        | 근월물전일대비구분      | String       | Y          | 1        | 1:상한          |
|                |                |              |            |          | 2:상승          |
|                |                |              |            |          | 3:보합          |
|                |                |              |            |          | 4:하한          |
|                |                |              |            |          | 5:하락          |
| -gmchange      | 근월물전일대비        | Number       | Y          | 6.2      |               |
| -gmdiff        | 근월물등락율         | Number       | Y          | 6.2      |               |
| -gmvolume      | 근월물거래량         | Number       | Y          | 12       |               |
| -gmshcode      | 근월물선물코드        | String       | Y          | 8        |               |
| t2301OutBlock1 | t2301OutBlock1 | Object Array | Y          | -        |               |
| -actprice      | 행사가            | Number       | Y          | 6.2      |               |
| -optcode       | 콜옵션코드          | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한          |
|                |                |              |            |          | 2:상승          |
|                |                |              |            |          | 3:보합          |
|                |                |              |            |          | 4:하한          |
|                |                |              |            |          | 5:하락          |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -iv            | IV             | Number       | Y          | 6.2      |               |
| -mgjv          | 미결제약정          | Number       | Y          | 12       |               |
| -mgjvupdn      | 미결제약정증감        | Number       | Y          | 12       |               |
| -offerho1      | 매도호가           | Number       | Y          | 6.2      |               |
| -bidho1        | 매수호가           | Number       | Y          | 6.2      |               |
| -cvolume       | 체결량            | Number       | Y          | 12       |               |
| -delt          | 델타             | Number       | Y          | 6.4      |               |
| -gama          | 감마             | Number       | Y          | 6.4      |               |
| -vega          | 베가             | Number       | Y          | 6.4      |               |
| -ceta          | 쎄타             | Number       | Y          | 6.4      |               |
| -rhox          | 로우             | Number       | Y          | 6.4      |               |
| -theoryprice   | 이론가            | Number       | Y          | 6.2      |               |
| -impv          | 내재가치           | Number       | Y          | 6.2      |               |
| -timevl        | 시간가치           | Number       | Y          | 6.2      |               |
| -jvolume       | 잔고수량           | Number       | Y          | 12       |               |
| -parpl         | 평가손익           | Number       | Y          | 12       |               |
| -jngo          | 청산가능수량         | Number       | Y          | 6        |               |
| -offerrem1     | 매도잔량           | Number       | Y          | 12       |               |
| -bidrem1       | 매수잔량           | Number       | Y          | 12       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -atmgubun      | ATM구분          | String       | Y          | 1        | 0:선물          |
|                |                |              |            |          | 1:ATM         |
|                |                |              |            |          | 2:ITM         |
|                |                |              |            |          | 3:OTM         |
| -jisuconv      | 지수환산           | Number       | Y          | 6.2      |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |
| t2301OutBlock2 | t2301OutBlock2 | Object Array | Y          | -        |               |
| -actprice      | 행사가            | Number       | Y          | 6.2      |               |
| -optcode       | 풋옵션코드          | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한          |
|                |                |              |            |          | 2:상승          |
|                |                |              |            |          | 3:보합          |
|                |                |              |            |          | 4:하한          |
|                |                |              |            |          | 5:하락          |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -iv            | IV             | Number       | Y          | 6.2      |               |
| -mgjv          | 미결제약정          | Number       | Y          | 12       |               |
| -mgjvupdn      | 미결제약정증감        | Number       | Y          | 12       |               |
| -offerho1      | 매도호가           | Number       | Y          | 6.2      |               |
| -bidho1        | 매수호가           | Number       | Y          | 6.2      |               |
| -cvolume       | 체결량            | Number       | Y          | 12       |               |
| -delt          | 델타             | Number       | Y          | 6.4      |               |
| -gama          | 감마             | Number       | Y          | 6.4      |               |
| -vega          | 베가             | Number       | Y          | 6.4      |               |
| -ceta          | 쎄타             | Number       | Y          | 6.4      |               |
| -rhox          | 로우             | Number       | Y          | 6.4      |               |
| -theoryprice   | 이론가            | Number       | Y          | 6.2      |               |
| -impv          | 내재가치           | Number       | Y          | 6.2      |               |
| -timevl        | 시간가치           | Number       | Y          | 6.2      |               |
| -jvolume       | 잔고수량           | Number       | Y          | 12       |               |
| -parpl         | 평가손익           | Number       | Y          | 12       |               |
| -jngo          | 청산가능수량         | Number       | Y          | 6        |               |
| -offerrem1     | 매도잔량           | Number       | Y          | 12       |               |
| -bidrem1       | 매수잔량           | Number       | Y          | 12       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -atmgubun      | ATM구분          | String       | Y          | 1        | 0:선물          |
|                |                |              |            |          | 1:ATM         |
|                |                |              |            |          | 2:ITM         |
|                |                |              |            |          | 3:OTM         |
| -jisuconv      | 지수환산           | Number       | Y          | 6.2      |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t2301InBlock": {
    "yyyymm": "",
    "gubun": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2301OutBlock2": [
        {
            "parpl": 0,
            "offerrem1": 2,
            "sign": "5",
            "cvolume": 1,
            "mgjvupdn": 0,
            "bidrem1": 7,
            "high": "175.70",
            "jisuconv": "3951.92",
            "mgjv": 471,
            "low": "175.50",
            "price": "175.70",
            "actprice": "520.00",
            "impv": "176.46",
            "bidho1": "175.50",
            "jngo": 0,
            "value": "000000000176",
            "gama": "0.0000",
            "offerho1": "176.55",
            "ceta": "0.0535",
            "optcode": "301T6520",
            "change": "1.40",
            "delt": "-1.0000",
            "diff": "-0.79",
            "rhox": "-0.0570",
            "iv": "0.01",
            "timevl": "-0.76",
            "volume": 4,
            "atmgubun": "2",
            "jvolume": 0,
            "theoryprice": "176.08",
            "vega": "0.0000",
            "open": "175.50"
        }
    ],
    "t2301OutBlock": {
        "pimpv": "12.763",
        "gmchange": "0.70",
        "gmprice": "343.65",
        "histimpv": 0,
        "cimpv": "11.681",
        "gmdiff": "0.20",
        "gmsign": "2",
        "jandatecnt": 4,
        "gmvolume": 65769,
        "gmshcode": "101T6000"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}

```

---

## 🏷️ 선물옵션호가잔량비율챠트 (t2405)
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
| Element      | 한글명          | type   | Required   | Length   | Description                              |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------------|
| t2405InBlock | t2405InBlock | Object | Y          | -        |                                          |
| -focode      | 단축코드         | String | Y          | 8        |                                          |
| -bgubun      | 분구분          | String | Y          | 1        | 0:30초                                    |
|              |              |        |            |          | 1:분                                      |
| -nmin        | N분           | Object | Y          | 2        | bgubun = 1 인 경우 N분 입력값                   |
| -etime       | 종료시간         | String | Y          | 4        | etime 이전 시간대를 조회함                        |
| -hgubun      | 호가구분         | String | Y          | 1        | 0@총 호가잔량                                 |
|              |              |        |            |          | 1@1차 호가잔량                                |
|              |              |        |            |          | 2@2차 호가잔량                                |
|              |              |        |            |          | 3@3차 호가잔량                                |
|              |              |        |            |          | 4@4차 호가잔량                                |
|              |              |        |            |          | 5@5차 호가잔량                                |
| -cnt         | 조회건수         | Object | Y          | 3        |                                          |
| -cts_time    | 시간CTS        | String | Y          | 6        | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                             |
|:---------------|:---------------|:-------------|:-----------|:---------|:----------------------------------------|
| t2405OutBlock  | t2405OutBlock  | Object       | Y          | -        |                                         |
| -mdvolume      | 매도체결수량         | Number       | Y          | 12       |                                         |
| -mdchecnt      | 매도체결건수         | Number       | Y          | 8        |                                         |
| -msvolume      | 매수체결수량         | Number       | Y          | 12       |                                         |
| -mschecnt      | 매수체결건수         | Number       | Y          | 8        |                                         |
| -cts_time      | 시간CTS          | String       | Y          | 6        | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다. |
| t2405OutBlock1 | t2405OutBlock1 | Object Array | Y          | -        |                                         |
| -time          | 시간             | String       | Y          | 6        |                                         |
| -price         | 현재가            | Number       | Y          | 6.2      |                                         |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한                                    |
|                |                |              |            |          | 2:상승                                    |
|                |                |              |            |          | 3:보합                                    |
|                |                |              |            |          | 4:하한                                    |
|                |                |              |            |          | 5:하락                                    |
| -change        | 전일대비           | Number       | Y          | 6.2      |                                         |
| -volume        | 누적거래량          | Number       | Y          | 12       |                                         |
| -cvolume       | 체결수량           | Number       | Y          | 8        |                                         |
| -offerho1      | 매도1호가          | Number       | Y          | 6.2      |                                         |
| -bidho1        | 매수1호가          | Number       | Y          | 6.2      |                                         |
| -offerrem      | 매도수량           | Number       | Y          | 8        |                                         |
| -bidrem        | 매수수량           | Number       | Y          | 8        |                                         |
| -offercnt      | 매도건수           | Number       | Y          | 8        |                                         |
| -bidcnt        | 매수건수           | Number       | Y          | 8        |                                         |
| -c_offerrem    | 매도증감수량         | Number       | Y          | 8        |                                         |
| -c_bidrem      | 매수증감수량         | Number       | Y          | 8        |                                         |
| -c_offercnt    | 매도증감건수         | Number       | Y          | 8        |                                         |
| -c_bidcnt      | 매수증감건수         | Number       | Y          | 8        |                                         |
| -r_bidrem      | 매수수량비율         | Number       | Y          | 6.2      |                                         |
| -r_bidcnt      | 매수건수비율         | Number       | Y          | 6.2      |                                         |
| -r_sign        | 매수비율구분         | String       | Y          | 1        | 2:매수수량비율 > 100                          |
|                |                |              |            |          | 5:매수수량비율 <= 100                         |
| -date          | 일자             | Object       | Y          | 8        |                                         |


### 💡 Request Example
```json
{
   "t2405InBlock" :{
      "focode" : "101T6000",
      "bgubun" : "0",
      "nmin" : 0,
      "etime" : "1600",
      "hgubun" : "0",
      "cnt" : 20,
      "cts_time" : ""
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2405OutBlock1": [
    ],
    "t2405OutBlock": {
        "mdchecnt": 26165,
        "msvolume": "000000058080",
        "mschecnt": 25591,
        "mdvolume": "000000060493",
        "cts_time": ""
    },
    "rsp_msg": "조회완료"
}
```

---

## 🏷️ 미결제약정추이 (t2421)
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
| Element      | 한글명          | type   | Required   | Length   | Description                     |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------------------|
| t2421InBlock | t2421InBlock | Object | Y          | -        |                                 |
| -focode      | 종목코드         | String | Y          | 8        |                                 |
| -bdgubun     | 분일구분         | String | Y          | 1        | 0:30초                           |
|              |              |        |            |          | 1:분                             |
|              |              |        |            |          | 2:일                             |
| -nmin        | N분           | Object | Y          | 3        | t2421InBlock.bdgubun 이 1인 경우 N분 |
| -tcgubun     | 당일연결구분       | String | Y          | 1        | 0:전체                            |
|              |              |        |            |          | 1:당일                            |
| -cnt         | 조회건수         | Object | Y          | 4        |                                 |


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
| t2421OutBlock  | t2421OutBlock  | Object       | Y          | -        |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한          |
|                |                |              |            |          | 2:상승          |
|                |                |              |            |          | 3:보합          |
|                |                |              |            |          | 4:하한          |
|                |                |              |            |          | 5:하락          |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -cvolume       | 체결수량           | Number       | Y          | 8        |               |
| -volume        | 누적거래량          | Number       | Y          | 15       |               |
| -openyak       | 미결제수량          | Number       | Y          | 8        |               |
| t2421OutBlock1 | t2421OutBlock1 | Object Array | Y          | -        |               |
| -dt            | 일자시간           | String       | Y          | 14       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -close         | 종가             | Number       | Y          | 6.2      |               |
| -openopenyak   | 미결제시량          | Number       | Y          | 8        |               |
| -highopenyak   | 미결제고량          | Number       | Y          | 8        |               |
| -lowopenyak    | 미결제저량          | Number       | Y          | 8        |               |
| -closeopenyak  | 미결제종량          | Number       | Y          | 8        |               |
| -openupdn      | 미결증감           | Number       | Y          | 8        |               |


### 💡 Request Example
```json
{
   "t2421InBlock" :{
      "focode" : "101T6000",
      "bdgubun" : "0",
      "nmin" : 0,
      "tcgubun" : "0",
      "cnt" : 20
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t2421OutBlock": {
        "volume": "000000000119523",
        "price": "342.30",
        "change": "0.95",
        "sign": "5",
        "diff": "0.28",
        "openyak": 0,
        "cvolume": 13
    },
    "t2421OutBlock1": [
        {
            "dt": "154500",
            "closeopenyak": 0,
            "high": "342.30",
            "low": "342.30",
            "openupdn": -107149,
            "highopenyak": 107149,
            "lowopenyak": 0,
            "close": "342.30",
            "open": "342.30",
            "openopenyak": 107149
        },
        {
            "dt": "153500",
            "closeopenyak": 107149,
            "high": "342.30",
            "low": "342.30",
            "openupdn": 0,
            "highopenyak": 107149,
            "lowopenyak": 107149,
            "close": "342.30",
            "open": "342.30",
            "openopenyak": 107149
        },
        {
            "dt": "153430",
            "closeopenyak": 107149,
            "high": "342.30",
            "low": "342.30",
            "openupdn": 0,
            "highopenyak": 107149,
            "lowopenyak": 107149,
            "close": "342.30",
            "open": "342.30",
            "openopenyak": 107149
        },
        {
            "dt": "153400",
            "closeopenyak": 107149,
            "high": "342.30",
            "low": "342.30",
            "openupdn": 0,
            "highopenyak": 107149,
            "lowopenyak": 107149,
            "close": "342.30",
            "open": "342.30",
            "openopenyak": 107149
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 주식선물마스터조회(API용) (t8401)
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
| t8401InBlock | t8401InBlock | Object | Y          | -        |               |
| -dummy       | Dummy        | String | Y          | 1        |               |


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
| t8401OutBlock | t8401OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |
| -basecode     | 기초자산코드        | String       | Y          | 9        |               |


### 💡 Request Example
```json
{
  "t8401InBlock": {
    "dummy": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8401OutBlock": [
        {
            "basecode": "A005930",
            "shcode": "111T7000",
            "expcode": "KR4111T70004",
            "hname": "삼성전자   F 202307"
        },
        {
            "basecode": "A000810",
            "shcode": "1CTWC000",
            "expcode": "KR41CTWC0007",
            "hname": "삼성화재   F 202512"
        },
        {
            "basecode": "A008930",
            "shcode": "1CVT7000",
            "expcode": "KR41CVT70007",
            "hname": "한미사이언 F 202307"
        },
        {
            "basecode": "A008930",
            "shcode": "1CVT8000",
            "expcode": "KR41CVT80006",
            "hname": "한미사이언 F 202308"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 주식선물현재가조회(API용) (t8402)
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
| t8402InBlock | t8402InBlock | Object | Y          | -        |               |
| -focode      | 단축코드         | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type   | Required   | Length   | Description   |
|:---------------|:---------------|:-------|:-----------|:---------|:--------------|
| t8402OutBlock  | t8402OutBlock  | Object | Y          | -        |               |
| -hname         | 한글명            | String | Y          | 20       |               |
| -price         | 현재가            | Number | Y          | 8        |               |
| -sign          | 전일대비구분         | String | Y          | 1        |               |
| -change        | 전일대비           | Number | Y          | 8        |               |
| -jnilclose     | 전일종가           | Number | Y          | 8        |               |
| -diff          | 등락율            | Number | Y          | 6.2      |               |
| -volume        | 거래량            | Number | Y          | 12       |               |
| -stimeqrt      | 거래량전일동시간비율     | Number | Y          | 6.2      |               |
| -value         | 거래대금           | Number | Y          | 12       |               |
| -mgjv          | 미결제량           | Number | Y          | 8        |               |
| -mgjvdiff      | 미결제증감          | Number | Y          | 8        |               |
| -open          | 시가             | Number | Y          | 8        |               |
| -high          | 고가             | Number | Y          | 8        |               |
| -low           | 저가             | Number | Y          | 8        |               |
| -uplmtprice    | 상한가            | Number | Y          | 8        |               |
| -dnlmtprice    | 하한가            | Number | Y          | 8        |               |
| -high52w       | 52최고가          | Number | Y          | 8        |               |
| -low52w        | 52최저가          | Number | Y          | 8        |               |
| -basis         | 베이시스           | Number | Y          | 6.2      |               |
| -recprice      | 기준가            | Number | Y          | 8        |               |
| -theoryprice   | 이론가            | Number | Y          | 8        |               |
| -glyl          | 괴리율            | Number | Y          | 6.3      |               |
| -lastmonth     | 만기일            | String | Y          | 8        |               |
| -jandatecnt    | 잔여일            | Number | Y          | 8        |               |
| -pricejisu     | 종합지수           | Number | Y          | 6.2      |               |
| -jisusign      | 종합지수전일대비구분     | String | Y          | 1        |               |
| -jisuchange    | 종합지수전일대비       | Number | Y          | 6.2      |               |
| -jisudiff      | 종합지수등락율        | Number | Y          | 6.2      |               |
| -kospijisu     | KOSPI200지수     | Number | Y          | 6.2      |               |
| -kospisign     | KOSPI200전일대비구분 | String | Y          | 1        |               |
| -kospichange   | KOSPI200전일대비   | Number | Y          | 6.2      |               |
| -kospidiff     | KOSPI200등락율    | Number | Y          | 6.2      |               |
| -listhprice    | 상장최고가          | Number | Y          | 8        |               |
| -listlprice    | 상장최저가          | Number | Y          | 8        |               |
| -delt          | 델타             | Number | Y          | 6.4      |               |
| -gama          | 감마             | Number | Y          | 6.4      |               |
| -ceta          | 세타             | Number | Y          | 6.4      |               |
| -vega          | 베가             | Number | Y          | 6.4      |               |
| -rhox          | 로우             | Number | Y          | 6.4      |               |
| -gmprice       | 근월물현재가         | Number | Y          | 8        |               |
| -gmsign        | 근월물전일대비구분      | String | Y          | 1        |               |
| -gmchange      | 근월물전일대비        | Number | Y          | 8        |               |
| -gmdiff        | 근월물등락율         | Number | Y          | 6.2      |               |
| -theorypriceg  | 이론가            | Number | Y          | 8        |               |
| -histimpv      | 역사적변동성         | Number | Y          | 6.2      |               |
| -impv          | 내재변동성          | Number | Y          | 6.2      |               |
| -sbasis        | 시장BASIS        | Number | Y          | 8        |               |
| -ibasis        | 이론BASIS        | Number | Y          | 8        |               |
| -gmfutcode     | 근월물종목코드        | String | Y          | 8        |               |
| -actprice      | 행사가            | Number | Y          | 8        |               |
| -shcode        | 기초자산단축코드       | String | Y          | 6        |               |
| -basehname     | 기초자산한글명        | String | Y          | 20       |               |
| -baseprice     | 기초자산현재가        | Number | Y          | 8        |               |
| -basesign      | 기초자산현재가대비구분    | String | Y          | 1        |               |
| -basechange    | 기초자산현재가전일대비    | Number | Y          | 8        |               |
| -basediff      | 기초자산등락률        | Number | Y          | 6.2      |               |
| -basevol       | 기초자산거래량        | Number | Y          | 12       |               |
| -baseprevol    | 기초자산전일거래량      | Number | Y          | 12       |               |
| -basebidprc    | 기초자산매수호가       | Number | Y          | 9        |               |
| -baseaskprc    | 기초자산매도호가       | Number | Y          | 9        |               |
| -basefornetbid | 기초자산외국계회원사순매수  | Number | Y          | 12       |               |
| -prodgrp       | 상품군            | String | Y          | 20       |               |
| -mulcnt        | 승수             | Number | Y          | 12.8     |               |
| -danhochk      | 단일가호가여부        | String | Y          | 1        |               |
| -yeprice       | 예상체결가          | Number | Y          | 8        |               |
| -jnilysign     | 예상체결가전일종가대비구분  | String | Y          | 1        |               |
| -jnilychange   | 예상체결가전일종가대비    | Number | Y          | 8        |               |
| -jnilydrate    | 예상체결가전일종가등락율   | Number | Y          | 6.2      |               |


### 💡 Request Example
```json
{
   "t8402InBlock" :{
      "focode" : "111T6000"
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t8402OutBlock": {
        "jnilysign": "5",
        "mulcnt": "10.00000000",
        "jnilclose": 71200,
        "sign": "5",
        "high52w": 0,
        "glyl": "0.132",
        "kospichange": "0.47",
        "baseaskprc": 70900,
        "basefornetbid": 547559,
        "jisusign": "5",
        "gmfutcode": "",
        "high": 70800,
        "price": 70700,
        "gmdiff": "0",
        "danhochk": "0",
        "jandatecnt": 1,
        "impv": "0",
        "hname": "삼성전자   F 202306",
        "basechange": 100,
        "listhprice": 72800,
        "gmprice": 0,
        "prodgrp": "",
        "diff": "-0.70",
        "rhox": "0",
        "basis": "0",
        "basebidprc": 70800,
        "volume": 811347,
        "baseprice": 70900,
        "yeprice": 70500,
        "low52w": 0,
        "basediff": "-0.14",
        "kospisign": "5",
        "listlprice": 55200,
        "ibasis": -93,
        "dnlmtprice": 64100,
        "basevol": 19157578,
        "recprice": 71200,
        "mgjv": 0,
        "low": 70000,
        "theorypriceg": 0,
        "jnilychange": 700,
        "gmsign": "",
        "actprice": 0,
        "value": 570684700,
        "gama": "0",
        "jisuchange": "4.75",
        "jisudiff": "-0.15",
        "ceta": "0",
        "gmchange": 0,
        "stimeqrt": "106.86",
        "change": 500,
        "delt": "75.9257",
        "shcode": "005930",
        "uplmtprice": 78300,
        "kospijisu": "342.75",
        "lastmonth": "20230608",
        "jnilydrate": "-0.98",
        "kospidiff": "0.00",
        "histimpv": "0",
        "basehname": "삼성전자",
        "mgjvdiff": -539300,
        "sbasis": -200,
        "basesign": "5",
        "theoryprice": 70607,
        "baseprevol": 14796613,
        "open": 70500,
        "vega": "0",
        "pricejisu": "2610.85"
    }
}
```

---

## 🏷️ 주식선물호가조회(API용) (t8403)
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
| t8403InBlock | t8403InBlock | Object | Y          | -        |               |
| -shcode      | 단축코드         | String | Y          | 8        |               |


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
| t8403OutBlock | t8403OutBlock | Object | Y          | -        |               |
| -hname        | 종목명           | String | Y          | 20       |               |
| -price        | 현재가           | Number | Y          | 8        |               |
| -sign         | 전일대비구분        | String | Y          | 1        |               |
| -change       | 전일대비          | Number | Y          | 8        |               |
| -diff         | 등락율           | Number | Y          | 6.2      |               |
| -volume       | 거래량           | Number | Y          | 12       |               |
| -stimeqrt     | 거래량전일동시간비율    | Number | Y          | 6.2      |               |
| -jnilclose    | 전일종가          | Number | Y          | 8        |               |
| -offerho1     | 매도호가1         | Number | Y          | 8        |               |
| -bidho1       | 매수호가1         | Number | Y          | 8        |               |
| -offerrem1    | 매도호가수량1       | Number | Y          | 8        |               |
| -bidrem1      | 매수호가수량1       | Number | Y          | 8        |               |
| -dcnt1        | 매도호가건수1       | Number | Y          | 8        |               |
| -scnt1        | 매수호가건수1       | Number | Y          | 8        |               |
| -offerho2     | 매도호가2         | Number | Y          | 8        |               |
| -bidho2       | 매수호가2         | Number | Y          | 8        |               |
| -offerrem2    | 매도호가수량2       | Number | Y          | 8        |               |
| -bidrem2      | 매수호가수량2       | Number | Y          | 8        |               |
| -dcnt2        | 매도호가건수2       | Number | Y          | 8        |               |
| -scnt2        | 매수호가건수2       | Number | Y          | 8        |               |
| -offerho3     | 매도호가3         | Number | Y          | 8        |               |
| -bidho3       | 매수호가3         | Number | Y          | 8        |               |
| -offerrem3    | 매도호가수량3       | Number | Y          | 8        |               |
| -bidrem3      | 매수호가수량3       | Number | Y          | 8        |               |
| -dcnt3        | 매도호가건수3       | Number | Y          | 8        |               |
| -scnt3        | 매수호가건수3       | Number | Y          | 8        |               |
| -offerho4     | 매도호가4         | Number | Y          | 8        |               |
| -bidho4       | 매수호가4         | Number | Y          | 8        |               |
| -offerrem4    | 매도호가수량4       | Number | Y          | 8        |               |
| -bidrem4      | 매수호가수량4       | Number | Y          | 8        |               |
| -dcnt4        | 매도호가건수4       | Number | Y          | 8        |               |
| -scnt4        | 매수호가건수4       | Number | Y          | 8        |               |
| -offerho5     | 매도호가5         | Number | Y          | 8        |               |
| -bidho5       | 매수호가5         | Number | Y          | 8        |               |
| -offerrem5    | 매도호가수량5       | Number | Y          | 8        |               |
| -bidrem5      | 매수호가수량5       | Number | Y          | 8        |               |
| -dcnt5        | 매도호가건수5       | Number | Y          | 8        |               |
| -scnt5        | 매수호가건수5       | Number | Y          | 8        |               |
| -offerho6     | 매도호가6         | Number | Y          | 8        |               |
| -bidho6       | 매수호가6         | Number | Y          | 8        |               |
| -offerrem6    | 매도호가수량6       | Number | Y          | 8        |               |
| -bidrem6      | 매수호가수량6       | Number | Y          | 8        |               |
| -dcnt6        | 매도호가건수6       | Number | Y          | 8        |               |
| -scnt6        | 매수호가건수6       | Number | Y          | 8        |               |
| -offerho7     | 매도호가7         | Number | Y          | 8        |               |
| -bidho7       | 매수호가7         | Number | Y          | 8        |               |
| -offerrem7    | 매도호가수량7       | Number | Y          | 8        |               |
| -bidrem7      | 매수호가수량7       | Number | Y          | 8        |               |
| -dcnt7        | 매도호가건수7       | Number | Y          | 8        |               |
| -scnt7        | 매수호가건수7       | Number | Y          | 8        |               |
| -offerho8     | 매도호가8         | Number | Y          | 8        |               |
| -bidho8       | 매수호가8         | Number | Y          | 8        |               |
| -offerrem8    | 매도호가수량8       | Number | Y          | 8        |               |
| -bidrem8      | 매수호가수량8       | Number | Y          | 8        |               |
| -dcnt8        | 매도호가건수8       | Number | Y          | 8        |               |
| -scnt8        | 매수호가건수8       | Number | Y          | 8        |               |
| -offerho9     | 매도호가9         | Number | Y          | 8        |               |
| -bidho9       | 매수호가9         | Number | Y          | 8        |               |
| -offerrem9    | 매도호가수량9       | Number | Y          | 8        |               |
| -bidrem9      | 매수호가수량9       | Number | Y          | 8        |               |
| -dcnt9        | 매도호가건수9       | Number | Y          | 8        |               |
| -scnt9        | 매수호가건수9       | Number | Y          | 8        |               |
| -offerho10    | 매도호가10        | Number | Y          | 8        |               |
| -bidho10      | 매수호가10        | Number | Y          | 8        |               |
| -offerrem10   | 매도호가수량10      | Number | Y          | 8        |               |
| -bidrem10     | 매수호가수량10      | Number | Y          | 8        |               |
| -dcnt10       | 매도호가건수10      | Number | Y          | 8        |               |
| -scnt10       | 매수호가건수10      | Number | Y          | 8        |               |
| -dvol         | 매도호가총수량       | Number | Y          | 8        |               |
| -svol         | 매수호가총수량       | Number | Y          | 8        |               |
| -toffernum    | 총매도호가건수       | Number | Y          | 8        |               |
| -tbidnum      | 총매수호가건수       | Number | Y          | 8        |               |
| -time         | 수신시간          | String | Y          | 6        |               |
| -shcode       | 단축코드          | String | Y          | 6        |               |


### 💡 Request Example
```json
{
   "t8403InBlock" :{
      "shcode" : "111T6000"
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8403OutBlock": {
        "offerho4": 71100,
        "offerho3": 71000,
        "offerho6": 71300,
        "offerho5": 71200,
        "offerho8": 71500,
        "offerho7": 71400,
        "jnilclose": 71200,
        "offerho9": 71600,
        "sign": "5",
        "price": 70700,
        "hname": "삼성전자   F 202306",
        "offerho2": 70900,
        "offerho1": 70800,
        "diff": "-0.70",
        "toffernum": 91,
        "dcnt10": 2,
        "volume": 811347,
        "offerho10": 71700,
        "svol": 62353,
        "offerrem2": 1286,
        "bidho5": 70300,
        "dvol": 38649,
        "offerrem3": 117,
        "bidho4": 70400,
        "offerrem4": 25,
        "bidho7": 70100,
        "offerrem5": 25,
        "bidho6": 70200,
        "bidho9": 69900,
        "bidho8": 70000,
        "offerrem1": 1079,
        "offerrem6": 1,
        "offerrem7": 2000,
        "offerrem8": 2042,
        "offerrem9": 2001,
        "bidrem3": 2800,
        "bidrem4": 7281,
        "scnt10": 7,
        "bidrem1": 833,
        "bidrem2": 5198,
        "scnt1": 4,
        "tbidnum": 131,
        "bidrem9": 3162,
        "bidho1": 70700,
        "scnt5": 12,
        "bidrem7": 1371,
        "scnt4": 10,
        "bidrem8": 2062,
        "bidho3": 70500,
        "scnt3": 7,
        "bidrem5": 6304,
        "bidho2": 70600,
        "scnt2": 18,
        "bidrem6": 5160,
        "dcnt4": 4,
        "scnt9": 13,
        "bidrem10": 2143,
        "dcnt3": 3,
        "scnt8": 9,
        "dcnt2": 17,
        "scnt7": 10,
        "bidho10": 69800,
        "dcnt1": 14,
        "scnt6": 13,
        "stimeqrt": "106.86",
        "change": 500,
        "shcode": "111T60",
        "offerrem10": 2000,
        "dcnt9": 3,
        "time": "152000",
        "dcnt8": 5,
        "dcnt7": 2,
        "dcnt6": 1,
        "dcnt5": 3
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 주식선물시간대별체결조회(API용) (t8404)
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
| Element      | 한글명          | type   | Required   | Length   | Description                              |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------------|
| t8404InBlock | t8404InBlock | Object | Y          | -        |                                          |
| -focode      | 단축코드         | String | Y          | 8        |                                          |
| -cvolume     | 특이거래량        | Number | Y          | 12       | 거래량 > 특이거래량                              |
| -stime       | 시작시간         | String | Y          | 4        | 장시작시간 이후                                 |
| -etime       | 종료시간         | String | Y          | 4        | 장종료시간 이전                                 |
| -cts_time    | 시간CTS        | String | Y          | 10       | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 cts_time 값으로 설정 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                             |
|:---------------|:---------------|:-------------|:-----------|:---------|:----------------------------------------|
| t8404OutBlock  | t8404OutBlock  | Object       | Y          | -        |                                         |
| -cts_time      | 시간CTS          | String       | Y          | 10       | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 cts_time 필드에 넣어준다. |
| t8404OutBlock1 | t8404OutBlock1 | Object Array | Y          | -        |                                         |
| -chetime       | 시간             | String       | Y          | 10       |                                         |
| -price         | 현재가            | Number       | Y          | 8        |                                         |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한                                    |
|                |                |              |            |          | 2:상승                                    |
|                |                |              |            |          | 3:보합                                    |
|                |                |              |            |          | 4:하한                                    |
|                |                |              |            |          | 5:하락                                    |
| -change        | 전일대비           | Number       | Y          | 8        |                                         |
| -cvolume       | 체결수량           | Number       | Y          | 8        |                                         |
| -chdegree      | 체결강도           | Number       | Y          | 8.2      |                                         |
| -offerho       | 매도호가           | Number       | Y          | 8        |                                         |
| -bidho         | 매수호가           | Number       | Y          | 8        |                                         |
| -volume        | 거래량            | Number       | Y          | 12       |                                         |
| -openyak       | 미결수량           | Number       | Y          | 8        |                                         |
| -jnilopenupdn  | 미결전일증감         | Number       | Y          | 8        |                                         |
| -ibasis        | 이론BASIS        | Number       | Y          | 8        |                                         |
| -sbasis        | 시장BASIS        | Number       | Y          | 8        |                                         |
| -kasis         | 괴리율            | Number       | Y          | 6.2      |                                         |
| -value         | 거래대금           | Number       | Y          | 12       |                                         |
| -j_openupdn    | 미결직전증감         | Number       | Y          | 8        |                                         |
| -n_msvolume    | 누적매수체결량        | Number       | Y          | 12       |                                         |
| -n_mdvolume    | 누적매도체결량        | Number       | Y          | 12       |                                         |
| -s_msvolume    | 누적순매수체결량       | Number       | Y          | 12       |                                         |
| -n_mschecnt    | 누적매수체결건수       | Number       | Y          | 8        |                                         |
| -n_mdchecnt    | 누적매도체결건수       | Number       | Y          | 8        |                                         |
| -s_mschecnt    | 누적순매수체결건수      | Number       | Y          | 8        |                                         |


### 💡 Request Example
```json
{
   "t8404InBlock" :{
      "focode" : "111T6000",
      "cvolume" : 0,
      "stime" : "0900",
      "etime" : "1600",
      "cts_time" : ""
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8404OutBlock1": [
        {
            "change": "00000500",
            "sign": "5",
            "ibasis": 7,
            "n_mdchecnt": 3991,
            "chetime": "1519494834",
            "offerho": 70800,
            "openyak": 291595,
            "j_openupdn": 0,
            "cvolume": 197,
            "n_mdvolume": "000000443424",
            "volume": "000000811347",
            "chdegree": "82.82",
            "bidho": 70700,
            "s_mschecnt": -2445,
            "price": 70700,
            "kasis": "0.13",
            "s_msvolume": "-00000076196",
            "n_mschecnt": 1546,
            "jnilopenupdn": -247705,
            "n_msvolume": "000000367228",
            "sbasis": 100,
            "value": "000570684700"
        },
        {
            "change": "00000500",
            "sign": "5",
            "ibasis": 7,
            "n_mdchecnt": 3991,
            "chetime": "1519470921",
            "offerho": 70700,
            "openyak": 291595,
            "j_openupdn": -7739,
            "cvolume": 3,
            "n_mdvolume": "000000443424",
            "volume": "000000811150",
            "chdegree": "82.77",
            "bidho": 70600,
            "s_mschecnt": -2446,
            "price": 70700,
            "kasis": "-0.01",
            "s_msvolume": "-00000076393",
            "n_mschecnt": 1545,
            "jnilopenupdn": -247705,
            "n_msvolume": "000000367031",
            "sbasis": 0,
            "value": "000570545421"
        }
    ],
    "t8404OutBlock": {
        "cts_time": "1514124266"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 주식선물기간별주가(API용) (t8405)
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
| Element      | 한글명          | type   | Required   | Length   | Description                              |
|:-------------|:-------------|:-------|:-----------|:---------|:-----------------------------------------|
| t8405InBlock | t8405InBlock | Object | Y          | -        |                                          |
| -shcode      | 단축코드         | String | Y          | 8        |                                          |
| -futcheck    | 선물최근월물       | String | Y          | 1        | 0:default                                |
|              |              |        |            |          | 1:최근월물만연결                                |
| -date        | 날짜           | String | Y          | 8        | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 date 값으로 설정     |
| -cts_code    | CTS종목코드      | String | Y          | 8        | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 cts_code 값으로 설정 |
| -lastdate    | 전종목만기일       | String | Y          | 8        | 처음 조회시는 Space                            |
|              |              |        |            |          | 연속 조회시에 이전 조회한 OutBlock의 lastdate 값으로 설정 |
| -cnt         | 조회요청건수       | Object | Y          | 3        |                                          |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description                             |
|:---------------|:---------------|:-------------|:-----------|:---------|:----------------------------------------|
| t8405OutBlock  | t8405OutBlock  | Object       | Y          | -        |                                         |
| -date          | 날짜             | String       | Y          | 8        | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 date 필드에 넣어준다.     |
| -cts_code      | CTS종목코드        | String       | Y          | 8        | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 cts_code 필드에 넣어준다. |
| -lastdate      | 전종목만기일         | String       | Y          | 8        | 연속조회키                                   |
|                |                |              |            |          | 연속 조회시 이 값을 InBlock의 lastdate 필드에 넣어준다. |
| -nowfutyn      | 최근월선물여부        | String       | Y          | 1        |                                         |
| t8405OutBlock1 | t8405OutBlock1 | Object Array | Y          | -        |                                         |
| -date          | 날짜             | String       | Y          | 8        |                                         |
| -open          | 시가             | Number       | Y          | 8        |                                         |
| -high          | 고가             | Number       | Y          | 8        |                                         |
| -low           | 저가             | Number       | Y          | 8        |                                         |
| -close         | 종가             | Number       | Y          | 8        |                                         |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한                                    |
|                |                |              |            |          | 2:상승                                    |
|                |                |              |            |          | 3:보합                                    |
|                |                |              |            |          | 4:하한                                    |
|                |                |              |            |          | 5:하락                                    |
| -change        | 전일대비           | Number       | Y          | 8        |                                         |
| -diff          | 등락율            | Number       | Y          | 6.2      |                                         |
| -volume        | 거래량            | Number       | Y          | 12       |                                         |
| -diff_vol      | 거래증가율          | Number       | Y          | 10.2     |                                         |
| -openyak       | 미결수량           | Number       | Y          | 8        |                                         |
| -openyakupdn   | 미결증감           | Number       | Y          | 8        |                                         |
| -value         | 거래대금           | Number       | Y          | 12       |                                         |


### 💡 Request Example
```json
{
   "t8405InBlock" :{
      "shcode" : "111T6000",
      "futcheck" : "0",
      "date" : "",
      "cts_code" : "",
      "lastdate" : "",
      "cnt" : 20
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8405OutBlock": {
        "date": "20230509",
        "cts_code": "111T6000",
        "nowfutyn": "Y",
        "lastdate": ""
    },
    "t8405OutBlock1": [
        {
            "date": "20230608",
            "openyakupdn": -539300,
            "diff_vol": "-4.73",
            "change": 500,
            "sign": "5",
            "diff": "-0.70",
            "openyak": 0,
            "volume": 811347,
            "high": 70800,
            "low": 70000,
            "close": 70700,
            "value": "000570684700",
            "open": 70500
        },
        {
            "date": "20230607",
            "openyakupdn": -400372,
            "diff_vol": "-4.48",
            "change": 400,
            "sign": "5",
            "diff": "-0.56",
            "openyak": 539300,
            "volume": 851670,
            "high": 71600,
            "low": 70900,
            "close": 71200,
            "value": "000606460142",
            "open": 71300
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}

```

---

## 🏷️ 주식선물틱분별체결조회(API용) (t8406)
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
| Element      | 한글명          | type   | Required   | Length   | Description     |
|:-------------|:-------------|:-------|:-----------|:---------|:----------------|
| t8406InBlock | t8406InBlock | Object | Y          | -        |                 |
| -focode      | 단축코드         | String | Y          | 8        |                 |
| -cgubun      | 챠트구분         | String | Y          | 1        | T:틱차트           |
|              |              |        |            |          | B:분차트           |
| -bgubun      | 분구분          | Object | Y          | 3        | 차트구분이 'B'일때만 체크 |
|              |              |        |            |          | 0: 30초          |
|              |              |        |            |          | 0초과 : n분        |
| -cnt         | 조회건수         | Object | Y          | 3        |                 |


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
| t8406OutBlock1 | t8406OutBlock1 | Object Array | Y          | -        |               |
| -chetime       | 시간             | String       | Y          | 10       |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 전일대비구분         | String       | Y          | 1        | 1:상한          |
|                |                |              |            |          | 2:상승          |
|                |                |              |            |          | 3:보합          |
|                |                |              |            |          | 4:하한          |
|                |                |              |            |          | 5:하락          |
| -change        | 전일대비           | Number       | Y          | 8        |               |
| -open          | 시가             | Number       | Y          | 8        |               |
| -high          | 고가             | Number       | Y          | 8        |               |
| -low           | 저가             | Number       | Y          | 8        |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |
| -openyak       | 미결수량           | Number       | Y          | 8        |               |
| -openupdn      | 미결증감           | Number       | Y          | 8        |               |
| -cvolume       | 체결수량           | Number       | Y          | 8        |               |
| -s_mschecnt    | 매수순간체결건수       | Number       | Y          | 8        |               |
| -s_mdchecnt    | 매도순간체결건수       | Number       | Y          | 8        |               |
| -ss_mschecnt   | 순매수순간체결건수      | Number       | Y          | 8        |               |
| -s_mschevol    | 매수순간체결량        | Number       | Y          | 12       |               |
| -s_mdchevol    | 매도순간체결량        | Number       | Y          | 12       |               |
| -ss_mschevol   | 순매수순간체결량       | Number       | Y          | 12       |               |
| -chdegvol      | 체결강도(거래량)      | Number       | Y          | 8.2      |               |
| -chdegcnt      | 체결강도(건수)       | Number       | Y          | 8.2      |               |


### 💡 Request Example
```json
{
   "t8406InBlock" :{
      "focode" : "111T6000",
      "cgubun" : "T",
      "bgubun" : 0,
      "cnt" : 20
   }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8406OutBlock1": [
        {
            "s_mdchecnt": 0,
            "change": 500,
            "sign": "5",
            "chdegcnt": "38.74",
            "ss_mschecnt": 1,
            "chetime": "151949",
            "openyak": 291595,
            "s_mschevol": "000000000197",
            "cvolume": 197,
            "volume": "000000811347",
            "high": 0,
            "chdegvol": "82.82",
            "s_mschecnt": 1,
            "low": 0,
            "openupdn": 0,
            "price": 70700,
            "value": "570684700000",
            "s_mdchevol": "000000000000",
            "ss_mschevol": "000000000197",
            "open": 0
        },
        {
            "s_mdchecnt": 0,
            "change": 500,
            "sign": "5",
            "chdegcnt": "38.71",
            "ss_mschecnt": 1,
            "chetime": "151947",
            "openyak": 291595,
            "s_mschevol": "000000000003",
            "cvolume": 3,
            "volume": "000000811150",
            "high": 0,
            "chdegvol": "82.77",
            "s_mschecnt": 1,
            "low": 0,
            "openupdn": -7739,
            "price": 70700,
            "value": "570545421000",
            "s_mdchevol": "000000000000",
            "ss_mschevol": "000000000003",
            "open": 0
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 상품선물마스터조회(API용) (t8426)
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
| t8426InBlock | t8426InBlock | Object | Y          | -        |               |
| -dummy       | Dummy        | String | Y          | 1        |               |


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
| t8426OutBlock | t8426OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8426InBlock": {
    "dummy": ""
  }
}
```

### 💡 Response Example
```json
{
    "t8426OutBlock": [
        {
            "shcode": "165T6000",
            "expcode": "KR4165T60001",
            "hname": "3년국채    F 202306"
        },
        {
            "shcode": "165T9000",
            "expcode": "KR4165T90008",
            "hname": "3년국채    F 202309"
        },
        {
            "shcode": "166T6000",
            "expcode": "KR4166T60009",
            "hname": "5년국채    F 202306"
        }
    ],
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 과거데이터시간대별조회 (t8427)
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
| Element      | 한글명          | type   | Required   | Length   | Description                |
|:-------------|:-------------|:-------|:-----------|:---------|:---------------------------|
| t8427InBlock | t8427InBlock | Object | Y          | -        |                            |
| -fo_gbn      | 선물옵션구분       | String | Y          | 1        | F:선물                       |
|              |              |        |            |          | O:옵션                       |
| -yyyy        | 조회년도         | String | Y          | 4        | YYYY                       |
| -mm          | 조회월          | String | Y          | 2        | MM                         |
| -cp_gbn      | 옵션콜풋구분       | String | Y          | 1        | 2:콜                        |
|              |              |        |            |          | 3:풋                        |
| -actprice    | 옵션행사가        | Number | Y          | 6.2      |                            |
| -focode      | 선물옵션코드       | String | Y          | 8        |                            |
| -dt_gbn      | 일분구분         | String | Y          | 1        | D:일                        |
|              |              |        |            |          | M:분                        |
| -min_term    | 분간격          | String | Y          | 2        |                            |
| -date        | 날짜           | String | Y          | 8        | 다음 조회시 OutBlock의 date 값 입력 |
|              |              |        |            |          | 처음 조회시 Space               |
| -time        | 시간           | String | Y          | 6        | 다음 조회시 OutBlock의 time 값 입력 |
|              |              |        |            |          | 처음 조회시 Space               |


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
| t8427OutBlock  | t8427OutBlock  | Object       | Y          | -        |               |
| -focode        | 선물옵션코드         | String       | Y          | 8        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| t8427OutBlock1 | t8427OutBlock1 | Object Array | Y          | -        |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -close         | 종가             | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -diff_vol      | 거래증가율          | Number       | Y          | 10.2     |               |
| -openyak       | 미결수량           | Number       | Y          | 8        |               |
| -openyakupdn   | 미결증감           | Number       | Y          | 8        |               |
| -value         | 거래대금           | Number       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t8427InBlock": {
    "fo_gbn": "F",
    "yyyy": "2023",
    "mm": "05",
    "cp_gbn": "2",
    "actprice": 0.00,
    "focode": "101T6000",
    "dt_gbn": "D",
    "min_term": "",
    "date": "",
    "time": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t8427OutBlock": {
        "date": "20230209",
        "time": "",
        "focode": "101T3000"
    },
    "t8427OutBlock1": [
        {
            "date": "20230309",
            "openyakupdn": -118144,
            "diff_vol": "-36.42",
            "change": "0.70",
            "sign": "5",
            "diff": "-0.22",
            "openyak": 0,
            "volume": 127279,
            "high": "316.85",
            "low": "313.70",
            "time": "",
            "close": "313.95",
            "value": "10030940",
            "open": "316.50"
        },
        {
            "date": "20230308",
            "openyakupdn": -46160,
            "diff_vol": "4.24",
            "change": "4.75",
            "sign": "5",
            "diff": "-1.48",
            "openyak": 118144,
            "volume": 200201,
            "high": "316.70",
            "low": "314.25",
            "time": "",
            "close": "314.65",
            "value": "15783656",
            "open": "316.20"
        }
    ]
}
```

---

## 🏷️ 지수선물마스터조회API용 (t8432)
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
| Element      | 한글명          | type   | Required   | Length   | Description         |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------|
| t8432InBlock | t8432InBlock | Object | Y          | -        |                     |
| -gubun       | 구분           | String | Y          | 1        | V:변동성지수선물           |
|              |              |        |            |          | S:섹터지수선물            |
|              |              |        |            |          | 그 이외의 값은 코스피200지수선물 |


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
| t8432OutBlock | t8432OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |
| -uplmtprice   | 상한가           | Number       | Y          | 6.2      |               |
| -dnlmtprice   | 하한가           | Number       | Y          | 6.2      |               |
| -jnilclose    | 전일종가          | Number       | Y          | 6.2      |               |
| -jnilhigh     | 전일고가          | Number       | Y          | 6.2      |               |
| -jnillow      | 전일저가          | Number       | Y          | 6.2      |               |
| -recprice     | 기준가           | Number       | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t8432InBlock": {
    "gubun": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8432OutBlock": [
        {
            "jnilhigh": "350.35",
            "recprice": "346.20",
            "shcode": "101T9000",
            "jnilclose": "346.20",
            "uplmtprice": "398.10",
            "expcode": "KR4101T90003",
            "hname": "F 2309",
            "jnillow": "345.15",
            "dnlmtprice": "318.55"
        },
        {
            "jnilhigh": "0.00",
            "recprice": "0.00",
            "shcode": "401T9WCS",
            "jnilclose": "0.00",
            "uplmtprice": "30.30",
            "expcode": "KR4401T9WCS9",
            "hname": "F SP 09-2512",
            "jnillow": "0.00",
            "dnlmtprice": "-4.30"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 지수옵션마스터조회API용 (t8433)
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
| t8433InBlock | t8433InBlock | Object | Y          | -        |               |
| -dummy       | Dummy        | String | Y          | 1        |               |


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
| t8433OutBlock | t8433OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |
| -hprice       | 상한가           | Number       | Y          | 6.2      |               |
| -lprice       | 하한가           | Number       | Y          | 6.2      |               |
| -jnilclose    | 전일종가          | Number       | Y          | 6.2      |               |
| -jnilhigh     | 전일고가          | Number       | Y          | 6.2      |               |
| -jnillow      | 전일저가          | Number       | Y          | 6.2      |               |
| -recprice     | 기준가           | Number       | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t8433InBlock": {
    "dummy": ""
  }
}
```

### 💡 Response Example
```json
{
    "t8433OutBlock": [
        {
            "jnilhigh": "0.00",
            "recprice": "127.95",
            "hprice": "175.80",
            "lprice": "102.90",
            "shcode": "201T7185",
            "jnilclose": "127.95",
            "expcode": "KR4201T71852",
            "hname": "C 2307 185.0",
            "jnillow": "0.00"
        },
        {
            "jnilhigh": "0.00",
            "recprice": "62.00",
            "hprice": "159.20",
            "lprice": "0.01",
            "shcode": "201V6330",
            "jnilclose": "62.00",
            "expcode": "KR4201V63301",
            "hname": "C 2406 330.0",
            "jnillow": "0.00"
        },
        {
            "jnilhigh": "0.00",
            "recprice": "54.05",
            "hprice": "145.30",
            "lprice": "0.01",
            "shcode": "201V6335",
            "jnilclose": "54.05",
            "expcode": "KR4201V63350",
            "hname": "C 2406 335.0",
            "jnillow": "0.00"
        }
    ],
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 선물/옵션멀티현재가조회 (t8434)
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
| Element      | 한글명          | type   | Required   | Length   | Description         |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------|
| t8434InBlock | t8434InBlock | Object | Y          | -        |                     |
| -qrycnt      | 건수           | Number | Y          | 3        | 최대50개까지             |
| -focode      | 단축코드         | String | Y          | 400      | 구분자 없이 종목코드를 붙여서 입력 |


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
| t8434OutBlock1 | t8434OutBlock1 | Object Array | Y          | -        |               |
| -hname         | 한글명            | String       | Y          | 20       |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 누적거래량          | Number       | Y          | 12       |               |
| -checnt        | 체결건수           | Number       | Y          | 8        |               |
| -focode        | 단축코드           | String       | Y          | 8        |               |


### 💡 Request Example
```json
{
  "t8434InBlock": {
    "qrycnt": 1,
    "focode": "101T6000"
  }
}

```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8434OutBlock1": [
        {
            "volume": 119523,
            "checnt": 51756,
            "price": "342.30",
            "change": "0.95",
            "sign": "5",
            "diff": "0.28",
            "hname": "코스피200 F 202306",
            "focode": "101T6000"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 파생종목마스터조회API용 (t8435)
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
| Element      | 한글명          | type   | Required   | Length   | Description                                                     |
|:-------------|:-------------|:-------|:-----------|:---------|:----------------------------------------------------------------|
| t8435InBlock | t8435InBlock | Object | Y          | -        |                                                                 |
| -gubun       | 구분(MF/MO)    | String | Y          | 2        | MF : 미니선물MO : 미니옵션WK : 코스피200위클리옵션SF : 코스닥150선물QW : 코스닥150위클리옵션 |


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
| t8435OutBlock | t8435OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |
| -uplmtprice   | 상한가           | Number       | Y          | 6.2      |               |
| -dnlmtprice   | 하한가           | Number       | Y          | 6.2      |               |
| -jnilclose    | 전일종가          | Number       | Y          | 6.2      |               |
| -jnilhigh     | 전일고가          | Number       | Y          | 6.2      |               |
| -jnillow      | 전일저가          | Number       | Y          | 6.2      |               |
| -recprice     | 기준가           | Number       | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t8435InBlock": {
    "gubun": "SF"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t8435OutBlock": [
        {
            "jnilhigh": "1349.8",
            "recprice": "1348.7",
            "shcode": "106T6000",
            "jnilclose": "1348.7",
            "uplmtprice": "1456.5",
            "expcode": "KR4106T60005",
            "hname": "KQF 2306",
            "jnillow": "1323.9",
            "dnlmtprice": "1240.9"
        },
        {
            "jnilhigh": "1348.5",
            "recprice": "1348.5",
            "shcode": "106T9000",
            "jnilclose": "1348.5",
            "uplmtprice": "1456.3",
            "expcode": "KR4106T90002",
            "hname": "KQF 2309",
            "jnillow": "1320.2",
            "dnlmtprice": "1240.7"
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 지수선물마스터조회API용 (t9943)
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
| Element      | 한글명          | type   | Required   | Length   | Description         |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------------|
| t9943InBlock | t9943InBlock | Object | Y          | -        |                     |
| -gubun       | 구분           | String | Y          | 1        | V:변동성지수선물           |
|              |              |        |            |          | S:섹터지수선물            |
|              |              |        |            |          | 그 이외의 값은 코스피200지수선물 |


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
| t9943OutBlock | t9943OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t9943InBlock": {
    "gubun": "V"
  }
}
```

### 💡 Response Example
```json
{
    "t9943OutBlock": [
        {
            "shcode": "104T6000",
            "expcode": "KR4104T60000",
            "hname": "VF 2306"
        },
        {
            "shcode": "104T7000",
            "expcode": "KR4104T70009",
            "hname": "VF 2307"
        },
        {
            "shcode": "104T8000",
            "expcode": "KR4104T80008",
            "hname": "VF 2308"
        },
        {
            "shcode": "104T9000",
            "expcode": "KR4104T90007",
            "hname": "VF 2309"
        },
        {
            "shcode": "104TA000",
            "expcode": "KR4104TA0007",
            "hname": "VF 2310"
        },
        {
            "shcode": "104TB000",
            "expcode": "KR4104TB0006",
            "hname": "VF 2311"
        },
        {
            "shcode": "404T6T7S",
            "expcode": "KR4404T6T7S7",
            "hname": "VF SP 06-2307"
        },
        {
            "shcode": "404T6T8S",
            "expcode": "KR4404T6T8S5",
            "hname": "VF SP 06-2308"
        },
        {
            "shcode": "404T6T9S",
            "expcode": "KR4404T6T9S3",
            "hname": "VF SP 06-2309"
        },
        {
            "shcode": "404T6TAS",
            "expcode": "KR4404T6TAS2",
            "hname": "VF SP 06-2310"
        },
        {
            "shcode": "404T6TBS",
            "expcode": "KR4404T6TBS0",
            "hname": "VF SP 06-2311"
        }
    ],
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ 지수옵션마스터조회API용 (t9944)
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
| t9944InBlock | t9944InBlock | Object | Y          | -        |               |
| -dummy       | Dummy        | String | Y          | 1        |               |


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
| t9944OutBlock | t9944OutBlock | Object Array | Y          | -        |               |
| -hname        | 종목명           | String       | Y          | 20       |               |
| -shcode       | 단축코드          | String       | Y          | 8        |               |
| -expcode      | 확장코드          | String       | Y          | 12       |               |


### 💡 Request Example
```json
{
  "t9944InBlock": {
    "dummy": ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t9944OutBlock": [
        {
            "shcode": "201T6160",
            "expcode": "KR4201T61606",
            "hname": "C 2306 160.0"
        },
        {
            "shcode": "201T6162",
            "expcode": "KR4201T61622",
            "hname": "C 2306 162.5"
        },
        {
            "shcode": "201T6165",
            "expcode": "KR4201T61655",
            "hname": "C 2306 165.0"
        },
        {
            "shcode": "201T6167",
            "expcode": "KR4201T61671",
            "hname": "C 2306 167.5"
        },
        {
            "shcode": "201T6170",
            "expcode": "KR4201T61705",
            "hname": "C 2306 170.0"
        },
        {
            "shcode": "201T6172",
            "expcode": "KR4201T61721",
            "hname": "C 2306 172.5"
        }
  ]
}

```

---

## 🏷️ KRX야간파생 마스터조회(API용) (t8455)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명             | type   | Required   | Length   | Description                                                                                                               |
|:-------------|:----------------|:-------|:-----------|:---------|:--------------------------------------------------------------------------------------------------------------------------|
| t8455InBlock | t8455InBlock    | Object | Y          |          |                                                                                                                           |
| -gubun       | 구분(NF/NC/NM/NO) | String | Y          | 2        | - 선물 gubunNFU : KOSPI200선물NMF : 미니선물NQF : 코스닥150선물NCF : 상품선물- 옵션 gubunNOP : KOSPI200옵션NMO : 미니옵션NQO : 코스닥150옵션NWO : 위클리옵션 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element       | 한글명                    | type         | Required   | Length   | Description   |
|:--------------|:-----------------------|:-------------|:-----------|:---------|:--------------|
| t8455OutBlock | t8455OutBlock          | Object Array | Y          |          |               |
| -hname        | 종목명                    | String       | Y          | 20       |               |
| -shcode       | 종목코드                   | String       | Y          | 8        |               |
| -expcode      | 표준코드                   | String       | Y          | 12       |               |
| -tradeunit    | 거래승수                   | Number       | Y          | 21.8     |               |
| -atmgb        | ATM구분(1:ATM2:ITM3:OTM) | String       | Y          | 1        |               |


### 💡 Request Example
```json
{
  "t8455InBlock": {
    "gubun": "NFU"
  }
}
```

### 💡 Response Example
```json
{
	"t8455OutBlock": [
		{
			"hname": "F 2506",
			"shcode": "101W6000",
			"expcode": "KR4101W60000",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F 2509",
			"shcode": "101W9000",
			"expcode": "KR4101W90007",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F 2512",
			"shcode": "101WC000",
			"expcode": "KR4101WC0003",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F 2603",
			"shcode": "A0163000",
			"expcode": "KR4A01630008",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F 2606",
			"shcode": "A0166000",
			"expcode": "KR4A01660005",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F 2612",
			"shcode": "A016C000",
			"expcode": "KR4A016C0004",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F 2712",
			"shcode": "A017C000",
			"expcode": "KR4A017C0003",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F SP 06-2509",
			"shcode": "401W6W9S",
			"expcode": "KR4401W6W9S8",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F SP 06-2512",
			"shcode": "401W6WCS",
			"expcode": "KR4401W6WCS0",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F SP 06-2603",
			"shcode": "401W663S",
			"expcode": "KR4401W663S0",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F SP 06-2606",
			"shcode": "401W666S",
			"expcode": "KR4401W666S3",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F SP 06-2612",
			"shcode": "401W66CS",
			"expcode": "KR4401W66CS7",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		},
		{
			"hname": "F SP 06-2712",
			"shcode": "401W67CS",
			"expcode": "KR4401W67CS5",
			"tradeunit": "250000.00000000",
			"atmgb": ""
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ KRX야간파생 시세조회(API용) (t8456)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| t8456InBlock | t8456InBlock | Object | Y          |          |               |
| -focode      | 단축코드         | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element            | 한글명            | type   | Required   | Length   | Description   |
|:-------------------|:---------------|:-------|:-----------|:---------|:--------------|
| t8456OutBlock      | t8456OutBlock  | Object | Y          |          |               |
| -hname             | 한글명            | String | Y          | 20       |               |
| -price             | 현재가            | Number | Y          | 6.2      |               |
| -sign              | 전일대비구분         | String | Y          | 1        |               |
| -change            | 전일대비           | Number | Y          | 6.2      |               |
| -jnilclose         | 전일종가           | Number | Y          | 6.2      |               |
| -diff              | 등락율            | Number | Y          | 6.2      |               |
| -volume            | 거래량            | Number | Y          | 12       |               |
| -value             | 거래대금           | Number | Y          | 12       |               |
| -open              | 시가             | Number | Y          | 6.2      |               |
| -high              | 고가             | Number | Y          | 6.2      |               |
| -low               | 저가             | Number | Y          | 6.2      |               |
| -recprice          | 기준가            | Number | Y          | 6.2      |               |
| -theoryprice       | 이론가            | Number | Y          | 6.2      |               |
| -actprice          | 행사가            | Number | Y          | 6.2      |               |
| -impv              | 내재가치           | Number | Y          | 6.2      |               |
| -timevl            | 시간가치           | Number | Y          | 6.2      |               |
| -kospijisu         | KOSPI200지수     | Number | Y          | 6.2      |               |
| -kospisign         | KOSPI200전일대비구분 | String | Y          | 1        |               |
| -kospichange       | KOSPI200전일대비   | Number | Y          | 6.2      |               |
| -kospidiff         | KOSPI200등락율    | Number | Y          | 6.2      |               |
| -cmeprice          | CME야간선물현재가     | Number | Y          | 6.2      |               |
| -cmesign           | CME야간선물전일대비구분  | String | Y          | 1        |               |
| -cmechange         | CME야간선물전일대비    | Number | Y          | 6.2      |               |
| -cmediff           | CME야간선물등락율     | Number | Y          | 6.2      |               |
| -cmefocode         | CME야간선물종목코드    | String | Y          | 8        |               |
| -uplmtprice        | 정규장적용상한가       | Number | Y          | 6.2      |               |
| -dnlmtprice        | 정규장적용하한가       | Number | Y          | 6.2      |               |
| -focode            | 단축코드           | String | Y          | 8        |               |
| -yeprice           | 예상체결가          | Number | Y          | 6.2      |               |
| -ysign             | 전일대비구분         | String | Y          | 1        |               |
| -ychange           | 전일대비           | Number | Y          | 6.2      |               |
| -ydiff             | 등락율            | Number | Y          | 6.2      |               |
| -danhochk          | 단일가호가여부        | String | Y          | 1        |               |
| -jnilvolume        | 전일거래량          | Number | Y          | 12       |               |
| -jnilvalue         | 전일거래대금         | Number | Y          | 12       |               |
| -uplmtprice_3rd    | 정규장3단계상한가      | Number | Y          | 6.2      |               |
| -dnlmtprice_3rd    | 정규장3단계하한가      | Number | Y          | 6.2      |               |
| -ndv_uplmtprice    | 야간장_적용상한가      | Number | Y          | 6.2      |               |
| -ndv_dnlmtprice    | 야간장_적용하한가      | Number | Y          | 6.2      |               |
| -ndv_rt_uplmtprice | 야간장_실시간상한가     | Number | Y          | 6.2      |               |
| -ndv_rt_dnlmtprice | 야간장_실시간하한가     | Number | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t8456InBlock": {
    "focode": "101W9000"
  }
}
```

### 💡 Response Example
```json
{
	"t8456OutBlock": {
		"hname": "코스피200 F 202509",
		"price": "424.70",
		"sign": "5",
		"change": "0.70",
		"jnilclose": "425.40",
		"diff": "-0.16",
		"volume": 11275,
		"value": 1196821488,
		"open": "425.05",
		"high": "425.30",
		"low": "423.60",
		"recprice": "425.40",
		"theoryprice": "0",
		"actprice": "0.00",
		"impv": "0.00",
		"timevl": "-3.97",
		"kospijisu": "428.67",
		"kospisign": "2",
		"kospichange": "4.26",
		"kospidiff": "1.00",
		"cmeprice": "424.70",
		"cmesign": "5",
		"cmechange": "0.70",
		"cmediff": "-0.16",
		"cmefocode": "101W9000",
		"uplmtprice": "459.40",
		"dnlmtprice": "391.40",
		"focode": "101W9000",
		"yeprice": "424.70",
		"ysign": "5",
		"ychange": "0.70",
		"ydiff": "-0.16",
		"danhochk": "0",
		"jnilvolume": 15296,
		"jnilvalue": 1621978500,
		"uplmtprice_3rd": "510.45",
		"dnlmtprice_3rd": "340.35",
		"ndv_uplmtprice": "459.40",
		"ndv_dnlmtprice": "391.40",
		"ndv_rt_uplmtprice": "459.40",
		"ndv_rt_dnlmtprice": "391.40"
	},
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---

## 🏷️ KRX야간파생 호가조회(API용) (t8457)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| t8457InBlock | t8457InBlock | Object | Y          |          |               |
| -shcode      | 단축코드         | String | Y          | 8        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element       | 한글명           | type   | Required   | Length   | Description   |
|:--------------|:--------------|:-------|:-----------|:---------|:--------------|
| t8457OutBlock | t8457OutBlock | Object | Y          |          |               |
| -hname        | 종목명           | String | Y          | 20       |               |
| -price        | 현재가           | Number | Y          | 6.2      |               |
| -sign         | 전일대비구분        | String | Y          | 1        |               |
| -change       | 전일대비          | Number | Y          | 6.2      |               |
| -diff         | 등락율           | Number | Y          | 6.2      |               |
| -volume       | 거래량           | Number | Y          | 12       |               |
| -jnilclose    | 전일종가          | Number | Y          | 6.2      |               |
| -offerho1     | 매도호가1         | Number | Y          | 6.2      |               |
| -bidho1       | 매수호가1         | Number | Y          | 6.2      |               |
| -offerrem1    | 매도호가수량1       | Number | Y          | 8        |               |
| -bidrem1      | 매수호가수량1       | Number | Y          | 8        |               |
| -dcnt1        | 매도호가건수1       | Number | Y          | 8        |               |
| -scnt1        | 매수호가건수1       | Number | Y          | 8        |               |
| -offerho2     | 매도호가2         | Number | Y          | 6.2      |               |
| -bidho2       | 매수호가2         | Number | Y          | 6.2      |               |
| -offerrem2    | 매도호가수량2       | Number | Y          | 8        |               |
| -bidrem2      | 매수호가수량2       | Number | Y          | 8        |               |
| -dcnt2        | 매도호가건수2       | Number | Y          | 8        |               |
| -scnt2        | 매수호가건수2       | Number | Y          | 8        |               |
| -offerho3     | 매도호가3         | Number | Y          | 6.2      |               |
| -bidho3       | 매수호가3         | Number | Y          | 6.2      |               |
| -offerrem3    | 매도호가수량3       | Number | Y          | 8        |               |
| -bidrem3      | 매수호가수량3       | Number | Y          | 8        |               |
| -dcnt3        | 매도호가건수3       | Number | Y          | 8        |               |
| -scnt3        | 매수호가건수3       | Number | Y          | 8        |               |
| -offerho4     | 매도호가4         | Number | Y          | 6.2      |               |
| -bidho4       | 매수호가4         | Number | Y          | 6.2      |               |
| -offerrem4    | 매도호가수량4       | Number | Y          | 8        |               |
| -bidrem4      | 매수호가수량4       | Number | Y          | 8        |               |
| -dcnt4        | 매도호가건수4       | Number | Y          | 8        |               |
| -scnt4        | 매수호가건수4       | Number | Y          | 8        |               |
| -offerho5     | 매도호가5         | Number | Y          | 6.2      |               |
| -bidho5       | 매수호가5         | Number | Y          | 6.2      |               |
| -offerrem5    | 매도호가수량5       | Number | Y          | 8        |               |
| -bidrem5      | 매수호가수량5       | Number | Y          | 8        |               |
| -dcnt5        | 매도호가건수5       | Number | Y          | 8        |               |
| -scnt5        | 매수호가건수5       | Number | Y          | 8        |               |
| -dvol         | 매도호가총수량       | Number | Y          | 8        |               |
| -svol         | 매수호가총수량       | Number | Y          | 8        |               |
| -toffernum    | 총매도호가건수       | Number | Y          | 8        |               |
| -tbidnum      | 총매수호가건수       | Number | Y          | 8        |               |
| -time         | 수신시간          | String | Y          | 6        |               |
| -shcode       | 단축코드          | String | Y          | 8        |               |


### 💡 Request Example
```json
{
  "t8457InBlock": {
    "shcode": "101W6000"
  }
}
```

### 💡 Response Example
```json
{
	"t8457OutBlock": {
		"hname": "코스피200 F 202506",
		"price": "407.50",
		"sign": "2",
		"change": "1.35",
		"diff": "0.33",
		"volume": 6969,
		"jnilclose": "406.15",
		"offerho1": "410.00",
		"bidho1": "407.50",
		"offerrem1": 5,
		"bidrem1": 75,
		"dcnt1": 1,
		"scnt1": 4,
		"offerho2": "430.00",
		"bidho2": "406.50",
		"offerrem2": 500,
		"bidrem2": 11,
		"dcnt2": 1,
		"scnt2": 2,
		"offerho3": "435.00",
		"bidho3": "406.45",
		"offerrem3": 500,
		"bidrem3": 2,
		"dcnt3": 1,
		"scnt3": 2,
		"offerho4": "0.00",
		"bidho4": "406.40",
		"offerrem4": 0,
		"bidrem4": 370,
		"dcnt4": 0,
		"scnt4": 3,
		"offerho5": "0.00",
		"bidho5": "406.30",
		"offerrem5": 0,
		"bidrem5": 10,
		"dcnt5": 0,
		"scnt5": 1,
		"dvol": 1005,
		"svol": 789,
		"toffernum": 3,
		"tbidnum": 122,
		"time": "160931",
		"shcode": "101W6000"
	},
	"rsp_cd": "00000",
	"rsp_msg": "조회완료"
}
```

---

## 🏷️ KRX야간파생 시간대별체결(API용) (t8458)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| t8458InBlock | t8458InBlock | Object | Y          |          |               |
| -focode      | 단축코드         | String | Y          | 8        |               |
| -cvolume     | 특이거래량        | Number | Y          | 12       |               |
| -stime       | 시작시간         | String | Y          | 4        |               |
| -etime       | 종료시간         | String | Y          | 4        |               |
| -cts_time    | 시간CTS        | String | Y          | 10       |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description   |
|:---------------|:---------------|:-------------|:-----------|:---------|:--------------|
| t8458OutBlock  | t8458OutBlock  | Object       | Y          |          |               |
| -cts_time      | 시간CTS          | String       | Y          | 10       |               |
| t8458OutBlock1 | t8458OutBlock1 | Object Array | Y          |          |               |
| -chetime       | 시간             | String       | Y          | 10       |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -cvolume       | 체결수량           | Number       | Y          | 8        |               |
| -chdegree      | 체결강도           | Number       | Y          | 8.2      |               |
| -offerho       | 매도호가           | Number       | Y          | 6.2      |               |
| -bidho         | 매수호가           | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -n_msvolume    | 누적매수체결량        | Number       | Y          | 12       |               |
| -n_mdvolume    | 누적매도체결량        | Number       | Y          | 12       |               |
| -s_msvolume    | 누적순매수체결량       | Number       | Y          | 12       |               |
| -n_mschecnt    | 누적매수체결건수       | Number       | Y          | 8        |               |
| -n_mdchecnt    | 누적매도체결건수       | Number       | Y          | 8        |               |
| -s_mschecnt    | 누적순매수체결건수      | Number       | Y          | 8        |               |


### 💡 Request Example
```json
{
  "t8458InBlock": {
    "focode": "101W6000",
    "cvolume": 0,
    "stime": "",
    "etime": "",
    "cts_time": ""
  }
}
```

### 💡 Response Example
```json
{
	"t8458OutBlock": {
		"cts_time": "1609311813"
	},
	"t8458OutBlock1": [
		{
			"chetime": "1609471992",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 9,
			"chdegree": "144.55",
			"offerho": "407.50",
			"bidho": "406.50",
			"volume": "7045",
			"n_msvolume": "3063",
			"n_mdvolume": "2119",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 174,
			"s_mschecnt": 18
		},
		{
			"chetime": "1609464045",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 10,
			"chdegree": "145.17",
			"offerho": "407.95",
			"bidho": "407.50",
			"volume": "7036",
			"n_msvolume": "3063",
			"n_mdvolume": "2110",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 173,
			"s_mschecnt": 19
		},
		{
			"chetime": "1609460283",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 10,
			"chdegree": "145.86",
			"offerho": "407.95",
			"bidho": "407.50",
			"volume": "7026",
			"n_msvolume": "3063",
			"n_mdvolume": "2100",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 172,
			"s_mschecnt": 20
		},
		{
			"chetime": "1609455185",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 10,
			"chdegree": "146.56",
			"offerho": "407.95",
			"bidho": "407.50",
			"volume": "7016",
			"n_msvolume": "3063",
			"n_mdvolume": "2090",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 171,
			"s_mschecnt": 21
		},
		{
			"chetime": "1609446411",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 10,
			"chdegree": "147.26",
			"offerho": "407.95",
			"bidho": "407.50",
			"volume": "7006",
			"n_msvolume": "3063",
			"n_mdvolume": "2080",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 170,
			"s_mschecnt": 22
		},
		{
			"chetime": "1609442580",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 9,
			"chdegree": "147.97",
			"offerho": "407.90",
			"bidho": "407.50",
			"volume": "6996",
			"n_msvolume": "3063",
			"n_mdvolume": "2070",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 169,
			"s_mschecnt": 23
		},
		{
			"chetime": "1609370811",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 10,
			"chdegree": "148.62",
			"offerho": "407.90",
			"bidho": "407.50",
			"volume": "6987",
			"n_msvolume": "3063",
			"n_mdvolume": "2061",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 168,
			"s_mschecnt": 24
		},
		{
			"chetime": "1609327291",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.34",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6977",
			"n_msvolume": "3063",
			"n_mdvolume": "2051",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 167,
			"s_mschecnt": 25
		},
		{
			"chetime": "1609326459",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.41",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6976",
			"n_msvolume": "3063",
			"n_mdvolume": "2050",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 166,
			"s_mschecnt": 26
		},
		{
			"chetime": "1609324709",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.49",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6975",
			"n_msvolume": "3063",
			"n_mdvolume": "2049",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 165,
			"s_mschecnt": 27
		},
		{
			"chetime": "1609323787",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.56",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6974",
			"n_msvolume": "3063",
			"n_mdvolume": "2048",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 164,
			"s_mschecnt": 28
		},
		{
			"chetime": "1609321985",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.63",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6973",
			"n_msvolume": "3063",
			"n_mdvolume": "2047",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 163,
			"s_mschecnt": 29
		},
		{
			"chetime": "1609321137",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.71",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6972",
			"n_msvolume": "3063",
			"n_mdvolume": "2046",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 162,
			"s_mschecnt": 30
		},
		{
			"chetime": "1609319271",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.78",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6971",
			"n_msvolume": "3063",
			"n_mdvolume": "2045",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 161,
			"s_mschecnt": 31
		},
		{
			"chetime": "1609318470",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.85",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6970",
			"n_msvolume": "3063",
			"n_mdvolume": "2044",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 160,
			"s_mschecnt": 32
		},
		{
			"chetime": "1609316740",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "149.93",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6969",
			"n_msvolume": "3063",
			"n_mdvolume": "2043",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 159,
			"s_mschecnt": 33
		},
		{
			"chetime": "1609315925",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "150.00",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6968",
			"n_msvolume": "3063",
			"n_mdvolume": "2042",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 158,
			"s_mschecnt": 34
		},
		{
			"chetime": "1609314037",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "150.07",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6967",
			"n_msvolume": "3063",
			"n_mdvolume": "2041",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 157,
			"s_mschecnt": 35
		},
		{
			"chetime": "1609313226",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "150.15",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6966",
			"n_msvolume": "3063",
			"n_mdvolume": "2040",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 156,
			"s_mschecnt": 36
		},
		{
			"chetime": "1609311813",
			"price": "407.50",
			"sign": "2",
			"change": "1.35",
			"cvolume": 1,
			"chdegree": "150.22",
			"offerho": "410.00",
			"bidho": "407.50",
			"volume": "6965",
			"n_msvolume": "3063",
			"n_mdvolume": "2039",
			"s_msvolume": "0",
			"n_mschecnt": 192,
			"n_mdchecnt": 155,
			"s_mschecnt": 37
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ KRX야간파생 기간별주가(API용) (t8459)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명          | type   | Required   | Length   | Description   |
|:-------------|:-------------|:-------|:-----------|:---------|:--------------|
| t8459InBlock | t8459InBlock | Object | Y          |          |               |
| -shcode      | 단축코드         | String | Y          | 8        |               |
| -futcheck    | 선물최근월물       | String | Y          | 1        |               |
| -date        | 날짜           | String | Y          | 8        |               |
| -cts_code    | CTS종목코드      | String | Y          | 8        |               |
| -lastdate    | 전종목만기일       | String | Y          | 8        |               |
| -cnt         | 조회요청건수       | Object | Y          | 3        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description   |
|:---------------|:---------------|:-------------|:-----------|:---------|:--------------|
| t8459OutBlock  | t8459OutBlock  | Object       | Y          |          |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -cts_code      | CTS종목코드        | String       | Y          | 8        |               |
| -lastdate      | 전종목만기일         | String       | Y          | 8        |               |
| -nowfutyn      | 최근월선물여부        | String       | Y          | 1        |               |
| t8459OutBlock1 | t8459OutBlock1 | Object Array | Y          |          |               |
| -date          | 날짜             | String       | Y          | 8        |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -close         | 종가             | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -diff_vol      | 거래증가율          | Number       | Y          | 10.2     |               |


### 💡 Request Example
```json
{
   "t8459InBlock" :{
      "shcode" : "201W7342",
      "futcheck" : "",
      "date" : "",
      "cts_code" : "",
      "lastdate" : "",
      "cnt" : 20
   }
}
```

### 💡 Response Example
```json
{
	"t8459OutBlock": {
		"date": "",
		"cts_code": "201W7342",
		"lastdate": "",
		"nowfutyn": "N"
	},
	"t8459OutBlock1": [
		{
			"date": "20250610",
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"close": "33.70",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"diff_vol": "0.00"
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ KRX야간파생 옵션 전광판 (t8460)
### 요청 Header
| Element       | 한글명       | type   | Required   |   Length | Description   |
|:--------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type  | 컨텐츠타입     | String | Y          |      100 |               |
| authorization | 접근토큰      | String | Y          |     1000 |               |
| tr_cd         | 거래 CD     | String | Y          |       10 |               |
| tr_cont       | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key   | 연속 거래 Key | String | Y          |       18 |               |
| mac_address   | MAC 주소    | String | Y          |       12 |               |


### 요청 Body
| Element      | 한글명            | type   | Required   | Length   | Description         |
|:-------------|:---------------|:-------|:-----------|:---------|:--------------------|
| t8460InBlock | t8460InBlock   | Object | Y          |          |                     |
| -yyyymm      | 월물(혹은주물WN)     | String | Y          | 6        |                     |
| -gubun       | 구분(G:원지수W:위클리) | String | Y          | 1        | M:미니G:원지수Q:코스닥W:위클리 |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description   |
|:-------------|:----------|:-------|:-----------|---------:|:--------------|
| content-type | 컨텐츠타입     | String | Y          |      100 |               |
| tr_cd        | 거래 CD     | String | Y          |       10 |               |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 |               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 |               |


### 응답 Body
| Element        | 한글명            | type         | Required   | Length   | Description   |
|:---------------|:---------------|:-------------|:-----------|:---------|:--------------|
| t8460OutBlock  | t8460OutBlock  | Object       | Y          |          |               |
| -gmprice       | 근월물현재가         | Number       | Y          | 6.2      |               |
| -gmsign        | 근월물전일대비구분      | String       | Y          | 1        |               |
| -gmchange      | 근월물전일대비        | Number       | Y          | 6.2      |               |
| -gmdiff        | 근월물등락율         | Number       | Y          | 6.2      |               |
| -gmvolume      | 근월물거래량         | Number       | Y          | 12       |               |
| -gmshcode      | 근월물선물코드        | String       | Y          | 8        |               |
| t8460OutBlock1 | t8460OutBlock1 | Object Array | Y          |          |               |
| -actprice      | 행사가            | Number       | Y          | 6.2      |               |
| -optcode       | 콜옵션코드          | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -offerho1      | 매도호가           | Number       | Y          | 6.2      |               |
| -bidho1        | 매수호가           | Number       | Y          | 6.2      |               |
| -cvolume       | 체결량            | Number       | Y          | 12       |               |
| -impv          | 내재가치           | Number       | Y          | 6.2      |               |
| -timevl        | 시간가치           | Number       | Y          | 6.2      |               |
| -offerrem1     | 매도잔량           | Number       | Y          | 12       |               |
| -bidrem1       | 매수잔량           | Number       | Y          | 12       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -atmgubun      | ATM구분          | String       | Y          | 1        |               |
| -jisuconv      | 지수환산           | Number       | Y          | 6.2      |               |
| t8460OutBlock2 | t8460OutBlock2 | Object Array | Y          |          |               |
| -actprice      | 행사가            | Number       | Y          | 6.2      |               |
| -optcode       | 풋옵션코드          | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 6.2      |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 6.2      |               |
| -diff          | 등락율            | Number       | Y          | 6.2      |               |
| -volume        | 거래량            | Number       | Y          | 12       |               |
| -offerho1      | 매도호가           | Number       | Y          | 6.2      |               |
| -bidho1        | 매수호가           | Number       | Y          | 6.2      |               |
| -cvolume       | 체결량            | Number       | Y          | 12       |               |
| -impv          | 내재가치           | Number       | Y          | 6.2      |               |
| -timevl        | 시간가치           | Number       | Y          | 6.2      |               |
| -offerrem1     | 매도잔량           | Number       | Y          | 12       |               |
| -bidrem1       | 매수잔량           | Number       | Y          | 12       |               |
| -open          | 시가             | Number       | Y          | 6.2      |               |
| -high          | 고가             | Number       | Y          | 6.2      |               |
| -low           | 저가             | Number       | Y          | 6.2      |               |
| -atmgubun      | ATM구분          | String       | Y          | 1        |               |
| -jisuconv      | 지수환산           | Number       | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t8460InBlock": {
    "yyyymm": "202506",
    "gubun": "M"
  }
}
```

### 💡 Response Example
```json
{
	"t8460OutBlock": {
		"gmprice": "434.75",
		"gmsign": "2",
		"gmchange": "28.60",
		"gmdiff": "7.04",
		"gmvolume": 8274,
		"gmshcode": "101W6000"
	},
	"t8460OutBlock1": [
		{
			"actprice": "457.50",
			"optcode": "205W6457",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3416.67"
		},
		{
			"actprice": "455.00",
			"optcode": "205W6455",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3398.00"
		},
		{
			"actprice": "452.50",
			"optcode": "205W6452",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3379.33"
		},
		{
			"actprice": "450.00",
			"optcode": "205W6450",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3360.66"
		},
		{
			"actprice": "447.50",
			"optcode": "205W6447",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3341.99"
		},
		{
			"actprice": "445.00",
			"optcode": "205W6445",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3323.32"
		},
		{
			"actprice": "442.50",
			"optcode": "205W6442",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3304.65"
		},
		{
			"actprice": "440.00",
			"optcode": "205W6440",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3285.98"
		},
		{
			"actprice": "437.50",
			"optcode": "205W6437",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3267.31"
		},
		{
			"actprice": "435.00",
			"optcode": "205W6435",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3248.64"
		},
		{
			"actprice": "432.50",
			"optcode": "205W6432",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3229.97"
		},
		{
			"actprice": "430.00",
			"optcode": "205W6430",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3211.30"
		},
		{
			"actprice": "427.50",
			"optcode": "205W6427",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3192.63"
		},
		{
			"actprice": "425.00",
			"optcode": "205W6425",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3173.96"
		},
		{
			"actprice": "422.50",
			"optcode": "205W6422",
			"price": "0.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3155.29"
		},
		{
			"actprice": "420.00",
			"optcode": "205W6420",
			"price": "0.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3136.61"
		},
		{
			"actprice": "417.50",
			"optcode": "205W6417",
			"price": "0.09",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.09",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3117.94"
		},
		{
			"actprice": "415.00",
			"optcode": "205W6415",
			"price": "0.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3099.27"
		},
		{
			"actprice": "412.50",
			"optcode": "205W6412",
			"price": "0.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3080.60"
		},
		{
			"actprice": "410.00",
			"optcode": "205W6410",
			"price": "0.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3061.93"
		},
		{
			"actprice": "407.50",
			"optcode": "205W6407",
			"price": "0.04",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.04",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3043.26"
		},
		{
			"actprice": "405.00",
			"optcode": "205W6405",
			"price": "0.04",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.04",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3024.59"
		},
		{
			"actprice": "402.50",
			"optcode": "205W6402",
			"price": "0.04",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.04",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "3005.92"
		},
		{
			"actprice": "400.00",
			"optcode": "205W6400",
			"price": "0.13",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.13",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2987.25"
		},
		{
			"actprice": "397.50",
			"optcode": "205W6397",
			"price": "0.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2968.58"
		},
		{
			"actprice": "395.00",
			"optcode": "205W6395",
			"price": "0.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.02",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2949.91"
		},
		{
			"actprice": "392.50",
			"optcode": "205W6392",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2931.24"
		},
		{
			"actprice": "390.00",
			"optcode": "205W6390",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2912.57"
		},
		{
			"actprice": "387.50",
			"optcode": "205W6387",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2893.90"
		},
		{
			"actprice": "385.00",
			"optcode": "205W6385",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2875.23"
		},
		{
			"actprice": "382.50",
			"optcode": "205W6382",
			"price": "1.75",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "1.76",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "1.75",
			"offerrem1": 0,
			"bidrem1": 1,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2856.56"
		},
		{
			"actprice": "380.00",
			"optcode": "205W6380",
			"price": "7.24",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "7.24",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2837.89"
		},
		{
			"actprice": "377.50",
			"optcode": "205W6377",
			"price": "10.00",
			"sign": "5",
			"change": "6.00",
			"diff": "-37.50",
			"volume": 75,
			"offerho1": "10.00",
			"bidho1": "9.92",
			"cvolume": 13,
			"impv": "0.00",
			"timevl": "10.00",
			"offerrem1": 45,
			"bidrem1": 2,
			"open": "10.00",
			"high": "10.00",
			"low": "9.98",
			"atmgubun": "1",
			"jisuconv": "2819.22"
		},
		{
			"actprice": "375.00",
			"optcode": "205W6375",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 3,
			"offerho1": "0.01",
			"bidho1": "0.00",
			"cvolume": 3,
			"impv": "1.54",
			"timevl": "-1.53",
			"offerrem1": 2,
			"bidrem1": 0,
			"open": "0.01",
			"high": "0.01",
			"low": "0.01",
			"atmgubun": "2",
			"jisuconv": "2800.55"
		},
		{
			"actprice": "372.50",
			"optcode": "205W6372",
			"price": "11.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "4.04",
			"timevl": "6.96",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2781.88"
		},
		{
			"actprice": "370.00",
			"optcode": "205W6370",
			"price": "10.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "6.54",
			"timevl": "3.56",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2763.21"
		},
		{
			"actprice": "367.50",
			"optcode": "205W6367",
			"price": "10.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "9.04",
			"timevl": "0.96",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2744.54"
		},
		{
			"actprice": "365.00",
			"optcode": "205W6365",
			"price": "11.65",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "11.54",
			"timevl": "0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2725.87"
		},
		{
			"actprice": "362.50",
			"optcode": "205W6362",
			"price": "14.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "14.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2707.20"
		},
		{
			"actprice": "360.00",
			"optcode": "205W6360",
			"price": "16.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "16.54",
			"timevl": "-0.54",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2688.53"
		},
		{
			"actprice": "357.50",
			"optcode": "205W6357",
			"price": "19.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "19.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2669.86"
		},
		{
			"actprice": "355.00",
			"optcode": "205W6355",
			"price": "21.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "21.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2651.19"
		},
		{
			"actprice": "352.50",
			"optcode": "205W6352",
			"price": "24.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "24.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2632.52"
		},
		{
			"actprice": "350.00",
			"optcode": "205W6350",
			"price": "26.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "26.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2613.85"
		},
		{
			"actprice": "347.50",
			"optcode": "205W6347",
			"price": "29.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "29.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2595.18"
		},
		{
			"actprice": "345.00",
			"optcode": "205W6345",
			"price": "31.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "31.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2576.51"
		},
		{
			"actprice": "342.50",
			"optcode": "205W6342",
			"price": "34.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "34.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2557.83"
		},
		{
			"actprice": "340.00",
			"optcode": "205W6340",
			"price": "36.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "36.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2539.16"
		},
		{
			"actprice": "337.50",
			"optcode": "205W6337",
			"price": "39.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "39.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2520.49"
		},
		{
			"actprice": "335.00",
			"optcode": "205W6335",
			"price": "41.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "41.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2501.82"
		},
		{
			"actprice": "332.50",
			"optcode": "205W6332",
			"price": "44.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "44.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2483.15"
		},
		{
			"actprice": "330.00",
			"optcode": "205W6330",
			"price": "46.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "46.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2464.48"
		},
		{
			"actprice": "327.50",
			"optcode": "205W6327",
			"price": "49.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "49.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2445.81"
		},
		{
			"actprice": "325.00",
			"optcode": "205W6325",
			"price": "51.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "51.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2427.14"
		},
		{
			"actprice": "322.50",
			"optcode": "205W6322",
			"price": "54.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "54.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2408.47"
		},
		{
			"actprice": "320.00",
			"optcode": "205W6320",
			"price": "56.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "56.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2389.80"
		},
		{
			"actprice": "317.50",
			"optcode": "205W6317",
			"price": "59.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "59.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2371.13"
		},
		{
			"actprice": "315.00",
			"optcode": "205W6315",
			"price": "61.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "61.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2352.46"
		},
		{
			"actprice": "312.50",
			"optcode": "205W6312",
			"price": "64.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "64.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2333.79"
		},
		{
			"actprice": "310.00",
			"optcode": "205W6310",
			"price": "66.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "66.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2315.12"
		},
		{
			"actprice": "307.50",
			"optcode": "205W6307",
			"price": "69.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "69.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2296.45"
		},
		{
			"actprice": "305.00",
			"optcode": "205W6305",
			"price": "71.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "71.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2277.78"
		},
		{
			"actprice": "302.50",
			"optcode": "205W6302",
			"price": "74.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "74.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2259.11"
		},
		{
			"actprice": "300.00",
			"optcode": "205W6300",
			"price": "76.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "76.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2240.44"
		},
		{
			"actprice": "297.50",
			"optcode": "205W6297",
			"price": "79.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "79.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2221.77"
		},
		{
			"actprice": "295.00",
			"optcode": "205W6295",
			"price": "81.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "81.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2203.10"
		},
		{
			"actprice": "292.50",
			"optcode": "205W6292",
			"price": "84.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "84.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2184.43"
		},
		{
			"actprice": "290.00",
			"optcode": "205W6290",
			"price": "86.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "86.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2165.76"
		},
		{
			"actprice": "287.50",
			"optcode": "205W6287",
			"price": "89.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "89.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2147.09"
		},
		{
			"actprice": "285.00",
			"optcode": "205W6285",
			"price": "91.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "91.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2128.42"
		},
		{
			"actprice": "282.50",
			"optcode": "205W6282",
			"price": "94.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "94.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2109.75"
		},
		{
			"actprice": "280.00",
			"optcode": "205W6280",
			"price": "96.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "96.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2091.08"
		},
		{
			"actprice": "277.50",
			"optcode": "205W6277",
			"price": "99.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "99.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2072.41"
		},
		{
			"actprice": "275.00",
			"optcode": "205W6275",
			"price": "101.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "101.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2053.74"
		},
		{
			"actprice": "272.50",
			"optcode": "205W6272",
			"price": "104.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "104.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2035.07"
		},
		{
			"actprice": "270.00",
			"optcode": "205W6270",
			"price": "106.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "106.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2016.40"
		},
		{
			"actprice": "267.50",
			"optcode": "205W6267",
			"price": "109.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "109.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1997.73"
		},
		{
			"actprice": "265.00",
			"optcode": "205W6265",
			"price": "111.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "111.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1979.05"
		},
		{
			"actprice": "262.50",
			"optcode": "205W6262",
			"price": "114.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "114.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1960.38"
		},
		{
			"actprice": "260.00",
			"optcode": "205W6260",
			"price": "116.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "116.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1941.71"
		},
		{
			"actprice": "257.50",
			"optcode": "205W6257",
			"price": "119.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "119.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1923.04"
		},
		{
			"actprice": "255.00",
			"optcode": "205W6255",
			"price": "121.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "121.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1904.37"
		},
		{
			"actprice": "252.50",
			"optcode": "205W6252",
			"price": "124.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "124.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1885.70"
		},
		{
			"actprice": "250.00",
			"optcode": "205W6250",
			"price": "126.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "126.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1867.03"
		},
		{
			"actprice": "247.50",
			"optcode": "205W6247",
			"price": "129.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "129.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1848.36"
		},
		{
			"actprice": "245.00",
			"optcode": "205W6245",
			"price": "131.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "131.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1829.69"
		},
		{
			"actprice": "242.50",
			"optcode": "205W6242",
			"price": "134.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "134.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1811.02"
		},
		{
			"actprice": "240.00",
			"optcode": "205W6240",
			"price": "136.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "136.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1792.35"
		},
		{
			"actprice": "237.50",
			"optcode": "205W6237",
			"price": "139.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "139.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1773.68"
		},
		{
			"actprice": "235.00",
			"optcode": "205W6235",
			"price": "141.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "141.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1755.01"
		},
		{
			"actprice": "232.50",
			"optcode": "205W6232",
			"price": "144.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "144.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1736.34"
		},
		{
			"actprice": "230.00",
			"optcode": "205W6230",
			"price": "146.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "146.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1717.67"
		},
		{
			"actprice": "227.50",
			"optcode": "205W6227",
			"price": "149.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "149.04",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1699.00"
		},
		{
			"actprice": "225.00",
			"optcode": "205W6225",
			"price": "151.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "151.54",
			"timevl": "0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "1680.33"
		}
	],
	"t8460OutBlock2": [
		{
			"actprice": "457.50",
			"optcode": "305W6457",
			"price": "80.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "80.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3416.67"
		},
		{
			"actprice": "455.00",
			"optcode": "305W6455",
			"price": "78.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "78.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3398.00"
		},
		{
			"actprice": "452.50",
			"optcode": "305W6452",
			"price": "75.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "75.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3379.33"
		},
		{
			"actprice": "450.00",
			"optcode": "305W6450",
			"price": "73.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "73.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3360.66"
		},
		{
			"actprice": "447.50",
			"optcode": "305W6447",
			"price": "70.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "70.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3341.99"
		},
		{
			"actprice": "445.00",
			"optcode": "305W6445",
			"price": "68.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "68.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3323.32"
		},
		{
			"actprice": "442.50",
			"optcode": "305W6442",
			"price": "65.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "65.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3304.65"
		},
		{
			"actprice": "440.00",
			"optcode": "305W6440",
			"price": "63.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "63.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3285.98"
		},
		{
			"actprice": "437.50",
			"optcode": "305W6437",
			"price": "60.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "60.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3267.31"
		},
		{
			"actprice": "435.00",
			"optcode": "305W6435",
			"price": "58.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "58.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3248.64"
		},
		{
			"actprice": "432.50",
			"optcode": "305W6432",
			"price": "55.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "55.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3229.97"
		},
		{
			"actprice": "430.00",
			"optcode": "305W6430",
			"price": "53.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "53.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3211.30"
		},
		{
			"actprice": "427.50",
			"optcode": "305W6427",
			"price": "50.85",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "50.96",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3192.63"
		},
		{
			"actprice": "425.00",
			"optcode": "305W6425",
			"price": "48.35",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "48.46",
			"timevl": "-0.11",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3173.96"
		},
		{
			"actprice": "422.50",
			"optcode": "305W6422",
			"price": "45.90",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "45.96",
			"timevl": "-0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3155.29"
		},
		{
			"actprice": "420.00",
			"optcode": "305W6420",
			"price": "43.40",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "43.46",
			"timevl": "-0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3136.61"
		},
		{
			"actprice": "417.50",
			"optcode": "305W6417",
			"price": "40.90",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "40.96",
			"timevl": "-0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3117.94"
		},
		{
			"actprice": "415.00",
			"optcode": "305W6415",
			"price": "38.40",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "38.46",
			"timevl": "-0.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3099.27"
		},
		{
			"actprice": "412.50",
			"optcode": "305W6412",
			"price": "35.95",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "35.96",
			"timevl": "-0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3080.60"
		},
		{
			"actprice": "410.00",
			"optcode": "305W6410",
			"price": "33.45",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "33.46",
			"timevl": "-0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3061.93"
		},
		{
			"actprice": "407.50",
			"optcode": "305W6407",
			"price": "31.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "30.96",
			"timevl": "0.04",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3043.26"
		},
		{
			"actprice": "405.00",
			"optcode": "305W6405",
			"price": "28.60",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "28.46",
			"timevl": "0.14",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3024.59"
		},
		{
			"actprice": "402.50",
			"optcode": "305W6402",
			"price": "26.20",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "25.96",
			"timevl": "0.24",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "3005.92"
		},
		{
			"actprice": "400.00",
			"optcode": "305W6400",
			"price": "24.25",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "23.46",
			"timevl": "0.79",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2987.25"
		},
		{
			"actprice": "397.50",
			"optcode": "305W6397",
			"price": "21.40",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "20.96",
			"timevl": "0.44",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2968.58"
		},
		{
			"actprice": "395.00",
			"optcode": "305W6395",
			"price": "19.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "18.46",
			"timevl": "0.54",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2949.91"
		},
		{
			"actprice": "392.50",
			"optcode": "305W6392",
			"price": "16.70",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "15.96",
			"timevl": "0.74",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2931.24"
		},
		{
			"actprice": "390.00",
			"optcode": "305W6390",
			"price": "14.40",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "13.46",
			"timevl": "0.94",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2912.57"
		},
		{
			"actprice": "387.50",
			"optcode": "305W6387",
			"price": "12.20",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "10.96",
			"timevl": "1.24",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2893.90"
		},
		{
			"actprice": "385.00",
			"optcode": "305W6385",
			"price": "10.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "8.46",
			"timevl": "1.54",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2875.23"
		},
		{
			"actprice": "382.50",
			"optcode": "305W6382",
			"price": "8.02",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "5.96",
			"timevl": "2.06",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2856.56"
		},
		{
			"actprice": "380.00",
			"optcode": "305W6380",
			"price": "6.16",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "3.46",
			"timevl": "2.70",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "2",
			"jisuconv": "2837.89"
		},
		{
			"actprice": "377.50",
			"optcode": "305W6377",
			"price": "3.22",
			"sign": "5",
			"change": "1.84",
			"diff": "-36.36",
			"volume": 2,
			"offerho1": "10.00",
			"bidho1": "0.00",
			"cvolume": 1,
			"impv": "0.96",
			"timevl": "2.26",
			"offerrem1": 1,
			"bidrem1": 0,
			"open": "3.56",
			"high": "3.56",
			"low": "3.22",
			"atmgubun": "1",
			"jisuconv": "2819.22"
		},
		{
			"actprice": "375.00",
			"optcode": "305W6375",
			"price": "1.80",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "1.80",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2800.55"
		},
		{
			"actprice": "372.50",
			"optcode": "305W6372",
			"price": "2.80",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "2.80",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "2.80",
			"offerrem1": 2,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2781.88"
		},
		{
			"actprice": "370.00",
			"optcode": "305W6370",
			"price": "2.03",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "2.03",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2763.21"
		},
		{
			"actprice": "367.50",
			"optcode": "305W6367",
			"price": "1.10",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "1.10",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2744.54"
		},
		{
			"actprice": "365.00",
			"optcode": "305W6365",
			"price": "2.98",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "2.98",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2725.87"
		},
		{
			"actprice": "362.50",
			"optcode": "305W6362",
			"price": "5.44",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "5.44",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2707.20"
		},
		{
			"actprice": "360.00",
			"optcode": "305W6360",
			"price": "10.00",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "10.00",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2688.53"
		},
		{
			"actprice": "357.50",
			"optcode": "305W6357",
			"price": "6.72",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "6.72",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2669.86"
		},
		{
			"actprice": "355.00",
			"optcode": "305W6355",
			"price": "5.54",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "5.54",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2651.19"
		},
		{
			"actprice": "352.50",
			"optcode": "305W6352",
			"price": "4.42",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "4.42",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2632.52"
		},
		{
			"actprice": "350.00",
			"optcode": "305W6350",
			"price": "3.56",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "3.56",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2613.85"
		},
		{
			"actprice": "347.50",
			"optcode": "305W6347",
			"price": "2.55",
			"sign": "5",
			"change": "0.14",
			"diff": "-5.20",
			"volume": 10,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 10,
			"impv": "0.00",
			"timevl": "2.55",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "2.55",
			"high": "2.55",
			"low": "2.55",
			"atmgubun": "3",
			"jisuconv": "2595.18"
		},
		{
			"actprice": "345.00",
			"optcode": "305W6345",
			"price": "2.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 10,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 10,
			"impv": "0.00",
			"timevl": "2.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "2.01",
			"high": "2.01",
			"low": "2.01",
			"atmgubun": "3",
			"jisuconv": "2576.51"
		},
		{
			"actprice": "342.50",
			"optcode": "305W6342",
			"price": "1.42",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "1.42",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2557.83"
		},
		{
			"actprice": "340.00",
			"optcode": "305W6340",
			"price": "0.98",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.98",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2539.16"
		},
		{
			"actprice": "337.50",
			"optcode": "305W6337",
			"price": "0.51",
			"sign": "5",
			"change": "0.09",
			"diff": "-15.00",
			"volume": 10,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 10,
			"impv": "0.00",
			"timevl": "0.51",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.51",
			"high": "0.51",
			"low": "0.51",
			"atmgubun": "3",
			"jisuconv": "2520.49"
		},
		{
			"actprice": "335.00",
			"optcode": "305W6335",
			"price": "0.37",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.37",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2501.82"
		},
		{
			"actprice": "332.50",
			"optcode": "305W6332",
			"price": "0.20",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.20",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2483.15"
		},
		{
			"actprice": "330.00",
			"optcode": "305W6330",
			"price": "0.09",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.09",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2464.48"
		},
		{
			"actprice": "327.50",
			"optcode": "305W6327",
			"price": "0.04",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.04",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2445.81"
		},
		{
			"actprice": "325.00",
			"optcode": "305W6325",
			"price": "0.05",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.05",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2427.14"
		},
		{
			"actprice": "322.50",
			"optcode": "305W6322",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2408.47"
		},
		{
			"actprice": "320.00",
			"optcode": "305W6320",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2389.80"
		},
		{
			"actprice": "317.50",
			"optcode": "305W6317",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2371.13"
		},
		{
			"actprice": "315.00",
			"optcode": "305W6315",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2352.46"
		},
		{
			"actprice": "312.50",
			"optcode": "305W6312",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2333.79"
		},
		{
			"actprice": "310.00",
			"optcode": "305W6310",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2315.12"
		},
		{
			"actprice": "307.50",
			"optcode": "305W6307",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2296.45"
		},
		{
			"actprice": "305.00",
			"optcode": "305W6305",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2277.78"
		},
		{
			"actprice": "302.50",
			"optcode": "305W6302",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2259.11"
		},
		{
			"actprice": "300.00",
			"optcode": "305W6300",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2240.44"
		},
		{
			"actprice": "297.50",
			"optcode": "305W6297",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2221.77"
		},
		{
			"actprice": "295.00",
			"optcode": "305W6295",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2203.10"
		},
		{
			"actprice": "292.50",
			"optcode": "305W6292",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2184.43"
		},
		{
			"actprice": "290.00",
			"optcode": "305W6290",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2165.76"
		},
		{
			"actprice": "287.50",
			"optcode": "305W6287",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2147.09"
		},
		{
			"actprice": "285.00",
			"optcode": "305W6285",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2128.42"
		},
		{
			"actprice": "282.50",
			"optcode": "305W6282",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2109.75"
		},
		{
			"actprice": "280.00",
			"optcode": "305W6280",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2091.08"
		},
		{
			"actprice": "277.50",
			"optcode": "305W6277",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2072.41"
		},
		{
			"actprice": "275.00",
			"optcode": "305W6275",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2053.74"
		},
		{
			"actprice": "272.50",
			"optcode": "305W6272",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2035.07"
		},
		{
			"actprice": "270.00",
			"optcode": "305W6270",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "2016.40"
		},
		{
			"actprice": "267.50",
			"optcode": "305W6267",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1997.73"
		},
		{
			"actprice": "265.00",
			"optcode": "305W6265",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1979.05"
		},
		{
			"actprice": "262.50",
			"optcode": "305W6262",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1960.38"
		},
		{
			"actprice": "260.00",
			"optcode": "305W6260",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1941.71"
		},
		{
			"actprice": "257.50",
			"optcode": "305W6257",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1923.04"
		},
		{
			"actprice": "255.00",
			"optcode": "305W6255",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1904.37"
		},
		{
			"actprice": "252.50",
			"optcode": "305W6252",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1885.70"
		},
		{
			"actprice": "250.00",
			"optcode": "305W6250",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1867.03"
		},
		{
			"actprice": "247.50",
			"optcode": "305W6247",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1848.36"
		},
		{
			"actprice": "245.00",
			"optcode": "305W6245",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1829.69"
		},
		{
			"actprice": "242.50",
			"optcode": "305W6242",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1811.02"
		},
		{
			"actprice": "240.00",
			"optcode": "305W6240",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1792.35"
		},
		{
			"actprice": "237.50",
			"optcode": "305W6237",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1773.68"
		},
		{
			"actprice": "235.00",
			"optcode": "305W6235",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1755.01"
		},
		{
			"actprice": "232.50",
			"optcode": "305W6232",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1736.34"
		},
		{
			"actprice": "230.00",
			"optcode": "305W6230",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1717.67"
		},
		{
			"actprice": "227.50",
			"optcode": "305W6227",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1699.00"
		},
		{
			"actprice": "225.00",
			"optcode": "305W6225",
			"price": "0.01",
			"sign": "3",
			"change": "0.00",
			"diff": "0.00",
			"volume": 0,
			"offerho1": "0.00",
			"bidho1": "0.00",
			"cvolume": 0,
			"impv": "0.00",
			"timevl": "0.01",
			"offerrem1": 0,
			"bidrem1": 0,
			"open": "0.00",
			"high": "0.00",
			"low": "0.00",
			"atmgubun": "3",
			"jisuconv": "1680.33"
		}
	],
	"rsp_cd": "00000",
	"rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---
