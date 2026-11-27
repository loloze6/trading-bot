---
plan: 067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative_1d
idea: 067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 10-bar return on forecast (short grid bars): 0.00240171; OLS slope t: 1.83154 (threshold: slope > 0 with t >= 2 confirms (with mean excess < 0); slope < 0 with t <= -2 rejects)
- Supporting check: mean excess 10-bar return on short grid bars below 0: -0.00793258, passed: True
- Counts: short grid cases: 423
- Decided by: The slope's t lies between -2 and 2.
- Reading: 60-bar return recomputed in percent from each window's closes (bounds inclusive), with the recorded regime used where fewer than 60 earlier bars exist in the window; 30-bar return taken from month_fall's raw value; grid at positions 0,10,20,... of each window, coin mean 10-bar return over all grid bars of all its windows; the fewer-than-100 rule treated as a minimum count (not observable); short grid cases counted only where the 10-bar return exists.
- Size: unusual move +1.40 % (t 2.08, the cases of one day together: 522 days) per case over 10 bars, 0.072 of the coin's usual move (16.82 %); normal drift in its direction -1.50 %, total -0.10 %; 850 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.g1.d2_slide-continues-while-month-negative_1d`
Measure: `measure.py`
