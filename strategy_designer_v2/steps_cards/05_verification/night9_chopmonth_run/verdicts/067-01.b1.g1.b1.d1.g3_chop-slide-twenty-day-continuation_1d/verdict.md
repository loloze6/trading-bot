---
plan: 067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation_1d
idea: 067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 20-bar move of short cases, before costs: 0.00751602; t of the mean, cases summed per day: 0.444616 (threshold: confirm: mean > 0 with t >= 2 and depth check passes; reject: mean < 0 with t <= -2)
- Supporting check: deepest third by |forecast| has a higher mean unusual move than shallowest third: 0.0298394, passed: True
- Counts: cases: 571, distinct days: 376
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: Situation = recorded fall30 raw value (30-bar return, recomputed from closes where missing) below 0 with a negative forecast; a case is the first bet (short-side forecast deepening by >= 2 points from its lowest depth since the last bet, reset at flat) in each 20-bar grid cell of each window, dropped if its 20-bar return leaves the window; drift = mean of a coin's non-overlapping 20-bar returns over all its windows; t uses a day-clustered standard error with D/(D-1) correction; thirds split by rank of |forecast|; the plan's 'fewer than 30 cases or 30 distinct days' is applied as 'not observable'.
- Size: unusual move +0.75 % (t 0.45, the cases of one day together: 376 days) per case over 20 bars, 0.009 of the coin's usual move (25.96 %); normal drift in its direction -3.20 %, total -2.45 %; 571 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d1.g3_chop-slide-twenty-day-continuation_1d`
Measure: `measure.py`
