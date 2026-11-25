---
plan: 032-01.b1_agitated-trend-weekly-reversal_1d
idea: 032-01.b1_agitated-trend-weekly-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move of short cases (short direction): -0.0116897; t of the mean, cases summed per day: -1.02739 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases (and slope > 0); reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: OLS slope of unusual move on |forecast|: -0.00269356, passed: False
- Counts: cases: 298, days: 220
- Decided by: t lies between -2 and 2.
- Reading: Situation recomputed from prices (30-day std of daily returns, ddof 1, over its 60-bar mean including the bar, >= 1, and 30-day Kaufman ER >= 0.3), falling back to the recorded regime on bars whose history lacks the warm-up, with a short forecast and a positive raw rise where recorded; a case is the first short bet (forecast deepening >= 2 points from its shallowest level since the last bet) in each 7-bar grid cell, its return taken from that bar's close over 7 bars inside the window, drift = mean of non-overlapping 7-bar grid returns over all the coin's windows, t clustered by calendar day.
- Size: unusual move -1.17 % (t -1.03, the cases of one day together: 220 days) per case over 7 bars, -0.065 of the coin's usual move (12.44 %); normal drift in its direction -0.94 %, total -2.10 %; 298 cases
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1_agitated-trend-weekly-reversal_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1_agitated-trend-weekly-reversal_1d`
Measure: `measure.py`
