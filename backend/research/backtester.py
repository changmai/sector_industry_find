"""
백테스팅 모듈
저장된 UPH 원본 데이터를 기반으로 전략 검증 수행
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from .event_detector import EventDetector, THRESHOLD_VALUE


@dataclass
class BacktestEvent:
    """백테스트 이벤트"""
    idx: int  # 데이터 인덱스
    time: str
    code: str
    event_type: str
    price_at_event: int
    delta_vol: int
    estimated_value: float
    # 가격 추적 결과 (분 -> 가격)
    prices_after: Dict[int, int] = field(default_factory=dict)
    # 수익률 (분 -> %)
    returns: Dict[int, float] = field(default_factory=dict)


@dataclass
class BacktestResult:
    """백테스트 결과"""
    code: str
    date: str
    threshold_value: int
    total_events: int
    events: List[BacktestEvent]
    # 시간대별 통계
    stats: Dict[int, Dict[str, float]] = field(default_factory=dict)  # minutes -> {avg, win_rate, count}


class Backtester:
    """
    프로그램 매매 전략 백테스터

    저장된 UPH 데이터 파일을 읽어 이벤트 감지 및 수익률 계산
    """

    # 추적 시점 (분 단위를 데이터 행 수로 변환)
    # UPH 데이터는 약 1초 간격으로 수신됨 (종목별로 다를 수 있음)
    TRACKING_INTERVALS = [1, 5, 10, 30]  # 분

    def __init__(self, uph_data_dir: str = "uph_raw_data"):
        """
        Args:
            uph_data_dir: UPH 원본 데이터 디렉토리
        """
        self.uph_data_dir = uph_data_dir

    def list_available_files(self) -> List[Dict[str, str]]:
        """
        사용 가능한 UPH 데이터 파일 목록 조회

        Returns:
            List[Dict]: [{"code": "005930", "date": "20241128", "filename": "uph_005930_20241128.txt"}, ...]
        """
        files = []
        if not os.path.exists(self.uph_data_dir):
            return files

        for filename in os.listdir(self.uph_data_dir):
            if filename.startswith("uph_") and filename.endswith(".txt"):
                # uph_005930_20241128.txt 형식 파싱
                parts = filename.replace(".txt", "").split("_")
                if len(parts) >= 3:
                    code = parts[1]
                    date = parts[2]
                    files.append({
                        "code": code,
                        "date": date,
                        "filename": filename,
                        "path": os.path.join(self.uph_data_dir, filename)
                    })

        # 날짜 내림차순 정렬
        files.sort(key=lambda x: (x["date"], x["code"]), reverse=True)
        return files

    def load_uph_data(self, code: str, date: str) -> List[Dict[str, Any]]:
        """
        UPH 데이터 파일 로드

        Args:
            code: 종목코드
            date: 날짜 (YYYYMMDD)

        Returns:
            List[Dict]: UPH 데이터 리스트
        """
        filename = f"uph_{code}_{date}.txt"
        filepath = os.path.join(self.uph_data_dir, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"UPH 데이터 파일을 찾을 수 없습니다: {filepath}")

        data = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        row = json.loads(line)
                        data.append(row)
                    except json.JSONDecodeError:
                        continue

        print(f"[BACKTEST] Loaded {len(data)} rows from {filename}")
        return data

    def _estimate_rows_per_minute(self, data: List[Dict[str, Any]]) -> int:
        """
        데이터 빈도 추정 (1분당 행 수)

        UPH 데이터의 time 필드를 분석하여 1분당 평균 데이터 수 계산
        """
        if len(data) < 10:
            return 60  # 기본값: 1초에 1개

        # 시간 파싱해서 빈도 계산
        times = []
        for row in data[:100]:  # 앞 100개만 샘플링
            time_str = row.get("time", "")
            if len(time_str) >= 6:
                try:
                    # HHMMSS 또는 HHMMSSmmm 형식
                    h = int(time_str[0:2])
                    m = int(time_str[2:4])
                    s = int(time_str[4:6])
                    total_seconds = h * 3600 + m * 60 + s
                    times.append(total_seconds)
                except ValueError:
                    continue

        if len(times) < 2:
            return 60

        # 시간 간격 계산
        time_diff = times[-1] - times[0]
        if time_diff <= 0:
            return 60

        rows_per_second = len(times) / time_diff
        rows_per_minute = int(rows_per_second * 60)

        return max(1, rows_per_minute)

    def run_backtest(
        self,
        code: str,
        date: str,
        threshold_value: int = THRESHOLD_VALUE
    ) -> BacktestResult:
        """
        백테스트 실행

        Args:
            code: 종목코드
            date: 날짜 (YYYYMMDD)
            threshold_value: 이벤트 감지 임계값 (기본: 3천만원)

        Returns:
            BacktestResult: 백테스트 결과
        """
        # 데이터 로드
        data = self.load_uph_data(code, date)
        if not data:
            return BacktestResult(
                code=code,
                date=date,
                threshold_value=threshold_value,
                total_events=0,
                events=[],
                stats={}
            )

        # 데이터 빈도 추정
        rows_per_minute = self._estimate_rows_per_minute(data)
        print(f"[BACKTEST] Estimated {rows_per_minute} rows per minute")

        # 이벤트 감지기 생성
        detector = EventDetector(threshold_value=threshold_value)

        # 이벤트 감지
        events: List[BacktestEvent] = []

        for i, row in enumerate(data):
            result = detector.detect(code, row)

            if result.is_event:
                event = BacktestEvent(
                    idx=i,
                    time=row.get("time", ""),
                    code=code,
                    event_type=result.event_type,
                    price_at_event=result.current_price,
                    delta_vol=result.delta_vol,
                    estimated_value=result.estimated_value
                )

                # 미래 가격 추적
                for minutes in self.TRACKING_INTERVALS:
                    future_idx = i + (minutes * rows_per_minute)

                    if future_idx < len(data):
                        future_price = int(data[future_idx].get("price", 0))
                        if future_price > 0 and event.price_at_event > 0:
                            event.prices_after[minutes] = future_price
                            # 수익률 계산
                            return_pct = (future_price - event.price_at_event) / event.price_at_event * 100
                            event.returns[minutes] = round(return_pct, 4)

                events.append(event)

        print(f"[BACKTEST] Detected {len(events)} events")

        # 통계 계산
        stats = {}
        for minutes in self.TRACKING_INTERVALS:
            returns = [e.returns.get(minutes) for e in events if minutes in e.returns]
            if returns:
                avg_return = sum(returns) / len(returns)
                wins = len([r for r in returns if r > 0])
                win_rate = wins / len(returns) * 100

                stats[minutes] = {
                    "avg_return": round(avg_return, 4),
                    "win_rate": round(win_rate, 2),
                    "count": len(returns),
                    "wins": wins,
                    "losses": len(returns) - wins
                }

        return BacktestResult(
            code=code,
            date=date,
            threshold_value=threshold_value,
            total_events=len(events),
            events=events,
            stats=stats
        )

    def run_multi_backtest(
        self,
        codes: List[str] = None,
        dates: List[str] = None,
        threshold_value: int = THRESHOLD_VALUE
    ) -> Dict[str, Any]:
        """
        여러 종목/날짜에 대한 백테스트 실행

        Args:
            codes: 종목코드 리스트 (None이면 전체)
            dates: 날짜 리스트 (None이면 전체)
            threshold_value: 이벤트 감지 임계값

        Returns:
            Dict: 종합 백테스트 결과
        """
        available_files = self.list_available_files()

        # 필터링
        if codes:
            available_files = [f for f in available_files if f["code"] in codes]
        if dates:
            available_files = [f for f in available_files if f["date"] in dates]

        if not available_files:
            return {
                "total_files": 0,
                "total_events": 0,
                "results": [],
                "overall_stats": {}
            }

        # 각 파일에 대해 백테스트 실행
        results = []
        all_events = []

        for file_info in available_files:
            try:
                result = self.run_backtest(
                    code=file_info["code"],
                    date=file_info["date"],
                    threshold_value=threshold_value
                )
                results.append(result)
                all_events.extend(result.events)
            except Exception as e:
                print(f"[BACKTEST] Error processing {file_info['filename']}: {e}")

        # 전체 통계 계산
        overall_stats = {}
        for minutes in self.TRACKING_INTERVALS:
            returns = [e.returns.get(minutes) for e in all_events if minutes in e.returns]
            if returns:
                avg_return = sum(returns) / len(returns)
                wins = len([r for r in returns if r > 0])
                win_rate = wins / len(returns) * 100

                overall_stats[minutes] = {
                    "avg_return": round(avg_return, 4),
                    "win_rate": round(win_rate, 2),
                    "count": len(returns),
                    "wins": wins,
                    "losses": len(returns) - wins
                }

        return {
            "total_files": len(results),
            "total_events": len(all_events),
            "threshold_value": threshold_value,
            "results": [self._result_to_dict(r) for r in results],
            "overall_stats": overall_stats
        }

    def _result_to_dict(self, result: BacktestResult) -> Dict[str, Any]:
        """BacktestResult를 dict로 변환"""
        return {
            "code": result.code,
            "date": result.date,
            "threshold_value": result.threshold_value,
            "total_events": result.total_events,
            "stats": result.stats,
            "events": [
                {
                    "idx": e.idx,
                    "time": e.time,
                    "event_type": e.event_type,
                    "price_at_event": e.price_at_event,
                    "delta_vol": e.delta_vol,
                    "estimated_value": e.estimated_value,
                    "prices_after": e.prices_after,
                    "returns": e.returns
                }
                for e in result.events
            ]
        }

    def generate_backtest_report(self, result: BacktestResult) -> str:
        """
        백테스트 결과 리포트 생성

        Args:
            result: BacktestResult

        Returns:
            str: 텍스트 리포트
        """
        lines = [
            "=" * 60,
            f"백테스트 리포트 - {result.code} ({result.date})",
            "=" * 60,
            "",
            f"임계값: {result.threshold_value:,}원",
            f"총 이벤트: {result.total_events}건",
            ""
        ]

        if result.stats:
            lines.append("[수익률 통계]")
            for minutes in self.TRACKING_INTERVALS:
                if minutes in result.stats:
                    s = result.stats[minutes]
                    sign = '+' if s['avg_return'] >= 0 else ''
                    lines.append(
                        f"  {minutes}분 후: 평균 {sign}{s['avg_return']:.2f}% | "
                        f"승률 {s['win_rate']:.1f}% ({s['wins']}/{s['count']})"
                    )
        else:
            lines.append("[수익률 통계]")
            lines.append("  데이터 없음")

        lines.append("")

        if result.events:
            lines.append("[이벤트 상세 (최근 10건)]")
            for event in result.events[-10:]:
                lines.append(f"  시간: {event.time} | 가격: {event.price_at_event:,}원 | "
                            f"변동량: {event.delta_vol:,}주 | 금액: {event.estimated_value:,.0f}원")
                if event.returns:
                    returns_str = ", ".join([
                        f"{m}분:{'+' if r >= 0 else ''}{r:.2f}%"
                        for m, r in sorted(event.returns.items())
                    ])
                    lines.append(f"    → 수익률: {returns_str}")

        lines.append("")
        lines.append("=" * 60)

        return "\n".join(lines)


def create_backtester(uph_data_dir: str = "uph_raw_data") -> Backtester:
    """백테스터 팩토리 함수"""
    return Backtester(uph_data_dir=uph_data_dir)
