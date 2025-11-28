"""
리포트 생성 모듈
일간 통계 및 수익률 분석 리포트 생성
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from .research_db import ResearchDB


class ReportGenerator:
    """
    프로그램 매매 전략 검증 리포트 생성기
    """

    def __init__(self, db: ResearchDB, stock_name_getter: callable = None):
        """
        Args:
            db: ResearchDB 인스턴스
            stock_name_getter: 종목코드 -> 종목명 변환 함수 (옵션)
        """
        self.db = db
        self._stock_name_getter = stock_name_getter

    def set_stock_name_getter(self, getter: callable):
        """종목명 조회 함수 설정"""
        self._stock_name_getter = getter

    def _get_stock_name(self, code: str) -> str:
        """종목명 조회"""
        if self._stock_name_getter:
            try:
                return self._stock_name_getter(code) or code
            except:
                pass
        return code

    async def generate_daily_report(self, date: str = None) -> str:
        """
        일간 리포트 생성

        Args:
            date: 날짜 (YYYY-MM-DD), 기본값은 오늘

        Returns:
            str: 리포트 텍스트
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        # 이벤트와 추적 데이터 조회
        events_data = await self.db.get_events_with_tracking(date)

        if not events_data:
            return f"""
==========================================
프로그램 매매 전략 검증 리포트 - {date}
==========================================

이벤트가 없습니다.
==========================================
"""

        # 종목별 집계
        by_code: Dict[str, List[Dict]] = {}
        for event in events_data:
            code = event['code']
            if code not in by_code:
                by_code[code] = []
            by_code[code].append(event)

        # 리포트 생성
        lines = [
            "=" * 50,
            f"프로그램 매매 전략 검증 리포트 - {date}",
            "=" * 50,
            ""
        ]

        total_events = 0
        all_returns = {1: [], 5: [], 10: [], 30: []}

        for code, events in sorted(by_code.items()):
            stock_name = self._get_stock_name(code)
            total_events += len(events)

            # 수익률 집계
            returns = {1: [], 5: [], 10: [], 30: []}
            for event in events:
                tracking = event.get('tracking', {})
                for minutes in [1, 5, 10, 30]:
                    if minutes in tracking and tracking[minutes] is not None:
                        returns[minutes].append(tracking[minutes])
                        all_returns[minutes].append(tracking[minutes])

            lines.append(f"[{code} {stock_name}]")
            lines.append(f"- 총 이벤트: {len(events)}건")
            lines.append("- 평균 수익률:")

            for minutes in [1, 5, 10, 30]:
                if returns[minutes]:
                    avg = sum(returns[minutes]) / len(returns[minutes])
                    sign = '+' if avg >= 0 else ''
                    lines.append(f"  * {minutes}분 후: {sign}{avg:.2f}%")
                else:
                    lines.append(f"  * {minutes}분 후: 데이터 없음")

            lines.append("- 승률 (양수 수익):")
            for minutes in [1, 5, 10, 30]:
                if returns[minutes]:
                    wins = len([r for r in returns[minutes] if r > 0])
                    win_rate = wins / len(returns[minutes]) * 100
                    lines.append(f"  * {minutes}분 후: {win_rate:.1f}% ({wins}/{len(returns[minutes])})")
                else:
                    lines.append(f"  * {minutes}분 후: 데이터 없음")

            lines.append("")

        # 전체 요약
        lines.append("-" * 50)
        lines.append("[전체 요약]")
        lines.append(f"- 총 이벤트: {total_events}건")
        lines.append(f"- 종목 수: {len(by_code)}개")

        for minutes in [1, 5, 10, 30]:
            if all_returns[minutes]:
                avg = sum(all_returns[minutes]) / len(all_returns[minutes])
                wins = len([r for r in all_returns[minutes] if r > 0])
                win_rate = wins / len(all_returns[minutes]) * 100
                sign = '+' if avg >= 0 else ''
                lines.append(f"- {minutes}분 후 전체 평균: {sign}{avg:.2f}% | 승률: {win_rate:.1f}%")

        lines.append("=" * 50)

        return "\n".join(lines)

    async def generate_event_detail_report(self, event_id: int) -> str:
        """
        이벤트 상세 리포트 생성

        Args:
            event_id: program_events.id

        Returns:
            str: 리포트 텍스트
        """
        event = await self.db.get_event_by_id(event_id)
        if not event:
            return f"이벤트 #{event_id}를 찾을 수 없습니다."

        trackings = await self.db.get_price_tracking_for_event(event_id)

        stock_name = self._get_stock_name(event.code)

        lines = [
            "=" * 50,
            f"이벤트 상세 리포트 - #{event_id}",
            "=" * 50,
            "",
            f"종목: {event.code} {stock_name}",
            f"발생 시간: {event.event_time}",
            f"이벤트 유형: {event.event_type}",
            f"트리거 금액: {event.trigger_value:,.0f}원",
            f"이벤트 시점 가격: {event.price_at_event:,}원",
            "",
            "[프로그램 매매 데이터]",
            f"- 비차익 매수 변동량: {event.delta_vol:,}주",
            f"- 비차익매수호가잔량: {event.bshrem:,}",
            f"- 비차익매도호가잔량: {event.bdhrem:,}",
            f"- 비차익매수체결수량: {event.bshvolume:,}",
            f"- 비차익매도체결수량: {event.bdhvolume:,}",
            f"- 전체순매수금액: {event.tval:,}원",
            ""
        ]

        if trackings:
            lines.append("[가격 추적 결과]")
            for t in trackings:
                sign = '+' if t.price_change_pct >= 0 else ''
                lines.append(
                    f"- {t.minutes_after}분 후: {t.price:,}원 "
                    f"({sign}{t.price_change_pct:.2f}%) @ {t.tracking_time}"
                )
        else:
            lines.append("[가격 추적 결과]")
            lines.append("- 추적 데이터 없음 (추적 진행 중이거나 데이터 수집 실패)")

        lines.append("")
        lines.append("=" * 50)

        return "\n".join(lines)

    async def generate_summary_json(self, date: str = None) -> Dict[str, Any]:
        """
        JSON 형식 일간 요약 생성

        Args:
            date: 날짜 (YYYY-MM-DD)

        Returns:
            dict: 요약 데이터
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        events_data = await self.db.get_events_with_tracking(date)

        # 종목별 집계
        by_code: Dict[str, Dict] = {}
        all_returns = {1: [], 5: [], 10: [], 30: []}

        for event in events_data:
            code = event['code']
            if code not in by_code:
                by_code[code] = {
                    'code': code,
                    'name': self._get_stock_name(code),
                    'events': 0,
                    'returns': {1: [], 5: [], 10: [], 30: []}
                }

            by_code[code]['events'] += 1
            tracking = event.get('tracking', {})

            for minutes in [1, 5, 10, 30]:
                if minutes in tracking and tracking[minutes] is not None:
                    by_code[code]['returns'][minutes].append(tracking[minutes])
                    all_returns[minutes].append(tracking[minutes])

        # 종목별 통계 계산
        stocks_summary = []
        for code, data in sorted(by_code.items()):
            stock_stats = {
                'code': code,
                'name': data['name'],
                'total_events': data['events'],
                'stats': {}
            }

            for minutes in [1, 5, 10, 30]:
                returns = data['returns'][minutes]
                if returns:
                    avg = sum(returns) / len(returns)
                    wins = len([r for r in returns if r > 0])
                    win_rate = wins / len(returns) * 100
                    stock_stats['stats'][f'{minutes}m'] = {
                        'avg_return': round(avg, 4),
                        'win_rate': round(win_rate, 2),
                        'samples': len(returns)
                    }
                else:
                    stock_stats['stats'][f'{minutes}m'] = None

            stocks_summary.append(stock_stats)

        # 전체 통계
        total_stats = {}
        for minutes in [1, 5, 10, 30]:
            if all_returns[minutes]:
                avg = sum(all_returns[minutes]) / len(all_returns[minutes])
                wins = len([r for r in all_returns[minutes] if r > 0])
                win_rate = wins / len(all_returns[minutes]) * 100
                total_stats[f'{minutes}m'] = {
                    'avg_return': round(avg, 4),
                    'win_rate': round(win_rate, 2),
                    'samples': len(all_returns[minutes])
                }
            else:
                total_stats[f'{minutes}m'] = None

        return {
            'date': date,
            'total_events': len(events_data),
            'total_stocks': len(by_code),
            'stocks': stocks_summary,
            'overall': total_stats,
            'generated_at': datetime.now().isoformat()
        }

    async def update_daily_summaries(self, date: str = None):
        """모든 종목의 일간 요약 업데이트"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        events = await self.db.get_events_by_date(date)
        codes = set(e.code for e in events)

        for code in codes:
            await self.db.update_daily_summary(date, code)

        print(f"[REPORT] Updated daily summaries for {len(codes)} stocks on {date}")
