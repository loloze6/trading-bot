---
plan: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d
idea: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per case (return from signal close minus coin's normal 3-bar drift): -0.00520776; t of the mean, cases grouped by day: -0.296185 (threshold: confirm: mean > 0 with day-grouped t >= 2 and check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-forecast half minus smaller half, above 0: 0.0201278, passed: True
- Counts: cases: 59, days: 56
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Cases are the first bet in each 3-bar grid cell of a window (grid from the window's first row) with 3 bars ahead; the t uses deviations summed per UTC day; the halves are the n//2 largest and n//2 smallest forecasts at the signal bar (the middle case dropped when n is odd); situation bars not computable in-window are left out of the agreement share; the plan's 'fewer than 30 cases or 30 days' rule is reported as not observable.
- Size: unusual move -0.52 % (t -0.30, the cases of one day together: 56 days) per case over 3 bars, -0.003 of the coin's usual move (13.83 %); normal drift in its direction +2.82 %, total +2.30 %; 59 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/unseen_2016_2017/backtests/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d`
Measure: `measure.py`
