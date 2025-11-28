"""
이벤트 감지 모듈
비차익 프로그램 매수 급증 이벤트를 실시간으로 감지
"""

from collections import deque
from datetime import datetime
import time
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass

# ============================================================================
# 설정값 (조절 가능)
# ============================================================================
THRESHOLD_VALUE = 30_000_000  # 최소 금액 필터: 3천만원
TREND_THRESHOLD_PCT = 0.3  # 추세 판단 임계값: ±0.3%
PRICE_HISTORY_SECONDS = 300  # 가격 히스토리 보관 기간: 5분 (300초)

"""
[중요] threshold_value는 종목별 유동성에 따라 조정이 필요합니다.
- 대형주 (삼성전자): 5천만원~1억원
- 중형주: 3천만원
- 소형주: 1천만원
"""


# ============================================================================
# 가격 히스토리 버퍼
# ============================================================================
class PriceHistoryBuffer:
    """
    종목별 최근 5분간 가격 히스토리 관리
    이벤트 발생 시 직전 N분간 가격 추세를 계산하기 위해 사용
    """

    def __init__(self, max_seconds: int = PRICE_HISTORY_SECONDS):
        """
        Args:
            max_seconds: 가격 히스토리 보관 기간 (초)
        """
        self.max_seconds = max_seconds
        # 종목별 가격 히스토리: {code: deque of (timestamp, price)}
        self.buffers: Dict[str, deque] = {}

    def add_price(self, code: str, price: int):
        """
        새 가격 추가 (체결 시마다 호출)

        Args:
            code: 종목코드
            price: 체결 가격
        """
        if code not in self.buffers:
            self.buffers[code] = deque()

        now = time.time()
        self.buffers[code].append((now, price))
        self._cleanup(code, now)

    def _cleanup(self, code: str, now: float):
        """오래된 데이터 정리"""
        if code not in self.buffers:
            return

        cutoff = now - self.max_seconds
        while self.buffers[code] and self.buffers[code][0][0] < cutoff:
            self.buffers[code].popleft()

    def get_price_ago(self, code: str, seconds_ago: int, tolerance: int = 10) -> Optional[int]:
        """
        N초 전 가격 조회

        Args:
            code: 종목코드
            seconds_ago: 몇 초 전 가격을 조회할지
            tolerance: 허용 오차 (초)

        Returns:
            해당 시점의 가격 또는 None
        """
        if code not in self.buffers or not self.buffers[code]:
            return None

        now = time.time()
        target_time = now - seconds_ago

        # 허용 오차 범위 내에서 가장 가까운 가격 찾기
        best_price = None
        best_diff = float('inf')

        for ts, price in self.buffers[code]:
            diff = abs(ts - target_time)
            if diff <= tolerance and diff < best_diff:
                best_diff = diff
                best_price = price

        return best_price

    def get_high_low(self, code: str, seconds: int = 300) -> Tuple[Optional[int], Optional[int]]:
        """
        최근 N초간 최고가/최저가 조회

        Args:
            code: 종목코드
            seconds: 조회 기간 (초)

        Returns:
            (최고가, 최저가) 또는 (None, None)
        """
        if code not in self.buffers or not self.buffers[code]:
            return None, None

        now = time.time()
        cutoff = now - seconds

        prices = [price for ts, price in self.buffers[code] if ts >= cutoff]
        if not prices:
            return None, None

        return max(prices), min(prices)

    def get_trend_info(self, code: str, current_price: int) -> Dict[str, Any]:
        """
        이벤트 발생 시점의 추세 정보 계산

        Args:
            code: 종목코드
            current_price: 현재가

        Returns:
            추세 정보 딕셔너리
        """
        # N분 전 가격 조회
        price_1m_ago = self.get_price_ago(code, 60)
        price_3m_ago = self.get_price_ago(code, 180)
        price_5m_ago = self.get_price_ago(code, 300)

        # 변동률 계산
        price_change_1m = self._calc_change_pct(price_1m_ago, current_price)
        price_change_3m = self._calc_change_pct(price_3m_ago, current_price)
        price_change_5m = self._calc_change_pct(price_5m_ago, current_price)

        # 5분간 최고가/최저가
        price_high_5m, price_low_5m = self.get_high_low(code, 300)

        # 5분 추세 판단 (임계값: ±0.3%)
        price_trend_5m = self._determine_trend(price_change_5m)

        return {
            "price_1m_ago": price_1m_ago,
            "price_3m_ago": price_3m_ago,
            "price_5m_ago": price_5m_ago,
            "price_change_1m": price_change_1m,
            "price_change_3m": price_change_3m,
            "price_change_5m": price_change_5m,
            "price_trend_5m": price_trend_5m,
            "price_high_5m": price_high_5m,
            "price_low_5m": price_low_5m,
        }

    def _calc_change_pct(self, old_price: Optional[int], new_price: int) -> Optional[float]:
        """변동률 계산"""
        if old_price is None or old_price == 0:
            return None
        return round((new_price - old_price) / old_price * 100, 4)

    def _determine_trend(self, change_pct: Optional[float]) -> Optional[str]:
        """
        추세 판단

        Args:
            change_pct: 변동률 (%)

        Returns:
            'up', 'down', 'sideways', 또는 None
        """
        if change_pct is None:
            return None
        if change_pct >= TREND_THRESHOLD_PCT:
            return "up"
        elif change_pct <= -TREND_THRESHOLD_PCT:
            return "down"
        else:
            return "sideways"

    def get_buffer_size(self, code: str) -> int:
        """버퍼 크기 조회 (디버깅용)"""
        return len(self.buffers.get(code, []))


@dataclass
class EventResult:
    """이벤트 감지 결과"""
    is_event: bool
    event_type: str  # 'buy_surge', 'sell_surge', ''
    delta_vol: int  # 변동 수량
    estimated_value: float  # 추정 금액
    current_price: int  # 현재가
    details: Dict[str, Any]  # 추가 상세 정보


class EventDetector:
    """
    프로그램 매매 이벤트 감지기

    UPH(통합프로그램매매종목별) 데이터를 분석하여
    비차익 프로그램 매수/매도 급증 이벤트를 감지합니다.
    """

    def __init__(self, threshold_value: int = THRESHOLD_VALUE):
        """
        Args:
            threshold_value: 이벤트 트리거 최소 금액 (기본: 3천만원)
        """
        self.threshold_value = threshold_value
        # 종목별 이전 데이터 저장 (메모리 관리: 종목당 1개만 유지)
        self._prev_data: Dict[str, Dict[str, Any]] = {}
        # 가격 히스토리 버퍼 (다이버전스 분석용)
        self.price_history = PriceHistoryBuffer(max_seconds=PRICE_HISTORY_SECONDS)

        # 로그 출력
        print(f"[RESEARCH] 이벤트 감지 최소 금액: {self.threshold_value:,}원")
        print(f"[RESEARCH] 추세 판단 임계값: ±{TREND_THRESHOLD_PCT}%")
        print(f"[RESEARCH] 가격 히스토리 보관: {PRICE_HISTORY_SECONDS}초")

    def update_price(self, code: str, price: int):
        """
        체결 가격 업데이트 (main.py의 on_data에서 호출)

        Args:
            code: 종목코드
            price: 체결 가격
        """
        if price > 0:
            self.price_history.add_price(code, price)

    def detect(self, code: str, curr_data: Dict[str, Any]) -> EventResult:
        """
        이벤트 감지

        Args:
            code: 종목코드
            curr_data: 현재 UPH 데이터 (bshvolume, bdhvolume, price 등)

        Returns:
            EventResult: 이벤트 감지 결과
        """
        # 이전 데이터 가져오기
        prev_data = self._prev_data.get(code)

        # 현재 데이터 저장 (다음 비교용)
        self._prev_data[code] = curr_data.copy()

        # 이전 데이터가 없으면 비교 불가
        if prev_data is None:
            return EventResult(
                is_event=False,
                event_type='',
                delta_vol=0,
                estimated_value=0,
                current_price=int(curr_data.get('price', 0)),
                details={'reason': 'first_data'}
            )

        # 비차익 매수 급증 감지
        buy_result = self._detect_buy_surge(code, prev_data, curr_data)
        if buy_result.is_event:
            return buy_result

        # 비차익 매도 급증 감지
        sell_result = self._detect_sell_surge(code, prev_data, curr_data)
        if sell_result.is_event:
            return sell_result

        # 이벤트 없음
        return EventResult(
            is_event=False,
            event_type='',
            delta_vol=0,
            estimated_value=0,
            current_price=int(curr_data.get('price', 0)),
            details={'reason': 'no_event'}
        )

    def _detect_buy_surge(
        self,
        code: str,
        prev_data: Dict[str, Any],
        curr_data: Dict[str, Any]
    ) -> EventResult:
        """
        비차익 프로그램 매수 급증 이벤트 감지

        조건:
        1. bshvolume(비차익매수체결수량) 증가
        2. 증가량 × 현재가 ≥ threshold_value
        """
        # 비차익 매수 변동량 계산
        prev_bshvolume = int(prev_data.get('bshvolume', 0))
        curr_bshvolume = int(curr_data.get('bshvolume', 0))
        delta_vol = curr_bshvolume - prev_bshvolume

        current_price = int(curr_data.get('price', 0))

        # 1. 수량 증가 확인 (매수 유입)
        if delta_vol > 0 and current_price > 0:
            # 2. 금액 가치 환산 (노이즈 필터링)
            estimated_value = delta_vol * current_price

            if estimated_value >= self.threshold_value:
                # 추세 정보 계산
                trend_info = self.price_history.get_trend_info(code, current_price)
                # 다이버전스 분류
                divergence_type = self._classify_divergence(
                    event_type='buy_surge',
                    trend=trend_info.get('price_trend_5m')
                )

                # 이벤트 발생!
                return EventResult(
                    is_event=True,
                    event_type='buy_surge',
                    delta_vol=delta_vol,
                    estimated_value=estimated_value,
                    current_price=current_price,
                    details={
                        'prev_bshvolume': prev_bshvolume,
                        'curr_bshvolume': curr_bshvolume,
                        'threshold_value': self.threshold_value,
                        'bshrem': int(curr_data.get('bshrem', 0)),
                        'bdhrem': int(curr_data.get('bdhrem', 0)),
                        'bdhvolume': int(curr_data.get('bdhvolume', 0)),
                        'tval': int(curr_data.get('tval', 0)),
                        'tvol': int(curr_data.get('tvol', 0)),
                        'trend_info': trend_info,
                        'divergence_type': divergence_type,
                    }
                )

        # 조건 미충족
        return EventResult(
            is_event=False,
            event_type='',
            delta_vol=delta_vol,
            estimated_value=delta_vol * current_price if current_price > 0 else 0,
            current_price=current_price,
            details={
                'reason': 'below_threshold' if delta_vol > 0 else 'no_increase',
                'delta_vol': delta_vol,
                'threshold_value': self.threshold_value
            }
        )

    def _detect_sell_surge(
        self,
        code: str,
        prev_data: Dict[str, Any],
        curr_data: Dict[str, Any]
    ) -> EventResult:
        """
        비차익 프로그램 매도 급증 이벤트 감지

        조건:
        1. bdhvolume(비차익매도체결수량) 증가
        2. 증가량 × 현재가 ≥ threshold_value
        """
        # 비차익 매도 변동량 계산
        prev_bdhvolume = int(prev_data.get('bdhvolume', 0))
        curr_bdhvolume = int(curr_data.get('bdhvolume', 0))
        delta_vol = curr_bdhvolume - prev_bdhvolume

        current_price = int(curr_data.get('price', 0))

        # 1. 수량 증가 확인 (매도 유입)
        if delta_vol > 0 and current_price > 0:
            # 2. 금액 가치 환산
            estimated_value = delta_vol * current_price

            if estimated_value >= self.threshold_value:
                # 추세 정보 계산
                trend_info = self.price_history.get_trend_info(code, current_price)
                # 다이버전스 분류
                divergence_type = self._classify_divergence(
                    event_type='sell_surge',
                    trend=trend_info.get('price_trend_5m')
                )

                # 이벤트 발생!
                return EventResult(
                    is_event=True,
                    event_type='sell_surge',
                    delta_vol=delta_vol,
                    estimated_value=estimated_value,
                    current_price=current_price,
                    details={
                        'prev_bdhvolume': prev_bdhvolume,
                        'curr_bdhvolume': curr_bdhvolume,
                        'threshold_value': self.threshold_value,
                        'bshrem': int(curr_data.get('bshrem', 0)),
                        'bdhrem': int(curr_data.get('bdhrem', 0)),
                        'bshvolume': int(curr_data.get('bshvolume', 0)),
                        'tval': int(curr_data.get('tval', 0)),
                        'tvol': int(curr_data.get('tvol', 0)),
                        'trend_info': trend_info,
                        'divergence_type': divergence_type,
                    }
                )

        return EventResult(
            is_event=False,
            event_type='',
            delta_vol=delta_vol,
            estimated_value=delta_vol * current_price if current_price > 0 else 0,
            current_price=current_price,
            details={'reason': 'below_threshold' if delta_vol > 0 else 'no_increase'}
        )

    def _classify_divergence(
        self,
        event_type: str,
        trend: Optional[str]
    ) -> Optional[str]:
        """
        다이버전스 유형 분류

        - bullish: 가격 하락 + 매수 급증 (강세 다이버전스)
        - bearish: 가격 상승 + 매도 급증 (약세 다이버전스)
        - none: 방향 일치 또는 추세 불명

        Args:
            event_type: 이벤트 유형 ('buy_surge' 또는 'sell_surge')
            trend: 가격 추세 ('up', 'down', 'sideways' 또는 None)

        Returns:
            다이버전스 유형 문자열 또는 None
        """
        if trend is None:
            return None

        if event_type == 'buy_surge':
            if trend == 'down':
                return 'bullish'  # 가격↓ + 매수↑ = 강세 다이버전스
            elif trend == 'up':
                return 'none'  # 방향 일치 (추세 추종)
            else:  # sideways
                return 'none'

        elif event_type == 'sell_surge':
            if trend == 'up':
                return 'bearish'  # 가격↑ + 매도↑ = 약세 다이버전스
            elif trend == 'down':
                return 'none'  # 방향 일치 (추세 추종)
            else:  # sideways
                return 'none'

        return None

    def update_threshold(self, new_threshold: int):
        """임계값 업데이트"""
        self.threshold_value = new_threshold
        print(f"[RESEARCH] 이벤트 감지 임계값 변경: {self.threshold_value:,}원")

    def get_prev_data(self, code: str) -> Optional[Dict[str, Any]]:
        """이전 데이터 조회 (디버깅용)"""
        return self._prev_data.get(code)

    def clear_prev_data(self, code: str = None):
        """이전 데이터 초기화"""
        if code:
            self._prev_data.pop(code, None)
        else:
            self._prev_data.clear()


def create_event_detector(threshold_value: int = THRESHOLD_VALUE) -> EventDetector:
    """이벤트 감지기 팩토리 함수"""
    return EventDetector(threshold_value=threshold_value)
