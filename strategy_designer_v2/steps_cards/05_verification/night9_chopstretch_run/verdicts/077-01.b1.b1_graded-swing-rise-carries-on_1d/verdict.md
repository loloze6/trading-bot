---
plan: 077-01.b1.b1_graded-swing-rise-carries-on_1d
idea: 077-01.b1.b1_graded-swing-rise-carries-on
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar forward return minus normal drift on forecast, in-profile grid bars: 0.00106633; slope t, deviations summed per day: 0.998326 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean unusual 7-bar move over grid cases with forecast > 0 above 0: 0.00402052, passed: True
- Counts: grid cases with forecast > 0: 409, distinct days: 157, in-profile grid bars: 777
- Decided by: The slope's t lies between -2 and 2.
- Reading: The profile is the recorded regime 'unknown' (the config's only active regime); the slope is OLS with intercept over all in-profile grid bars (forecast 0 included), its t from residual-times-deviation scores summed per UTC day with a G/(G-1) correction; the drift is the coin's mean 7-bar grid return over all its windows and bars; the plan's 'fewer cases' rule is reported as not observable.
- Size: unusual move +0.05 % (t 0.09, the cases of one day together: 473 days) per case over 7 bars, -0.005 of the coin's usual move (12.84 %); normal drift in its direction +0.95 %, total +1.01 %; 746 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-01.b1.b1_graded-swing-rise-carries-on_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1.b1_graded-swing-rise-carries-on_1d`
Measure: `measure.py`
