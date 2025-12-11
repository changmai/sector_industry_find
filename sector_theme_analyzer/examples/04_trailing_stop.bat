@echo off
chcp 65001 > nul
REM ============================================================================
REM 예시 4: 트레일링 스탑 사용
REM ============================================================================
REM
REM 사용 옵션 설명:
REM   --trailing-start  : 트레일링 시작 수익률 %
REM                       예: 5 = 수익률 5% 도달 시 트레일링 활성화
REM   --trailing-offset : 고점 대비 하락 허용폭 %
REM                       예: 3 = 고점 대비 3% 하락하면 청산
REM
REM 트레일링 스탑 동작 방식:
REM   1. 수익률이 trailing-start(5%)에 도달하면 트레일링 활성화
REM   2. 이후 고점 수익률을 계속 추적
REM   3. 고점 대비 trailing-offset(3%) 하락하면 청산
REM   4. 예: 수익률 8% 도달 후 5%로 하락 → 청산 (8-3=5)
REM
REM 이 예시:
REM   - 5% 수익 도달 시 트레일링 활성화
REM   - 고점 대비 3% 하락 시 청산
REM ============================================================================

cd /d "%~dp0.."

python combination_tester.py ^
    --conditions A,D,H ^
    --start-date 20241101 ^
    --end-date 20251205 ^
    --tp 15 ^
    --sl -5 ^
    --max-holding 10 ^
    --trailing-start 5 ^
    --trailing-offset 3

pause
