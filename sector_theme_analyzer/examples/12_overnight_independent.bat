@echo off
chcp 65001 > nul

REM ============================================================================
REM 야간 독립 실행 (VS Code와 완전 분리) - 헬퍼 파일 방식
REM ============================================================================
REM
REM 이 파일을 실행하면:
REM   1. 임시 배치 파일을 생성
REM   2. 새로운 독립 CMD 창에서 실행
REM   3. VS Code를 완전히 종료해도 테스트 계속 진행
REM   4. 결과는 logs 폴더에 저장됨
REM
REM ============================================================================

echo ============================================================================
echo   야간 독립 테스트 시작
echo ============================================================================
echo.

REM ============================================================================
REM 아래 옵션들을 원하는 대로 수정하세요
REM ============================================================================

set CONDITIONS=A,D,H,B
set REQUIRED=
set START_DATE=20241101
set END_DATE=20251205
set TP=10
set SL=-5
set MAX_HOLDING=7
set MIN_TRADES=50
set MIN_SIZE=2
set MAX_SIZE=3

REM 상위 폴더 경로 (combination_tester.py 위치)
set WORK_DIR=%~dp0..

REM 임시 실행 파일 생성
set TEMP_BAT=%TEMP%\combo_test_runner.bat

echo @echo off > "%TEMP_BAT%"
echo chcp 65001 ^> nul >> "%TEMP_BAT%"
echo cd /d "%WORK_DIR%" >> "%TEMP_BAT%"
echo echo. >> "%TEMP_BAT%"
echo echo ============================================================================ >> "%TEMP_BAT%"
echo echo   Combination Tester 실행 중... >> "%TEMP_BAT%"
echo echo   VS Code를 닫아도 이 창은 계속 실행됩니다. >> "%TEMP_BAT%"
echo echo ============================================================================ >> "%TEMP_BAT%"
echo echo. >> "%TEMP_BAT%"
echo python combination_tester.py ^
    --conditions %CONDITIONS% ^
    --start-date %START_DATE% ^
    --end-date %END_DATE% ^
    --tp %TP% ^
    --sl %SL% ^
    --max-holding %MAX_HOLDING% ^
    --min-trades %MIN_TRADES% ^
    --min-size %MIN_SIZE% ^
    --max-size %MAX_SIZE% ^
    --log >> "%TEMP_BAT%"
echo echo. >> "%TEMP_BAT%"
echo echo ============================================================================ >> "%TEMP_BAT%"
echo echo   테스트 완료! logs 폴더에서 결과를 확인하세요. >> "%TEMP_BAT%"
echo echo ============================================================================ >> "%TEMP_BAT%"
echo pause >> "%TEMP_BAT%"

echo 설정된 옵션:
echo   CONDITIONS: %CONDITIONS%
echo   기간: %START_DATE% ~ %END_DATE%
echo   TP: %TP%%% / SL: %SL%%%
echo   최대보유: %MAX_HOLDING%일
echo   최소거래: %MIN_TRADES%건
echo   조합크기: %MIN_SIZE% ~ %MAX_SIZE%
echo.
echo 새 CMD 창에서 테스트를 시작합니다...
timeout /t 3 > nul

REM 독립 CMD 창에서 실행
start "Combination Tester" cmd /c "%TEMP_BAT%"

echo.
echo 이 창은 닫아도 됩니다. 테스트는 새 창에서 계속 진행됩니다.
timeout /t 5
