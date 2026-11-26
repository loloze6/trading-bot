---
plan: 032-01.b1.b1_large-weekly-rise-continues_1d
idea: 032-01.b1.b1_large-weekly-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move of the long cases (return minus the coin's mean 7-bar return): 0.0491755; t of the mean, cases of one day taken together: 1.93699 (threshold: confirm: mean > 0 with day-clustered t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: least-squares slope of the unusual move on the forecast: 0.00423313, passed: True
- Counts: cases: 103, distinct days: 63
- Decided by: The t lies between -2 and 2.
- Reading: Cases are grid bars (positions 0, 7, 14, ... of each window, with a full 7-bar return inside the window) with forecast > 0, the drift is the coin's mean 7-bar return on that grid over all its windows, the t uses day-clustered deviations with a D/(D-1) correction, and the plan's 'fewer than 30 cases or 20 days' is treated as the minimum count giving 'not observable'.
- Size: unusual move +2.24 % (t 1.72, the cases of one day together: 192 days) per case over 7 bars, 0.152 of the coin's usual move (12.44 %); normal drift in its direction +0.92 %, total +3.16 %; 257 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1_large-weekly-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1_large-weekly-rise-continues_1d`
Measure: `measure.py`
