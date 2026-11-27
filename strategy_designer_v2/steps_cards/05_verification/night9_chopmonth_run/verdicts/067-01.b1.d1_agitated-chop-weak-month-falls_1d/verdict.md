---
plan: 067-01.b1.d1_agitated-chop-weak-month-falls_1d
idea: 067-01.b1.d1_agitated-chop-weak-month-falls
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 7-bar forward return on the forecast (grid bars with negative forecast): 0.00165791; OLS slope t: 1.09368 (threshold: confirm if slope t >= 2 (with mean unusual short move > 0); reject if slope t <= -2)
- Supporting check: mean unusual move in the short direction (net of drift, before costs): 0.0053883, passed: True
- Counts: non-overlapping cases: 215, distinct days: 108
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation bars are those in the choppy agitated profile (regime 'unknown', the detector's non-vetoed state) with a negative 30-day return; cases are the plan's grid bars (positions 0,7,14,... of each window) with a negative forecast and a full 7-bar forward return in the window; the coin's normal drift is the mean of its non-overlapping 7-bar returns over all its windows; the slope's t is the ordinary OLS t (n-2 dof); distinct days are the UTC dates of the cases; the plan's 'fewer than 30 cases on 20 days' is treated as a minimum count giving 'not observable'.
- Size: unusual move +1.22 % (t 1.66, the cases of one day together: 265 days) per case over 7 bars, 0.076 of the coin's usual move (12.84 %); normal drift in its direction -0.94 %, total +0.28 %; 359 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.d1_agitated-chop-weak-month-falls_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.d1_agitated-chop-weak-month-falls_1d`
Measure: `measure.py`
