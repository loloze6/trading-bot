---
plan: 016-04_down-jump-price-reversal_1h
idea: 016-04_down-jump-price-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of 72-bar excess return on forecast (fallen grid bars): -0.000448957; OLS slope t: -1.91619 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 fallen grid cases)
- Supporting check: top forecast tercile mean excess 72-bar return > 0: -0.00428773, passed: False
- Counts: fallen grid cases: 2762, top tercile cases: 921
- Decided by: The slope's t lies between -2 and 2.
- Reading: The situation is taken as a 72-bar close-to-close fall inside the window with a positive raw top-3-losses share, on the long side, and active bars within a window's first 72 rows (where the fall cannot be recomputed) are left out of the check; the coin's mean 72-bar return is the mean over all its grid bars in all windows, the regression is pooled OLS of excess return on forecast with its ordinary t, and terciles are equal-count thirds of the fallen cases ranked by forecast (ties broken by order).
- Size: unusual move -0.39 % per case over 72 bars, -0.046 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.02 %; 4942 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-04_down-jump-price-reversal_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-04_down-jump-price-reversal_1h`
Measure: `measure.py`
