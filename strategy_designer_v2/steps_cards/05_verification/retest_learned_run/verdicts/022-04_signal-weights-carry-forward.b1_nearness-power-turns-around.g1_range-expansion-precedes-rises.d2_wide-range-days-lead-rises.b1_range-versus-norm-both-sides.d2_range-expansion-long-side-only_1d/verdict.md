---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 3-bar return: 0.00591078; t of per-bar forecast x excess: 2.22524 (threshold: above 0 with t >= 2 confirms; below 0 with t <= -2 rejects; at least 100 grid cases)
- Supporting check: none
- Counts: independent grid cases with forecast > 0: 2173
- Decided by: Confirm: the forecast-weighted mean excess 3-bar return is above 0 with t >= 2 over at least 100 grid cases.
- Reading: The coin's mean 3-bar return is taken over all its non-overlapping grid bars (positions 0, 3, 6, ... of every window, forward return inside the window), and the plan's 'fewer than 100 cases' is reported as not observable per the minimum-count rule.
- Size: unusual move +0.44 % per case over 3 bars, 0.049 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.80 %; 3025 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.d2_range-expansion-long-side-only_1d`
Measure: `measure.py`
