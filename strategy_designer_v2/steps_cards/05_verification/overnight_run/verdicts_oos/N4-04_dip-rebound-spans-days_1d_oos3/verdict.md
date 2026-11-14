---
plan: N4-04_dip-rebound-spans-days_1d_oos3
idea: N4-04_dip-rebound-spans-days
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess return close t+1 to close t+3 after top-decile forecasts: 0.0151732; t of the mean: 1.6268 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 30 non-overlapping cases)
- Supporting check: mean 3-bar excess return close t to t+3 vs coin mean 3-bar return: 0.023345, passed: True
- Counts: non-overlapping cases: 49, top-decile bars: 59, positive forecasts: 315
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: Top decile is forecast >= the 90th percentile of all pooled positive forecasts (ties included); coin mean 2- and 3-bar returns use every bar of every window of the coin; cases on the same coin and window are chained into one case when within 3 bars of the previous case, and the case value is the mean of its members' excess returns.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-04_dip-rebound-spans-days_1d_oos3.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-04_dip-rebound-spans-days_1d_oos3`
Measure: `measure.py`
