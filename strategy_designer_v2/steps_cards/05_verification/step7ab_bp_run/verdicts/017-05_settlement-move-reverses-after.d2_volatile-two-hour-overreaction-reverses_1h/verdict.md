---
plan: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h
idea: 017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 8-bar move of cases, signed in the forecast's direction: 0.00134717; t of the mean: 5.8916 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above minus below median |forecast|: 0.000306701, passed: True
- Counts: independent cases: 22346, cases above median |forecast|: 11173, cases below median |forecast|: 11173
- Decided by: Mean unusual move > 0 with t >= 2, and the supporting check passes.
- Reading: A case is the first bet (forecast rise of >= 2 points on its side from its lowest level since the last bet) in each 8-bar grid cell counted from each window's first row, with its 8-bar return inside the window; normal drift is the coin's mean grid 8-bar return over all its windows; the supporting check splits cases strictly above versus strictly below the median |forecast|; the plan's 'fewer than 100 independent cases' is applied as the minimum count (not observable).
- Size: unusual move +0.13 % per case over 8 bars, 0.048 of the coin's usual move (2.81 %); normal drift in its direction -0.00 %, total +0.13 %; 22346 cases
Plan: `steps_cards/03_test_plan/step7ab_bp_run/plans/017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h.md`
Record: `steps_cards/04_backtest/step7ab_bp_run/backtests/017-05_settlement-move-reverses-after.d2_volatile-two-hour-overreaction-reverses_1h`
Measure: `measure.py`
