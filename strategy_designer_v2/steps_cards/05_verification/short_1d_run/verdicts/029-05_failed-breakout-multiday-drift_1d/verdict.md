---
plan: 029-05_failed-breakout-multiday-drift_1d
idea: 029-05_failed-breakout-multiday-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 8-bar move per case (before costs): -0.0035882; t of the mean: -0.524322 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: mean unusual move of deeper half minus shallower half (split at median entry forecast size): None, passed: False
- Counts: independent cases: 539, deeper half: 0, shallower half: 539
- Decided by: The t of the main measure lies between -2 and 2.
- Reading: A case is the first short-side bet (forecast falling >= 2 points from its lowest short level since the last bet, reset at flat) in each 8-bar grid cell from each window's first row, needing 8 bars ahead in the window; drift is the coin's mean 8-bar grid return over all windows; the deeper half is entry |forecast| strictly above the median, the shallower half at or below it.
- Size: unusual move -0.36 % per case over 8 bars, -0.017 of the coin's usual move (13.97 %); normal drift in its direction -1.06 %, total -1.42 %; 539 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-05_failed-breakout-multiday-drift_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-05_failed-breakout-multiday-drift_1d`
Measure: `measure.py`
