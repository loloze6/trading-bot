---
plan: 074-02.b1_calm-stretch-falls-five-days_1d
idea: 074-02.b1_calm-stretch-falls-five-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar unusual return on depth -forecast: -0.000609616; day-clustered OLS t of slope: -0.846334 (threshold: confirm: slope < 0 with day-clustered t <= -2 and mean unusual move of shorts > 0; reject: slope > 0 with t >= +2)
- Supporting check: mean unusual move of short cases, in short direction: 0.00608593, passed: True
- Counts: grid cases: 903, distinct days: 322
- Decided by: The slope's t lies between -2 and +2.
- Reading: Both minimums are required (at least 100 grid cases and at least 60 distinct days), the coin's mean 5-bar return is the mean of its non-overlapping grid returns over all its windows, the t uses cluster-robust standard errors by UTC day of the signal bar, and the calm profile is regime other than 'chop'.
- Size: unusual move +0.72 % (t 1.80, the cases of one day together: 558 days) per case over 5 bars, 0.070 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total +0.07 %; 958 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/074-02.b1_calm-stretch-falls-five-days_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-02.b1_calm-stretch-falls-five-days_1d`
Measure: `measure.py`
