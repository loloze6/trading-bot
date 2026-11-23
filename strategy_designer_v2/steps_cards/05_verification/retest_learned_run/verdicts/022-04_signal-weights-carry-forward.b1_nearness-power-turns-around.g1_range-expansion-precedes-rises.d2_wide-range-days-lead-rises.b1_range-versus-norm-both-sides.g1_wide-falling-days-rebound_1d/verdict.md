---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound
fit: adapted
status: confirmed
---
Situation check: 91 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 3-day return on forecast, falling-day grid cases pooled: 2.90635; OLS slope t: 2.90635 (threshold: confirm if slope t >= 2 with top-third mean excess > 0; reject if slope t <= -2; at least 300 cases)
- Supporting check: top-third forecast mean excess 3-day return: 0.00683467, passed: True
- Counts: falling-day grid cases: 2718, top-third cases: 906
- Decided by: Slope t is 2 or more and the top-third mean excess return is positive: confirm.
- Reading: Situation = a falling day (close below prior close, regime column on a window's first row) and the side is long when its raw range ratio is above 1 (range above its 30-day average) and, for the graded adaptation, short when below 1; grid cases are regime 'mean_reversion' bars at positions 0,3,6,... of each window, the coin's mean 3-day return is the mean of all its grid returns over all windows, the slope t is the OLS slope over its standard error, and the top third is the n//3 cases with the highest forecast.
- Size: unusual move +0.78 % per case over 3 bars, 0.090 of the coin's usual move (7.96 %); normal drift in its direction -0.05 %, total +0.73 %; 2755 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound_1d`
Measure: `measure.py`
