"""
업종 연속 상승 탐색 모듈

t8424: 전체 업종 목록 조회
t1514: 업종 기간별 추이 조회 (5일치 sign 값으로 연속 상승 판단)
"""
from typing import Optional
from ls_api_client import LSApiClient
from config import DEFAULT_CONSECUTIVE_DAYS


class SectorFinder:
    """
    업종 연속 상승 탐색기

    t1514 API로 각 업종의 N일치 기간별 추이를 조회하고,
    sign 값이 모두 "1"(상한) 또는 "2"(상승)인 업종을 찾습니다.
    """

    # 제외할 업종 패턴 (ETF, 레버리지, 인버스 등)
    EXCLUDE_PATTERNS = [
        "ETF", "레버리지", "인버스", "선물", "KODEX", "TIGER",
        "200", "150", "100", "KP200", "KQ150"
    ]

    def __init__(self, api_client: Optional[LSApiClient] = None):
        """
        Args:
            api_client: LS증권 API 클라이언트 (없으면 새로 생성)
        """
        self.api = api_client or LSApiClient()
        self.all_sectors: list[dict] = []
        self.sector_info: dict[str, dict] = {}  # {upcode: {hname, period_data, ...}}
        self.actual_base_date: str = ""  # 실제 조회된 기준일

    def fetch_all_sectors(self, gubun1: str = "") -> list[dict]:
        """
        전체 업종 목록 조회

        Args:
            gubun1: 구분 ("": 전체, "1": 코스피, "2": 코스닥)
        """
        print(f"\n   [t8424] 전체 업종 목록 조회 중...")
        self.all_sectors = self.api.get_all_sectors(gubun1)
        print(f"   -> {len(self.all_sectors)}개 업종 조회 완료")

        # 업종 정보 저장
        for sector in self.all_sectors:
            upcode = sector.get("upcode", "")
            hname = sector.get("hname", "").strip()
            if upcode:
                self.sector_info[upcode] = {
                    "upcode": upcode,
                    "hname": hname
                }

        return self.all_sectors

    def _should_exclude(self, hname: str) -> bool:
        """제외해야 할 업종인지 확인"""
        for pattern in self.EXCLUDE_PATTERNS:
            if pattern in hname:
                return True
        return False

    def _is_consecutive_rising(self, period_data: list[dict], days: int) -> bool:
        """
        연속 상승 여부 판단

        Args:
            period_data: 기간별 추이 데이터
            days: 연속 상승 판단 기준 일수

        Returns:
            bool: 연속 상승 여부
        """
        if len(period_data) < days:
            return False

        # 최근 N일 데이터만 확인 (최신순으로 정렬되어 있다고 가정)
        recent_data = period_data[:days]

        for data in recent_data:
            sign = str(data.get("sign", ""))
            # sign: 1=상한, 2=상승, 3=보합, 4=하한, 5=하락
            if sign not in ("1", "2"):
                return False

        return True

    def _calculate_total_change(self, period_data: list[dict], days: int) -> float:
        """총 등락율 계산"""
        if len(period_data) < days:
            return 0.0

        total = 0.0
        for data in period_data[:days]:
            try:
                diff = float(data.get("diff", "0") or "0")
                total += diff
            except (ValueError, TypeError):
                pass

        return total

    def find_rising_sectors(self, days: int = DEFAULT_CONSECUTIVE_DAYS, base_date: str = "") -> list[dict]:
        """
        N거래일 연속 상승 업종 탐색

        Args:
            days: 연속 상승 판단 기준 일수 (기본 5일)
            base_date: 기준일 (YYYYMMDD 형식, 빈 문자열이면 오늘 기준)

        Returns:
            list[dict]: 연속 상승 업종 정보 리스트
        """
        # 기준일 표시
        base_date_display = base_date if base_date else "오늘"
        cts_date = base_date if base_date else " "

        print("\n" + "="*60)
        print(f"   [SECTOR] 업종 {days}거래일 연속 상승 탐색")
        if base_date:
            print(f"   [BASE DATE] 기준일: {base_date}")
        print("="*60)

        # 1. 전체 업종 목록 조회
        self.fetch_all_sectors()

        # 2. 각 업종별 기간 추이 조회 및 연속 상승 판단
        print(f"\n   [t1514] 업종별 기간 추이 조회 중...")
        print(f"   (254개 업종 x 1초 딜레이 = 약 4-5분 소요)")
        rising_sectors = []
        total = len(self.all_sectors)
        checked = 0

        for i, sector in enumerate(self.all_sectors, 1):
            upcode = sector.get("upcode", "")
            hname = sector.get("hname", "").strip()

            # 제외 업종 스킵
            if self._should_exclude(hname):
                continue

            checked += 1
            # 진행 상황 (10개마다)
            if checked % 10 == 0 or checked == 1:
                print(f"   -> 조회 중... {checked}개 완료 (전체 진행: {i}/{total})", flush=True)

            # 기간 추이 조회 (base_date 전달)
            period_data = self.api.get_sector_period(upcode, cnt=days, cts_date=cts_date)

            if not period_data:
                continue

            # 실제 기준일 저장 (첫 번째 데이터의 날짜)
            if not self.actual_base_date and period_data:
                self.actual_base_date = period_data[0].get("date", "")
                if base_date and self.actual_base_date != base_date:
                    print(f"   [INFO] 실제 조회 기준일: {self.actual_base_date} (요청: {base_date})")

            # 업종 정보 업데이트
            self.sector_info[upcode]["period_data"] = period_data

            # 연속 상승 판단
            if self._is_consecutive_rising(period_data, days):
                total_change = self._calculate_total_change(period_data, days)

                rising_sectors.append({
                    "upcode": upcode,
                    "hname": hname,
                    "total_change": round(total_change, 2),
                    "period_data": [
                        {
                            "date": d.get("date", ""),
                            "sign": d.get("sign", ""),
                            "diff": d.get("diff", ""),
                            "jisu": d.get("jisu", "")
                        }
                        for d in period_data[:days]
                    ]
                })

        print(f"\n   [RESULT] {days}거래일 연속 상승 업종: {len(rising_sectors)}개")

        # 총 등락율 기준 정렬
        rising_sectors.sort(key=lambda x: x.get("total_change", 0), reverse=True)

        return rising_sectors

    def get_rising_sector_codes(self) -> set:
        """연속 상승 업종 코드 집합 반환"""
        rising_codes = set()
        for upcode, info in self.sector_info.items():
            period_data = info.get("period_data", [])
            if period_data and self._is_consecutive_rising(period_data, DEFAULT_CONSECUTIVE_DAYS):
                rising_codes.add(upcode)
        return rising_codes

    def print_results(self, sectors: list[dict]):
        """결과 출력"""
        if not sectors:
            print("\n   연속 상승 업종이 없습니다.")
            return

        print("\n" + "-"*60)
        print(f"   {'업종코드':<6} {'업종명':<20} {'총등락율':>10}")
        print("-"*60)

        for sector in sectors:
            upcode = sector.get("upcode", "")
            hname = sector.get("hname", "")[:18]
            total_change = sector.get("total_change", 0)
            print(f"   {upcode:<6} {hname:<20} {total_change:>+10.2f}%")

        print("-"*60)


if __name__ == "__main__":
    # 테스트 실행
    finder = SectorFinder()
    rising_sectors = finder.find_rising_sectors(5)
    finder.print_results(rising_sectors)
