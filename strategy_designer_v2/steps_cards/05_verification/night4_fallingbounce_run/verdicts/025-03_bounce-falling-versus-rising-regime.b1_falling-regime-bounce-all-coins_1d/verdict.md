---
plan: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d
idea: 025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move, mean_reversion cases minus trending cases: -0.0135727; Welch t: -3.65002 (threshold: confirm at Welch t <= -2 with the supporting check passing; reject at Welch t >= +2)
- Supporting check: same difference on cases with rise reading above pooled median, more negative than main: -0.0173839, passed: True
- Counts: mean_reversion cases: 2285, trending cases: 2519, mean_reversion cases above median rise: 1066, trending cases above median rise: 1336
- Decided by: Welch t <= -2 on the main difference and the above-median difference is more negative.
- Reading: The unusual move is the raw 5-bar return minus the coin's mean 5-bar grid return, not signed by the bet's direction (the plan compares returns across regimes), the case's regime is the bar's recorded regime, the first bet of each 5-bar grid cell is the case, and the plan's 30-case minimum per regime is applied as 'not observable'.
- Size: unusual move +0.68 % per case over 5 bars, 0.051 of the coin's usual move (12.45 %); normal drift in its direction +0.05 %, total +0.73 %; 4804 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.b1_falling-regime-bounce-all-coins_1d`
Measure: `measure.py`
