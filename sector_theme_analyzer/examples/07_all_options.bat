@echo off
chcp 65001 > nul
REM ============================================================================
REM 예시 7: 모든 옵션 사용 (최대 설정)
REM ============================================================================
REM
REM ■ 필수 옵션
REM   --conditions, -c  : 테스트할 조건 목록 (콤마 구분)
REM   --start-date, -s  : 백테스트 시작일 (YYYYMMDD)
REM   --end-date, -e    : 백테스트 종료일 (YYYYMMDD)
REM
REM ■ 필수 조건 옵션
REM   --required, -r    : 필수 조건 (모든 조합에 포함)
REM
REM ■ 조합 크기 옵션
REM   --min-size        : 최소 조합 크기 (기본: 2)
REM   --max-size        : 최대 조합 크기 (기본: 전체)
REM   --min-trades      : 최소 거래 건수 (이하 무효, 기본: 100)
REM
REM ■ 기본 TP/SL 옵션 (--optimize 미사용 시)
REM   --tp              : 익절선 % (기본: 10)
REM   --sl              : 손절선 % (기본: -5)
REM   --max-holding     : 최대 보유일 (기본: 14)
REM
REM ■ 트레일링 스탑 옵션
REM   --trailing-start  : 트레일링 시작 수익률 %
REM   --trailing-offset : 고점 대비 하락 허용폭 %
REM
REM ■ 타임컷 옵션
REM   --time-cut-days       : 타임컷 체크 일수
REM   --time-cut-min-return : 타임컷 최소 수익률 %
REM
REM ■ TP/SL 최적화 옵션 (--optimize 사용 시)
REM   --optimize        : 최적화 모드 활성화 (플래그)
REM   --tp-min          : TP 최적화 최소값 (기본: 5)
REM   --tp-max          : TP 최적화 최대값 (기본: 15)
REM   --sl-min          : SL 최적화 최소값 (기본: -7)
REM   --sl-max          : SL 최적화 최대값 (기본: -3)
REM   --step            : TP/SL 탐색 스텝 (기본: 1)
REM
REM ■ 출력 옵션
REM   --sort-by         : 정렬 기준 (win_rate 또는 avg_return, 기본: avg_return)
REM   --top             : 상위 N개만 출력 (기본: 20)
REM
REM ============================================================================
REM 주의: 이 예시는 모든 옵션을 보여주기 위한 것입니다.
REM       --optimize 사용 시 --tp, --sl은 무시됩니다.
REM       실행 시간이 매우 오래 걸릴 수 있습니다!
REM ============================================================================

cd /d "%~dp0.."

python combination_tester.py ^
    --conditions D,G,H,I,GT_A,GT_C ^
    --required A ^
    --start-date 20241101 ^
    --end-date 20251205 ^
    --min-size 1 ^
    --max-size 2 ^
    --min-trades 50 ^
    --max-holding 10 ^
    --trailing-start 5 ^
    --trailing-offset 3 ^
    --time-cut-days 3 ^
    --time-cut-min-return 2 ^
    --optimize ^
    --tp-min 5 ^
    --tp-max 15 ^
    --sl-min -7 ^
    --sl-max -3 ^
    --step 1 ^
    --sort-by avg_return ^
    --top 30

pause
