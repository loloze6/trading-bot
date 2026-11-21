---
plan: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 10-bar excess return of the bets over the coin's normal 10-bar drift: 0.00309019; ordinary t of the mean: 0.621326 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess return of larger-forecast half minus smaller half: 0.00587858, passed: True
- Counts: cases: 1084
- Decided by: The t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: A case is the first bet (a rise of the long forecast of at least 2 points from its lowest level since the last bet, from 0 after flat) in each 10-bar grid cell of a window counted from its first row, with its 10-bar return taken from that bet's own close and dropped if the window ends first; the normal drift is the mean of the coin's non-overlapping 10-bar grid returns over all its windows; the median split sorts cases by entry forecast (ties by coin, window and time) and compares the top n//2 against the bottom n//2, leaving out the middle case when n is odd; the plan's 'fewer than 30 cases' is reported as not observable, per the workflow.
- Size: unusual move +0.31 % per case over 10 bars, 0.009 of the coin's usual move (14.49 %); normal drift in its direction +1.17 %, total +1.48 %; 1084 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance_1d`
Measure: `measure.py`
