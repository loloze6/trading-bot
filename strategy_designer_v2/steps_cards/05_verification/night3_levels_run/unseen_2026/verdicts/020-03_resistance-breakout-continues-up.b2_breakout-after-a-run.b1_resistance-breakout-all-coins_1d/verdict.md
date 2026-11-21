---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar unusual move per case (return minus coin's normal 5-day drift), before costs: 0.00706548; t of the mean: 1.38245 (threshold: confirm t >= 2, reject t <= -2, over at least 30 independent cases)
- Supporting check: mean unusual move of cases with entry forecast above the median minus below it (> 0): 0.00153535, passed: True
- Counts: independent cases: 465
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Cases are forecast rises of at least 2 points on the long side, the first per 5-bar grid cell of each window, dropped when the 5-bar return leaves the window; the drift is the mean non-overlapping 5-bar return over all the coin's windows; cases exactly at the median forecast are in neither group, and an empty group fails the supporting check.
- Size: unusual move +0.71 % per case over 5 bars, 0.063 of the coin's usual move (9.44 %); normal drift in its direction +0.17 %, total +0.88 %; 465 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/unseen_2026/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d`
Measure: `measure.py`
