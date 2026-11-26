---
plan: 074-01.b2_three-day-low-close-rebound_1d
idea: 074-01.b2_three-day-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move per long case (return minus coin's normal 3-day drift): 0.00733984; t of the mean, cases summed per day: 1.14138 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on entry forecast: 0.00246878, passed: True
- Counts: cases: 290, distinct days: 164
- Decided by: The t of the mean unusual move lies between -2 and 2: inconclusive.
- Reading: Situation bars are regime 'mean_reversion' (the detector's record, which carries the rising-calm vetoes that cannot be recomputed from 120-bar windows with a 365-bar lookback) with close location from the high >= 0.75 from prices and width >= 2 (range/close over the ddof-1 std of the last 30 in-window daily returns, where 30 returns exist) and a long forecast; a case is the first bet bar of each 3-bar grid cell counted from each window's first row; the t clusters cases by UTC day; the plan's 'fewer than 30 cases or days' is treated as a minimum count, hence 'not observable'.
- Size: unusual move +0.73 % (t 1.14, the cases of one day together: 164 days) per case over 3 bars, 0.101 of the coin's usual move (8.85 %); normal drift in its direction +0.44 %, total +1.17 %; 290 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/074-01.b2_three-day-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/074-01.b2_three-day-low-close-rebound_1d`
Measure: `measure.py`
