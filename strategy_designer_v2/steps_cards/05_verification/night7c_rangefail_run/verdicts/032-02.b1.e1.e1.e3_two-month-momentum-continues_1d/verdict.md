---
plan: 032-02.b1.e1.e1.e3_two-month-momentum-continues_1d
idea: 032-02.b1.e1.e1.e3_two-month-momentum-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of the 20-bar forward return (minus the coin's mean 20-bar return) on the forecast: 0.000497406; OLS t of the slope: 0.609427 (threshold: confirm: slope > 0 with t >= 2 and timing part > 0; reject: slope < 0 with t <= -2)
- Supporting check: timing part of the book's mean daily return (book minus market gain) > 0: 8.07738e-05, passed: True
- Counts: non-overlapping grid cases with a nonzero forecast: 827, non-overlapping grid cases: 827
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The regression uses all non-overlapping 20-bar grid cases (positions 0, 20, ... of each window) with an intercept, the coin's mean 20-bar return is the mean over those grid cases of all its windows, and the timing part is the book's mean daily return (postRebalance_total_value, mean across coins per day) minus the previous bar's allocation times the coin's all-window mean daily return, averaged the same way.
- Size: unusual move +1.36 % (t 0.96, the cases of one day together: 398 days) per case over 20 bars, 0.056 of the coin's usual move (21.24 %); normal drift in its direction -0.11 %, total +1.25 %; 704 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e3_two-month-momentum-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e3_two-month-momentum-continues_1d`
Measure: `measure.py`
