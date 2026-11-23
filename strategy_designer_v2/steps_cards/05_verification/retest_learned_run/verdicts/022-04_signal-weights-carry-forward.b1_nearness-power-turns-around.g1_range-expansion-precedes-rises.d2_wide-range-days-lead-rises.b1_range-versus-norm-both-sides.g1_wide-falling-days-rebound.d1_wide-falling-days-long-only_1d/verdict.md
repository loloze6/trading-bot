---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move per case (3-bar return from signal close minus coin's normal 3-bar drift, long): 0.00912803; t of the mean: 3.95717 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, top third of entry forecast minus bottom third: 0.00997414, passed: True
- Counts: cases: 1619, active bars: 3306
- Decided by: The mean unusual move is above 0 with t >= 2 and the top third beats the bottom third.
- Reading: Cases are the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet) in each non-overlapping 3-bar cell counted from each window's first row, the normal drift is the coin's mean 3-bar return on that grid over all its windows, thirds are split by rank of entry forecast (n//3 cases each), the plan's 'fewer than 30 cases' minimum is reported as not observable, and the situation is rebuilt from prices (falling back to the recorded regime / raw component where a window lacks the prior close or 30 bars).
- Size: unusual move +0.91 % per case over 3 bars, 0.108 of the coin's usual move (7.96 %); normal drift in its direction +0.35 %, total +1.27 %; 1619 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d1_wide-falling-days-long-only_1d`
Measure: `measure.py`
