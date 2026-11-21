---
plan: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d
idea: 021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 26-bar unusual move (short direction) after cross bars: 0.00696764; t of the mean: 0.303571 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: slope of unusual move on |forecast| at the cross: -0.0028977, passed: False
- Counts: cases across all coins and windows: 112
- Decided by: the t of the mean unusual move lies between -2 and 2 (or is not computable), which is inconclusive.
- Reading: the situation is checked on the active bars where the cloud (52+26 bars of history) and the prior outside state can be computed inside their window, with the 26-bar return taken from the recorded fall26 raw value or recomputed from closes; cases are the short bets (forecast rising by at least 2 points on the short side from its low since the last bet), one per 26-bar grid cell of each window, with the coin's drift the mean of its non-overlapping 26-bar returns over all windows, and the plan's 'fewer than 30 cases' rule reported as not observable.
- Size: unusual move +0.70 % per case over 26 bars, -0.004 of the coin's usual move (25.48 %); normal drift in its direction -4.15 %, total -3.45 %; 112 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-04_thin-cloud-downward-breakdown.d1_cloud-breakdown-after-deep-fall_1d`
Measure: `measure.py`
