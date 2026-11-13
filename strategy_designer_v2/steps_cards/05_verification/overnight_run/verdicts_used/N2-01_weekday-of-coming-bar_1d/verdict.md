---
plan: N2-01_weekday-of-coming-bar_1d
idea: N2-01_weekday-of-coming-bar
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of allocation x (next-bar return minus coin all-window mean daily return) over forecast>0 bars: 0.00393234; t of the mean: 2.58537 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 300 active Saturday bars pooled)
- Supporting check: mean Saturday return minus coin all-window mean daily return (t = 3.7497): 0.003056, passed: None
- Counts: active Saturday bars: 1528, Saturday bars: 2462
- Decided by: The pooled main-measure mean is positive with t >= 2 (confirm rule).
- Reading: A Saturday bar is the return from a Friday-dated bar's close to the next bar's close, active bars are forecast > 0 bars with a valid next return weighted by postRebalance_current_allocation, the coin mean is the mean of all within-window one-bar returns pooled over its windows, the plan's 'fewer than 300 is inconclusive' minimum is reported as not observable, and the supporting check has no pass rule in the plan so its passed is null.
Plan: `steps_cards/03_test_plan/overnight_run/plans_rerun/N2-01_weekday-of-coming-bar_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-01_weekday-of-coming-bar_1d`
Measure: `measure.py`
