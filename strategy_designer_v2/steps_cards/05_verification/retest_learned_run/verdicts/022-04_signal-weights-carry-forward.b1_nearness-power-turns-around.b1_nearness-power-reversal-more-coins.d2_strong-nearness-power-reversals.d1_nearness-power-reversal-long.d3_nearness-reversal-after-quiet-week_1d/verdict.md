---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of excess 5-day return on the forecast (forecast > 0, non-overlapping grid): 0.000393146; OLS slope t: 1.32817 (threshold: confirm: slope t >= 2 (with Welch t >= 2); reject: slope t <= -2 or Welch t <= -2)
- Supporting check: mean excess 5-day return after prior 5-day return <= 0 minus after > 0, Welch t: 2.1583, passed: True
- Counts: grid cases with a positive forecast: 2489, cases with prior 5-day return <= 0: 1183, cases with prior 5-day return > 0: 1189
- Decided by: Neither rule met (slope t 1.33, Welch t 2.16): any other result is inconclusive.
- Reading: The coin's mean 5-day return is taken over all grid bars of all its windows; the regression uses every positive-forecast grid case with a 5-day forward return in its window, while the prior-return groups use only those with a prior 5-day return inside the window; the plan's minimum counts give 'not observable'.
- Size: unusual move -0.12 % per case over 5 bars, -0.010 of the coin's usual move (11.11 %); normal drift in its direction +0.71 %, total +0.59 %; 1251 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long.d3_nearness-reversal-after-quiet-week_1d`
Measure: `measure.py`
