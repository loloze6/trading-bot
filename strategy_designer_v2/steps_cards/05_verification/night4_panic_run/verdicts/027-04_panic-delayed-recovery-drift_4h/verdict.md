---
plan: 027-04_panic-delayed-recovery-drift_4h
idea: 027-04_panic-delayed-recovery-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 78-bar unusual move (return minus coin's normal drift) over cases, before costs: -0.00410336; t of the mean: -0.704723 (threshold: confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2)
- Supporting check: mean unusual move of upper half minus lower half (median forecast split) > 0: 0.00524401, passed: True
- Counts: cases: 1266, upper half cases: 633, lower half cases: 633
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first long bet (forecast rise of >= 2 points from its lowest level since the last bet, from 0 after a flat) in each non-overlapping 78-bar cell from each window's first row, cases without a full 78-bar return inside the window are dropped, the drift is the coin's mean 78-bar return on that grid over all windows, and the median split puts forecasts above the median in the upper half and the rest in the lower half.
- Size: unusual move -0.41 % per case over 78 bars, -0.027 of the coin's usual move (16.89 %); normal drift in its direction +1.97 %, total +1.56 %; 1266 cases
Plan: `steps_cards/03_test_plan/night4_panic_run/plans/027-04_panic-delayed-recovery-drift_4h.md`
Record: `steps_cards/04_backtest/night4_panic_run/backtests/027-04_panic-delayed-recovery-drift_4h`
Measure: `measure.py`
