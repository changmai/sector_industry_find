"""
가격 추적 모듈
이벤트 발생 후 1분, 5분, 10분, 30분 시점의 가격 변동을 추적
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field
from .research_db import ResearchDB, PriceTracking


# 추적 시점 (분)
TRACKING_INTERVALS = [1, 5, 10, 30]


@dataclass
class TrackingTask:
    """가격 추적 작업"""
    event_id: int
    code: str
    price_at_event: int
    event_time: datetime
    tracking_times: Dict[int, datetime] = field(default_factory=dict)  # minutes -> target_time
    completed: Dict[int, bool] = field(default_factory=dict)  # minutes -> is_completed

    def __post_init__(self):
        # 추적 시간 설정
        for minutes in TRACKING_INTERVALS:
            self.tracking_times[minutes] = self.event_time + timedelta(minutes=minutes)
            self.completed[minutes] = False


class PriceTracker:
    """
    가격 추적기

    이벤트 발생 후 지정된 시점(1분, 5분, 10분, 30분)에
    현재가를 조회하여 수익률을 계산하고 DB에 저장합니다.
    """

    def __init__(
        self,
        db: ResearchDB,
        get_current_price: Callable[[str], Optional[int]] = None
    ):
        """
        Args:
            db: ResearchDB 인스턴스
            get_current_price: 현재가 조회 함수 (code -> price)
        """
        self.db = db
        self._get_current_price = get_current_price
        self._tracking_tasks: List[TrackingTask] = []
        self._running = False
        self._task: Optional[asyncio.Task] = None

        # 최근 가격 캐시 (종목코드 -> 가격)
        self._price_cache: Dict[str, int] = {}

    def set_price_getter(self, get_current_price: Callable[[str], Optional[int]]):
        """현재가 조회 함수 설정"""
        self._get_current_price = get_current_price

    def update_price(self, code: str, price: int):
        """가격 캐시 업데이트 (US3 데이터에서 호출)"""
        self._price_cache[code] = price

    def get_current_price(self, code: str) -> Optional[int]:
        """현재가 조회"""
        # 1. 캐시에서 조회
        if code in self._price_cache:
            return self._price_cache[code]

        # 2. 외부 함수로 조회
        if self._get_current_price:
            price = self._get_current_price(code)
            if price:
                self._price_cache[code] = price
            return price

        return None

    async def add_tracking_event(
        self,
        event_id: int,
        code: str,
        price_at_event: int,
        event_time: datetime = None
    ):
        """
        추적 이벤트 추가

        Args:
            event_id: program_events.id
            code: 종목코드
            price_at_event: 이벤트 발생 시점 가격
            event_time: 이벤트 발생 시간 (기본: 현재 시간)
        """
        if event_time is None:
            event_time = datetime.now()

        task = TrackingTask(
            event_id=event_id,
            code=code,
            price_at_event=price_at_event,
            event_time=event_time
        )

        self._tracking_tasks.append(task)
        print(f"[PRICE TRACKER] Added tracking for event #{event_id} ({code}) @ {price_at_event:,}원")
        print(f"[PRICE TRACKER] Tracking times: 1m={task.tracking_times[1].strftime('%H:%M:%S')}, "
              f"5m={task.tracking_times[5].strftime('%H:%M:%S')}, "
              f"10m={task.tracking_times[10].strftime('%H:%M:%S')}, "
              f"30m={task.tracking_times[30].strftime('%H:%M:%S')}")

    async def check_and_record_prices(self):
        """추적 시간이 된 이벤트의 가격 기록"""
        now = datetime.now()
        completed_tasks = []

        for task in self._tracking_tasks:
            all_completed = True

            for minutes, target_time in task.tracking_times.items():
                # 이미 완료된 시점은 건너뛰기
                if task.completed[minutes]:
                    continue

                all_completed = False

                # 추적 시간 도달 확인
                if now >= target_time:
                    # 현재가 조회
                    current_price = self.get_current_price(task.code)

                    if current_price:
                        # 수익률 계산
                        price_change_pct = (
                            (current_price - task.price_at_event) / task.price_at_event * 100
                        )

                        # DB 저장
                        tracking = PriceTracking(
                            event_id=task.event_id,
                            tracking_time=now.strftime('%Y-%m-%d %H:%M:%S'),
                            minutes_after=minutes,
                            price=current_price,
                            price_change_pct=round(price_change_pct, 4)
                        )

                        try:
                            await self.db.insert_price_tracking(tracking)
                            task.completed[minutes] = True

                            sign = '+' if price_change_pct >= 0 else ''
                            print(f"[PRICE TRACKER] Event #{task.event_id} | {minutes}분 후 | "
                                  f"{task.price_at_event:,} → {current_price:,} ({sign}{price_change_pct:.2f}%)")
                        except Exception as e:
                            print(f"[PRICE TRACKER] DB 저장 실패: {e}")
                    else:
                        print(f"[PRICE TRACKER] 가격 조회 실패: {task.code}")

            # 모든 추적 완료 확인
            if all_completed or all(task.completed.values()):
                completed_tasks.append(task)

        # 완료된 작업 제거
        for task in completed_tasks:
            self._tracking_tasks.remove(task)
            print(f"[PRICE TRACKER] Event #{task.event_id} 추적 완료 - 작업 제거")

    async def _run_loop(self):
        """추적 루프 (1초 간격으로 체크)"""
        while self._running:
            try:
                if self._tracking_tasks:
                    await self.check_and_record_prices()
            except Exception as e:
                print(f"[PRICE TRACKER] 루프 에러: {e}")

            await asyncio.sleep(1)

    def start(self):
        """추적 루프 시작"""
        if not self._running:
            self._running = True
            self._task = asyncio.create_task(self._run_loop())
            print("[PRICE TRACKER] Started")

    def stop(self):
        """추적 루프 중지"""
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
        print("[PRICE TRACKER] Stopped")

    def get_pending_count(self) -> int:
        """대기 중인 추적 작업 수"""
        return len(self._tracking_tasks)

    def get_pending_tasks(self) -> List[Dict[str, Any]]:
        """대기 중인 추적 작업 목록"""
        return [
            {
                'event_id': task.event_id,
                'code': task.code,
                'price_at_event': task.price_at_event,
                'event_time': task.event_time.isoformat(),
                'pending_intervals': [m for m, completed in task.completed.items() if not completed]
            }
            for task in self._tracking_tasks
        ]
