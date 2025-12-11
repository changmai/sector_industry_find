@echo off
chcp 65001 > nul

REM ============================================================================
REM combination_tester.py 전체 옵션 테스트 (모든 기능 포함)
REM ============================================================================
REM
REM 이 파일 하나로 combination_tester.py의 모든 옵션을 사용할 수 있습니다.
REM --log 옵션으로 결과가 logs 폴더에 저장됩니다.
REM
REM 사용 방법:
REM   1. 아래 옵션들을 원하는 대로 수정
REM   2. 사용 안할 옵션은 값을 비워두기 (예: set REQUIRED=)
REM   3. 이 파일을 더블클릭하여 실행
REM   4. 테스트 완료 후 logs 폴더에서 결과 확인
REM
REM ============================================================================

REM ============================================================================
REM [필수 설정] 반드시 입력해야 하는 옵션
REM ============================================================================

REM 테스트할 조건들 (콤마로 구분)
REM 사용 가능: A,B,C,D,E,F,G,H,I,GT_A,GT_B,GT_B1,GT_B2,GT_C,GT_D,GT_D2,GT_E,GT_F,GT_M1,GT_M2,GT_P1
set CONDITIONS=GT_C,GT_D,GT_D2,GT_E,GT_F

REM 테스트 기간 (YYYYMMDD 형식)
set START_DATE=20240601
set END_DATE=20250630

REM ============================================================================
REM [기본 설정] TP/SL 및 필터링 옵션
REM ============================================================================

REM 필수 조건 (모든 조합에 포함, 비워두면 사용 안함)
REM 예: D 또는 A,B 또는 "A AND B"
set REQUIRED=GT_A,GT_B

REM TP/SL 설정 (고정 모드에서 사용)
set TP=10
set SL=-5

REM 최대 보유일 (기본값: 14)
set MAX_HOLDING=14

REM 최소 거래 건수 - 이하는 무효 처리 (기본값: 100)
set MIN_TRADES=100

REM 조합 크기 범위
set MIN_SIZE=0
set MAX_SIZE=2

REM ============================================================================
REM [출력 설정] 결과 정렬 및 표시 옵션
REM ============================================================================

REM 정렬 기준 (avg_return 또는 win_rate)
set SORT_BY=avg_return

REM 상위 N개 결과만 출력 (기본값: 20)
set TOP_N=30

REM ============================================================================
REM [로깅 설정] 로그 파일 저장 옵션
REM ============================================================================

REM 로그 저장 여부 (YES 또는 비워두기)
REM YES로 설정하면 logs 폴더에 .log 와 .json 파일 생성
set USE_LOG=YES

REM 로그 저장 디렉토리 (비워두면 기본값 ./logs 사용)
set LOG_DIR=

REM ============================================================================
REM [병렬 처리] 멀티코어 활용 (최적화 모드에서는 미지원)
REM ============================================================================

REM 병렬 워커 수 (1=순차처리, 0=자동(CPU코어수), 2~8 권장)
REM 조합 수가 많을 때 (20개 이상) 효과적
set WORKERS=1

REM ============================================================================
REM [참고] 이 파일을 CMD나 탐색기에서 더블클릭하면 현재 창에서 실행됩니다.
REM VS Code를 닫아도 CMD 창은 계속 실행됩니다.
REM ============================================================================

REM ============================================================================
REM [트레일링 스탑] 수익 보존 전략 (둘 다 입력해야 활성화)
REM ============================================================================

REM 트레일링 시작 수익률 % (예: 5 = 5% 수익 시 활성화)
set TRAILING_START=5

REM 고점 대비 하락 허용폭 % (예: 3 = 고점 대비 3% 하락 시 청산)
set TRAILING_OFFSET=3

REM ============================================================================
REM [타임컷] 시간 기반 청산 전략 (둘 다 입력해야 활성화)
REM ============================================================================

REM 타임컷 체크 일수 (예: 5 = 5일차에 수익률 체크)
set TIME_CUT_DAYS=5

REM 타임컷 최소 수익률 % (이하면 청산, 예: 3 = 3% 미만 시 청산)
set TIME_CUT_MIN_RETURN=3

REM ============================================================================
REM [TP/SL 최적화] 조합별 최적 TP/SL 탐색 (시간 오래 걸림)
REM ============================================================================

REM 최적화 모드 사용 여부 (YES 또는 비워두기)
REM YES로 설정하면 위의 고정 TP/SL 대신 아래 범위에서 최적값 탐색
set OPTIMIZE=

REM TP 최적화 범위
set TP_MIN=5
set TP_MAX=15

REM SL 최적화 범위
set SL_MIN=-7
set SL_MAX=-3

REM 최적화 스텝 (기본값: 1)
set STEP=2

REM ============================================================================
REM [실행 코드] 아래는 수정하지 마세요
REM ============================================================================

REM 작업 디렉토리 저장
set WORK_DIR=%~dp0..

echo ============================================================================
echo   combination_tester.py 실행
echo ============================================================================
echo.
echo   [필수 설정]
echo   조건: %CONDITIONS%
echo   기간: %START_DATE% ~ %END_DATE%
echo.
echo   [기본 설정]
if defined REQUIRED (echo   필수 조건: %REQUIRED%) else (echo   필수 조건: 없음)
echo   TP: %TP%%% / SL: %SL%%%
echo   최대 보유일: %MAX_HOLDING%일
echo   최소거래수: %MIN_TRADES%건
echo   조합 크기: %MIN_SIZE% ~ %MAX_SIZE%
echo.
echo   [출력 설정]
echo   정렬 기준: %SORT_BY%
echo   상위 출력: %TOP_N%개
echo.
echo   [고급 설정]
if defined TRAILING_START (echo   트레일링: %TRAILING_START%%% 도달시 시작, 고점대비 %TRAILING_OFFSET%%% 하락시 청산) else (echo   트레일링: 사용 안함)
if defined TIME_CUT_DAYS (echo   타임컷: %TIME_CUT_DAYS%일 후 %TIME_CUT_MIN_RETURN%%% 미만시 청산) else (echo   타임컷: 사용 안함)
if defined OPTIMIZE (echo   최적화: TP %TP_MIN%%%~%TP_MAX%%%, SL %SL_MIN%%%~%SL_MAX%%% [step %STEP%]) else (echo   최적화: 사용 안함 [고정 TP/SL])
echo.
echo   [로깅]
if defined USE_LOG (echo   로그 저장: YES - logs 폴더) else (echo   로그 저장: NO)
if defined LOG_DIR (echo   로그 디렉토리: %LOG_DIR%)
echo.
echo   [병렬 처리]
if "%WORKERS%"=="0" (echo   워커 수: 자동 CPU코어수) else if "%WORKERS%"=="1" (echo   워커 수: 1 - 순차처리) else (echo   워커 수: %WORKERS%개 - 병렬처리)
echo.
echo ============================================================================
echo   테스트가 완료되면 logs 폴더에서 결과를 확인하세요.
echo   (Ctrl+C로 중단 가능)
echo ============================================================================
echo.
timeout /t 3 > nul

REM 기본 명령어 구성
set CMD=python combination_tester.py
set CMD=%CMD% --conditions %CONDITIONS%
set CMD=%CMD% --start-date %START_DATE%
set CMD=%CMD% --end-date %END_DATE%
set CMD=%CMD% --tp %TP%
set CMD=%CMD% --sl %SL%
set CMD=%CMD% --max-holding %MAX_HOLDING%
set CMD=%CMD% --min-trades %MIN_TRADES%
set CMD=%CMD% --min-size %MIN_SIZE%
set CMD=%CMD% --max-size %MAX_SIZE%
set CMD=%CMD% --sort-by %SORT_BY%
set CMD=%CMD% --top %TOP_N%

REM 로깅 옵션 추가
if defined USE_LOG set CMD=%CMD% --log
if defined LOG_DIR set CMD=%CMD% --log-dir "%LOG_DIR%"

REM 병렬 처리 옵션 추가
if defined WORKERS if not "%WORKERS%"=="1" set CMD=%CMD% --workers %WORKERS%

REM 필수 조건 추가
if defined REQUIRED set CMD=%CMD% --required "%REQUIRED%"

REM 트레일링 스탑 추가 (둘 다 있어야 함)
if defined TRAILING_START if defined TRAILING_OFFSET (
    set CMD=%CMD% --trailing-start %TRAILING_START%
    set CMD=%CMD% --trailing-offset %TRAILING_OFFSET%
)

REM 타임컷 추가 (둘 다 있어야 함)
if defined TIME_CUT_DAYS if defined TIME_CUT_MIN_RETURN (
    set CMD=%CMD% --time-cut-days %TIME_CUT_DAYS%
    set CMD=%CMD% --time-cut-min-return %TIME_CUT_MIN_RETURN%
)

REM 최적화 모드 추가
if defined OPTIMIZE (
    set CMD=%CMD% --optimize
    set CMD=%CMD% --tp-min %TP_MIN%
    set CMD=%CMD% --tp-max %TP_MAX%
    set CMD=%CMD% --sl-min %SL_MIN%
    set CMD=%CMD% --sl-max %SL_MAX%
    set CMD=%CMD% --step %STEP%
)

REM 실행 명령어 출력
echo [실행 명령어]
echo %CMD%
echo.

REM 현재 창에서 실행
cd /d "%WORK_DIR%"
%CMD%

echo.
echo ============================================================================
echo   테스트 완료!
echo   결과 파일: logs 폴더 확인
echo ============================================================================
pause
