---
plan: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d
idea: 029-05_failed-breakout-multiday-drift.d1_failure-still-below-high
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 8-bar move per case: 0.00841377; t of the mean: 1.44191 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases; reject: t <= -2 over >= 30 cases)
- Supporting check: OLS slope of unusual move on |forecast|: 0.00281276, passed: True
- Counts: cases: 436
- Decided by: t strictly between -2 and 2 over at least 30 cases.
- Reading: Cases are the first short bet (a rise of the short forecast of at least 2 points from its low since the last bet) in each 8-bar grid cell from each window's first row, dropped when 8 bars do not remain in the window; the drift is the coin's mean non-overlapping 8-bar return over all its windows; the situation is recomputed from closes and active bars without enough in-window history are left out of the check.
- Size: unusual move +0.84 % per case over 8 bars, 0.048 of the coin's usual move (13.97 %); normal drift in its direction -1.05 %, total -0.21 %; 436 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-05_failed-breakout-multiday-drift.d1_failure-still-below-high_1d`
Measure: `measure.py`
