@echo off
chcp 65001 > nul
REM ============================================
REM TP/SL optimization test
REM Warning: Takes long time (combinations x TP/SL combinations)
REM ============================================

python combination_tester.py ^
  --conditions A,D,G ^
  --start-date 20251101 ^
  --end-date 20251130 ^
  --optimize ^
  --tp-min 5 --tp-max 15 ^
  --sl-min -7 --sl-max -3 ^
  --step 1 ^
  --max-holding 10 ^
  --min-trades 30

pause
