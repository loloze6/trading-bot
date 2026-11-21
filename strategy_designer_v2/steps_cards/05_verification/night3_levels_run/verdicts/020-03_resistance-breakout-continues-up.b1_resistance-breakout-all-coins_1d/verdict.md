---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per long case: 0.00285348; ordinary t of the mean: 1.34087 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2)
- Supporting check: upper minus lower half (by signal-bar forecast) mean unusual move, Welch t >= 1: None, passed: False
- Counts: cases: 3937, upper half cases: 0, lower half cases: 3937
- Decided by: The t of the mean unusual move lies between -2 and 2 (or is undefined), with at least 30 cases.
- Reading: A case is the first bet bar (forecast rise >= 2 from its floor since the last bet, floor reset to 0 when flat) in each 5-bar grid cell counted from each window's first row, cases without 5 later bars in the window are dropped, the drift is the coin's mean 5-bar return on that grid over all its windows, and the median split puts forecasts above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +0.29 % per case over 5 bars, 0.022 of the coin's usual move (12.24 %); normal drift in its direction +0.74 %, total +1.03 %; 3937 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins_1d`
Measure: `measure.py`
