---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 3-day excess return on forecast, forecast > 0 grid bars, pooled: 0.000514141; OLS slope t: 1.76806 (threshold: confirm: slope > 0 with t >= 2 on >= 100 cases; reject: slope < 0 with t <= -2 on >= 100 cases)
- Supporting check: mean excess per unit forecast, trending minus unknown: 0.000434344, passed: True
- Counts: cases: 2718, trending cases: 1256, unknown cases: 1462
- Decided by: The slope's t is between -2 and 2.
- Reading: The normal drift is each coin's mean 3-day return over all grid bars of all its windows, the mean excess per unit of forecast is sum(excess)/sum(forecast) per regime, a regime is the record's regime on the case bar, and a supporting check that cannot be computed counts as not passed.
- Size: unusual move +0.08 % per case over 3 bars, 0.008 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.44 %; 4558 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.d2_wide-falls-rebound-in-uptrends_1d`
Measure: `measure.py`
