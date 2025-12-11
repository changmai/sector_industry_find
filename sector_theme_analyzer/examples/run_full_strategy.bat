@echo off
chcp 65001 > nul
REM ============================================
REM Full strategy test (trailing + timecut)
REM Trailing: activate at 5%, exit at peak-3%
REM Timecut: exit if under 2% at day 3
REM ============================================

python combination_tester.py ^
  --conditions A,D,G ^
  --start-date 20251101 ^
  --end-date 20251130 ^
  --tp 10 --sl -5 ^
  --max-holding 10 ^
  --trailing-start 5 --trailing-offset 3 ^
  --time-cut-days 3 --time-cut-min-return 2 ^
  --min-trades 30

pause
