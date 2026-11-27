---
plan: 067-02.b1.b1.d3_calm-choppy-month-rise-continues_1d
idea: 067-02.b1.b1.d3_calm-choppy-month-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 7-bar excess return on forecast: 0.000944011; slope t, day-clustered: 1.35367 (threshold: confirm if t >= 2 (with supporting check), reject if t <= -2, with at least 100 cases on at least 60 days)
- Supporting check: mean excess return >0 on long cases and <0 on short cases: 0.00787609, passed: True
- Counts: cases: 776, days: 229, long cases: 406, short cases: 370, active bars: 5451
- Decided by: The slope's t lies between -2 and 2.
- Reading: The choppy calm profile is the detector's non-chop regime 'unknown' and the side is the sign of the 30-bar return. The slope's t uses OLS with an intercept and day-clustered (CR1) standard errors, clustering cases by their grid bar's UTC day. The coin's mean is over every valid non-overlapping 7-bar grid return in all its windows. The minimums (100 cases, 60 days, 30 per side) gate the result as 'not observable'. The supporting check's value is the long mean excess minus the short mean excess.
- Size: unusual move +0.94 % (t 1.93, the cases of one day together: 693 days) per case over 7 bars, 0.069 of the coin's usual move (12.84 %); normal drift in its direction +0.02 %, total +0.96 %; 1178 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1.b1.d3_calm-choppy-month-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1.b1.d3_calm-choppy-month-rise-continues_1d`
Measure: `measure.py`
