@echo off
chcp 65001 > nul
REM ============================================================================
REM 예시 5: 타임컷 사용
REM ============================================================================
REM
REM 사용 옵션 설명:
REM   --time-cut-days       : 타임컷 체크 일수
REM                           예: 3 = 3일차 종가 기준으로 수익률 체크
REM   --time-cut-min-return : 타임컷 최소 수익률 %
REM                           예: 2 = 2% 미만이면 청산
REM
REM 타임컷 동작 방식:
REM   1. 매수 후 time-cut-days(3)일 경과 시점에서 수익률 체크
REM   2. 수익률이 time-cut-min-return(2%) 미만이면 즉시 청산
REM   3. 모멘텀 없는 종목 조기 손절에 유용
REM
REM 이 예시:
REM   - 3일차에 수익률 체크
REM   - 2% 미만이면 청산 (모멘텀 부족 판단)
REM ============================================================================

cd /d "%~dp0.."

python combination_tester.py ^
    --conditions A,D,H ^
    --start-date 20241101 ^
    --end-date 20251205 ^
    --tp 10 ^
    --sl -5 ^
    --max-holding 10 ^
    --time-cut-days 3 ^
    --time-cut-min-return 2

pause
