---
plan: 022-03_combined-extremes-larger-moves_1d
idea: 022-03_combined-extremes-larger-moves
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed unusual 5-bar move, combined top-10% minus best single top-10%: -0.0094146; Welch t: -1.01246 (threshold: Welch t >= 2 (with combined beating every single and slope t >= 2) confirms; Welch t <= -2 or slope t <= -2 rejects)
- Supporting check: slope t of signed unusual move on abs(combined post_pipeline_value): 0.653086, passed: False
- Counts: combined top-10% cells: 326, s_momentum top-10% cells: 326, s_reversal top-10% cells: 326, s_high top-10% cells: 326, s_volatility top-10% cells: 326, combined cells in regression: 3254
- Decided by: Neither rule met: Welch t -1.01 vs best single s_reversal, combined beats all singles: False, slope t 0.65.
- Reading: Cells are rows 0,5,10,... of each window with a 5-bar return inside it; each group's top 10% is abs(last_history_value) at or above its pooled 90th percentile over measured cells, signed by that same component's raw value; the best single is the one with the highest mean signed unusual move; and since the minimum-count rule is stated, a group under 30 cases gives 'not observable'.
- Size: unusual move +0.02 % per case over 5 bars, 0.002 of the coin's usual move (10.60 %); normal drift in its direction -0.05 %, total -0.03 %; 1739 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves_1d`
Measure: `measure.py`
