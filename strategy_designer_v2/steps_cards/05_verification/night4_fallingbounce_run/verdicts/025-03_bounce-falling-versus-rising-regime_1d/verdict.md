---
plan: 025-03_bounce-falling-versus-rising-regime_1d
idea: 025-03_bounce-falling-versus-rising-regime
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day excess return, long cases minus short cases: 0.00381643; Welch t: 0.946369 (threshold: confirm: difference > 0 with Welch t >= 2 and supporting check passes; reject: difference < 0 with Welch t <= -2)
- Supporting check: larger-|forecast|-half gap minus smaller-half gap: 0.00404712, passed: True
- Counts: long cases: 1481, short cases: 1300
- Decided by: The Welch t lies between -2 and 2.
- Reading: Cases are the first bet (forecast rise of >= 2 points on its side) in each 5-bar grid cell, grouped long/short by the bet's forecast sign; the larger half is |forecast| above the median, the smaller half at or below it; fewer than 30 cases in a group is treated as not observable.
- Size: unusual move +0.17 % per case over 5 bars, 0.017 of the coin's usual move (10.60 %); normal drift in its direction +0.03 %, total +0.20 %; 2781 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime_1d`
Measure: `measure.py`
