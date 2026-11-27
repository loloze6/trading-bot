---
plan: 067-02.b1.b1_two-sided-swing-stretch-five-days_1d
idea: 067-02.b1.b1_two-sided-swing-stretch-five-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-day excess return on forecast (grid bars, clustered by day): 0.000353043; day-clustered t of slope: 0.910955 (threshold: confirm: slope > 0 with t >= 2 and both sides' signed excess > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean signed excess 5-day return, long and short sides (min of the two): -0.00532488, passed: False
- Counts: grid cases in total: 819, long grid cases: 414, short grid cases: 405
- Decided by: The slope has |t| < 2, neither confirming nor rejecting.
- Reading: The choppy profile is the strategy's active regime (stretch recorded / regime 'unknown') and the side is the raw stretch's sign; the coin's mean 5-day return is over all its non-overlapping grid bars of all windows; the slope's t is OLS with day-clustered standard errors (with small-sample correction); the plan's 'fewer is inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.24 % (t 0.78, the cases of one day together: 807 days) per case over 5 bars, 0.018 of the coin's usual move (10.60 %); normal drift in its direction -0.01 %, total +0.23 %; 1112 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02.b1.b1_two-sided-swing-stretch-five-days_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1_two-sided-swing-stretch-five-days_1d`
Measure: `measure.py`
