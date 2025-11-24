# REST[주식] ETF
> 원본 URL: https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=30b6dfd6-b0bd-4e63-a510-7d5d94edc740

## 📌 기본 정보
| 항목           | 내용                                |
|:-------------|:----------------------------------|
| Method       | POST                              |
| Domain       | https://openapi.ls-sec.co.kr:8080 |
| 운영 도메인       | https://openapi.ls-sec.co.kr:8080 |
| 모의투자 도메인     |                                   |
| URL          | /stock/etf                        |
| Format       | JSON                              |
| Content-Type | application/json; charset=UTF-8   |
| Description  | ETF 시세 및 종목별정보를 확인할 수 있습니다.       |


## 🏷️ ETF현재가(시세)조회 (t1901)
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
| t1901InBlock | t1901InBlock | Object | Y          | -        |               |
| -shcode      | 단축코드         | String | Y          | 6        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element           | 한글명            | type   | Required   | Length   | Description   |
|:------------------|:---------------|:-------|:-----------|:---------|:--------------|
| t1901OutBlock     | t1901OutBlock  | Object | Y          | -        |               |
| -hname            | 한글명            | String | Y          | 20       |               |
| -price            | 현재가            | Number | Y          | 8        |               |
| -sign             | 전일대비구분         | String | Y          | 1        |               |
| -change           | 전일대비           | Number | Y          | 8        |               |
| -diff             | 등락율            | Number | Y          | 6.2      |               |
| -volume           | 누적거래량          | Number | Y          | 12       |               |
| -recprice         | 기준가            | Number | Y          | 8        |               |
| -avg              | 가중평균           | Number | Y          | 8        |               |
| -uplmtprice       | 상한가            | Number | Y          | 8        |               |
| -dnlmtprice       | 하한가            | Number | Y          | 8        |               |
| -jnilvolume       | 전일거래량          | Number | Y          | 12       |               |
| -volumediff       | 거래량차           | Number | Y          | 12       |               |
| -open             | 시가             | Number | Y          | 8        |               |
| -opentime         | 시가시간           | String | Y          | 6        |               |
| -high             | 고가             | Number | Y          | 8        |               |
| -hightime         | 고가시간           | String | Y          | 6        |               |
| -low              | 저가             | Number | Y          | 8        |               |
| -lowtime          | 저가시간           | String | Y          | 6        |               |
| -high52w          | 52최고가          | Number | Y          | 8        |               |
| -high52wdate      | 52최고가일         | String | Y          | 8        |               |
| -low52w           | 52최저가          | Number | Y          | 8        |               |
| -low52wdate       | 52최저가일         | String | Y          | 8        |               |
| -exhratio         | 소진율            | Number | Y          | 6.2      |               |
| -flmtvol          | 외국인보유수량        | Number | Y          | 12       |               |
| -per              | PER            | Number | Y          | 6.2      |               |
| -listing          | 상장주식수(천)       | Number | Y          | 12       |               |
| -jkrate           | 증거금율           | Number | Y          | 8        |               |
| -vol              | 회전율            | Number | Y          | 6.2      |               |
| -shcode           | 단축코드           | String | Y          | 6        |               |
| -value            | 누적거래대금         | Number | Y          | 12       |               |
| -highyear         | 연중최고가          | Number | Y          | 8        |               |
| -highyeardate     | 연중최고일자         | String | Y          | 8        |               |
| -lowyear          | 연중최저가          | Number | Y          | 8        |               |
| -lowyeardate      | 연중최저일자         | String | Y          | 8        |               |
| -upname           | 업종명            | String | Y          | 20       |               |
| -upcode           | 업종코드           | String | Y          | 3        |               |
| -upprice          | 업종현재가          | Number | Y          | 7.2      |               |
| -upsign           | 업종전일비구분        | String | Y          | 1        |               |
| -upchange         | 업종전일대비         | Number | Y          | 6.2      |               |
| -updiff           | 업종등락율          | Number | Y          | 6.2      |               |
| -futname          | 선물최근월물명        | String | Y          | 20       |               |
| -futcode          | 선물최근월물코드       | String | Y          | 8        |               |
| -futprice         | 선물현재가          | Number | Y          | 6.2      |               |
| -futsign          | 선물전일비구분        | String | Y          | 1        |               |
| -futchange        | 선물전일대비         | Number | Y          | 6.2      |               |
| -futdiff          | 선물등락율          | Number | Y          | 6.2      |               |
| -nav              | NAV            | Number | Y          | 8.2      |               |
| -navsign          | NAV전일대비구분      | String | Y          | 1        |               |
| -navchange        | NAV전일대비        | Number | Y          | 8.2      |               |
| -navdiff          | NAV등락율         | Number | Y          | 6.2      |               |
| -cocrate          | 추적오차율          | Number | Y          | 6.2      |               |
| -kasis            | 괴리율            | Number | Y          | 6.2      |               |
| -subprice         | 대용가            | Number | Y          | 10       |               |
| -offerno1         | 매도증권사코드1       | String | Y          | 6        |               |
| -bidno1           | 매수증권사코드1       | String | Y          | 6        |               |
| -dvol1            | 총매도수량1         | Number | Y          | 8        |               |
| -svol1            | 총매수수량1         | Number | Y          | 8        |               |
| -dcha1            | 매도증감1          | Number | Y          | 8        |               |
| -scha1            | 매수증감1          | Number | Y          | 8        |               |
| -ddiff1           | 매도비율1          | Number | Y          | 6.2      |               |
| -sdiff1           | 매수비율1          | Number | Y          | 6.2      |               |
| -offerno2         | 매도증권사코드2       | String | Y          | 6        |               |
| -bidno2           | 매수증권사코드2       | String | Y          | 6        |               |
| -dvol2            | 총매도수량2         | Number | Y          | 8        |               |
| -svol2            | 총매수수량2         | Number | Y          | 8        |               |
| -dcha2            | 매도증감2          | Number | Y          | 8        |               |
| -scha2            | 매수증감2          | Number | Y          | 8        |               |
| -ddiff2           | 매도비율2          | Number | Y          | 6.2      |               |
| -sdiff2           | 매수비율2          | Number | Y          | 6.2      |               |
| -offerno3         | 매도증권사코드3       | String | Y          | 6        |               |
| -bidno3           | 매수증권사코드3       | String | Y          | 6        |               |
| -dvol3            | 총매도수량3         | Number | Y          | 8        |               |
| -svol3            | 총매수수량3         | Number | Y          | 8        |               |
| -dcha3            | 매도증감3          | Number | Y          | 8        |               |
| -scha3            | 매수증감3          | Number | Y          | 8        |               |
| -ddiff3           | 매도비율3          | Number | Y          | 6.2      |               |
| -sdiff3           | 매수비율3          | Number | Y          | 6.2      |               |
| -offerno4         | 매도증권사코드4       | String | Y          | 6        |               |
| -bidno4           | 매수증권사코드4       | String | Y          | 6        |               |
| -dvol4            | 총매도수량4         | Number | Y          | 8        |               |
| -svol4            | 총매수수량4         | Number | Y          | 8        |               |
| -dcha4            | 매도증감4          | Number | Y          | 8        |               |
| -scha4            | 매수증감4          | Number | Y          | 8        |               |
| -ddiff4           | 매도비율4          | Number | Y          | 6.2      |               |
| -sdiff4           | 매수비율4          | Number | Y          | 6.2      |               |
| -offerno5         | 매도증권사코드5       | String | Y          | 6        |               |
| -bidno5           | 매수증권사코드5       | String | Y          | 6        |               |
| -dvol5            | 총매도수량5         | Number | Y          | 8        |               |
| -svol5            | 총매수수량5         | Number | Y          | 8        |               |
| -dcha5            | 매도증감5          | Number | Y          | 8        |               |
| -scha5            | 매수증감5          | Number | Y          | 8        |               |
| -ddiff5           | 매도비율5          | Number | Y          | 6.2      |               |
| -sdiff5           | 매수비율5          | Number | Y          | 6.2      |               |
| -fwdvl            | 외국계매도합계수량      | Number | Y          | 12       |               |
| -ftradmdcha       | 외국계매도직전대비      | Number | Y          | 12       |               |
| -ftradmddiff      | 외국계매도비율        | Number | Y          | 6.2      |               |
| -fwsvl            | 외국계매수합계수량      | Number | Y          | 12       |               |
| -ftradmscha       | 외국계매수직전대비      | Number | Y          | 12       |               |
| -ftradmsdiff      | 외국계매수비율        | Number | Y          | 6.2      |               |
| -upname2          | 참고지수명          | String | Y          | 20       |               |
| -upcode2          | 참고지수코드         | String | Y          | 3        |               |
| -upprice2         | 참고지수현재가        | Number | Y          | 7.2      |               |
| -jnilnav          | 전일NAV          | Number | Y          | 8.2      |               |
| -jnilnavsign      | 전일NAV전일대비구분    | String | Y          | 1        |               |
| -jnilnavchange    | 전일NAV전일대비      | Number | Y          | 8.2      |               |
| -jnilnavdiff      | 전일NAV등락율       | Number | Y          | 6.2      |               |
| -etftotcap        | 순자산총액(억원)      | Number | Y          | 12       |               |
| -spread           | 스프레드           | Number | Y          | 6.2      |               |
| -leverage         | 레버리지           | Number | Y          | 2        |               |
| -taxgubun         | 과세구분           | String | Y          | 1        |               |
| -opcom_nmk        | 운용사            | String | Y          | 20       |               |
| -lp_nm1           | LP1            | String | Y          | 20       |               |
| -lp_nm2           | LP2            | String | Y          | 20       |               |
| -lp_nm3           | LP3            | String | Y          | 20       |               |
| -lp_nm4           | LP4            | String | Y          | 20       |               |
| -lp_nm5           | LP5            | String | Y          | 20       |               |
| -etf_cp           | 복제방법           | String | Y          | 10       |               |
| -etf_kind         | 상품유형(Filler)   | String | Y          | 10       |               |
| -vi_gubun         | VI발동해제         | String | Y          | 10       |               |
| -etn_kind_cd      | ETN상품분류        | String | Y          | 20       |               |
| -lastymd          | ETN만기일         | String | Y          | 8        |               |
| -payday           | ETN지급일         | String | Y          | 8        |               |
| -lastdate         | ETN최종거래일       | String | Y          | 8        |               |
| -issuernmk        | ETN발행시장참가자     | String | Y          | 20       |               |
| -last_sdate       | ETN만기상환가격결정시작일 | String | Y          | 8        |               |
| -last_edate       | ETN만기상환가격결정종료일 | String | Y          | 8        |               |
| -lp_holdvol       | ETNLP보유수량      | String | Y          | 12       |               |
| -listdate         | 상장일            | String | Y          | 8        |               |
| -etp_gb           | ETP상품구분코드      | String | Y          | 1        |               |
| -etn_elback_yn    | ETN조기상환가능여부    | String | Y          | 1        |               |
| -settletype       | 최종결제           | String | Y          | 2        |               |
| -idx_asset_class1 | 지수자산분류코드(대분류)  | String | Y          | 2        |               |
| -ty_text          | ETF/ETN투자유의    | String | Y          | 8        |               |
| -leverage2        | 추적수익률배수        | Number | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t1901InBlock" : {
    "shcode" : "001200"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1901OutBlock": {
        "futcode": "101T6000",
        "jnilnavchange": "0",
        "opcom_nmk": "",
        "high52w": 3750,
        "jnilnavdiff": "0",
        "price": 3685,
        "per": "021.79",
        "hname": "유진투자증권",
        "updiff": "0",
        "futchange": "000.75",
        "nav": "00000.00",
        "issuernmk": "",
        "navchange": "00000.00",
        "diff": "000.68",
        "fwsvl": 110000,
        "low52w": 2185,
        "svol3": 24170,
        "etftotcap": 0,
        "upprice": "0",
        "futsign": "2",
        "svol2": 66206,
        "svol1": 110000,
        "svol5": 18102,
        "svol4": 20913,
        "leverage2": "000.00",
        "highyear": 3750,
        "bidno1": "에스지",
        "bidno3": "KB증권",
        "etn_elback_yn": "",
        "bidno2": "키움증",
        "bidno5": "NH투자",
        "bidno4": "신한투",
        "navsign": "3",
        "lastymd": "",
        "lastdate": "",
        "etn_kind_cd": "",
        "low": 3645,
        "ftradmsdiff": "034.14",
        "low52wdate": "20220930",
        "jnilnav": "0",
        "payday": "",
        "jkrate": 40,
        "listing": 96866,
        "upprice2": "0.00",
        "jnilnavsign": "",
        "volumediff": 951905,
        "change": 25,
        "uplmtprice": 4755,
        "futname": "F 202306",
        "lowtime": "090057",
        "settletype": "",
        "listdate": "19870824",
        "upchange": "0",
        "vi_gubun": "",
        "lp_holdvol": "000000000000",
        "fwdvl": 30884,
        "open": 3660,
        "offerno2": "미래에",
        "high52wdate": "20230605",
        "offerno1": "키움증",
        "offerno4": "삼성증",
        "offerno3": "신한투",
        "sign": "2",
        "scha4": 0,
        "navdiff": "000.00",
        "scha3": 0,
        "offerno5": "NH투자",
        "scha2": 5,
        "scha1": 0,
        "scha5": 0,
        "high": 3750,
        "last_edate": "",
        "etf_kind": "",
        "ty_text": "",
        "dvol1": 54814,
        "idx_asset_class1": "",
        "dvol2": 49011,
        "highyeardate": "20230605",
        "dvol3": 34055,
        "dvol4": 32384,
        "dvol5": 26162,
        "upname": "20230512",
        "futprice": "343.70",
        "ftradmscha": 0,
        "volume": "000000322192",
        "ftradmddiff": "009.59",
        "lp_nm1": "신영증권",
        "jnilvolume": "000001274097",
        "exhratio": "007.17",
        "lp_nm4": "",
        "lp_nm5": "",
        "lp_nm2": "eBEST 증권",
        "ddiff5": "008.12",
        "lp_nm3": "",
        "last_sdate": "",
        "ddiff4": "010.05",
        "ddiff3": "010.57",
        "ddiff2": "015.21",
        "ddiff1": "017.01",
        "lowyear": 2230,
        "leverage": 0,
        "etp_gb": "",
        "cocrate": "0",
        "dnlmtprice": 2565,
        "vol": "000.33",
        "dcha5": 0,
        "sdiff5": "005.62",
        "recprice": 3660,
        "avg": 3698,
        "dcha4": 0,
        "sdiff4": "006.49",
        "dcha3": 0,
        "sdiff3": "007.50",
        "upcode2": "",
        "dcha2": 0,
        "sdiff2": "020.55",
        "kasis": "0",
        "dcha1": 5,
        "sdiff1": "034.14",
        "value": 1192,
        "lowyeardate": "20230103",
        "upsign": "",
        "upname2": "",
        "ftradmdcha": 0,
        "shcode": "001200",
        "opentime": "090013",
        "taxgubun": "0",
        "spread": "000.14",
        "subprice": 2560,
        "hightime": "091719",
        "upcode": "000",
        "flmtvol": "000006944768",
        "futdiff": "000.22",
        "etf_cp": ""
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ ETF시간별추이 (t1902)
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
| Element      | 한글명          | type   | Required   | Length   | Description                         |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------------------|
| t1902InBlock | t1902InBlock | Object | Y          | -        |                                     |
| -shcode      | 단축코드         | String | Y          | 6        |                                     |
| -time        | 시간           | String | Y          | 6        | 연속조회키                               |
|              |              |        |            |          | 연속 조회시 이 값을 InBlock의 time 필드에 넣어준다. |


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
| t1902OutBlock  | t1902OutBlock  | Object       | Y          | -        |               |
| -time          | 시간             | String       | Y          | 6        |               |
| -hname         | 종목명            | String       | Y          | 20       |               |
| -upname        | 업종지수명          | String       | Y          | 20       |               |
| t1902OutBlock1 | t1902OutBlock1 | Object Array | Y          | -        |               |
| -time          | 시간             | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 8        |               |
| -volume        | 누적거래량          | Number       | Y          | 12       |               |
| -navdiff       | NAV대비          | Number       | Y          | 9.2      |               |
| -nav           | NAV            | Number       | Y          | 9.2      |               |
| -navchange     | 전일대비           | Number       | Y          | 9.2      |               |
| -crate         | 추적오차           | Number       | Y          | 9.2      |               |
| -grate         | 괴리             | Number       | Y          | 9.2      |               |
| -jisu          | 지수             | Number       | Y          | 8.2      |               |
| -jichange      | 전일대비           | Number       | Y          | 8.2      |               |
| -jirate        | 전일대비율          | Number       | Y          | 8.2      |               |


### 💡 Request Example
```json
{
  "t1902InBlock" : {
    "shcode" : "448330",
    "time" : ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1902OutBlock": {
        "upname": "",
        "time": "152954",
        "hname": "KODEX 삼성전자채권혼"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1902OutBlock1": [
        {
            "jirate": "0.00",
            "nav": "10683.10",
            "navchange": "-18.66",
            "change": 35,
            "grate": "-0.22",
            "sign": "5",
            "navdiff": "-23.10",
            "crate": "0.04",
            "jichange": "0.00",
            "volume": "13498",
            "jisu": "0.00",
            "price": 10660,
            "time": "장:마:감"
        },
        {
            "jirate": "0.00",
            "nav": "10683.79",
            "navchange": "-17.97",
            "change": 35,
            "grate": "-0.22",
            "sign": "5",
            "navdiff": "-23.79",
            "crate": "0.03",
            "jichange": "0.00",
            "volume": "13485",
            "jisu": "0.00",
            "price": 10660,
            "time": "15:30:30"
        }
    ]
}
```

---

## 🏷️ ETF일별추이 (t1903)
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
| Element      | 한글명          | type   | Required   | Length   | Description                         |
|:-------------|:-------------|:-------|:-----------|:---------|:------------------------------------|
| t1903InBlock | t1903InBlock | Object | Y          | -        |                                     |
| -shcode      | 단축코드         | String | Y          | 6        |                                     |
| -date        | 일자           | String | Y          | 8        | 연속조회키                               |
|              |              |        |            |          | 연속 조회시 이 값을 InBlock의 date 필드에 넣어준다. |


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
| t1903OutBlock  | t1903OutBlock  | Object       | Y          | -        |               |
| -date          | 일자             | String       | Y          | 8        |               |
| -hname         | 종목명            | String       | Y          | 20       |               |
| -upname        | 업종지수명          | String       | Y          | 20       |               |
| t1903OutBlock1 | t1903OutBlock1 | Object Array | Y          | -        |               |
| -date          | 일자             | String       | Y          | 8        |               |
| -price         | 현재가            | Number       | Y          | 8        |               |
| -sign          | 전일대비구분         | String       | Y          | 1        |               |
| -change        | 전일대비           | Number       | Y          | 8        |               |
| -volume        | 누적거래량          | Number       | Y          | 12       |               |
| -navdiff       | NAV대비          | Number       | Y          | 9.2      |               |
| -nav           | NAV            | Number       | Y          | 9.2      |               |
| -navchange     | 전일대비           | Number       | Y          | 9.2      |               |
| -crate         | 추적오차           | Number       | Y          | 9.2      |               |
| -grate         | 괴리             | Number       | Y          | 9.2      |               |
| -jisu          | 지수             | Number       | Y          | 8.2      |               |
| -jichange      | 전일대비           | Number       | Y          | 8.2      |               |
| -jirate        | 전일대비율          | Number       | Y          | 8.2      |               |


### 💡 Request Example
```json
{
  "t1903InBlock" : {
    "shcode" : "448330",
    "date" : ""
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1903OutBlock": {
        "date": "20230509",
        "upname": "",
        "hname": "KODEX 삼성전자채권혼"
    },
    "t1903OutBlock1": [
        {
            "date": "20230608",
            "jirate": "0.00",
            "nav": "10683.10",
            "navchange": "18.66",
            "change": 35,
            "grate": "-0.22",
            "sign": "5",
            "navdiff": "-23.10",
            "crate": "0.04",
            "jichange": "0.00",
            "volume": "13498",
            "jisu": "0.00",
            "price": 10660
        },
        {
            "date": "20230607",
            "jirate": "0.00",
            "nav": "10701.76",
            "navchange": "-24.79",
            "change": 35,
            "grate": "-0.06",
            "sign": "5",
            "navdiff": "-6.76",
            "crate": "0.52",
            "jichange": "0.00",
            "volume": "16803",
            "jisu": "0.00",
            "price": 10695
        }
    ],
    "rsp_msg": "정상적으로 조회가 완료되었습니다."
}
```

---

## 🏷️ ETF구성종목조회 (t1904)
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
| Element      | 한글명               | type   | Required   | Length   | Description   |
|:-------------|:------------------|:-------|:-----------|:---------|:--------------|
| t1904InBlock | t1904InBlock      | Object | Y          | -        |               |
| -shcode      | ETF단축코드           | String | Y          | 6        |               |
| -date        | PDF적용일자           | String | Y          | 8        |               |
| -sgb         | 정렬기준(1:평가금액2:증권수) | String | Y          | 1        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element        | 한글명                        | type         | Required   | Length   | Description   |
|:---------------|:---------------------------|:-------------|:-----------|:---------|:--------------|
| t1904OutBlock  | t1904OutBlock              | Object       | Y          | -        |               |
| -chk_tday      | 당일구분                       | String       | Y          | 1        |               |
| -date          | PDF적용일자                    | String       | Y          | 8        |               |
| -price         | ETF현재가                     | Number       | Y          | 8        |               |
| -sign          | ETF전일대비구분                  | String       | Y          | 1        |               |
| -change        | ETF전일대비                    | Number       | Y          | 8        |               |
| -diff          | ETF등락율                     | Number       | Y          | 6.2      |               |
| -volume        | ETF누적거래량                   | Number       | Y          | 12       |               |
| -nav           | NAV                        | Number       | Y          | 8.2      |               |
| -navsign       | NAV전일대비구분                  | String       | Y          | 1        |               |
| -navchange     | NAV전일대비                    | Number       | Y          | 8.2      |               |
| -navdiff       | NAV등락율                     | Number       | Y          | 6.2      |               |
| -jnilnav       | 전일NAV                      | Number       | Y          | 8.2      |               |
| -jnilnavsign   | 전일NAV전일대비구분                | String       | Y          | 1        |               |
| -jnilnavchange | 전일NAV전일대비                  | Number       | Y          | 8.2      |               |
| -jnilnavdiff   | 전일NAV등락율                   | Number       | Y          | 6.2      |               |
| -upname        | 업종명                        | String       | Y          | 20       |               |
| -upcode        | 업종코드                       | String       | Y          | 3        |               |
| -upprice       | 업종현재가                      | Number       | Y          | 7.2      |               |
| -upsign        | 업종전일비구분                    | String       | Y          | 1        |               |
| -upchange      | 업종전일대비                     | Number       | Y          | 6.2      |               |
| -updiff        | 업종등락율                      | Number       | Y          | 6.2      |               |
| -futname       | 선물최근월물명                    | String       | Y          | 20       |               |
| -futcode       | 선물최근월물코드                   | String       | Y          | 8        |               |
| -futprice      | 선물현재가                      | Number       | Y          | 6.2      |               |
| -futsign       | 선물전일비구분                    | String       | Y          | 1        |               |
| -futchange     | 선물전일대비                     | Number       | Y          | 6.2      |               |
| -futdiff       | 선물등락율                      | Number       | Y          | 6.2      |               |
| -upname2       | 참고지수명                      | String       | Y          | 20       |               |
| -upcode2       | 참고지수코드                     | String       | Y          | 3        |               |
| -upprice2      | 참고지수현재가                    | Number       | Y          | 7.2      |               |
| -etftotcap     | 순자산총액(단위:억)                | Number       | Y          | 12       |               |
| -etfnum        | 구성종목수                      | Number       | Y          | 4        |               |
| -etfcunum      | CU주식수                      | Number       | Y          | 12       |               |
| -cash          | 현금                         | Number       | Y          | 12       |               |
| -opcom_nmk     | 운용사명                       | String       | Y          | 20       |               |
| -tot_pval      | 전종목평가금액합                   | Number       | Y          | 12       |               |
| -tot_sigatval  | 전종목구성시가총액합                 | Number       | Y          | 12       |               |
| t1904OutBlock1 | t1904OutBlock1             | Object Array | Y          | -        |               |
| -shcode        | 단축코드                       | String       | Y          | 12       |               |
| -hname         | 한글명                        | String       | Y          | 20       |               |
| -price         | 현재가                        | Number       | Y          | 8        |               |
| -sign          | 전일대비구분                     | String       | Y          | 1        |               |
| -change        | 전일대비                       | Number       | Y          | 8        |               |
| -diff          | 등락율                        | Number       | Y          | 6.2      |               |
| -volume        | 누적거래량                      | Number       | Y          | 12       |               |
| -value         | 거래대금(백만)                   | Number       | Y          | 12       |               |
| -icux          | 단위증권수(계약수/원화현금/USD현금/창고증권) | Number       | Y          | 12       |               |
| -parprice      | 액면금액/설정현금액                 | Number       | Y          | 12       |               |
| -pvalue        | 평가금액                       | Number       | Y          | 12       |               |
| -sigatvalue    | 구성시가총액                     | Number       | Y          | 12       |               |
| -profitdate    | PDF적용일자                    | String       | Y          | 8        |               |
| -weight        | 비중(평가금액)                   | Number       | Y          | 6.2      |               |
| -diff2         | ETF종목과등락차                  | Number       | Y          | 6.2      |               |


### 💡 Request Example
```json
{
  "t1904InBlock" : {
    "shcode" : "448330",
    "date" : "20230104",
    "sgb" : "1"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "t1904OutBlock": {
        "date": "20230104",
        "futcode": "101T9000",
        "chk_tday": "0",
        "jnilnavchange": "-3.50",
        "opcom_nmk": "삼성자산운용(ETF)",
        "sign": "3",
        "navsign": "3",
        "navdiff": "0.00",
        "jnilnavdiff": "-0.03",
        "upcode2": "",
        "price": 10690,
        "jnilnav": "10689.10",
        "upprice2": "0",
        "cash": 0,
        "upsign": "",
        "upname2": "",
        "jnilnavsign": "5",
        "updiff": "0",
        "nav": "0.00",
        "upname": "？\u0006      p\r      鄒？",
        "futchange": "0.00",
        "navchange": "0.00",
        "etfnum": 7,
        "futprice": "351.70",
        "change": 0,
        "futname": "F 202309",
        "diff": "0.00",
        "tot_pval": 1008302135,
        "volume": 0,
        "upchange": "0",
        "upcode": "000",
        "etftotcap": 224,
        "upprice": "0",
        "futsign": "3",
        "tot_sigatval": 401022935,
        "etfcunum": 21,
        "futdiff": "0.00"
    },
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1904OutBlock1": [
        {
            "parprice": 0,
            "profitdate": "00000000",
            "shcode": "005930",
            "change": 2400,
            "sign": "2",
            "weight": "27.94",
            "diff": "4.33",
            "pvalue": 281709000,
            "icux": 5085,
            "sigatvalue": 293913000,
            "volume": 20188071,
            "price": 57800,
            "value": 1151474,
            "hname": "삼성전자",
            "diff2": "4.33"
        },
        {
            "parprice": 0,
            "profitdate": "",
            "shcode": "KR103501GC90",
            "change": 0,
            "sign": "",
            "weight": "19.57",
            "diff": "0",
            "pvalue": 0,
            "icux": 0,
            "sigatvalue": 0,
            "volume": 0,
            "price": 0,
            "value": 0,
            "hname": "국고03125-2709(22-8)",
            "diff2": "0"
        }
    ]
}
```

---

## 🏷️ ETFLP호가 (t1906)
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
| t1906InBlock | t1906InBlock | Object | Y          | -        |               |
| -shcode      | 단축코드         | String | Y          | 6        |               |


### 응답 Header
| Element      | 한글명       | type   | Required   |   Length | Description                                                                     |
|:-------------|:----------|:-------|:-----------|---------:|:--------------------------------------------------------------------------------|
| content-type | 컨텐츠타입     | String | Y          |      100 | LS증권 제공 API를 호출하기 위한 Request Body 데이터 포맷으로 "application/json; charset=utf-8 설정" |
| tr_cd        | 거래 CD     | String | Y          |       10 | LS증권 거래코드                                                                       |
| tr_cont      | 연속 거래 여부  | String | Y          |        1 | 연속거래 여부Y:연속○N:연속×                                                               |
| tr_cont_key  | 연속 거래 Key | String | Y          |       18 | 연속일 경우 그전에 내려온 연속키 값 올림                                                         |


### 응답 Body
| Element             | 한글명            | type   | Required   | Length   | Description   |
|:--------------------|:---------------|:-------|:-----------|:---------|:--------------|
| t1906OutBlock       | t1906OutBlock  | Object | Y          | -        |               |
| -hname              | 한글명            | String | Y          | 20       |               |
| -price              | 현재가            | Number | Y          | 8        |               |
| -sign               | 전일대비구분         | String | Y          | 1        |               |
| -change             | 전일대비           | Number | Y          | 8        |               |
| -diff               | 등락율            | Number | Y          | 6.2      |               |
| -volume             | 누적거래량          | Number | Y          | 12       |               |
| -lp_offerrem1       | LP매도호가수량1      | Number | Y          | 12       |               |
| -lp_bidrem1         | LP매수호가수량1      | Number | Y          | 12       |               |
| -lp_offerrem2       | LP매도호가수량2      | Number | Y          | 12       |               |
| -lp_bidrem2         | LP매수호가수량2      | Number | Y          | 12       |               |
| -lp_offerrem3       | LP매도호가수량3      | Number | Y          | 12       |               |
| -lp_bidrem3         | LP매수호가수량3      | Number | Y          | 12       |               |
| -lp_offerrem4       | LP매도호가수량4      | Number | Y          | 12       |               |
| -lp_bidrem4         | LP매수호가수량4      | Number | Y          | 12       |               |
| -lp_offerrem5       | LP매도호가수량5      | Number | Y          | 12       |               |
| -lp_bidrem5         | LP매수호가수량5      | Number | Y          | 12       |               |
| -lp_offerrem6       | LP매도호가수량6      | Number | Y          | 12       |               |
| -lp_bidrem6         | LP매수호가수량6      | Number | Y          | 12       |               |
| -lp_offerrem7       | LP매도호가수량7      | Number | Y          | 12       |               |
| -lp_bidrem7         | LP매수호가수량7      | Number | Y          | 12       |               |
| -lp_offerrem8       | LP매도호가수량8      | Number | Y          | 12       |               |
| -lp_bidrem8         | LP매수호가수량8      | Number | Y          | 12       |               |
| -lp_offerrem9       | LP매도호가수량9      | Number | Y          | 12       |               |
| -lp_bidrem9         | LP매수호가수량9      | Number | Y          | 12       |               |
| -lp_offerrem10      | LP매도호가수량10     | Number | Y          | 12       |               |
| -lp_bidrem10        | LP매수호가수량10     | Number | Y          | 12       |               |
| -jnilclose          | 전일종가           | Number | Y          | 8        |               |
| -offerho1           | 매도호가1          | Number | Y          | 8        |               |
| -bidho1             | 매수호가1          | Number | Y          | 8        |               |
| -offerrem1          | 매도호가수량1        | Number | Y          | 12       |               |
| -bidrem1            | 매수호가수량1        | Number | Y          | 12       |               |
| -preoffercha1       | 직전매도대비수량1      | Number | Y          | 12       |               |
| -prebidcha1         | 직전매수대비수량1      | Number | Y          | 12       |               |
| -offerho2           | 매도호가2          | Number | Y          | 8        |               |
| -bidho2             | 매수호가2          | Number | Y          | 8        |               |
| -offerrem2          | 매도호가수량2        | Number | Y          | 12       |               |
| -bidrem2            | 매수호가수량2        | Number | Y          | 12       |               |
| -preoffercha2       | 직전매도대비수량2      | Number | Y          | 12       |               |
| -prebidcha2         | 직전매수대비수량2      | Number | Y          | 12       |               |
| -offerho3           | 매도호가3          | Number | Y          | 8        |               |
| -bidho3             | 매수호가3          | Number | Y          | 8        |               |
| -offerrem3          | 매도호가수량3        | Number | Y          | 12       |               |
| -bidrem3            | 매수호가수량3        | Number | Y          | 12       |               |
| -preoffercha3       | 직전매도대비수량3      | Number | Y          | 12       |               |
| -prebidcha3         | 직전매수대비수량3      | Number | Y          | 12       |               |
| -offerho4           | 매도호가4          | Number | Y          | 8        |               |
| -bidho4             | 매수호가4          | Number | Y          | 8        |               |
| -offerrem4          | 매도호가수량4        | Number | Y          | 12       |               |
| -bidrem4            | 매수호가수량4        | Number | Y          | 12       |               |
| -preoffercha4       | 직전매도대비수량4      | Number | Y          | 12       |               |
| -prebidcha4         | 직전매수대비수량4      | Number | Y          | 12       |               |
| -offerho5           | 매도호가5          | Number | Y          | 8        |               |
| -bidho5             | 매수호가5          | Number | Y          | 8        |               |
| -offerrem5          | 매도호가수량5        | Number | Y          | 12       |               |
| -bidrem5            | 매수호가수량5        | Number | Y          | 12       |               |
| -preoffercha5       | 직전매도대비수량5      | Number | Y          | 12       |               |
| -prebidcha5         | 직전매수대비수량5      | Number | Y          | 12       |               |
| -offerho6           | 매도호가6          | Number | Y          | 8        |               |
| -bidho6             | 매수호가6          | Number | Y          | 8        |               |
| -offerrem6          | 매도호가수량6        | Number | Y          | 12       |               |
| -bidrem6            | 매수호가수량6        | Number | Y          | 12       |               |
| -preoffercha6       | 직전매도대비수량6      | Number | Y          | 12       |               |
| -prebidcha6         | 직전매수대비수량6      | Number | Y          | 12       |               |
| -offerho7           | 매도호가7          | Number | Y          | 8        |               |
| -bidho7             | 매수호가7          | Number | Y          | 8        |               |
| -offerrem7          | 매도호가수량7        | Number | Y          | 12       |               |
| -bidrem7            | 매수호가수량7        | Number | Y          | 12       |               |
| -preoffercha7       | 직전매도대비수량7      | Number | Y          | 12       |               |
| -prebidcha7         | 직전매수대비수량7      | Number | Y          | 12       |               |
| -offerho8           | 매도호가8          | Number | Y          | 8        |               |
| -bidho8             | 매수호가8          | Number | Y          | 8        |               |
| -offerrem8          | 매도호가수량8        | Number | Y          | 12       |               |
| -bidrem8            | 매수호가수량8        | Number | Y          | 12       |               |
| -preoffercha8       | 직전매도대비수량8      | Number | Y          | 12       |               |
| -prebidcha8         | 직전매수대비수량8      | Number | Y          | 12       |               |
| -offerho9           | 매도호가9          | Number | Y          | 8        |               |
| -bidho9             | 매수호가9          | Number | Y          | 8        |               |
| -offerrem9          | 매도호가수량9        | Number | Y          | 12       |               |
| -bidrem9            | 매수호가수량9        | Number | Y          | 12       |               |
| -preoffercha9       | 직전매도대비수량9      | Number | Y          | 12       |               |
| -prebidcha9         | 직전매수대비수량9      | Number | Y          | 12       |               |
| -offerho10          | 매도호가10         | Number | Y          | 8        |               |
| -bidho10            | 매수호가10         | Number | Y          | 8        |               |
| -offerrem10         | 매도호가수량10       | Number | Y          | 12       |               |
| -bidrem10           | 매수호가수량10       | Number | Y          | 12       |               |
| -preoffercha10      | 직전매도대비수량10     | Number | Y          | 12       |               |
| -prebidcha10        | 직전매수대비수량10     | Number | Y          | 12       |               |
| -offer              | 매도호가수량합        | Number | Y          | 12       |               |
| -bid                | 매수호가수량합        | Number | Y          | 12       |               |
| -preoffercha        | 직전매도대비수량합      | Number | Y          | 12       |               |
| -prebidcha          | 직전매수대비수량합      | Number | Y          | 12       |               |
| -hotime             | 수신시간           | String | Y          | 8        |               |
| -yeprice            | 예상체결가격         | Number | Y          | 8        |               |
| -yevolume           | 예상체결수량         | Number | Y          | 12       |               |
| -yesign             | 예상체결전일구분       | String | Y          | 1        |               |
| -yechange           | 예상체결전일대비       | Number | Y          | 8        |               |
| -yediff             | 예상체결등락율        | Number | Y          | 6.2      |               |
| -tmoffer            | 시간외매도잔량        | Number | Y          | 12       |               |
| -tmbid              | 시간외매수잔량        | Number | Y          | 12       |               |
| -ho_status          | 동시구분           | String | Y          | 1        |               |
| -shcode             | 단축코드           | String | Y          | 6        |               |
| -uplmtprice         | 상한가            | Number | Y          | 8        |               |
| -dnlmtprice         | 하한가            | Number | Y          | 8        |               |
| -open               | 시가             | Number | Y          | 8        |               |
| -high               | 고가             | Number | Y          | 8        |               |
| -low                | 저가             | Number | Y          | 8        |               |
| -krx_midprice       | KRX중간가격        | Number | Y          | 8        |               |
| -krx_offermidsumrem | KRX매도중간가잔량합계수량 | Number | Y          | 9        |               |
| -krx_bidmidsumrem   | KRX매수중간가잔량합계수량 | Number | Y          | 9        |               |


### 💡 Request Example
```json
{
  "t1906InBlock" : {
    "shcode" : "001200"
  }
}
```

### 💡 Response Example
```json
{
    "rsp_cd": "00000",
    "rsp_msg": "정상적으로 조회가 완료되었습니다.",
    "t1906OutBlock": {
        "offerho4": 3705,
        "offerho3": 3700,
        "offerho6": 3715,
        "offerho5": 3710,
        "offerho8": 3725,
        "offerho7": 3720,
        "offerho9": 3730,
        "lp_offerrem6": 0,
        "lp_offerrem5": 0,
        "lp_bidrem10": 0,
        "lp_offerrem8": 0,
        "lp_offerrem7": 0,
        "lp_offerrem2": 0,
        "lp_offerrem1": 0,
        "lp_offerrem4": 0,
        "lp_offerrem3": 0,
        "offer": 18352,
        "price": 3685,
        "lp_bidrem2": 0,
        "lp_bidrem3": 0,
        "lp_bidrem1": 0,
        "lp_bidrem6": 0,
        "tmoffer": 0,
        "lp_bidrem7": 0,
        "hname": "유진투자증권",
        "lp_bidrem4": 0,
        "offerho2": 3695,
        "lp_bidrem5": 0,
        "offerho1": 3690,
        "lp_bidrem8": 0,
        "lp_bidrem9": 0,
        "yediff": "000.00",
        "diff": "000.68",
        "prebidcha10": 0,
        "offerho10": 3735,
        "yeprice": 0,
        "preoffercha9": 0,
        "preoffercha8": 0,
        "preoffercha7": 0,
        "preoffercha6": 0,
        "preoffercha5": 0,
        "preoffercha4": 0,
        "preoffercha3": 0,
        "bidrem3": 4108,
        "bidrem4": 5458,
        "bidrem1": 2647,
        "bidrem2": 1668,
        "low": 3645,
        "preoffercha2": 0,
        "preoffercha1": 0,
        "bidrem9": 1886,
        "bidrem7": 5183,
        "bidrem8": 126,
        "bidrem5": 5181,
        "bidrem6": 6696,
        "change": 25,
        "uplmtprice": 4755,
        "tmbid": 0,
        "lp_offerrem9": 0,
        "lp_offerrem10": 0,
        "open": 3660,
        "jnilclose": 3660,
        "ho_status": "1",
        "sign": "2",
        "preoffercha": 0,
        "high": 3750,
        "hotime": "10265501",
        "yechange": 0,
        "volume": 322192,
        "preoffercha10": 0,
        "offerrem2": 1,
        "bidho5": 3665,
        "offerrem3": 21,
        "bidho4": 3670,
        "offerrem4": 528,
        "bidho7": 3655,
        "offerrem5": 8485,
        "bidho6": 3660,
        "bidho9": 3645,
        "bidho8": 3650,
        "offerrem1": 619,
        "yevolume": 0,
        "offerrem6": 1454,
        "offerrem7": 2803,
        "offerrem8": 828,
        "offerrem9": 2512,
        "dnlmtprice": 2565,
        "bidho1": 3685,
        "bidho3": 3675,
        "bidho2": 3680,
        "prebidcha": 318,
        "prebidcha2": 318,
        "bidrem10": 1569,
        "prebidcha3": 0,
        "prebidcha4": 0,
        "bidho10": 3640,
        "prebidcha5": 0,
        "prebidcha6": 0,
        "prebidcha7": 0,
        "prebidcha8": 0,
        "prebidcha9": 0,
        "shcode": "001200",
        "yesign": "3",
        "offerrem10": 1101,
        "bid": 34522,
        "prebidcha1": 0
    }
}
```

---
