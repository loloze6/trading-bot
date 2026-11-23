---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (5-day return minus coin's mean 5-day return), non-overlapping 5-bar cells, pooled: 0.000664617; t of the mean: 0.312122 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 non-zero cells)
- Supporting check: none
- Counts: non-zero cells: 3065, cells: 3065
- Decided by: t lies between -2 and 2 with at least 300 non-zero cells, which the plan calls inconclusive.
- Reading: The mean and t are taken over the non-zero-forecast cells only, which are the cells the plan's minimum counts. Each coin's mean 5-day return is the mean over all its valid grid cells in all windows. Cells whose 5-day return would leave the window are dropped.
- Size: unusual move +0.03 % per case over 5 bars, -0.003 of the coin's usual move (10.60 %); normal drift in its direction +0.04 %, total +0.07 %; 1161 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around_1d`
Measure: `measure.py`
