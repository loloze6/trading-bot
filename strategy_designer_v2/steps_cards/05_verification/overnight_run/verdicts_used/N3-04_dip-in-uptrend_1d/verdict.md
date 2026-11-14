---
plan: N3-04_dip-in-uptrend_1d
idea: N3-04_dip-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-bar return (vs coin holding mean) on forecast > 0 bars: 0.00315653; t of the mean: 3.06453 (threshold: confirm if mean > 0 with t >= 2.0; reject if mean < 0 with t <= -2.0; else inconclusive; at least 200 bars with forecast > 0)
- Supporting check: OLS slope of excess next-bar return on forecast size (positive expected): 0.000362065, passed: True
- Counts: bars with forecast > 0: 2383
- Decided by: The mean excess next-bar return is positive with t >= 2.0 (confirm rule).
- Reading: Holding mean is each coin's mean next-bar close-to-close return over every bar of all its windows pooled; cases are forecast > 0 bars with a next bar in the same window; the 200-bar minimum not reached is reported as not observable; uptrend checked on the regime column.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N3-04_dip-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-04_dip-in-uptrend_1d`
Measure: `measure.py`
