---
plan: N1-09_below-falling-long-average_1d
idea: N1-09_below-falling-long-average
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of -forecast/10 x (10-bar forward return - coin's all-window mean 10-bar return): -0.0036765; t of the mean: -0.4699 (threshold: mean > 0 with t >= 2 to confirm, mean < 0 with t <= -2 to reject, over at least 30 non-overlapping active cases)
- Supporting check: mean 10-bar excess return on top-quartile |forecast| bars, non-overlapping: -0.00303689, passed: True
- Counts: non-overlapping active cases: 610, non-overlapping top-quartile cases: 201
- Decided by: t lies between -2 and 2, which neither confirms nor rejects.
- Reading: The coin's mean 10-bar return uses every bar of all its windows (within-window returns); the top quartile is |forecast| at or above the 75th percentile over all active bars, then taken on the 0,10,20,... grid; below-average is read from dist200 if recorded, else the 'trending' label; fewer than 30 cases is reported as not observable.
Plan: `steps_cards/03_test_plan/overnight_run/plans_newcomp/N1-09_below-falling-long-average_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-09_below-falling-long-average_1d`
Measure: `measure.py`
