@echo off
chcp 65001 > nul
cd /d "%~dp0.."

REM ============================================================================
REM 로그 파일 저장 예시
REM ============================================================================
REM
REM --log 옵션을 사용하면:
REM   1. 진행 상황이 실시간으로 화면에 출력되면서 동시에 로그 파일에도 저장됨
REM   2. 최종 결과가 JSON 파일로도 저장됨 (나중에 분석용)
REM
REM 저장 위치: sector_theme_analyzer/logs/
REM   - combo_test_YYYYMMDD_HHMMSS.log     (전체 로그)
REM   - combo_test_YYYYMMDD_HHMMSS_results.json (결과 JSON)
REM
REM VS Code가 꺼져도 로그 파일은 남아있으므로, 장시간 테스트에 적합함
REM ============================================================================

python combination_tester.py ^
    --conditions A,D,H ^
    --start-date 20241209 ^
    --end-date 20251205 ^
    --tp 10 ^
    --sl -5 ^
    --max-holding 7 ^
    --min-trades 100 ^
    --min-size 2 ^
    --max-size 3 ^
    --log

echo.
echo ============================================================================
echo 테스트 완료! logs 폴더에서 결과를 확인하세요.
echo ============================================================================
pause
