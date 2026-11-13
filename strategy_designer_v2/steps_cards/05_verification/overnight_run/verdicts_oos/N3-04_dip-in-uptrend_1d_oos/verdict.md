---
plan: N3-04_dip-in-uptrend_1d_oos
idea: N3-04_dip-in-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-bar return (forecast > 0 bars minus coin holding mean): 0.000893777; t of the mean: 0.690945 (threshold: confirm if mean > 0 with t >= 2.0; reject if mean < 0 with t <= -2.0; else inconclusive; at least 200 forecast > 0 bars)
- Supporting check: OLS slope of excess next-bar return on forecast size: 0.000141637, passed: True
- Counts: bars with forecast > 0: 1654
- Decided by: The t-statistic lies between -2.0 and 2.0, which the plan calls inconclusive.
- Reading: Uptrend checked on the recorded regime label 'trending' and the drop as a negative 1-day return (down_day raw value, else close-to-close); the holding mean is each coin's mean next-bar return over all windows present in the record (12 here, not 24); fewer than 200 bars is reported as not observable per the minimum-count rule; the supporting slope passes if positive.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N3-04_dip-in-uptrend_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N3-04_dip-in-uptrend_1d_oos`
Measure: `measure.py`
