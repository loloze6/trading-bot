---
plan: 031-03.b1.b1_20-day-continuation-all-coins_1d
idea: 031-03.b1.b1_20-day-continuation-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x coin's excess 10-bar return, non-overlapping grid: 0.0106098; t of the mean, cases of one day summed as one piece of evidence: 1.52295 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: Welch difference of directional excess return, top third minus bottom third by |forecast| (Welch t 0.583): 0.00419292, passed: True
- Counts: cases with a nonzero forecast: 3598, distinct days: 304
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases are the grid bars (positions 0, 10, 20, ... of each window, with t+10 inside the window) with a nonzero forecast, the coin's mean 10-bar return is taken over all grid bars of all its windows, the thirds are the n//3 cases with the smallest and largest |forecast| by stable rank, and the day-clustered t sums the cases' deviations per UTC day.
- Size: unusual move +0.69 % (t 1.34, the cases of one day together: 1063 days) per case over 10 bars, 0.041 of the coin's usual move (16.82 %); normal drift in its direction -0.09 %, total +0.60 %; 3219 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.b1.b1_20-day-continuation-all-coins_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.b1.b1_20-day-continuation-all-coins_1d`
Measure: `measure.py`
