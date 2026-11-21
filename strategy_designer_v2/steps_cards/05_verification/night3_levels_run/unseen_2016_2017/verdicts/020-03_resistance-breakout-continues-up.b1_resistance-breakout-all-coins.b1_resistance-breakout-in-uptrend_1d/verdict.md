---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after long bets (return minus coin's mean 5-bar return): 0.022904; t of the mean: 1.74622 (threshold: confirm: positive with t >= 2 over at least 30 cases; reject: negative with t <= -2 over at least 30 cases)
- Supporting check: upper-half minus lower-half mean excess return (median split of entry forecast): 0.0528888, passed: True
- Counts: cases: 252, upper half cases: 126, lower half cases: 126
- Decided by: The t-statistic lies between -2 and 2.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) in each 5-bar grid cell counted from the window's first row, entered at that bar's close, with cases whose 5 bars run past the window dropped; the coin's mean 5-bar return uses the same grid pooled over its windows; the median split puts ties at the median in the lower half.
- Size: unusual move +2.29 % per case over 5 bars, 0.113 of the coin's usual move (17.89 %); normal drift in its direction +4.36 %, total +6.65 %; 252 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/unseen_2016_2017/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d`
Measure: `measure.py`
