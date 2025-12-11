@echo off
chcp 65001 > nul
REM ============================================================================
REM 예시 1: 기본 테스트 (고정 TP/SL)
REM ============================================================================
REM
REM 사용 옵션 설명:
REM   --conditions, -c  : 테스트할 조건 목록 (콤마 구분)
REM                       기본조건: A~I, GT조건: GT_A, GT_B, GT_C 등
REM   --start-date, -s  : 백테스트 시작일 (YYYYMMDD)
REM   --end-date, -e    : 백테스트 종료일 (YYYYMMDD)
REM   --tp              : 익절선 % (기본: 10)
REM   --sl              : 손절선 % (기본: -5, 음수로 입력)
REM   --max-holding     : 최대 보유일 (기본: 14)
REM
REM 이 예시는 A, D, G 조건의 모든 2~3개 조합을 테스트합니다.
REM ============================================================================

cd /d "%~dp0.."

python combination_tester.py ^
    --conditions A,D,G ^
    --start-date 20241101 ^
    --end-date 20251205 ^
    --tp 10 ^
    --sl -5 ^
    --max-holding 7

pause
