---
plan: 048-01_scaled-up-week-continuation_1d
idea: 048-01_scaled-up-week-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess next-3-bar return on forecast (forecast > 0 grid cases, pooled): 0.000951023; day-clustered OLS slope t: 3.03352 (threshold: confirm: slope t >= 2 with mean excess return > 0; reject: slope t <= -2)
- Supporting check: mean excess 3-bar return (long) on the same cases: 0.00230392, passed: True
- Counts: grid cases with a positive forecast: 2916, distinct days: 796
- Decided by: Slope t of 2 or more and a mean excess 3-bar return above 0: the plan's confirm rule.
- Reading: The slope is from an OLS of excess return on forecast with an intercept, its t from a day-clustered (CR1) sandwich variance, the normal drift is each coin's mean non-overlapping 3-bar grid return over all its windows, and grid bars without a full 3-bar return inside their window are left out.
- Size: unusual move +0.37 % (t 1.62, the cases of one day together: 1083 days) per case over 3 bars, 0.045 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.72 %; 2454 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.000438 on the check folds against +0.000951 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/048-01_scaled-up-week-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/048-01_scaled-up-week-continuation_1d`
Measure: `measure.py`
