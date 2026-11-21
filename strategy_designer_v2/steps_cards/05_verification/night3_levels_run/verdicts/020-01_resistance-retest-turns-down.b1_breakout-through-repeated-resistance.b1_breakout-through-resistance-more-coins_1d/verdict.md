---
plan: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins_1d
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move of long cases: 0.000830911; one-sample t: 0.233164 (threshold: mean above 0 with t >= 2 on at least 30 cases to confirm; below 0 with t <= -2 to reject)
- Supporting check: mean unusual move N>=3 minus N<=2: 0.00372795, passed: True
- Counts: cases: 2613, cases with N >= 3: 340, cases with N <= 2: 1658
- Decided by: The t of the mean unusual move is between -2 and 2 on at least 30 cases.
- Reading: A case is the first forecast rise of at least 2 points above its floor (reset to 0 when the forecast is flat) in each 10-bar grid cell of a window, and N is recomputed from the window's own closes (swing-high closes above their 2 neighbours on each side within the past 90 bars, using the crossed level whose N x margin matches the recorded raw value, else the one with most touches), with cases where no crossed level is found left out of the supporting check.
- Size: unusual move +0.08 % per case over 10 bars, 0.005 of the coin's usual move (16.53 %); normal drift in its direction +1.38 %, total +1.47 %; 2613 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins_1d`
Measure: `measure.py`
