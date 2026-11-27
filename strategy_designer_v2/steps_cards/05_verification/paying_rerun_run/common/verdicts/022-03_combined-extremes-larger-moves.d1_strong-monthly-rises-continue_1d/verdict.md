---
plan: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d
idea: 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-adjusted 5-bar return on forecast at cell's first bar: 0.00127977; OLS slope t: 6.87632 (threshold: confirm: slope t >= 2 with supporting check passing; reject: slope t <= -2)
- Supporting check: mean drift-adjusted 5-bar return over cells with forecast > 0 above 0: 0.00586566, passed: True
- Counts: grid cells: 10967, grid cells with forecast > 0: 5118
- Decided by: The slope's t is 2 or more and the supporting check passes (confirm rule).
- Reading: Situation bars are those whose raw 28-bar return (recomputed from closes where not recorded) is above 0 with a positive forecast; cells are bars at positions 0,5,10,... of each window having a close 5 bars later in the same window, the slope's t is the ordinary OLS t, and the plan's minimum counts are read as 'not observable' when unmet.
- Size: unusual move +0.83 % (t 1.95, the cases of one day together: 1409 days) per case over 5 bars, 0.054 of the coin's usual move (12.26 %); normal drift in its direction +0.81 %, total +1.63 %; 4006 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d`
Measure: `measure.py`
