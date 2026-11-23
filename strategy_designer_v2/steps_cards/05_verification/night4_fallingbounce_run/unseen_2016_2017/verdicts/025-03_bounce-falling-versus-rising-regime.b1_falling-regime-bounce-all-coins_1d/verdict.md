---
plan: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
idea: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move, mean_reversion cases minus trending cases: -0.0368937; Welch t: -1.70248 (threshold: confirm at Welch t <= -2 with the supporting check passing; reject at Welch t >= +2)
- Supporting check: same difference on cases with rise reading above pooled median, more negative than main: -0.0608964, passed: True
- Counts: mean_reversion cases: 68, trending cases: 325, mean_reversion cases above median rise: 25, trending cases above median rise: 171
- Decided by: Main Welch t lies between -2 and +2, which the plan calls inconclusive.
- Reading: The unusual move is the raw 5-bar return minus the coin's mean 5-bar grid return, not signed by the bet's direction (the plan compares returns across regimes), the case's regime is the bar's recorded regime, the first bet of each 5-bar grid cell is the case, and the plan's 30-case minimum per regime is applied as 'not observable'.
- Size: unusual move +1.65 % (t 1.10, the cases of one day together: 248 days) per case over 5 bars, 0.097 of the coin's usual move (18.32 %); normal drift in its direction +3.17 %, total +4.81 %; 393 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2016_2017/backtests/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d`
Measure: `measure.py`
