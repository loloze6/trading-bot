---
plan: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 72-bar unusual move per case (return minus coin's normal drift): 0.00441338; t of the mean: 0.850374 (threshold: t >= 2 over at least 100 independent cases to confirm; t <= -2 over at least 100 to reject)
- Supporting check: t of OLS slope of unusual move on forecast (>= 1): 3.96268, passed: True
- Counts: independent cases: 2249
- Decided by: The t of the mean unusual move lies between -2 and 2 over at least 100 independent cases.
- Reading: Breakout recomputed per window as close > max high of the prior 12 recorded bars, the first 12 bars of each window (no full prior history) left out of the agreement; a case is the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet, from 0 after flat) in each 72-bar grid cell from each window's first row, dropped if its 72-bar return leaves the window; normal drift is the mean of the coin's non-overlapping 72-bar returns over all its windows; the slope check is the OLS slope t of unusual move on the case's forecast.
- Size: unusual move +0.44 % per case over 72 bars, 0.017 of the coin's usual move (19.52 %); normal drift in its direction +2.18 %, total +2.63 %; 2249 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins.e1_breakout-continues-rising-week_4h`
Measure: `measure.py`
