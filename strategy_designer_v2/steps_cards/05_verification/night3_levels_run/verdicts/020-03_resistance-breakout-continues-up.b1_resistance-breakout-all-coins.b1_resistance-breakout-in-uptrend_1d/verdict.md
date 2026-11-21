---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after long bets (return minus coin's mean 5-bar return): 0.0110989; t of the mean: 3.8464 (threshold: confirm: positive with t >= 2 over at least 30 cases; reject: negative with t <= -2 over at least 30 cases)
- Supporting check: upper-half minus lower-half mean excess return (median split of entry forecast): 0.0126979, passed: True
- Counts: cases: 2638, upper half cases: 1319, lower half cases: 1319
- Decided by: Mean excess return positive with t >= 2 over at least 30 cases, and the upper-half-minus-lower-half difference is above 0.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) in each 5-bar grid cell counted from the window's first row, entered at that bar's close, with cases whose 5 bars run past the window dropped; the coin's mean 5-bar return uses the same grid pooled over its windows; the median split puts ties at the median in the lower half.
- Size: unusual move +1.11 % per case over 5 bars, 0.084 of the coin's usual move (12.24 %); normal drift in its direction +0.75 %, total +1.86 %; 2638 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d`
Measure: `measure.py`
