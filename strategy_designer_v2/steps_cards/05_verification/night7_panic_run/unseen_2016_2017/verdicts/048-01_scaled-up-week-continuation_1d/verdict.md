---
plan: 048-01_scaled-up-week-continuation_1d
idea: 048-01_scaled-up-week-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess next-3-bar return on forecast (forecast > 0 grid cases, pooled): 0.00156613; day-clustered OLS slope t: 1.77254 (threshold: confirm: slope t >= 2 with mean excess return > 0; reject: slope t <= -2)
- Supporting check: mean excess 3-bar return (long) on the same cases: 0.00935697, passed: True
- Counts: grid cases with a positive forecast: 561, distinct days: 233
- Decided by: Slope t between -2 and 2: the plan's inconclusive rule.
- Reading: The slope is from an OLS of excess return on forecast with an intercept, its t from a day-clustered (CR1) sandwich variance, the normal drift is each coin's mean non-overlapping 3-bar grid return over all its windows, and grid bars without a full 3-bar return inside their window are left out.
- Size: unusual move +1.29 % (t 1.55, the cases of one day together: 290 days) per case over 3 bars, 0.100 of the coin's usual move (13.83 %); normal drift in its direction +2.77 %, total +4.06 %; 459 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/048-01_scaled-up-week-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2016_2017/backtests/048-01_scaled-up-week-continuation_1d`
Measure: `measure.py`
