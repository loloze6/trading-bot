---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: one-sample t of mean excess 5-day return on positive-forecast grid bars: 0.00372994; one-sample t: 1.71847 (threshold: confirm t >= 2 (with check passing); reject t <= -2; otherwise inconclusive)
- Supporting check: mean excess return, larger half minus smaller half of positive forecasts: 0.00190904, passed: True
- Counts: positive-forecast grid cases: 2457
- Decided by: t lies between -2 and 2.
- Reading: Situation taken as raw component value < 0 with forecast > 0 (standardise only scales, so negate+clip leaves the forecast positive exactly when the raw value is negative); the coin's mean 5-day return is taken on the same non-overlapping grid over all its windows; the halves are split by sorted forecast with the middle case left out when the count is odd; the plan's fewer-than-100-cases rule is treated as a minimum count, giving 'not observable'.
- Size: unusual move -0.07 % per case over 5 bars, -0.004 of the coin's usual move (11.11 %); normal drift in its direction +0.72 %, total +0.64 %; 1224 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d`
Measure: `measure.py`
