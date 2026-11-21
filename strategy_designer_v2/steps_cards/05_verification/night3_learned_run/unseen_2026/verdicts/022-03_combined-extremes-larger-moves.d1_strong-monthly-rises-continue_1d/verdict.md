---
plan: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
idea: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-bar return on forecast at cell's first bar: 0.00123642; OLS slope t: 1.58088 (threshold: confirm: slope t >= 2 with supporting check passing; reject: slope t <= -2)
- Supporting check: mean drift-adjusted 5-bar return over cells with forecast > 0 above 0: 0.00622358, passed: True
- Counts: grid cells: 372, grid cells with forecast > 0: 198
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: Situation bars are those whose raw 28-bar return (recomputed from closes where not recorded) is above 0 with a positive forecast; cells are bars at positions 0,5,10,... of each window having a close 5 bars later in the same window, the slope's t is the ordinary OLS t, and the plan's minimum counts are read as 'not observable' when unmet.
- Size: unusual move +0.91 % per case over 5 bars, 0.079 of the coin's usual move (8.48 %); normal drift in its direction +0.23 %, total +1.14 %; 158 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2026/backtests/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d`
Measure: `measure.py`
