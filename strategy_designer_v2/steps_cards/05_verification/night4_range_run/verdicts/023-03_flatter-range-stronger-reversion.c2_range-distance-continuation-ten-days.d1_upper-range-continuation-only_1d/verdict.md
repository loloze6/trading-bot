---
plan: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-bar forward return on forecast (forecast > 0, non-overlapping grid): 0.00265496; OLS slope t: 2.32246 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean excess 10-bar return of forecast > 0 grid cases: 0.00857841, passed: True
- Counts: grid cases with forecast > 0: 792, grid cases total: 1691
- Decided by: The slope is positive with t >= 2 and the mean excess return of the forecast > 0 cases is above 0.
- Reading: The coin's mean 10-bar return is the mean over all grid cells of all its windows, the slope is an OLS fit with intercept, and the plan's 'fewer than 100 cases' rule is treated as a minimum count giving 'not observable'.
- Size: unusual move +0.61 % per case over 10 bars, 0.032 of the coin's usual move (14.49 %); normal drift in its direction +1.17 %, total +1.77 %; 977 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d`
Measure: `measure.py`
