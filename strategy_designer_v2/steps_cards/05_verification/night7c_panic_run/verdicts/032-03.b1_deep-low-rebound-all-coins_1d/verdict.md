---
plan: 032-03.b1_deep-low-rebound-all-coins_1d
idea: 032-03.b1_deep-low-rebound-all-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of bets (return minus coin's 5-bar drift): 0.00535866; t of the mean, cases of the same day pooled: 0.636562 (threshold: confirm: positive with t >= 2; reject: negative with t <= -2; at least 30 distinct case days)
- Supporting check: upper-half minus lower-half mean unusual move, split at median entry forecast: 0.0046835, passed: True
- Counts: distinct case days: 221, cases: 437
- Decided by: The t of the mean unusual move lies between -2 and 2, which the plan calls inconclusive.
- Reading: The range-ratio condition (365-bar over 30-bar mean range at or below 1) cannot be rebuilt from windows of about 122 recorded bars and the detector's components are not recorded, so it is read from the recorded regime ('mean_reversion'), while the 30-bar closing low is recomputed from closes where 30 bars of the window exist; a bet is a rise of the long forecast of at least 2 points from its lowest positive level since the last bet (from 0 after a flat), the first bet per 5-bar grid cell from each window's first row is the case; the drift is the coin's mean 5-bar return on that grid over all its windows; the day-pooled t uses per-day sums of deviations from the mean (cluster SE with G/(G-1)); the median split puts cases above the median entry forecast in the upper half and the rest in the lower.
- Size: unusual move +0.54 % (t 0.64, the cases of one day together: 221 days) per case over 5 bars, 0.064 of the coin's usual move (11.68 %); normal drift in its direction +0.86 %, total +1.40 %; 437 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-03.b1_deep-low-rebound-all-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-03.b1_deep-low-rebound-all-coins_1d`
Measure: `measure.py`
