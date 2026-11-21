---
plan: 019-03_upward-breakout-quiet-continuation_4h
idea: 019-03_upward-breakout-quiet-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 18-bar return of bets (return minus coin's normal 18-bar drift), before costs: 0.00202808; t of the mean: 1.27626 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2; at least 30 independent cases)
- Supporting check: mean excess return of cases above the median signal forecast minus those at or below it: None, passed: None
- Counts: independent cases: 3073, upper half cases: 0, lower half cases: 3073
- Decided by: The t of the mean excess return lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first long bet (forecast rise of at least 2 points from its lowest positive level since the last bet, from 0 after flat) in each 18-bar grid cell counted from each window's first row, with its 18-bar return needing to end inside the window; the median split puts cases with forecast strictly above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +0.20 % per case over 18 bars, 0.023 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.61 %; 3073 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation_4h`
Measure: `measure.py`
