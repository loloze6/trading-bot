---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move after long bets: 0.00436673; t of the mean: 1.27789 (threshold: above 0 with t >= 2 to confirm, below 0 with t <= -2 to reject, over at least 30 cases)
- Supporting check: slope t of unusual move on forecast size: 1.72568, passed: True
- Counts: independent cases: 1205
- Decided by: The t of the mean unusual 5-day move lies between -2 and 2.
- Reading: The 60-day return is recomputed from closes inside each window, so active bars in a window's first 60 bars (no 60-bar lookback) are left out of the agreement share; a case is the first long bet (forecast rise >= 2 points from its lowest long level since the last bet, from 0 after flat) in each 5-bar grid cell counted from the window's first row, its forecast size is the forecast on that bar, and the drift is the coin's mean 5-bar return on the same grid over all its windows; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.44 % per case over 5 bars, 0.034 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +1.02 %; 1205 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend_1d`
Measure: `measure.py`
