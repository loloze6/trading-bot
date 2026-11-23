---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 5-bar return on forecast>0 grid cells: 0.00575188; t of the weighted mean: 1.96554 (threshold: confirm if mean > 0 with t >= 2 (and timing gain > 0); reject if mean < 0 with t <= -2; at least 100 cells)
- Supporting check: book mean daily timing gain > 0: 0.000258885, passed: True
- Counts: grid cells with forecast > 0: 2490
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan rules inconclusive.
- Reading: The normal drift is the coin's mean return over the non-overlapping 5-bar grid of all its windows. The t of the weighted mean uses the weighted (sandwich) standard error with an n/(n-1) correction. The plan's 'below 100 cells' rule is reported as not observable. The market gain on day t uses the allocation held after day t-1's trade times the coin's mean daily close return over all windows.
- Size: unusual move -0.07 % per case over 5 bars, -0.003 of the coin's usual move (11.16 %); normal drift in its direction +0.71 %, total +0.63 %; 1236 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.b1_nearness-reversal-all-coins_1d`
Measure: `measure.py`
