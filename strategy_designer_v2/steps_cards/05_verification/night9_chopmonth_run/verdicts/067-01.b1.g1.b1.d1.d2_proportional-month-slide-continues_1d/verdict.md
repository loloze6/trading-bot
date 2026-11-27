---
plan: 067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues_1d
idea: 067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (10-bar return - coin drift) over chop short cases: 0.0121011; t of the mean, cases summed per day: 1.21138 (threshold: confirm: mean > 0 with t >= 2 (and both halves positive); reject: mean < 0 with t <= -2)
- Supporting check: min of mean short gain over drift in moderate and deep |forecast| halves (moderate -0.007464077229047727, deep 0.02325661003292701): -0.00746408, passed: False
- Counts: independent case-days: 150, cases: 423
- Decided by: The t of the main mean lies between -2 and 2.
- Reading: Chop is recomputed as the 60-day percent return from closes in [-10, +10] where 60 bars of the window exist, else taken from the recorded regime; the fall is fall30's raw value < 0; the drift is the coin's mean 10-bar return on the non-overlapping grid of all its windows; the t is the clustered t with deviations summed per UTC day; the halves are |forecast| below the median (moderate) and at or above it (deep).
- Size: unusual move +1.40 % (t 2.08, the cases of one day together: 522 days) per case over 10 bars, 0.072 of the coin's usual move (16.82 %); normal drift in its direction -1.50 %, total -0.10 %; 850 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d1.d2_proportional-month-slide-continues_1d`
Measure: `measure.py`
