---
plan: 023-03_flatter-range-stronger-reversion_1d
idea: 023-03_flatter-range-stronger-reversion
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (5-day return minus coin's normal drift) on the 5-bar grid: -0.00679748; t of the mean: -3.39038 (threshold: confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2)
- Supporting check: flatter-half minus less-flat-half mean reversion return per unit distance: -0.202237, passed: False
- Counts: grid cases with a nonzero forecast: 3418, grid cases in main measure: 3419, supporting flatter half: 1277, supporting less-flat half: 1278
- Decided by: Main mean is negative with t <= -2.
- Reading: Main mean is over all grid bars (zero forecasts contribute zero) with drift as the coin's mean grid 5-day return over all windows; the supporting check recomputes pos and flatness from prices (range of closes t-29..t, net move close[t]-close[t-30]), so grid bars with fewer than 30 prior bars in the window or at the exact middle are left out, and the flatter half is flatness above the median, the less-flat half at or below it.
- Size: unusual move -0.40 % per case over 5 bars, -0.039 of the coin's usual move (10.60 %); normal drift in its direction +0.02 %, total -0.39 %; 2912 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion_1d`
Measure: `measure.py`
