---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x (5-bar return minus coin's mean 5-bar return), grid bars with forecast > 0: 0.0418851; ordinary t of the mean: 1.07006 (threshold: confirm if t >= 2 (with supporting check > 0); reject if t <= -2)
- Supporting check: mean excess 5-bar return, 20-day return above median minus below median: 0.00125942, passed: True
- Counts: grid cases with forecast > 0: 1098
- Decided by: The main measure's t is between -2 and 2.
- Reading: The plan's situation is taken as raw component value < 0 (negated, standardised, clipped at 0 -> long) while the 20-day return recomputed from closes is > 0 (the regime column used only on the first 20 bars of a window, where it cannot be recomputed); the coin's mean 5-bar return is over all non-overlapping grid bars of all its windows; the supporting check splits the forecast > 0 cases at the pooled median of their recomputed 20-day return (cases without it left out, cases equal to the median in neither group); the 100-case minimum not reached gives 'not observable'.
- Size: unusual move -0.19 % per case over 5 bars, -0.018 of the coin's usual move (11.11 %); normal drift in its direction +0.71 %, total +0.51 %; 881 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d2_nearness-reversal-after-20-day-strength_1d`
Measure: `measure.py`
