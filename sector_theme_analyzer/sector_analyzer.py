"""
업종 연속 상승 분석 모듈

t8424: 전체 업종 목록 조회
t1514: 업종 기간별 추이 조회 (sign 값으로 연속 상승 판단)
"""
from typing import Optional
from ls_api_client import LSApiClient
from config import AnalysisConfig, DEFAULT_CONFIG


class SectorAnalyzer:
    """
    업종 연속 상승 분석기

    t1514 API로 각 업종의 N일치 기간별 추이를 조회하고,
    sign 값이 모두 "1"(상한) 또는 "2"(상승)인 업종을 찾습니다.
    """

    def __init__(self, api_client: LSApiClient, config: AnalysisConfig = None):
        """
        Args:
            api_client: LS증권 API 클라이언트
            config: 분석 설정
        """
        self.api = api_client
        self.config = config or DEFAULT_CONFIG
        self.all_sectors: list[dict] = []
        self.rising_sectors: list[dict] = []
        self.actual_base_date: str = ""

    def fetch_all_sectors(self) -> list[dict]:
        """전체 업종 목록 조회"""
        print(f"\n   [t8424] 전체 업종 목록 조회 중...")
        self.all_sectors = self.api.get_all_sectors()
        print(f"   -> {len(self.all_sectors)}개 업종 조회 완료")
        return self.all_sectors

    def _filter_target_sectors(self) -> list[dict]:
        """
        분석 대상 업종 필터링 (005~030)

        Returns:
            list[dict]: 필터링된 업종 목록
        """
        min_code, max_code = self.config.sector_range
        target_sectors = []

        for sector in self.all_sectors:
            upcode = sector.get("upcode", "")
            try:
                code_num = int(upcode)
                if min_code <= code_num <= max_code:
                    target_sectors.append(sector)
            except (ValueError, TypeError):
                continue

        return target_sectors

    def _is_rising(self, period_data: list[dict], days: int) -> bool:
        """
        상승 여부 판단 (X일 평균 등락률 양수)

        Args:
            period_data: 기간별 추이 데이터
            days: 기준 일수

        Returns:
            bool: 평균 등락률이 양수인지 여부
        """
        if len(period_data) < days:
            return False

        # X일 평균 등락률 계산
        avg_change = self._calculate_avg_change(period_data, days)
        return avg_change > 0

    def _calculate_total_change(self, period_data: list[dict], days: int) -> float:
        """총 등락율 계산"""
        if len(period_data) < days:
            return 0.0

        sorted_data = sorted(period_data, key=lambda x: x.get("date", ""))
        recent_data = sorted_data[-days:]

        total = 0.0
        for data in recent_data:
            try:
                diff = float(data.get("diff", "0") or "0")
                total += diff
            except (ValueError, TypeError):
                pass

        return total

    def _calculate_avg_change(self, period_data: list[dict], days: int) -> float:
        """평균 등락율 계산"""
        total = self._calculate_total_change(period_data, days)
        return total / days if days > 0 else 0.0

    def find_rising_sectors(self, base_date: str, days: int = 5) -> list[dict]:
        """
        N거래일 연속 상승 업종 탐색

        Args:
            base_date: 기준일 (YYYYMMDD)
            days: 연속 상승 판단 기준 일수

        Returns:
            list[dict]: 연속 상승 업종 정보 리스트
        """
        print("\n" + "="*60)
        print(f"   [SECTOR] 업종 {days}거래일 평균 상승 탐색")
        print(f"   [BASE DATE] 기준일: {base_date}")
        print("="*60)

        # 1. 전체 업종 목록 조회
        self.fetch_all_sectors()

        # 2. 분석 대상 업종 필터링 (005~030)
        target_sectors = self._filter_target_sectors()
        print(f"\n   [FILTER] 분석 대상 업종: {len(target_sectors)}개 (업종코드 {self.config.sector_range[0]:03d}~{self.config.sector_range[1]:03d})")

        # 3. 각 업종별 기간 추이 조회 및 연속 상승 판단
        print(f"\n   [t1514] 업종별 기간 추이 조회 중...")
        self.rising_sectors = []
        total = len(target_sectors)

        for i, sector in enumerate(target_sectors, 1):
            upcode = sector.get("upcode", "")
            hname = sector.get("hname", "").strip()

            # 진행 상황
            if i % 5 == 0 or i == 1:
                print(f"   -> 조회 중... {i}/{total}", flush=True)

            # 기간 추이 조회
            period_data = self.api.get_sector_period(upcode, base_date, cnt=days + 2)

            if not period_data:
                continue

            # 실제 기준일 저장
            if not self.actual_base_date and period_data:
                sorted_data = sorted(period_data, key=lambda x: x.get("date", ""), reverse=True)
                self.actual_base_date = sorted_data[0].get("date", "") if sorted_data else ""
                if self.actual_base_date != base_date:
                    print(f"   [INFO] 실제 조회 기준일: {self.actual_base_date} (요청: {base_date})")

            # 상승 판단 (평균 등락률 양수)
            if self._is_rising(period_data, days):
                total_change = self._calculate_total_change(period_data, days)
                avg_change = self._calculate_avg_change(period_data, days)

                sorted_data = sorted(period_data, key=lambda x: x.get("date", ""))
                recent_data = sorted_data[-days:]

                self.rising_sectors.append({
                    "upcode": upcode,
                    "hname": hname,
                    "total_change": round(total_change, 2),
                    "avg_change": round(avg_change, 2),
                    "period_data": [
                        {
                            "date": d.get("date", ""),
                            "sign": d.get("sign", ""),
                            "diff": d.get("diff", ""),
                            "jisu": d.get("jisu", "")
                        }
                        for d in recent_data
                    ]
                })

        print(f"\n   [RESULT] {days}거래일 평균 상승 업종: {len(self.rising_sectors)}개")

        # 총 등락율 기준 정렬
        self.rising_sectors.sort(key=lambda x: x.get("total_change", 0), reverse=True)

        return self.rising_sectors

    def get_rising_sector_codes(self) -> set:
        """연속 상승 업종 코드 집합 반환"""
        return {s.get("upcode", "") for s in self.rising_sectors}

    def print_results(self):
        """결과 출력"""
        if not self.rising_sectors:
            print("\n   연속 상승 업종이 없습니다.")
            return

        print("\n" + "-"*60)
        print(f"   {'업종코드':<6} {'업종명':<20} {'총등락율':>10} {'평균':>8}")
        print("-"*60)

        for sector in self.rising_sectors:
            upcode = sector.get("upcode", "")
            hname = sector.get("hname", "")[:18]
            total_change = sector.get("total_change", 0)
            avg_change = sector.get("avg_change", 0)
            print(f"   {upcode:<6} {hname:<20} {total_change:>+10.2f}% {avg_change:>+7.2f}%")

        print("-"*60)


if __name__ == "__main__":
    # 테스트 실행
    from datetime import datetime

    config = AnalysisConfig(base_date="20251201")
    api = LSApiClient(config)
    analyzer = SectorAnalyzer(api, config)

    rising_sectors = analyzer.find_rising_sectors("20251201", 5)
    analyzer.print_results()
