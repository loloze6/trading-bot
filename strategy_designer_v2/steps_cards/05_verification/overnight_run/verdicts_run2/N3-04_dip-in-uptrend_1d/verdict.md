---
plan: N3-04_dip-in-uptrend_1d
idea: N3-04_dip-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-bar return over holding mean: 0.00315653; t of the mean: 3.06453 (threshold: confirm if mean > 0 with t >= 2.0; reject if mean < 0 with t <= -2.0; else inconclusive; at least 200 forecast > 0 bars)
- Supporting check: OLS slope of excess next-bar return on forecast size: 0.000362065, passed: True
- Counts: bars with forecast > 0: 2383
- Decided by: The mean excess next-bar return is positive with t >= 2.0 (confirm rule).
- Reading: The situation is checked as regime == 'trending' and a negative raw 1-day return (down_day component, price return as fallback) with forecast > 0; the holding mean is each coin's mean next-bar return over all bars of all its windows, the 200-bar minimum counts forecast > 0 bars with a valid next-bar return, and the supporting check (positive OLS slope of excess return on forecast) is reported without changing the status.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N3-04_dip-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N3-04_dip-in-uptrend_1d`
Measure: `measure.py`
