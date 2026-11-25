---
plan: 047-01_falling-agitated-scaled-fall-rebound_1d
idea: 047-01_falling-agitated-scaled-fall-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move after forecast > 0 (long), minus the coin's normal 3-day drift: 0.00710902; t of the mean, same-day cases summed per day: 0.946873 (threshold: confirm: mean > 0 with t >= 2 over >= 30 case-days and slope > 0; reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: least-squares slope of unusual move on forecast, > 0: 0.000997759, passed: True
- Counts: case-days: 223, cases: 454, active bars: 1482
- Decided by: t lies between -2 and 2: inconclusive.
- Reading: Situation bars are taken as regime 'unknown' (the profile left by the vetoes) with a negative scaled_fall raw value (or a negative close-to-close return where unrecorded), side long; cases are grid bars 0,3,6,... of each window with forecast > 0 and a close 3 bars later in the same window, drift is the coin's mean 3-bar return on that grid over all its windows, and t uses the standard error from per-day summed deviations with the number of distinct case days as n.
- Size: unusual move +0.86 % (t 1.70, the cases of one day together: 412 days) per case over 3 bars, 0.107 of the coin's usual move (7.96 %); normal drift in its direction +0.39 %, total +1.24 %; 805 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/047-01_falling-agitated-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/047-01_falling-agitated-scaled-fall-rebound_1d`
Measure: `measure.py`
