---
plan: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d
idea: 031-02.b1.b1.b1.d2_width-graded-flat-uprun-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per case (return from signal close minus coin's normal 3-bar drift): 0.016663; t of the mean, cases grouped by day: 3.15665 (threshold: confirm: mean > 0 with day-grouped t >= 2 and check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-forecast half minus smaller half, above 0: 0.00570361, passed: True
- Counts: cases: 490, days: 352
- Decided by: The mean unusual move is above 0 with t >= 2 and the larger-forecast half beats the smaller half.
- Reading: Cases are the first bet in each 3-bar grid cell of a window (grid from the window's first row) with 3 bars ahead; the t uses deviations summed per UTC day; the halves are the n//2 largest and n//2 smallest forecasts at the signal bar (the middle case dropped when n is odd); situation bars not computable in-window are left out of the agreement share; the plan's 'fewer than 30 cases or 30 days' rule is reported as not observable.
- Size: unusual move +1.67 % (t 3.16, the cases of one day together: 352 days) per case over 3 bars, 0.181 of the coin's usual move (9.14 %); normal drift in its direction +0.47 %, total +2.14 %; 490 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.d2_width-graded-flat-uprun-day_1d`
Measure: `measure.py`
