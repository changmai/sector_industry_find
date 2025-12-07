# 멀티 조건 백테스팅 시스템 사용 가이드

## 개요

여러 조건(A~F)을 AND/OR로 조합하여 종목을 필터링하고, 해당 종목의 수익률을 백테스팅하는 시스템입니다.

---

## 파일 구조

```
sector_theme_analyzer/
├── condition_engine.py    # 조건 A~F 로직 구현
├── condition_parser.py    # AND/OR 조합 파서
├── multi_backtester.py    # 백테스팅 엔진 (TP/SL 포함)
├── backtest_cli.py        # CLI 인터페이스
├── config.py              # 경로 설정
├── conditions/
│   └── default.json       # 기본 조건 파라미터
└── output/
    └── backtest_results/  # 백테스트 결과 저장
```

---

## 조건 정의

### 조건 목록

| 조건 | 설명 | 파라미터 | 기본값 |
|------|------|----------|--------|
| **A** | 섹터+업종 N일 동시 상승 | `days`, `ratio` | 5일, 60% |
| **B** | N봉 신고거래대금 | `bars` | 60봉 |
| **C** | 거래량 회전율 상위 N종목 | `min_rate`, `top_n` | 0%, 100개 |
| **D** | 이평 정배열 (단기>중기>장기) | `short`, `mid`, `long` | 20, 60, 120 |
| **E** | N봉 신고가 대비 등락률 범위 | `bars`, `min_pct`, `max_pct` | 60봉, -5%, 0% |
| **F** | N봉전 대비 거래량 비율 | `compare_bars`, `min_ratio`, `max_ratio` | 5봉, 150%, 9000% |

### 조건 상세 설명

#### 조건 A: 섹터+업종 동시 상승
- **로직**: 최근 N일간 평균 등락률이 양수인 업종과 섹터에 동시 속한 종목
- **파라미터**:
  - `days`: 분석 기간 (기본 5일)
  - `ratio`: 섹터 내 상승 종목 비율 기준 (기본 60%)
- **위치**: `condition_engine.py:161-204`

#### 조건 B: N봉 신고거래대금
- **로직**: 해당일 거래대금이 최근 N봉 중 최고인 종목
- **파라미터**:
  - `bars`: 비교할 봉 수 (기본 60봉 ≈ 5일)
- **위치**: `condition_engine.py:286-321`

#### 조건 C: 거래량 회전율 상위
- **로직**: 당일 회전율(거래량/상장주식수×100) 상위 N종목
- **파라미터**:
  - `min_rate`: 최소 회전율 % (기본 0%)
  - `top_n`: 상위 종목 수 (기본 100개)
- **위치**: `condition_engine.py:326-362`

#### 조건 D: 이평 정배열
- **로직**: 단기 MA > 중기 MA > 장기 MA (종가 기준)
- **파라미터**:
  - `short`: 단기 이평 기간 (기본 20일)
  - `mid`: 중기 이평 기간 (기본 60일)
  - `long`: 장기 이평 기간 (기본 120일)
- **위치**: `condition_engine.py:367-404`

#### 조건 E: N봉 신고가 대비 등락률
- **로직**: 현재가가 최근 N봉 신고가 대비 특정 범위 내인 종목
- **파라미터**:
  - `bars`: 비교할 봉 수 (기본 60봉)
  - `min_pct`: 최소 등락률 (기본 -5%)
  - `max_pct`: 최대 등락률 (기본 0%)
- **예시**: 신고가 대비 -5% ~ 0% 범위 = 신고가 근처 종목
- **위치**: `condition_engine.py:426-467`

#### 조건 F: 거래량 비교
- **로직**: (현재 5봉 평균) / (N봉전 5봉 평균) × 100
- **파라미터**:
  - `compare_bars`: 비교 기준 봉 간격 (기본 5봉)
  - `min_ratio`: 최소 비율 (기본 150%)
  - `max_ratio`: 최대 비율 (기본 9000%)
- **예시**: 150% = 거래량이 1.5배 이상 증가
- **위치**: `condition_engine.py:472-514`

---

## 파라미터 변경 방법

### 방법 1: JSON 파일 수정

`conditions/default.json` 파일을 직접 수정:

```json
{
  "A": {
    "description": "섹터+업종 N일 동시 상승",
    "days": 3,
    "ratio": 0.7
  },
  "B": {
    "description": "N봉 신고거래대금",
    "bars": 120
  },
  "C": {
    "description": "거래량 회전율 상위 N종목",
    "min_rate": 1.0,
    "top_n": 50
  },
  "D": {
    "description": "이평 정배열 (단기>중기>장기)",
    "short": 10,
    "mid": 30,
    "long": 60
  },
  "E": {
    "description": "N봉 신고가 대비 등락률 범위",
    "bars": 120,
    "min_pct": -3.0,
    "max_pct": 0.0
  },
  "F": {
    "description": "N봉전 대비 거래량 비율",
    "compare_bars": 10,
    "min_ratio": 200,
    "max_ratio": 5000
  }
}
```

### 방법 2: 커스텀 JSON 파일 사용

새로운 JSON 파일을 만들고 `--params` 옵션으로 지정:

```bash
python backtest_cli.py --conditions "A AND C" --params my_custom_params.json
```

### 방법 3: Python 코드에서 직접 전달

```python
from condition_engine import ConditionEngine
from multi_backtester import MultiBacktester

engine = ConditionEngine()
engine.load_data()

# 커스텀 파라미터 정의
params = {
    'A': {'days': 3, 'ratio': 0.7},
    'C': {'top_n': 50, 'min_rate': 1.0},
    'D': {'short': 10, 'mid': 30, 'long': 60}
}

backtester = MultiBacktester(engine, stop_loss=-5.0, take_profit=10.0)
report = backtester.run(
    start_date='20241209',
    end_date='20251205',
    condition_expr='A AND C AND D',
    params=params
)
backtester.print_report()
```

---

## CLI 사용법

### 기본 실행

```bash
# 인터랙티브 모드 (대화형)
python backtest_cli.py

# 직접 실행 모드
python backtest_cli.py --start-date 20241209 --end-date 20251205 --conditions "A AND C"
```

### 조건 조합

```bash
# AND 조합 (교집합)
python backtest_cli.py --conditions "A AND B AND C"

# OR 조합 (합집합)
python backtest_cli.py --conditions "A OR B"

# 복합 조합
python backtest_cli.py --conditions "A AND (B OR C) AND D"
```

### 매매 설정

```bash
# 손절/익절 설정
python backtest_cli.py --conditions "A" --stop-loss -5 --take-profit 10

# 최대 보유일 설정
python backtest_cli.py --conditions "A" --max-holding 5
```

### TP/SL 최적화

```bash
# 기본 최적화 (TP: 5~10%, SL: -5~-3%)
python backtest_cli.py --conditions "A AND C" --optimize

# 커스텀 범위 최적화
python backtest_cli.py --conditions "A" --optimize \
    --tp-min 5 --tp-max 15 \
    --sl-min -7 --sl-max -2 \
    --step 1
```

### CLI 옵션 전체 목록

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--start-date` | 시작일 (YYYYMMDD) | - |
| `--end-date` | 종료일 (YYYYMMDD) | - |
| `--conditions`, `-c` | 조건 표현식 | - |
| `--params` | 파라미터 JSON 파일 경로 | default.json |
| `--stop-loss`, `-sl` | 손절 라인 % | -5.0 |
| `--take-profit`, `-tp` | 익절 라인 % | 10.0 |
| `--max-holding` | 최대 보유일 | 10 |
| `--optimize`, `-o` | TP/SL 최적화 모드 | False |
| `--tp-min` | 익절 최소값 % | 5.0 |
| `--tp-max` | 익절 최대값 % | 10.0 |
| `--sl-min` | 손절 최소값 % | -5.0 |
| `--sl-max` | 손절 최대값 % | -3.0 |
| `--step` | 최적화 스텝 | 1.0 |

---

## 백테스트 결과 해석

### 출력 예시

```
============================================================
   BACKTEST RESULT
   조건: A AND C
   기간: 2024-12-09 ~ 2025-12-05
============================================================

[매매 통계]
   총 매매 횟수: 1671회
   평균 보유 기간: 6.2일

[수익률]
   평균 수익률: +0.24%
   승률: 34.9%

[손절/익절 통계]
   손절(-5%): 312회 (18.7%)
   익절(+10%): 89회 (5.3%)
   기간만료: 1270회 (76.0%)

[최고/최저]
   최대 수익: +28.5%
   최대 손실: -12.3%
============================================================
```

### 주요 지표

| 지표 | 설명 |
|------|------|
| 총 매매 횟수 | 전체 기간 동안 발생한 매매 수 |
| 평균 보유 기간 | 포지션 평균 보유 일수 |
| 평균 수익률 | 모든 거래의 평균 수익률 |
| 승률 | 수익 거래 비율 (수익>0) |
| 손절 비율 | 손절로 종료된 거래 비율 |
| 익절 비율 | 익절로 종료된 거래 비율 |
| 기간만료 비율 | 최대 보유일 도달로 종료된 거래 비율 |

---

## 새 조건 추가하기

### 1. condition_engine.py에 메서드 추가

```python
# =========================================================================
# 조건 G: 새로운 조건
# =========================================================================
def condition_G(self, base_date: str, param1: int = 10) -> set[str]:
    """
    조건 G: 새로운 조건 설명

    Args:
        base_date: 기준일 (YYYYMMDD)
        param1: 파라미터 설명 (기본 10)

    Returns:
        set[str]: 조건 충족 종목코드 집합
    """
    matched = set()
    # 조건 로직 구현
    return matched
```

### 2. evaluate 메서드에 등록

```python
def evaluate(self, condition_id: str, base_date: str, params: dict = None) -> set[str]:
    condition_map = {
        'A': lambda: self.condition_A(base_date, **params),
        # ... 기존 조건들 ...
        'G': lambda: self.condition_G(base_date, **params),  # 추가
    }
```

### 3. CONDITION_DESCRIPTIONS에 설명 추가

```python
CONDITION_DESCRIPTIONS = {
    'A': '섹터+업종 N일 동시 상승',
    # ... 기존 조건들 ...
    'G': '새로운 조건 설명',  # 추가
}
```

### 4. conditions/default.json에 기본 파라미터 추가

```json
{
  "G": {
    "description": "새로운 조건 설명",
    "param1": 10
  }
}
```

### 5. condition_parser.py 유효성 검사 수정

```python
def validate_expression(self, expression: str) -> tuple[bool, str]:
    valid_conditions = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}  # G 추가
```

---

## 주의사항

1. **데이터 요구사항**: OHLC Parquet 파일과 종목 리스트 JSON 파일이 필요합니다.
2. **날짜 형식**: 모든 날짜는 `YYYYMMDD` 형식을 사용합니다.
3. **조건 조합**: 괄호를 사용하여 우선순위를 지정할 수 있습니다.
4. **최적화 시간**: TP/SL 최적화는 조합 수에 따라 시간이 오래 걸릴 수 있습니다.
