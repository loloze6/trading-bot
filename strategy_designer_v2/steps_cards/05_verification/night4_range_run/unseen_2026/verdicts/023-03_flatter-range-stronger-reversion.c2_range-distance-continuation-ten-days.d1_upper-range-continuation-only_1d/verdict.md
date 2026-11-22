---
plan: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d
idea: 023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 10-bar forward return on forecast (forecast > 0, non-overlapping grid): 0.00305032; OLS slope t: 1.03717 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: mean excess 10-bar return of forecast > 0 grid cases: 0.0269518, passed: True
- Counts: grid cases with forecast > 0: 81, grid cases total: 180
- Decided by: Only 81 grid cases with forecast > 0, fewer than the plan's minimum of 100.
- Reading: The coin's mean 10-bar return is the mean over all grid cells of all its windows, the slope is an OLS fit with intercept, and the plan's 'fewer than 100 cases' rule is treated as a minimum count giving 'not observable'.
- Size: unusual move +1.83 % per case over 10 bars, 0.172 of the coin's usual move (9.14 %); normal drift in its direction +0.44 %, total +2.27 %; 107 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/unseen_2026/backtests/023-03_flatter-range-stronger-reversion.c2_range-distance-continuation-ten-days.d1_upper-range-continuation-only_1d`
Measure: `measure.py`
