@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM ================================================================================
REM   [전체 옵션 템플릿] combination_tester.py 모든 옵션 참조용
REM ================================================================================
REM   이 파일은 combination_tester.py의 모든 가능한 옵션을 포함합니다.
REM   필요한 옵션만 활성화하고 나머지는 주석 처리하여 사용하세요.
REM
REM   실행 모드:
REM     1: 기본 조합 테스트 (고정 TP/SL)
REM     2: TP/SL 최적화 모드 (--optimize)
REM     3: 파라미터 그리드 테스트 (--param-grid)
REM     4: 2단계 자동 최적화 (--auto-optimize)
REM ================================================================================

REM ================================================================================
REM   [1] 실행 모드 선택
REM ================================================================================
set MODE=2

REM ================================================================================
REM   [2] 조건 설정 (필수)
REM ================================================================================

REM 테스트할 조건 (콤마 구분)
REM   기본 조건: A, B, C, D, E, F, G, H, I
REM   GT 조건: GT_A, GT_B, GT_B1, GT_B2, GT_C, GT_D, GT_D2, GT_E, GT_F
REM   GT 마켓: GT_P1, GT_M1, GT_M2
set CONDITIONS=A,B,D,E,F,G,H,I,GT_A,GT_B,GT_C,GT_D,GT_D2,GT_E,GT_F

REM 필수 조건 (선택) - 모든 조합에 반드시 포함될 조건
REM   예: A,B 또는 "A AND B"
REM   비워두면 사용 안함
set REQUIRED=

REM ================================================================================
REM   [3] 백테스트 기간 (필수)
REM ================================================================================
set START_DATE=20250101
set END_DATE=20250630

REM ================================================================================
REM   [4] 기본 TP/SL 설정 (MODE=1,3,4에서 사용)
REM ================================================================================

REM 익절선 (%)
set TP=10

REM 손절선 (%, 음수)
set SL=-5

REM 최대 보유일
set MAX_HOLDING=14

REM ================================================================================
REM   [5] 조합 크기 설정
REM ================================================================================

REM 최소 조합 크기 (몇 개 조건 AND로 묶을지)
set MIN_SIZE=2

REM 최대 조합 크기 (비워두면 CONDITIONS 개수만큼)
set MAX_SIZE=3

REM 최소 거래 건수 (이하면 무효 처리)
set MIN_TRADES=50

REM ================================================================================
REM   [6] 트레일링스탑 설정 (선택)
REM ================================================================================
REM   두 값 모두 입력해야 활성화됨. 비워두면 비활성화.

REM 트레일링 시작 수익률 (%)
REM   예: 5 = 5% 수익 도달 시 트레일링 시작
set TRAILING_START=5

REM 고점 대비 하락 허용폭 (%)
REM   예: 3 = 고점에서 3% 하락 시 청산
set TRAILING_OFFSET=3

REM ================================================================================
REM   [7] 타임컷 설정 (선택)
REM ================================================================================
REM   두 값 모두 입력해야 활성화됨. 비워두면 비활성화.

REM 타임컷 체크 일수
REM   예: 3 = 3일차에 수익률 체크
set TIME_CUT_DAYS=

REM 타임컷 최소 수익률 (%)
REM   예: 2 = 2% 미만이면 청산
set TIME_CUT_MIN_RETURN=

REM ================================================================================
REM   [8] TP/SL 최적화 설정 (MODE=2 전용)
REM ================================================================================

REM TP 최적화 범위 (%)
set TP_MIN=5
set TP_MAX=15

REM SL 최적화 범위 (%, 음수)
set SL_MIN=-7
set SL_MAX=-3

REM 최적화 스텝 (%)
set STEP=1

REM ================================================================================
REM   [9] 파라미터 그리드 설정 (MODE=3 전용)
REM ================================================================================
REM   형식: "조건.파라미터:값1,값2,값3;조건.파라미터:값1,값2"
REM
REM   조건별 주요 파라미터:
REM   --------------------------------------------------------------------------
REM   A: days (연속 상승일)
REM   B: days (신고거래대금 기간)
REM   C: top_n (상위 N종목), min_rate (최소 회전율)
REM   D: short (단기이평), mid (중기이평), long (장기이평)
REM   E: days (신고가 기간), min_pct, max_pct
REM   F: compare_days, min_ratio, max_ratio
REM   G: min_rate, max_rate (회전율 범위)
REM   H: smart_money_turnover, support_margin, min_trade_value
REM   I: disparity_min, disparity_max, min_turnover, min_trade_value
REM   GT_A: macd_fast, macd_slow, macd_signal
REM   GT_B: rsi_period, rsi_oversold
REM   GT_C: rsi_overbought
REM   GT_D: lookback_days, bounce_pct
REM   GT_D2: short_period, long_period
REM   GT_E: short_period, long_period, convergence_pct
REM   GT_F: avg_period, volume_multiplier
REM   --------------------------------------------------------------------------

set PARAM_GRID=H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03,0.05

REM ================================================================================
REM   [10] 자동 최적화 설정 (MODE=4 전용)
REM ================================================================================

REM 최적화 후 default.json 자동 업데이트 (1=예, 0=아니오)
set UPDATE_DEFAULTS=0

REM ================================================================================
REM   [11] 출력 및 로그 설정
REM ================================================================================

REM 정렬 기준 (avg_return 또는 win_rate)
set SORT_BY=avg_return

REM 상위 N개만 출력
set TOP_N=20

REM 로그 파일 저장 (1=예, 0=아니오)
set SAVE_LOG=1

REM 로그 저장 디렉토리 (비워두면 ./logs)
set LOG_DIR=

REM ================================================================================
REM   [12] 병렬 처리 설정
REM ================================================================================

REM 병렬 워커 수
REM   1: 순차 처리
REM   2이상: 병렬 처리
REM   0: CPU 코어 수만큼 자동 설정 (메모리 주의!)
REM   권장: 6 (메모리 최적화)
set WORKERS=6


REM ================================================================================
REM ================================================================================
REM   [실행부] - 아래 코드는 수정하지 마세요
REM ================================================================================
REM ================================================================================

cd /d "%~dp0.."

REM 기본 명령어 구성
set CMD=python combination_tester.py --conditions %CONDITIONS% --start-date %START_DATE% --end-date %END_DATE%

REM 필수 조건 추가
if not "%REQUIRED%"=="" (
    set CMD=!CMD! --required "%REQUIRED%"
)

REM 공통 옵션 추가
set CMD=!CMD! --min-size %MIN_SIZE%
if not "%MAX_SIZE%"=="" set CMD=!CMD! --max-size %MAX_SIZE%
set CMD=!CMD! --min-trades %MIN_TRADES%
set CMD=!CMD! --max-holding %MAX_HOLDING%
set CMD=!CMD! --sort-by %SORT_BY% --top %TOP_N%

REM 트레일링스탑 옵션
if not "%TRAILING_START%"=="" if not "%TRAILING_OFFSET%"=="" (
    set CMD=!CMD! --trailing-start %TRAILING_START% --trailing-offset %TRAILING_OFFSET%
)

REM 타임컷 옵션
if not "%TIME_CUT_DAYS%"=="" if not "%TIME_CUT_MIN_RETURN%"=="" (
    set CMD=!CMD! --time-cut-days %TIME_CUT_DAYS% --time-cut-min-return %TIME_CUT_MIN_RETURN%
)

REM 로그 옵션
if "%SAVE_LOG%"=="1" (
    set CMD=!CMD! --log
    if not "%LOG_DIR%"=="" set CMD=!CMD! --log-dir "%LOG_DIR%"
)

REM 모드별 옵션 추가
if "%MODE%"=="1" (
    echo.
    echo [MODE 1] 기본 조합 테스트 ^(고정 TP/SL^)
    echo.
    set CMD=!CMD! --tp %TP% --sl %SL% --workers %WORKERS%
)

if "%MODE%"=="2" (
    echo.
    echo [MODE 2] TP/SL 최적화 모드
    echo.
    set CMD=!CMD! --optimize --tp-min %TP_MIN% --tp-max %TP_MAX% --sl-min %SL_MIN% --sl-max %SL_MAX% --step %STEP%
)

if "%MODE%"=="3" (
    echo.
    echo [MODE 3] 파라미터 그리드 테스트
    echo.
    set CMD=!CMD! --tp %TP% --sl %SL% --param-grid "%PARAM_GRID%"
)

if "%MODE%"=="4" (
    echo.
    echo [MODE 4] 2단계 자동 최적화
    echo.
    set CMD=!CMD! --tp %TP% --sl %SL% --auto-optimize
    if "%UPDATE_DEFAULTS%"=="1" (
        set CMD=!CMD! --update-defaults
        echo    ^> 최적화 후 default.json 자동 업데이트 활성화
    )
)

echo ================================================================================
echo   실행 명령어:
echo ================================================================================
echo %CMD%
echo ================================================================================
echo.

REM 실행
%CMD%

echo.
echo ================================================================================
echo   실행 완료
echo ================================================================================

pause
