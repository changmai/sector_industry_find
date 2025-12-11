"""
조건 조합 파서 (Condition Parser)

AND/OR 표현식을 파싱하여 조건들을 조합합니다.

지원 문법:
    - AND: 교집합
    - OR: 합집합
    - 괄호: 우선순위 지정

사용 예시:
    parser = ConditionParser(engine)

    # 단순 조합
    result = parser.parse("A AND B", base_date)

    # 복합 조합
    result = parser.parse("A AND (B OR C) AND D", base_date)

    # 조건만
    result = parser.parse("A", base_date)
"""
import re
from typing import Optional
from condition_engine import ConditionEngine


class ConditionParser:
    """AND/OR 조합 표현식 파서"""

    def __init__(self, engine: ConditionEngine, params: dict = None):
        """
        Args:
            engine: 조건 평가 엔진
            params: 조건별 파라미터 딕셔너리
                    예: {'A': {'days': 5}, 'C': {'top_n': 50}}
        """
        self.engine = engine
        self.params = params or {}

    def parse(self, expression: str, base_date: str) -> set[str]:
        """
        조건 표현식 파싱 및 평가

        Args:
            expression: 조건 표현식 (예: "A AND (B OR C)")
            base_date: 기준일 (YYYYMMDD)

        Returns:
            set[str]: 조건 충족 종목코드 집합
        """
        # 표현식 정규화
        expr = expression.upper().strip()

        # 공백 정리
        expr = re.sub(r'\s+', ' ', expr)

        # 파싱
        try:
            result = self._evaluate_expression(expr, base_date)
            return result
        except Exception as e:
            print(f"   [ERROR] 표현식 파싱 실패: {expression}")
            print(f"   {e}")
            return set()

    def _evaluate_expression(self, expr: str, base_date: str) -> set[str]:
        """재귀적 표현식 평가"""
        expr = expr.strip()

        # 괄호 처리
        while '(' in expr:
            # 가장 안쪽 괄호 찾기
            match = re.search(r'\(([^()]+)\)', expr)
            if match:
                inner = match.group(1)
                result = self._evaluate_expression(inner, base_date)

                # 임시 플레이스홀더로 치환
                placeholder = f"__RESULT_{id(result)}__"
                self._temp_results = getattr(self, '_temp_results', {})
                self._temp_results[placeholder] = result

                expr = expr[:match.start()] + placeholder + expr[match.end():]
            else:
                break

        # OR 처리 (우선순위 낮음)
        if ' OR ' in expr:
            parts = expr.split(' OR ')
            result = set()
            for part in parts:
                part_result = self._evaluate_expression(part.strip(), base_date)
                result = result | part_result
            return result

        # AND 처리
        if ' AND ' in expr:
            parts = expr.split(' AND ')
            result = None
            for part in parts:
                part_result = self._evaluate_expression(part.strip(), base_date)
                if result is None:
                    result = part_result
                else:
                    result = result & part_result
            return result if result is not None else set()

        # 단일 조건 또는 플레이스홀더
        expr = expr.strip()

        # 플레이스홀더 확인
        if expr.startswith('__RESULT_') and expr.endswith('__'):
            return self._temp_results.get(expr, set())

        # 기본 조건 목록
        valid_conditions = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}
        # GT 조건 목록
        gt_conditions = {'GT_P1', 'GT_M1', 'GT_M2', 'GT_A', 'GT_B', 'GT_B1', 'GT_B2',
                         'GT_C', 'GT_D', 'GT_D2', 'GT_E', 'GT_F'}

        # 단일 조건 평가
        if expr in valid_conditions or expr in gt_conditions:
            condition_params = self.params.get(expr, {})
            # description 필드 제외 (함수 파라미터가 아님)
            condition_params = {k: v for k, v in condition_params.items() if k != 'description'}

            # GT_M1, GT_M2는 bool 반환 -> set으로 변환 필요
            result = self.engine.evaluate(expr, base_date, condition_params)

            # 시장 조건(GT_M1, GT_M2)은 bool 반환 - 전체 종목 또는 빈 set 반환
            if expr in ['GT_M1', 'GT_M2']:
                if isinstance(result, bool):
                    if result:
                        # True면 제한 없음 (모든 종목 통과)
                        return self._get_all_stock_codes()
                    else:
                        # False면 아무 종목도 통과 못함
                        return set()
                elif isinstance(result, dict) and 'result' in result:
                    if result['result']:
                        return self._get_all_stock_codes()
                    else:
                        return set()

            return result

        print(f"   [WARN] 알 수 없는 토큰: {expr}")
        return set()

    def _get_all_stock_codes(self) -> set:
        """엔진에 로드된 모든 종목코드 반환"""
        if hasattr(self.engine, 'stocks'):
            return {s.get('단축코드', '') for s in self.engine.stocks if s.get('단축코드')}
        return set()

    def validate_expression(self, expression: str) -> tuple[bool, str]:
        """
        표현식 유효성 검사

        Returns:
            tuple[bool, str]: (유효 여부, 오류 메시지)
        """
        expr = expression.upper().strip()

        # 괄호 짝 확인
        if expr.count('(') != expr.count(')'):
            return False, "괄호 짝이 맞지 않습니다"

        # 기본 조건 목록
        valid_conditions = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}
        # GT 조건 목록
        gt_conditions = {'GT_P1', 'GT_M1', 'GT_M2', 'GT_A', 'GT_B', 'GT_B1', 'GT_B2',
                         'GT_C', 'GT_D', 'GT_D2', 'GT_E', 'GT_F'}

        # GT_ 조건 추출
        gt_tokens = re.findall(r'GT_[A-Z0-9]+', expr)
        for gt_token in gt_tokens:
            if gt_token not in gt_conditions:
                return False, f"알 수 없는 GT 조건: {gt_token}"

        # GT 토큰 제거 후 단일 문자 조건 확인
        expr_without_gt = re.sub(r'GT_[A-Z0-9]+', '', expr)
        tokens = re.findall(r'\b[A-I]\b', expr_without_gt)

        invalid = [t for t in tokens if t not in valid_conditions]
        if invalid:
            return False, f"알 수 없는 조건: {', '.join(set(invalid))}"

        return True, "OK"


def parse_conditions(expression: str, engine: ConditionEngine, base_date: str, params: dict = None) -> set[str]:
    """
    헬퍼 함수: 조건 표현식 파싱

    Args:
        expression: 조건 표현식
        engine: 조건 평가 엔진
        base_date: 기준일
        params: 조건별 파라미터

    Returns:
        set[str]: 조건 충족 종목코드 집합
    """
    parser = ConditionParser(engine, params)
    return parser.parse(expression, base_date)


if __name__ == "__main__":
    # 테스트
    from condition_engine import ConditionEngine

    engine = ConditionEngine()
    if engine.load_data():
        parser = ConditionParser(engine)
        base_date = "20251205"

        test_expressions = [
            "A",
            "A AND B",
            "A OR B",
            "A AND B AND C",
            "A AND (B OR C)",
            "(A OR B) AND (C OR D)",
        ]

        print("\n[테스트] 조건 조합 파싱")
        print("=" * 60)

        for expr in test_expressions:
            valid, msg = parser.validate_expression(expr)
            if valid:
                result = parser.parse(expr, base_date)
                print(f"   {expr:<30} → {len(result):>4}개 종목")
            else:
                print(f"   {expr:<30} → [ERROR] {msg}")

        print("=" * 60)
