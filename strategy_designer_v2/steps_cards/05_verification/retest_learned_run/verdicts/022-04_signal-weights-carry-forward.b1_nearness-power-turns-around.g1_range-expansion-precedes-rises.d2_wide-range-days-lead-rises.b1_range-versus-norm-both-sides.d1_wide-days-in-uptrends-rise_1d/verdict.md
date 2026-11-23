---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x excess 3-bar return on positive-forecast grid bars: 0.12712; ordinary t of the mean: 3.39094 (threshold: t >= 2 (with supporting check > 0) confirms; t <= -2 rejects; at least 100 cases)
- Supporting check: mean excess 3-bar return, upper minus lower half at median forecast: 0.0117911, passed: True
- Counts: grid cases with positive forecast: 1322, upper half cases: 661, lower half cases: 661
- Decided by: the main measure's t is 2 or more and the supporting check is above 0, with at least 100 cases.
- Reading: The coin's mean 3-bar return is taken over all its windows' non-overlapping grid returns (grid from each window's first row, last incomplete cell dropped), and the median split puts forecasts above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +0.51 % per case over 3 bars, 0.053 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.87 %; 1794 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d1_wide-days-in-uptrends-rise_1d`
Measure: `measure.py`
