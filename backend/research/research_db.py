"""
SQLite 데이터베이스 관리 모듈
프로그램 매매 이벤트 기록 및 가격 추적 데이터 저장
"""

import sqlite3
import asyncio
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import os


@dataclass
class ProgramEvent:
    """프로그램 매매 이벤트 데이터"""
    id: Optional[int] = None
    event_time: str = ""  # YYYY-MM-DD HH:MM:SS
    code: str = ""
    event_type: str = ""  # 'buy_surge', 'sell_surge'
    trigger_value: float = 0.0  # 이벤트 트리거 값 (추정 금액)
    price_at_event: int = 0
    bshrem: int = 0  # 비차익매수호가잔량
    bdhrem: int = 0  # 비차익매도호가잔량
    bshvolume: int = 0  # 비차익매수체결수량 (누적)
    bdhvolume: int = 0  # 비차익매도체결수량 (누적)
    tval: int = 0  # 전체순매수금액
    delta_vol: int = 0  # 비차익매수 변동량
    # 가격 추세 정보 (다이버전스 분석용)
    price_1m_ago: Optional[int] = None  # 1분 전 가격
    price_3m_ago: Optional[int] = None  # 3분 전 가격
    price_5m_ago: Optional[int] = None  # 5분 전 가격
    price_change_1m: Optional[float] = None  # 1분간 가격 변동률 (%)
    price_change_3m: Optional[float] = None  # 3분간 가격 변동률 (%)
    price_change_5m: Optional[float] = None  # 5분간 가격 변동률 (%)
    price_trend_5m: Optional[str] = None  # 5분 추세: 'up', 'down', 'sideways'
    price_high_5m: Optional[int] = None  # 5분간 최고가
    price_low_5m: Optional[int] = None  # 5분간 최저가
    divergence_type: Optional[str] = None  # 다이버전스: 'bullish', 'bearish', 'none'
    # v2.0 추가 필드
    time_session: Optional[str] = None  # 시간대: '장초반', '장후반', '정규'
    is_noisy_time: bool = False  # 노이즈 시간대 여부
    threshold_used: Optional[int] = None  # 적용된 임계값
    threshold_type: Optional[str] = None  # 임계값 유형: 'dynamic', 'fixed'
    # 호가잔량 분석
    buy_intensity: Optional[float] = None  # 매수 체결강도
    sell_intensity: Optional[float] = None  # 매도 체결강도
    order_book_signal: Optional[str] = None  # 호가잔량 신호 설명


@dataclass
class PriceTracking:
    """가격 추적 데이터"""
    id: Optional[int] = None
    event_id: int = 0
    tracking_time: str = ""  # YYYY-MM-DD HH:MM:SS
    minutes_after: int = 0  # 이벤트 후 경과 시간 (분)
    price: int = 0
    price_change_pct: float = 0.0  # 변동률 (%)


class ResearchDB:
    """
    SQLite 데이터베이스 관리 클래스
    비동기 환경에서 ThreadPoolExecutor를 사용하여 동기 SQLite 호출을 래핑
    """

    def __init__(self, db_path: str = None):
        # 기본 경로: backend 폴더 내 research_data.db
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "..", "research_data.db")
        self.db_path = os.path.abspath(db_path)
        self._executor = ThreadPoolExecutor(max_workers=1)  # 단일 스레드로 동시성 문제 방지
        self._connection: Optional[sqlite3.Connection] = None

    def _get_connection(self) -> sqlite3.Connection:
        """SQLite 연결 가져오기 (스레드 당 하나)"""
        if self._connection is None:
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    async def init_tables(self):
        """테이블 초기화"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self._executor, self._init_tables_sync)
        print(f"[RESEARCH DB] Initialized at {self.db_path}")

    def _init_tables_sync(self):
        """동기 테이블 초기화"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 프로그램 매매 이벤트 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS program_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_time TEXT NOT NULL,
                code TEXT NOT NULL,
                event_type TEXT NOT NULL,
                trigger_value REAL NOT NULL,
                price_at_event INTEGER NOT NULL,
                bshrem INTEGER,
                bdhrem INTEGER,
                bshvolume INTEGER,
                bdhvolume INTEGER,
                tval INTEGER,
                delta_vol INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 가격 추적 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                tracking_time TEXT NOT NULL,
                minutes_after INTEGER NOT NULL,
                price INTEGER NOT NULL,
                price_change_pct REAL,
                FOREIGN KEY (event_id) REFERENCES program_events(id)
            )
        """)

        # 일간 통계 요약 테이블
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                code TEXT NOT NULL,
                total_events INTEGER,
                avg_return_1m REAL,
                avg_return_5m REAL,
                avg_return_10m REAL,
                avg_return_30m REAL,
                win_rate_1m REAL,
                win_rate_5m REAL,
                win_rate_10m REAL,
                win_rate_30m REAL,
                UNIQUE(date, code)
            )
        """)

        # 인덱스 생성
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_code ON program_events(code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_time ON program_events(event_time)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tracking_event ON price_tracking(event_id)")

        conn.commit()

    async def migrate_add_trend_columns(self):
        """기존 events 테이블에 추세/다이버전스 컬럼 추가 (마이그레이션)"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self._executor, self._migrate_add_trend_columns_sync)

    def _migrate_add_trend_columns_sync(self):
        """동기 마이그레이션: 추세 컬럼 및 v2.0 컬럼 추가"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 추가할 컬럼 목록 (v1.0 + v2.0)
        new_columns = [
            # v1.0 추세 정보
            ("price_1m_ago", "INTEGER"),
            ("price_3m_ago", "INTEGER"),
            ("price_5m_ago", "INTEGER"),
            ("price_change_1m", "REAL"),
            ("price_change_3m", "REAL"),
            ("price_change_5m", "REAL"),
            ("price_trend_5m", "TEXT"),
            ("price_high_5m", "INTEGER"),
            ("price_low_5m", "INTEGER"),
            ("divergence_type", "TEXT"),
            # v2.0 시간대/임계값/호가잔량
            ("time_session", "TEXT"),
            ("is_noisy_time", "INTEGER"),  # SQLite는 BOOLEAN 없음
            ("threshold_used", "INTEGER"),
            ("threshold_type", "TEXT"),
            ("buy_intensity", "REAL"),
            ("sell_intensity", "REAL"),
            ("order_book_signal", "TEXT"),
        ]

        # 기존 컬럼 확인
        cursor.execute("PRAGMA table_info(program_events)")
        existing_columns = {row['name'] for row in cursor.fetchall()}

        # 없는 컬럼만 추가
        added_columns = []
        for col_name, col_type in new_columns:
            if col_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE program_events ADD COLUMN {col_name} {col_type}")
                    added_columns.append(col_name)
                except sqlite3.OperationalError as e:
                    # 이미 존재하면 무시
                    if "duplicate column name" not in str(e).lower():
                        raise

        conn.commit()

        if added_columns:
            print(f"[RESEARCH DB] Migration: Added columns - {', '.join(added_columns)}")
        else:
            print("[RESEARCH DB] Migration: No new columns to add")

    async def insert_event(self, event: ProgramEvent) -> int:
        """이벤트 삽입 및 ID 반환"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._insert_event_sync, event)

    def _insert_event_sync(self, event: ProgramEvent) -> int:
        """동기 이벤트 삽입"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO program_events
            (event_time, code, event_type, trigger_value, price_at_event,
             bshrem, bdhrem, bshvolume, bdhvolume, tval, delta_vol,
             price_1m_ago, price_3m_ago, price_5m_ago,
             price_change_1m, price_change_3m, price_change_5m,
             price_trend_5m, price_high_5m, price_low_5m, divergence_type,
             time_session, is_noisy_time, threshold_used, threshold_type,
             buy_intensity, sell_intensity, order_book_signal)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.event_time, event.code, event.event_type, event.trigger_value,
            event.price_at_event, event.bshrem, event.bdhrem, event.bshvolume,
            event.bdhvolume, event.tval, event.delta_vol,
            event.price_1m_ago, event.price_3m_ago, event.price_5m_ago,
            event.price_change_1m, event.price_change_3m, event.price_change_5m,
            event.price_trend_5m, event.price_high_5m, event.price_low_5m,
            event.divergence_type,
            # v2.0 추가 필드
            event.time_session, 1 if event.is_noisy_time else 0,
            event.threshold_used, event.threshold_type,
            event.buy_intensity, event.sell_intensity, event.order_book_signal
        ))

        conn.commit()
        return cursor.lastrowid

    async def insert_price_tracking(self, tracking: PriceTracking):
        """가격 추적 데이터 삽입"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self._executor, self._insert_price_tracking_sync, tracking)

    def _insert_price_tracking_sync(self, tracking: PriceTracking):
        """동기 가격 추적 삽입"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO price_tracking
            (event_id, tracking_time, minutes_after, price, price_change_pct)
            VALUES (?, ?, ?, ?, ?)
        """, (
            tracking.event_id, tracking.tracking_time, tracking.minutes_after,
            tracking.price, tracking.price_change_pct
        ))

        conn.commit()

    async def get_event_by_id(self, event_id: int) -> Optional[ProgramEvent]:
        """이벤트 ID로 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_event_by_id_sync, event_id)

    def _get_event_by_id_sync(self, event_id: int) -> Optional[ProgramEvent]:
        """동기 이벤트 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM program_events WHERE id = ?", (event_id,))
        row = cursor.fetchone()

        if row:
            return ProgramEvent(
                id=row['id'],
                event_time=row['event_time'],
                code=row['code'],
                event_type=row['event_type'],
                trigger_value=row['trigger_value'],
                price_at_event=row['price_at_event'],
                bshrem=row['bshrem'],
                bdhrem=row['bdhrem'],
                bshvolume=row['bshvolume'],
                bdhvolume=row['bdhvolume'],
                tval=row['tval'],
                delta_vol=row['delta_vol']
            )
        return None

    async def get_events_by_date(self, date: str) -> List[ProgramEvent]:
        """날짜별 이벤트 목록 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_events_by_date_sync, date)

    def _get_events_by_date_sync(self, date: str) -> List[ProgramEvent]:
        """동기 날짜별 이벤트 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM program_events
            WHERE event_time LIKE ?
            ORDER BY event_time ASC
        """, (f"{date}%",))

        events = []
        for row in cursor.fetchall():
            events.append(ProgramEvent(
                id=row['id'],
                event_time=row['event_time'],
                code=row['code'],
                event_type=row['event_type'],
                trigger_value=row['trigger_value'],
                price_at_event=row['price_at_event'],
                bshrem=row['bshrem'],
                bdhrem=row['bdhrem'],
                bshvolume=row['bshvolume'],
                bdhvolume=row['bdhvolume'],
                tval=row['tval'],
                delta_vol=row['delta_vol']
            ))
        return events

    async def get_price_tracking_for_event(self, event_id: int) -> List[PriceTracking]:
        """이벤트의 가격 추적 데이터 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, self._get_price_tracking_for_event_sync, event_id
        )

    def _get_price_tracking_for_event_sync(self, event_id: int) -> List[PriceTracking]:
        """동기 가격 추적 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM price_tracking
            WHERE event_id = ?
            ORDER BY minutes_after ASC
        """, (event_id,))

        trackings = []
        for row in cursor.fetchall():
            trackings.append(PriceTracking(
                id=row['id'],
                event_id=row['event_id'],
                tracking_time=row['tracking_time'],
                minutes_after=row['minutes_after'],
                price=row['price'],
                price_change_pct=row['price_change_pct']
            ))
        return trackings

    async def get_events_with_tracking(self, date: str) -> List[Dict[str, Any]]:
        """이벤트와 가격 추적 데이터 함께 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, self._get_events_with_tracking_sync, date
        )

    def _get_events_with_tracking_sync(self, date: str) -> List[Dict[str, Any]]:
        """동기 이벤트+추적 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT e.*,
                   GROUP_CONCAT(p.minutes_after || ':' || p.price_change_pct) as tracking_data
            FROM program_events e
            LEFT JOIN price_tracking p ON e.id = p.event_id
            WHERE e.event_time LIKE ?
            GROUP BY e.id
            ORDER BY e.event_time ASC
        """, (f"{date}%",))

        results = []
        for row in cursor.fetchall():
            event_dict = dict(row)
            # tracking_data 파싱
            if event_dict.get('tracking_data'):
                tracking = {}
                for item in event_dict['tracking_data'].split(','):
                    minutes, pct = item.split(':')
                    tracking[int(minutes)] = float(pct) if pct != 'None' else None
                event_dict['tracking'] = tracking
            else:
                event_dict['tracking'] = {}
            del event_dict['tracking_data']
            results.append(event_dict)

        return results

    async def update_daily_summary(self, date: str, code: str):
        """일간 요약 업데이트"""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(self._executor, self._update_daily_summary_sync, date, code)

    def _update_daily_summary_sync(self, date: str, code: str):
        """동기 일간 요약 업데이트"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 해당 날짜/종목의 모든 이벤트와 추적 데이터 조회
        cursor.execute("""
            SELECT e.id, e.price_at_event, p.minutes_after, p.price_change_pct
            FROM program_events e
            LEFT JOIN price_tracking p ON e.id = p.event_id
            WHERE e.event_time LIKE ? AND e.code = ?
        """, (f"{date}%", code))

        rows = cursor.fetchall()
        if not rows:
            return

        # 데이터 집계
        returns = {1: [], 5: [], 10: [], 30: []}
        event_ids = set()

        for row in rows:
            event_ids.add(row['id'])
            if row['minutes_after'] and row['price_change_pct'] is not None:
                minutes = row['minutes_after']
                if minutes in returns:
                    returns[minutes].append(row['price_change_pct'])

        total_events = len(event_ids)

        def calc_stats(values: List[float]):
            if not values:
                return None, None
            avg = sum(values) / len(values)
            win_rate = len([v for v in values if v > 0]) / len(values) * 100
            return avg, win_rate

        avg_1m, win_1m = calc_stats(returns[1])
        avg_5m, win_5m = calc_stats(returns[5])
        avg_10m, win_10m = calc_stats(returns[10])
        avg_30m, win_30m = calc_stats(returns[30])

        # UPSERT
        cursor.execute("""
            INSERT INTO daily_summary
            (date, code, total_events, avg_return_1m, avg_return_5m, avg_return_10m, avg_return_30m,
             win_rate_1m, win_rate_5m, win_rate_10m, win_rate_30m)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(date, code) DO UPDATE SET
                total_events = excluded.total_events,
                avg_return_1m = excluded.avg_return_1m,
                avg_return_5m = excluded.avg_return_5m,
                avg_return_10m = excluded.avg_return_10m,
                avg_return_30m = excluded.avg_return_30m,
                win_rate_1m = excluded.win_rate_1m,
                win_rate_5m = excluded.win_rate_5m,
                win_rate_10m = excluded.win_rate_10m,
                win_rate_30m = excluded.win_rate_30m
        """, (
            date, code, total_events, avg_1m, avg_5m, avg_10m, avg_30m,
            win_1m, win_5m, win_10m, win_30m
        ))

        conn.commit()

    async def get_daily_summary(self, date: str) -> List[Dict[str, Any]]:
        """일간 요약 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_daily_summary_sync, date)

    def _get_daily_summary_sync(self, date: str) -> List[Dict[str, Any]]:
        """동기 일간 요약 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM daily_summary WHERE date = ?", (date,))
        return [dict(row) for row in cursor.fetchall()]

    async def get_recent_events(self, limit: int = 50) -> List[ProgramEvent]:
        """최근 이벤트 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_recent_events_sync, limit)

    def _get_recent_events_sync(self, limit: int) -> List[ProgramEvent]:
        """동기 최근 이벤트 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM program_events
            ORDER BY event_time DESC
            LIMIT ?
        """, (limit,))

        events = []
        for row in cursor.fetchall():
            events.append(ProgramEvent(
                id=row['id'],
                event_time=row['event_time'],
                code=row['code'],
                event_type=row['event_type'],
                trigger_value=row['trigger_value'],
                price_at_event=row['price_at_event'],
                bshrem=row['bshrem'],
                bdhrem=row['bdhrem'],
                bshvolume=row['bshvolume'],
                bdhvolume=row['bdhvolume'],
                tval=row['tval'],
                delta_vol=row['delta_vol']
            ))
        return events

    async def get_live_summary(self) -> Dict[str, Any]:
        """실시간 연구 대시보드용 전체 요약 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_live_summary_sync)

    def _get_live_summary_sync(self) -> Dict[str, Any]:
        """동기 실시간 요약 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 전체 이벤트 통계
        cursor.execute("""
            SELECT
                COUNT(*) as total_events,
                SUM(CASE WHEN event_type = 'buy_surge' THEN 1 ELSE 0 END) as buy_events,
                SUM(CASE WHEN event_type = 'sell_surge' THEN 1 ELSE 0 END) as sell_events
            FROM program_events
        """)
        row = cursor.fetchone()
        total_events = row['total_events'] or 0
        buy_events = row['buy_events'] or 0
        sell_events = row['sell_events'] or 0

        # 수익률 및 승률 계산 (각 시간대별)
        returns_query = """
            SELECT
                e.event_type,
                p.minutes_after,
                AVG(p.price_change_pct) as avg_return,
                SUM(CASE WHEN p.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as win_rate,
                COUNT(*) as count
            FROM program_events e
            JOIN price_tracking p ON e.id = p.event_id
            WHERE p.price_change_pct IS NOT NULL
            GROUP BY e.event_type, p.minutes_after
        """
        cursor.execute(returns_query)

        returns_data = {}
        for row in cursor.fetchall():
            key = f"{row['event_type']}_{row['minutes_after']}m"
            returns_data[key] = {
                'avg_return': row['avg_return'],
                'win_rate': row['win_rate'],
                'count': row['count']
            }

        # 전체 평균 수익률 계산
        def get_avg(minutes: int) -> Optional[float]:
            buy_key = f"buy_surge_{minutes}m"
            sell_key = f"sell_surge_{minutes}m"
            total_count = 0
            total_return = 0.0

            if buy_key in returns_data:
                buy_data = returns_data[buy_key]
                total_count += buy_data['count']
                total_return += buy_data['avg_return'] * buy_data['count']

            # sell_surge의 경우 방향이 반대이므로 부호 반전
            if sell_key in returns_data:
                sell_data = returns_data[sell_key]
                total_count += sell_data['count']
                total_return += (-sell_data['avg_return']) * sell_data['count']

            return total_return / total_count if total_count > 0 else None

        def get_win_rate(minutes: int) -> Optional[float]:
            buy_key = f"buy_surge_{minutes}m"
            sell_key = f"sell_surge_{minutes}m"
            total_count = 0
            win_count = 0

            if buy_key in returns_data:
                buy_data = returns_data[buy_key]
                total_count += buy_data['count']
                win_count += buy_data['win_rate'] * buy_data['count'] / 100

            if sell_key in returns_data:
                sell_data = returns_data[sell_key]
                total_count += sell_data['count']
                # sell_surge는 가격 하락이 승리
                win_count += (100 - sell_data['win_rate']) * sell_data['count'] / 100

            return (win_count / total_count * 100) if total_count > 0 else None

        return {
            'total_events': total_events,
            'buy_events': buy_events,
            'sell_events': sell_events,
            'avg_return_1m': get_avg(1),
            'avg_return_5m': get_avg(5),
            'avg_return_10m': get_avg(10),
            'avg_return_30m': get_avg(30),
            'win_rate_1m': get_win_rate(1),
            'win_rate_5m': get_win_rate(5),
            'win_rate_10m': get_win_rate(10),
            'win_rate_30m': get_win_rate(30),
            'last_updated': datetime.now().isoformat()
        }

    async def get_recent_events_with_returns(self, limit: int = 20) -> List[Dict[str, Any]]:
        """최근 이벤트와 수익률 함께 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self._executor, self._get_recent_events_with_returns_sync, limit
        )

    def _get_recent_events_with_returns_sync(self, limit: int) -> List[Dict[str, Any]]:
        """동기 최근 이벤트+수익률 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                e.*,
                p1.price_change_pct as return_1m,
                p5.price_change_pct as return_5m,
                p10.price_change_pct as return_10m,
                p30.price_change_pct as return_30m
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            LEFT JOIN price_tracking p5 ON e.id = p5.event_id AND p5.minutes_after = 5
            LEFT JOIN price_tracking p10 ON e.id = p10.event_id AND p10.minutes_after = 10
            LEFT JOIN price_tracking p30 ON e.id = p30.event_id AND p30.minutes_after = 30
            ORDER BY e.event_time DESC
            LIMIT ?
        """, (limit,))

        results = []
        for row in cursor.fetchall():
            # v2.0 필드 안전하게 추출 (없을 수 있음)
            row_dict = dict(row)
            results.append({
                'id': row['id'],
                'event_time': row['event_time'],
                'code': row['code'],
                'event_type': row['event_type'],
                'trigger_value': row['trigger_value'],
                'price_at_event': row['price_at_event'],
                'delta_vol': row['delta_vol'],
                'bshrem': row['bshrem'],
                'bdhrem': row['bdhrem'],
                'bshvolume': row['bshvolume'],
                'bdhvolume': row['bdhvolume'],
                'tval': row['tval'],
                'return_1m': row['return_1m'],
                'return_5m': row['return_5m'],
                'return_10m': row['return_10m'],
                'return_30m': row['return_30m'],
                # v2.0 추가 필드
                'divergence_type': row_dict.get('divergence_type'),
                'time_session': row_dict.get('time_session'),
                'is_noisy_time': bool(row_dict.get('is_noisy_time', 0)),
                'threshold_used': row_dict.get('threshold_used'),
                'threshold_type': row_dict.get('threshold_type'),
                'buy_intensity': row_dict.get('buy_intensity'),
                'sell_intensity': row_dict.get('sell_intensity'),
                'order_book_signal': row_dict.get('order_book_signal'),
            })
        return results

    async def get_stock_summary(self) -> List[Dict[str, Any]]:
        """종목별 통계 요약"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_stock_summary_sync)

    def _get_stock_summary_sync(self) -> List[Dict[str, Any]]:
        """동기 종목별 요약 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                e.code,
                COUNT(*) as event_count,
                AVG(p1.price_change_pct) as avg_return_1m,
                SUM(CASE WHEN p1.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(p1.price_change_pct) as win_rate_1m
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            GROUP BY e.code
            ORDER BY event_count DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    async def get_stock_detail(self, code: str) -> Dict[str, Any]:
        """특정 종목의 상세 통계"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_stock_detail_sync, code)

    def _get_stock_detail_sync(self, code: str) -> Dict[str, Any]:
        """동기 종목 상세 통계 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 종목 요약 통계
        cursor.execute("""
            SELECT
                COUNT(*) as total_events,
                AVG(p1.price_change_pct) as avg_return_1m,
                AVG(p5.price_change_pct) as avg_return_5m,
                AVG(p10.price_change_pct) as avg_return_10m,
                AVG(p30.price_change_pct) as avg_return_30m,
                SUM(CASE WHEN p1.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p1.price_change_pct), 0) as win_rate_1m
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            LEFT JOIN price_tracking p5 ON e.id = p5.event_id AND p5.minutes_after = 5
            LEFT JOIN price_tracking p10 ON e.id = p10.event_id AND p10.minutes_after = 10
            LEFT JOIN price_tracking p30 ON e.id = p30.event_id AND p30.minutes_after = 30
            WHERE e.code = ?
        """, (code,))

        summary_row = cursor.fetchone()
        summary = {
            'total_events': summary_row['total_events'] or 0,
            'avg_return_1m': summary_row['avg_return_1m'],
            'avg_return_5m': summary_row['avg_return_5m'],
            'avg_return_10m': summary_row['avg_return_10m'],
            'avg_return_30m': summary_row['avg_return_30m'],
            'win_rate_1m': summary_row['win_rate_1m']
        }

        # 이벤트 목록
        cursor.execute("""
            SELECT
                e.*,
                p1.price_change_pct as return_1m,
                p5.price_change_pct as return_5m,
                p10.price_change_pct as return_10m,
                p30.price_change_pct as return_30m
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            LEFT JOIN price_tracking p5 ON e.id = p5.event_id AND p5.minutes_after = 5
            LEFT JOIN price_tracking p10 ON e.id = p10.event_id AND p10.minutes_after = 10
            LEFT JOIN price_tracking p30 ON e.id = p30.event_id AND p30.minutes_after = 30
            WHERE e.code = ?
            ORDER BY e.event_time DESC
            LIMIT 100
        """, (code,))

        events = []
        for row in cursor.fetchall():
            events.append({
                'id': row['id'],
                'event_time': row['event_time'],
                'code': row['code'],
                'event_type': row['event_type'],
                'trigger_value': row['trigger_value'],
                'price_at_event': row['price_at_event'],
                'delta_vol': row['delta_vol'],
                'return_1m': row['return_1m'],
                'return_5m': row['return_5m'],
                'return_10m': row['return_10m'],
                'return_30m': row['return_30m']
            })

        # 시간대별 통계
        cursor.execute("""
            SELECT
                strftime('%H', e.event_time) as hour,
                COUNT(*) as count,
                AVG(p1.price_change_pct) as avg_return,
                SUM(CASE WHEN p1.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p1.price_change_pct), 0) as win_rate
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            WHERE e.code = ?
            GROUP BY strftime('%H', e.event_time)
            ORDER BY hour
        """, (code,))

        by_hour = [dict(row) for row in cursor.fetchall()]

        # Delta 범위별 통계
        cursor.execute("""
            SELECT
                CASE
                    WHEN delta_vol < 10000 THEN '0-10K'
                    WHEN delta_vol < 50000 THEN '10K-50K'
                    WHEN delta_vol < 100000 THEN '50K-100K'
                    ELSE '100K+'
                END as range,
                COUNT(*) as count,
                AVG(p1.price_change_pct) as avg_return,
                SUM(CASE WHEN p1.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p1.price_change_pct), 0) as win_rate
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            WHERE e.code = ?
            GROUP BY range
            ORDER BY
                CASE range
                    WHEN '0-10K' THEN 1
                    WHEN '10K-50K' THEN 2
                    WHEN '50K-100K' THEN 3
                    ELSE 4
                END
        """, (code,))

        by_delta = [dict(row) for row in cursor.fetchall()]

        return {
            'summary': summary,
            'events': events,
            'by_hour': by_hour,
            'by_delta': by_delta
        }

    async def get_event_count_by_date(self, date: str) -> int:
        """특정 날짜의 이벤트 수 조회"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_event_count_by_date_sync, date)

    def _get_event_count_by_date_sync(self, date: str) -> int:
        """동기 날짜별 이벤트 수 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) as count
            FROM program_events
            WHERE event_time LIKE ?
        """, (f"{date}%",))

        row = cursor.fetchone()
        return row['count'] if row else 0

    async def get_event_detail(self, event_id: int) -> Optional[Dict[str, Any]]:
        """이벤트 상세 정보 (추적 데이터 포함)"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_event_detail_sync, event_id)

    def _get_event_detail_sync(self, event_id: int) -> Optional[Dict[str, Any]]:
        """동기 이벤트 상세 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 이벤트 기본 정보
        cursor.execute("SELECT * FROM program_events WHERE id = ?", (event_id,))
        row = cursor.fetchone()
        if not row:
            return None

        event = dict(row)

        # 가격 추적 데이터
        cursor.execute("""
            SELECT minutes_after, price, price_change_pct, tracking_time
            FROM price_tracking
            WHERE event_id = ?
            ORDER BY minutes_after
        """, (event_id,))

        price_tracking = []
        for track_row in cursor.fetchall():
            price_tracking.append({
                'minutes_after': track_row['minutes_after'],
                'price': track_row['price'],
                'price_change_pct': track_row['price_change_pct'],
                'tracking_time': track_row['tracking_time']
            })

        event['price_tracking'] = price_tracking
        return event

    async def get_divergence_analysis(self, date: str = None) -> Dict[str, Any]:
        """다이버전스 패턴별 수익률 분석"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_divergence_analysis_sync, date)

    def _get_divergence_analysis_sync(self, date: str = None) -> Dict[str, Any]:
        """동기 다이버전스 분석 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 날짜 필터
        date_filter = f"AND e.event_time LIKE '{date}%'" if date else ""

        # 다이버전스 유형별 통계
        cursor.execute(f"""
            SELECT
                e.divergence_type,
                COUNT(*) as count,
                AVG(p5.price_change_pct) as avg_return_5m,
                SUM(CASE WHEN p5.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p5.price_change_pct), 0) as win_rate
            FROM program_events e
            LEFT JOIN price_tracking p5 ON e.id = p5.event_id AND p5.minutes_after = 5
            WHERE e.divergence_type IS NOT NULL {date_filter}
            GROUP BY e.divergence_type
        """)

        by_divergence = {}
        for row in cursor.fetchall():
            div_type = row['divergence_type'] or 'none'
            by_divergence[div_type] = {
                'count': row['count'],
                'avg_return_5m': row['avg_return_5m'],
                'win_rate': row['win_rate']
            }

        return by_divergence

    async def get_trend_based_analysis(self, date: str = None) -> List[Dict[str, Any]]:
        """가격 추세별 이벤트 수익률 분석"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self._executor, self._get_trend_based_analysis_sync, date)

    def _get_trend_based_analysis_sync(self, date: str = None) -> List[Dict[str, Any]]:
        """동기 추세별 분석 조회"""
        conn = self._get_connection()
        cursor = conn.cursor()

        # 날짜 필터
        date_filter = f"AND e.event_time LIKE '{date}%'" if date else ""

        # 추세 + 이벤트 유형별 통계
        cursor.execute(f"""
            SELECT
                e.price_trend_5m as trend,
                e.event_type,
                COUNT(*) as count,
                AVG(p1.price_change_pct) as avg_return_1m,
                AVG(p5.price_change_pct) as avg_return_5m,
                SUM(CASE WHEN p5.price_change_pct > 0 THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(p5.price_change_pct), 0) as win_rate_5m
            FROM program_events e
            LEFT JOIN price_tracking p1 ON e.id = p1.event_id AND p1.minutes_after = 1
            LEFT JOIN price_tracking p5 ON e.id = p5.event_id AND p5.minutes_after = 5
            WHERE e.price_trend_5m IS NOT NULL {date_filter}
            GROUP BY e.price_trend_5m, e.event_type
            ORDER BY e.price_trend_5m, e.event_type
        """)

        results = []
        for row in cursor.fetchall():
            results.append({
                'trend': row['trend'],
                'event_type': row['event_type'],
                'count': row['count'],
                'avg_return_1m': row['avg_return_1m'],
                'avg_return_5m': row['avg_return_5m'],
                'win_rate_5m': row['win_rate_5m']
            })

        return results

    def close(self):
        """연결 종료"""
        if self._connection:
            self._connection.close()
            self._connection = None
        self._executor.shutdown(wait=False)
