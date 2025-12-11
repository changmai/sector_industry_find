@echo off
chcp 65001 > nul
REM ============================================
REM Single day test with trailing stop
REM ============================================

python single_day_test.py ^
  --start-date 20251101 ^
  --end-date 20251130 ^
  --conditions "A AND D" ^
  --days 10 ^
  --tp 10 --sl -5 ^
  --trailing-start 5 --trailing-offset 3

pause
