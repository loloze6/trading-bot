---
plan: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of breakout bets (return minus coin's mean 18-bar return): 0.00174074; t of the mean: 1.34859 (threshold: confirm t >= 2 over >= 30 cases with upper-minus-lower > 0; reject t <= -2 over >= 30 cases)
- Supporting check: mean unusual move of upper half minus lower half (split at median signal-bar forecast): None, passed: None
- Counts: cases: 6664, upper half cases: 0, lower half cases: 6664
- Decided by: The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first bet (long forecast rising >= 2 points from its lowest level since the last bet, reset to 0 when flat) in each 18-bar grid cell counted from each window's first row, dropped if 18 bars do not remain in the window; the drift is the coin's mean return on the non-overlapping 18-bar grid of all its windows; the median split puts cases with forecast above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +0.17 % per case over 18 bars, 0.016 of the coin's usual move (9.29 %); normal drift in its direction +0.52 %, total +0.69 %; 6664 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins_4h`
Measure: `measure.py`
