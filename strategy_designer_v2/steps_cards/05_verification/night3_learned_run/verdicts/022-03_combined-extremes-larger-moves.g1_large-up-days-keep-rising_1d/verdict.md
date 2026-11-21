---
plan: 022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising_1d
idea: 022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope t of 5-bar excess return on forecast, positive-forecast grid bars: 0.000998008; OLS slope t: 2.36164 (threshold: confirm if t >= 2 with positive forecast-weighted mean excess; reject if t <= -2)
- Supporting check: forecast-weighted mean 5-bar excess return > 0: 0.00882405, passed: True
- Counts: positive-forecast grid cases: 1660
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return is positive.
- Reading: The normal drift is each coin's mean non-overlapping 5-bar grid return over all its windows, the regression pools all coins' positive-forecast grid cases into one OLS, and a grid bar whose 5-bar return would end beyond its window is dropped.
- Size: unusual move -0.26 % per case over 5 bars, -0.027 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.33 %; 3170 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.g1_large-up-days-keep-rising_1d`
Measure: `measure.py`
