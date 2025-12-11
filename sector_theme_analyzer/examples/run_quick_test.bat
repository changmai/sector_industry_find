@echo off
chcp 65001 > nul
REM ============================================
REM Quick test (fixed TP/SL, no trailing/timecut)
REM ============================================

python combination_tester.py ^
  --conditions A,D,G ^
  --start-date 20251101 ^
  --end-date 20251130 ^
  --tp 10 --sl -5 ^
  --max-holding 10 ^
  --min-trades 30

pause
