---
plan: 048-01_scaled-up-week-continuation_1d
idea: 048-01_scaled-up-week-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess next-3-bar return on forecast (forecast > 0 grid cases, pooled): 0.00081815; day-clustered OLS slope t: 1.96943 (threshold: confirm: slope t >= 2 with mean excess return > 0; reject: slope t <= -2)
- Supporting check: mean excess 3-bar return (long) on the same cases: 0.0021789, passed: True
- Counts: grid cases with a positive forecast: 3178, distinct days: 656
- Decided by: Slope t between -2 and 2: the plan's inconclusive rule.
- Reading: The slope is from an OLS of excess return on forecast with an intercept, its t from a day-clustered (CR1) sandwich variance, the normal drift is each coin's mean non-overlapping 3-bar grid return over all its windows, and grid bars without a full 3-bar return inside their window are left out.
- Size: unusual move +0.16 % (t 0.57, the cases of one day together: 1011 days) per case over 3 bars, 0.015 of the coin's usual move (9.38 %); normal drift in its direction +0.58 %, total +0.74 %; 2677 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/048-01_scaled-up-week-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/unseen_coins/backtests/048-01_scaled-up-week-continuation_1d`
Measure: `measure.py`
