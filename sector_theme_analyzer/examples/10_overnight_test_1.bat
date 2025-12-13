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
REM 참고:
REM   - VS Code 터미널에서 실행해도 되고, 탐색기에서 더블클릭해도 됩니다
REM   - 야간에 돌릴 때는 VS Code를 닫아도 CMD 창에서 계속 실행됩니다
REM   - Ctrl+C로 중단 가능
REM
REM ============================================================================

REM ============================================================================
REM [필수 설정] 반드시 입력해야 하는 옵션
REM ============================================================================

REM 테스트할 조건들 (콤마로 구분, 공백 없이)
REM ----------------------------------------------------------------------------
REM [기본 조건 A~I]
REM   A: 섹터+업종 N일 연속 상승 (테마/업종 동반 상승 종목)
REM   B: N일 신고거래대금 (거래대금이 N일 중 최고)
REM   C: 거래량 회전율 상위 N종목
REM   D: 이평 정배열 (단기 > 중기 > 장기, 상승 추세)
REM   E: N일 신고가 대비 등락률 범위 (고점 대비 눌림 정도)
REM   F: N일전 대비 거래량 비율 (거래량 급증)
REM   G: 회전율 X% ~ Y% 범위 (적정 거래 활성도)
REM   H: 20일선 눌림목 (세력 진입 후 조정, Reno_Swing_20MA)
REM   I: 5일선 급등주 (모멘텀 조정, Reno_Momentum_5MA)
REM
REM [GT 기술적 지표 조건]
REM   GT_A:  MACD 골든크로스 (MACD선이 Signal선 상향 돌파)
REM   GT_B:  RSI 매수 신호 (GT_B1 OR GT_B2)
REM   GT_B1: RSI 과매도 탈출 (30선 상향 돌파)
REM   GT_B2: RSI 2일 연속 상승
REM   GT_C:  RSI 과매수 아님 (RSI < 70)
REM   GT_D:  바닥 패턴 (저점 대비 반등)
REM   GT_D2: 변동성 축소 (단기 변동성 < 장기 변동성)
REM   GT_E:  이평선 수렴 (단기/장기 이평 차이 3% 이내)
REM   GT_F:  거래량 급증 (20일 평균 대비 2배 이상)
REM
REM [GT 시장/테마 조건]
REM   GT_M1: 지수 MACD 상승 추세 (코스피/코스닥 ETF 기준)
REM   GT_M2: 지수 RSI 과매수 아님 (지수 RSI < 70)
REM   GT_P1: 특정 테마(섹터) 소속 종목
REM ----------------------------------------------------------------------------
set CONDITIONS=GT_C,GT_D,GT_D2,GT_E,GT_F

REM 테스트 기간 (YYYYMMDD 형식)
REM 기간이 길수록 신뢰도 높음, 단 시간 오래 걸림
set START_DATE=20240601
set END_DATE=20241231

REM ============================================================================
REM [기본 설정] TP/SL 및 필터링 옵션
REM ============================================================================

REM 필수 조건 (모든 조합에 반드시 포함, 비워두면 사용 안함)
REM 예시:
REM   set REQUIRED=D           -> D 조건 필수
REM   set REQUIRED=A,B         -> A AND B 필수
REM   set REQUIRED=A AND B     -> A AND B 필수 (동일)
REM   set REQUIRED=GT_A,GT_B   -> GT_A AND GT_B 필수
set REQUIRED=GT_A,GT_B

REM TP/SL 설정 (고정 모드에서 사용, 최적화 모드에서는 무시됨)
REM TP: 익절 라인 (예: 10 = +10% 도달 시 익절)
REM SL: 손절 라인 (예: -5 = -5% 도달 시 손절)
set TP=10
set SL=-5

REM 최대 보유일 (기본값: 14)
REM TP/SL에 도달하지 않으면 이 기간 후 종가 청산
set MAX_HOLDING=14

REM 최소 거래 건수 - 이하는 무효 처리 (기본값: 100)
REM 거래 수가 너무 적으면 통계적 신뢰도 낮음
set MIN_TRADES=100

REM 조합 크기 범위
REM MIN_SIZE=0: 필수 조건만 테스트 (REQUIRED만 사용)
REM MIN_SIZE=1: 필수 조건 + 추가 1개 조건
REM MIN_SIZE=2, MAX_SIZE=3: 필수 조건 + 2~3개 조건 조합
set MIN_SIZE=0
set MAX_SIZE=2

REM ============================================================================
REM [출력 설정] 결과 정렬 및 표시 옵션
REM ============================================================================

REM 정렬 기준
REM   avg_return: 평균 수익률 기준 (수익 극대화)
REM   win_rate:   승률 기준 (안정성 중시)
set SORT_BY=avg_return

REM 상위 N개 결과만 출력 (기본값: 20)
set TOP_N=30

REM ============================================================================
REM [로깅 설정] 로그 파일 저장 옵션
REM ============================================================================

REM 로그 저장 여부 (YES 또는 비워두기)
REM YES로 설정하면 logs 폴더에 아래 파일들이 생성됨:
REM   - combo_test_YYYYMMDD_HHMMSS.log  (실행 로그)
REM   - combo_test_YYYYMMDD_HHMMSS.json (결과 데이터)
set USE_LOG=YES

REM 로그 저장 디렉토리 (비워두면 기본값 ./logs 사용)
set LOG_DIR=

REM ============================================================================
REM [병렬 처리] 멀티코어 활용
REM ============================================================================
REM
REM 병렬 처리 설정:
REM   WORKERS=1: 순차 처리 (기본값, 안정적)
REM   WORKERS=0: 자동 (CPU 코어 수만큼)
REM   WORKERS=4: 4개 워커로 병렬 처리
REM
REM 권장 사항:
REM   - 조합 수가 적으면 (10개 미만): WORKERS=1 (순차)
REM   - 조합 수가 많으면 (20개 이상): WORKERS=4~8 (병렬)
REM   - 최적화 모드(--optimize)에서는 병렬 미지원
REM
REM 주의: 병렬 처리 시 메모리 사용량 증가 (워커당 ~500MB)
REM ----------------------------------------------------------------------------
set WORKERS=1

REM ============================================================================
REM [트레일링 스탑] 수익 보존 전략
REM ============================================================================
REM
REM 트레일링 스탑 작동 원리:
REM   1. 수익률이 TRAILING_START에 도달하면 트레일링 활성화
REM   2. 이후 고점 수익률을 추적
REM   3. 고점 대비 TRAILING_OFFSET만큼 하락하면 청산
REM
REM 예시 (TRAILING_START=5, TRAILING_OFFSET=3):
REM   - 수익률 5% 도달 -> 트레일링 활성화
REM   - 수익률 8% 도달 (고점 갱신)
REM   - 수익률 5%로 하락 (8% - 3%) -> 청산
REM
REM 사용하지 않으려면 둘 다 비워두세요
REM ----------------------------------------------------------------------------
set TRAILING_START=5
set TRAILING_OFFSET=3

REM ============================================================================
REM [타임컷] 시간 기반 청산 전략
REM ============================================================================
REM
REM 타임컷 작동 원리:
REM   - TIME_CUT_DAYS일 후 수익률이 TIME_CUT_MIN_RETURN 미만이면 청산
REM   - 횡보하는 종목을 빠르게 정리하여 자금 효율성 향상
REM
REM 예시 (TIME_CUT_DAYS=5, TIME_CUT_MIN_RETURN=3):
REM   - 5일차에 수익률 체크
REM   - 수익률 < 3% 이면 종가에 청산
REM   - 수익률 >= 3% 이면 계속 보유 (TP/SL/MAX_HOLDING까지)
REM
REM 사용하지 않으려면 둘 다 비워두세요
REM ----------------------------------------------------------------------------
set TIME_CUT_DAYS=5
set TIME_CUT_MIN_RETURN=3

REM ============================================================================
REM [TP/SL 최적화] 조합별 최적 TP/SL 탐색
REM ============================================================================
REM
REM 최적화 모드 작동 원리:
REM   - 각 조합에 대해 TP/SL 범위 내 모든 조합을 테스트
REM   - 평균 수익률이 가장 높은 TP/SL 조합을 찾음
REM
REM 주의사항:
REM   - 시간이 매우 오래 걸림 (조합당 수십~수백 개 TP/SL 테스트)
REM   - 예: TP 5~15, SL -7~-3, step=1 -> 조합당 55개 테스트
REM   - 병렬 처리(--workers) 미지원
REM
REM 사용하려면: set OPTIMIZE=YES
REM 사용 안하려면: set OPTIMIZE=
REM ----------------------------------------------------------------------------
set OPTIMIZE=

REM TP 최적화 범위 (OPTIMIZE=YES일 때만 사용)
set TP_MIN=5
set TP_MAX=15

REM SL 최적화 범위 (OPTIMIZE=YES일 때만 사용)
set SL_MIN=-7
set SL_MAX=-3

REM 최적화 스텝 (기본값: 1)
REM 스텝이 클수록 빠르지만 정밀도 낮음
REM 예: step=2 -> TP: 5,7,9,11,13,15 / SL: -7,-5,-3
set STEP=2

REM ============================================================================
REM [실행 코드] 아래는 수정하지 마세요
REM ============================================================================

REM 작업 디렉토리 저장 (이 파일의 상위 폴더 = sector_theme_analyzer)
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

REM 병렬 처리 옵션 추가 (WORKERS가 1이 아닐 때만)
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
