---
plan: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
idea: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-bar return on forecast at cell's first bar: 0.00329405; OLS slope t: 3.36884 (threshold: confirm: slope t >= 2 with supporting check passing; reject: slope t <= -2)
- Supporting check: mean drift-adjusted 5-bar return over cells with forecast > 0 above 0: 0.0132189, passed: True
- Counts: grid cells: 572, grid cells with forecast > 0: 379
- Decided by: The slope's t is 2 or more and the supporting check passes (confirm rule).
- Reading: Situation bars are those whose raw 28-bar return (recomputed from closes where not recorded) is above 0 with a positive forecast; cells are bars at positions 0,5,10,... of each window having a close 5 bars later in the same window, the slope's t is the ordinary OLS t, and the plan's minimum counts are read as 'not observable' when unmet.
- Size: unusual move +3.50 % per case over 5 bars, 0.186 of the coin's usual move (18.32 %); normal drift in its direction +4.53 %, total +8.03 %; 264 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d`
Measure: `measure.py`
