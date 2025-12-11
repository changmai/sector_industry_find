@echo off
chcp 65001 > nul
REM ============================================
REM combination_tester.py - All options example
REM Reference template with all available options
REM ============================================

python combination_tester.py ^
  --conditions A,B,D,E,F,G,GT_M1,GT_M1,GT_M2,GT_A,GT_B,GT_C,GT_D,GT_E,GT_F ^
  --start-date 20240529 ^
  --end-date 20250530 ^
  --min-size 2 ^
  --max-size 4 ^
  --min-trades 50 ^
  --max-holding 14 ^
  --optimize ^
  --tp-min 5 ^
  --tp-max 15 ^
  --sl-min -7 ^
  --sl-max -3 ^
  --step 1 ^
  --trailing-start 5 ^
  --trailing-offset 3 ^
  --time-cut-days 3 ^
  --time-cut-min-return 2 ^
  --sort-by avg_return ^
  --top 20

REM ============================================
REM OPTIONS REFERENCE
REM ============================================
REM
REM [Required]
REM   --conditions, -c      Conditions to test (comma separated)
REM                         Example: A,B,C,D or A,D,GT_A,GT_B
REM                         Available: A,B,C,D,E,F,G,GT_P1,GT_M1,GT_M2,GT_A,GT_B,GT_B1,GT_B2,GT_C,GT_D,GT_D2,GT_E,GT_F
REM   --start-date, -s      Backtest start date (YYYYMMDD)
REM   --end-date, -e        Backtest end date (YYYYMMDD)
REM
REM [Combination]
REM   --min-size            Min combination size (default: 2)
REM   --max-size            Max combination size (default: all conditions)
REM   --min-trades          Min trades to be valid (default: 100)
REM
REM [TP/SL - Fixed mode]
REM   --tp                  Take profit %% (default: 10)
REM   --sl                  Stop loss %% (default: -5)
REM   --max-holding         Max holding days (default: 14)
REM
REM [TP/SL - Optimization mode]
REM   --optimize            Enable TP/SL optimization (ignores --tp, --sl)
REM   --tp-min              TP optimization min (default: 5)
REM   --tp-max              TP optimization max (default: 15)
REM   --sl-min              SL optimization min (default: -7)
REM   --sl-max              SL optimization max (default: -3)
REM   --step                TP/SL optimization step (default: 1)
REM
REM [Trailing Stop]
REM   --trailing-start      Trailing activation return %% (e.g., 5 = activate at 5%%)
REM   --trailing-offset     Trailing offset from peak %% (e.g., 3 = exit at peak-3%%)
REM                         * Both required to enable, disabled if not set
REM
REM [Time Cut]
REM   --time-cut-days       Time cut check day (e.g., 3 = check at day 3)
REM   --time-cut-min-return Time cut min return %% (e.g., 2 = exit if under 2%%)
REM                         * Both required to enable, disabled if not set
REM
REM [Output]
REM   --sort-by             Sort by: win_rate or avg_return (default: avg_return)
REM   --top                 Show top N results (default: 20)
REM
REM ============================================

pause
