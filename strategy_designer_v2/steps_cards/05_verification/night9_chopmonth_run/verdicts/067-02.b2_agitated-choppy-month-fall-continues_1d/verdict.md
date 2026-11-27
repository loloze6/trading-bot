---
plan: 067-02.b2_agitated-choppy-month-fall-continues_1d
idea: 067-02.b2_agitated-choppy-month-fall-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar excess return on the forecast (forecast < 0 grid bars): 0.00165791; t, errors clustered by day: 1.01474 (threshold: confirm: slope > 0 with t >= 2 (and mean unusual short move > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean unusual move in the short direction (minus excess return): 0.0053883, passed: True
- Counts: grid cases with a forecast below 0: 215, distinct days: 108
- Decided by: the slope t lies between -2 and 2
- Reading: the drift is each coin's mean 7-bar return on the non-overlapping grid of all its windows, the slope is in 7-bar excess return (fraction) per forecast point with CR1 day-clustered errors, and the plan's minimum counts lead to 'not observable' as the workflow requires
- Size: unusual move +1.22 % (t 1.66, the cases of one day together: 265 days) per case over 7 bars, 0.076 of the coin's usual move (12.84 %); normal drift in its direction -0.94 %, total +0.28 %; 359 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b2_agitated-choppy-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b2_agitated-choppy-month-fall-continues_1d`
Measure: `measure.py`
