---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next 3-bar excess return on forecast: 0.0012924; OLS t of the slope: 2.80623 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 1000 grid cases)
- Supporting check: none
- Counts: independent grid cases: 5723, active bars: 17524
- Decided by: Confirm rule met: the slope is positive with t >= 2 over at least 1000 grid cases.
- Reading: All grid cells (positions 0,3,6,... of each window with a bar 3 ahead) enter the regression, including those with a zero forecast, and the coin's mean 3-bar return is taken over its grid cells of all windows.
- Size: unusual move +0.42 % per case over 3 bars, 0.045 of the coin's usual move (7.96 %); normal drift in its direction -0.01 %, total +0.41 %; 3466 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides_1d`
Measure: `measure.py`
