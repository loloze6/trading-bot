---
plan: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d
idea: 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar return after long bets (return minus coin's mean 5-bar return): 0.00997196; t of the mean: 3.97642 (threshold: confirm: positive with t >= 2 over at least 30 cases; reject: negative with t <= -2 over at least 30 cases)
- Supporting check: upper-half minus lower-half mean excess return (median split of entry forecast): 0.0158764, passed: True
- Counts: cases: 3859, upper half cases: 1929, lower half cases: 1930
- Decided by: Mean excess return positive with t >= 2 over at least 30 cases, and the upper-half-minus-lower-half difference is above 0.
- Reading: A case is the first long bet (forecast rise >= 2 points from its lowest level since the last bet, from 0 after flat) in each 5-bar grid cell counted from the window's first row, entered at that bar's close, with cases whose 5 bars run past the window dropped; the coin's mean 5-bar return uses the same grid pooled over its windows; the median split puts ties at the median in the lower half.
- Size: unusual move +1.00 % (t 2.54, the cases of one day together: 1500 days) per case over 5 bars, 0.074 of the coin's usual move (12.26 %); normal drift in its direction +0.77 %, total +1.77 %; 3859 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d`
Measure: `measure.py`
