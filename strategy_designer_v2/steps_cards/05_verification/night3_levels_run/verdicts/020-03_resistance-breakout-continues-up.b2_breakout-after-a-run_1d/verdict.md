---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of long cases (return from signal close minus coin's normal 5-bar drift): 0.00548917; t of the mean: 1.75064 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: OLS slope of unusual move on forecast at entry: 0.000931823, passed: True
- Counts: cases: 1309
- Decided by: t between -2 and 2 over at least 30 cases: inconclusive.
- Reading: A case is the first long bet bar (forecast rise >= 2 from its low since the last bet) in each non-overlapping 5-bar grid cell of a window, its return taken from that bar's close over 5 bars within the window, minus the coin's mean grid 5-bar return over all its windows.
- Size: unusual move +0.55 % per case over 5 bars, 0.045 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +1.13 %; 1309 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run_1d`
Measure: `measure.py`
