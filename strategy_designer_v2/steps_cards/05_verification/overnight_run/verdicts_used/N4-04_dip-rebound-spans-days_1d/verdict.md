---
plan: N4-04_dip-rebound-spans-days_1d
idea: N4-04_dip-rebound-spans-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess return close t+1 to close t+3 after top-decile positive forecasts, vs coin mean 2-bar return: 0.0071814; t of the mean: 2.26171 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; fewer than 30 non-overlapping cases is not observable)
- Supporting check: mean 3-bar excess return vs coin mean 3-bar return: 0.0136341, passed: True
- Counts: non-overlapping cases: 455
- Decided by: The mean excess return over days 2-3 is above 0 with t >= 2.
- Reading: Top decile = forecast >= 90th percentile of all pooled positive forecasts; coin mean 2-bar and 3-bar returns use every in-window bar of all windows; cases are merged within a window when within 3 bars of the previous case (chained), each merged case keeping its first bar's returns; cases lacking close t+3 in the window are dropped first.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N4-04_dip-rebound-spans-days_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-04_dip-rebound-spans-days_1d`
Measure: `measure.py`
