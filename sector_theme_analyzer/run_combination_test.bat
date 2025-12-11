@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM ================================================================================
REM   조건 조합 테스트 도구 (Combination Tester) 실행 스크립트
REM ================================================================================
REM   이 파일의 변수들을 수정하여 다양한 테스트를 실행할 수 있습니다.
REM
REM   실행 모드:
REM     1: 기본 조합 테스트 (고정 TP/SL)
REM     2: TP/SL 최적화 모드
REM     3: 파라미터 그리드 테스트
REM     4: 2단계 자동 최적화
REM ================================================================================

REM --------------------------------------------------------------------------------
REM   [실행 모드 선택] - 1, 2, 3, 4 중 하나 선택
REM --------------------------------------------------------------------------------
set MODE=1

REM --------------------------------------------------------------------------------
REM   [공통 설정] - 모든 모드에서 사용
REM --------------------------------------------------------------------------------

REM 테스트할 조건 목록 (콤마 구분)
REM   - 기본 조건: A, B, C, D, E, F, G, H, I
REM   - GT 조건: GT_A, GT_B, GT_B1, GT_B2, GT_C, GT_D, GT_D2, GT_E, GT_F
REM   - GT 마켓 조건: GT_P1, GT_M1, GT_M2
set CONDITIONS=A,D,H

REM 필수 조건 (선택사항) - 모든 조합에 포함될 조건
REM   예: A,B 또는 "A AND B" (비워두면 사용 안함)
set REQUIRED=

REM 백테스트 기간
set START_DATE=20240601
set END_DATE=20241231

REM 기본 TP/SL 설정 (%)
set TP=10
set SL=-5

REM 최대 보유일
set MAX_HOLDING=14

REM 최소 거래 건수 (이하는 무효 처리)
set MIN_TRADES=100

REM 조합 크기 범위
set MIN_SIZE=2
set MAX_SIZE=3

REM 정렬 기준 (avg_return 또는 win_rate)
set SORT_BY=avg_return

REM 상위 N개만 출력
set TOP_N=20

REM --------------------------------------------------------------------------------
REM   [트레일링스탑 설정] (선택사항)
REM --------------------------------------------------------------------------------
REM   활성화하려면 값 입력, 비활성화하려면 비워두기

REM 트레일링 시작 수익률 (%) - 예: 5 = 5% 수익 시 트레일링 활성화
set TRAILING_START=

REM 고점 대비 하락 허용폭 (%) - 예: 3 = 고점 대비 3% 하락 시 청산
set TRAILING_OFFSET=

REM --------------------------------------------------------------------------------
REM   [타임컷 설정] (선택사항)
REM --------------------------------------------------------------------------------
REM   활성화하려면 값 입력, 비활성화하려면 비워두기

REM 타임컷 체크 일수 - 예: 5 = 5일차에 수익률 체크
set TIME_CUT_DAYS=

REM 타임컷 최소 수익률 (%) - 예: 2 = 2% 미만 시 청산
set TIME_CUT_MIN_RETURN=

REM --------------------------------------------------------------------------------
REM   [모드 2: TP/SL 최적화 설정]
REM --------------------------------------------------------------------------------
REM   MODE=2일 때만 사용됨

REM TP 최적화 범위 (%)
set TP_MIN=5
set TP_MAX=15

REM SL 최적화 범위 (%)
set SL_MIN=-7
set SL_MAX=-3

REM 최적화 스텝 (%)
set STEP=1

REM --------------------------------------------------------------------------------
REM   [모드 3: 파라미터 그리드 설정]
REM --------------------------------------------------------------------------------
REM   MODE=3일 때만 사용됨
REM   형식: "조건.파라미터:값1,값2,값3;조건.파라미터:값1,값2"
REM
REM   예시:
REM     "H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03,0.05"
REM     "A.days:2,3,5;D.short:5,10,20"
REM     "I.disparity_min:1.08,1.10,1.12;I.disparity_max:1.20,1.25,1.30"

set PARAM_GRID=H.smart_money_turnover:5,10,15;H.support_margin:0.02,0.03,0.05

REM --------------------------------------------------------------------------------
REM   [모드 4: 자동 최적화 설정]
REM --------------------------------------------------------------------------------
REM   MODE=4일 때만 사용됨

REM 최적화 후 default.json 업데이트 (1=예, 0=아니오)
set UPDATE_DEFAULTS=0

REM --------------------------------------------------------------------------------
REM   [로그 및 병렬 처리 설정]
REM --------------------------------------------------------------------------------

REM 로그 파일 저장 (1=예, 0=아니오)
set SAVE_LOG=1

REM 로그 저장 디렉토리 (비워두면 기본값 ./logs)
set LOG_DIR=

REM 병렬 워커 수 (1=순차처리, 2이상=병렬처리, 0=CPU코어수)
REM   주의: TP/SL 최적화, 파라미터 그리드, 자동 최적화 모드에서는 병렬 미지원
set WORKERS=1


REM ================================================================================
REM   [실행부] - 아래 코드는 수정하지 마세요
REM ================================================================================

cd /d "%~dp0"

REM 기본 명령어 구성
set CMD=python combination_tester.py --conditions %CONDITIONS% --start-date %START_DATE% --end-date %END_DATE%

REM 필수 조건 추가
if not "%REQUIRED%"=="" (
    set CMD=!CMD! --required "%REQUIRED%"
)

REM 공통 옵션 추가
set CMD=!CMD! --min-size %MIN_SIZE% --max-size %MAX_SIZE% --min-trades %MIN_TRADES%
set CMD=!CMD! --max-holding %MAX_HOLDING% --sort-by %SORT_BY% --top %TOP_N%

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
    if not "%LOG_DIR%"=="" (
        set CMD=!CMD! --log-dir "%LOG_DIR%"
    )
)

REM 모드별 옵션 추가
if "%MODE%"=="1" (
    echo [모드 1] 기본 조합 테스트 (고정 TP/SL)
    set CMD=!CMD! --tp %TP% --sl %SL% --workers %WORKERS%
)

if "%MODE%"=="2" (
    echo [모드 2] TP/SL 최적화 모드
    set CMD=!CMD! --optimize --tp-min %TP_MIN% --tp-max %TP_MAX% --sl-min %SL_MIN% --sl-max %SL_MAX% --step %STEP%
)

if "%MODE%"=="3" (
    echo [모드 3] 파라미터 그리드 테스트
    set CMD=!CMD! --tp %TP% --sl %SL% --param-grid "%PARAM_GRID%"
)

if "%MODE%"=="4" (
    echo [모드 4] 2단계 자동 최적화
    set CMD=!CMD! --tp %TP% --sl %SL% --auto-optimize
    if "%UPDATE_DEFAULTS%"=="1" (
        set CMD=!CMD! --update-defaults
    )
)

echo.
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
