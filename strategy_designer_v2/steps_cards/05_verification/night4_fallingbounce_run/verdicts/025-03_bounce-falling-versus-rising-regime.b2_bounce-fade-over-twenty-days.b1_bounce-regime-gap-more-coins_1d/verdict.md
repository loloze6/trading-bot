---
plan: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d
idea: 025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 20-bar move, trending minus mean_reversion: 0.0442081; Welch t: 2.61922 (threshold: gap > 0 with Welch t >= 2 (confirm, with supporting check); gap < 0 with Welch t <= -2 (reject))
- Supporting check: gap among larger-rise minus gap among smaller-rise cases (median |forecast| split): 0.00511563, passed: True
- Counts: trending cases: 792, mean_reversion cases: 779, larger-rise cases: 785, smaller-rise cases: 786
- Decided by: The gap is positive with Welch t >= 2 and the larger-rise gap exceeds the smaller-rise gap.
- Reading: A case is the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet) in each 20-bar cell of a window counted from its first row, grouped by the bar's recorded regime, its move is the raw 20-bar return minus the coin's drift (not signed by direction, as the main measure states), and the median split puts cases with |forecast| above the median in the larger-rise half.
- Size: unusual move +2.21 % per case over 20 bars, 0.071 of the coin's usual move (25.08 %); normal drift in its direction +0.01 %, total +2.23 %; 1571 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.b2_bounce-fade-over-twenty-days.b1_bounce-regime-gap-more-coins_1d`
Measure: `measure.py`
