---
plan: 003-01_thin-volume-rise-reverses_1d
idea: 003-01_thin-volume-rise-reverses
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of -forecast/10 x (coin 5-bar return minus coin mean 5-bar return), active grid bars: -0.00141715; ordinary t of the mean: -0.301137 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; < 100 active grid cases not observable)
- Supporting check: mean excess 5-bar return of the 20% most negative-forecast active grid bars below 0: -0.00221344, passed: True
- Counts: active grid cases: 999, top 20% cases: 200
- Decided by: The main measure's t is strictly between -2 and 2.
- Reading: The coin's mean 5-bar return is the mean over all its non-overlapping grid bars (positions 0,5,10,... with a full 5-bar return inside the window) in all windows, the top 20% is the ceiling of 0.2 x the active grid cases ranked by most negative forecast, and the plan's 'fewer than 100 active grid cases' is applied as the minimum count giving 'not observable'.
Plan: `steps_cards/03_test_plan/night_run/plans/003-01_thin-volume-rise-reverses_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/003-01_thin-volume-rise-reverses_1d`
Measure: `measure.py`
