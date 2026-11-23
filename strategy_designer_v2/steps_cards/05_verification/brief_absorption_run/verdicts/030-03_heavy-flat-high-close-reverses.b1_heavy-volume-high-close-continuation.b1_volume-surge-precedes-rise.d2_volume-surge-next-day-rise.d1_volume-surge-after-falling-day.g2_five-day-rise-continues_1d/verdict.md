---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 3-bar excess forward return on rise5 forecast (grid cases with forecast > 0): 0.00064224; OLS t of the slope: 2.82267 (threshold: confirm: slope > 0 with t >= 2.0 and supporting check passes; reject: slope < 0 with t <= -2.0)
- Supporting check: forecast-weighted mean excess 3-bar return > 0: 0.00552988, passed: True
- Counts: grid cases with a positive forecast: 2850
- Decided by: The slope is positive with t >= 2.0 and the forecast-weighted mean excess return is above 0.
- Reading: Grid cases are bars at positions 0, 3, 6, ... of each window with forecast > 0 and a 3-bar forward return inside the window; the drift is the coin's mean 3-bar return on that grid over all its windows; the slope is an OLS regression with intercept, t = slope / its standard error.
- Size: unusual move +0.24 % per case over 3 bars, 0.029 of the coin's usual move (7.96 %); normal drift in its direction +0.39 %, total +0.63 %; 2607 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g2_five-day-rise-continues_1d`
Measure: `measure.py`
