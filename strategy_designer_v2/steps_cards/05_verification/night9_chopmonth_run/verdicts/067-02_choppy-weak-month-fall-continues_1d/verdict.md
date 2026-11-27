---
plan: 067-02_choppy-weak-month-fall-continues_1d
idea: 067-02_choppy-weak-month-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean short-side unusual 7-bar move: 0.0155944; weighted t, cases of one day summed: 1.57148 (threshold: confirm: above 0 with t >= 2 and supporting check passing; reject: below 0 with t <= -2; else inconclusive)
- Supporting check: mean short-side unusual move, larger half of abs(forecast) minus smaller half: 0.0242012, passed: True
- Counts: independent days with cases: 211, cases: 633
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are bars at positions 0,7,14,... of each window with forecast < 0 and a close 7 bars later in the same window, the coin's mean 7-bar return is the mean over that grid in all its windows, the halves split the cases sorted by abs(forecast) with the odd middle case in the smaller half and unweighted means, and the plan's 'fewer than 100 independent days' is treated as the minimum count giving 'not observable'.
- Size: unusual move +1.13 % (t 2.08, the cases of one day together: 624 days) per case over 7 bars, 0.071 of the coin's usual move (14.34 %); normal drift in its direction -1.13 %, total -0.01 %; 1024 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02_choppy-weak-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02_choppy-weak-month-fall-continues_1d`
Measure: `measure.py`
