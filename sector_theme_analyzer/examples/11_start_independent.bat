@echo off
chcp 65001 > nul

REM ============================================================================
REM 독립 CMD 창에서 실행 (VS Code와 완전 분리)
REM ============================================================================
REM
REM 이 파일을 실행하면:
REM   1. 새로운 독립 CMD 창이 열림
REM   2. VS Code를 완전히 종료해도 테스트 계속 진행
REM   3. 결과는 logs 폴더에 저장됨
REM
REM 주의: 새 창이 열린 후 이 창은 자동으로 닫힙니다
REM ============================================================================

echo 새 CMD 창에서 테스트를 시작합니다...
echo 이 창은 자동으로 닫힙니다.
timeout /t 2 > nul

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

REM 상위 폴더 경로 설정
set SCRIPT_DIR=%~dp0..

REM 독립 CMD 창에서 실행
start "Combination Tester" cmd /k "cd /d "%SCRIPT_DIR%" && python combination_tester.py --conditions %CONDITIONS% --start-date %START_DATE% --end-date %END_DATE% --tp %TP% --sl %SL% --max-holding %MAX_HOLDING% --min-trades %MIN_TRADES% --min-size %MIN_SIZE% --max-size %MAX_SIZE% --log && echo. && echo 테스트 완료! logs 폴더 확인 && pause"
