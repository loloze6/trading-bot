---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar unusual move per case (return minus coin's normal 5-day drift), before costs: 0.00719421; t of the mean: 3.01988 (threshold: confirm t >= 2, reject t <= -2, over at least 30 independent cases)
- Supporting check: mean unusual move of cases with entry forecast above the median minus below it (> 0): 0.0136047, passed: True
- Counts: independent cases: 4109
- Decided by: Mean unusual move has t >= 2 over at least 30 independent cases and the supporting check passes.
- Reading: Cases are forecast rises of at least 2 points on the long side, the first per 5-bar grid cell of each window, dropped when the 5-bar return leaves the window; the drift is the mean non-overlapping 5-bar return over all the coin's windows; cases exactly at the median forecast are in neither group, and an empty group fails the supporting check.
- Size: unusual move +0.72 % (t 1.88, the cases of one day together: 1541 days) per case over 5 bars, 0.053 of the coin's usual move (12.26 %); normal drift in its direction +0.76 %, total +1.48 %; 4109 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d`
Measure: `measure.py`
