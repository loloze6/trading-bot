---
plan: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x 72-bar excess forward return on positive-forecast grid bars: 0.00270066; t of the mean: 1.41194 (threshold: confirm if t >= 2 with OLS slope > 0; reject if t <= -2; otherwise inconclusive)
- Supporting check: OLS slope of excess 72-bar forward return on forecast: 0.00032429, passed: True
- Counts: positive-forecast grid cases across all coins and windows: 2916
- Decided by: The main measure's t lies between -2 and 2 (inconclusive rule).
- Reading: The coin's mean 72-bar return is the mean over all non-overlapping grid returns of all its windows (not only positive-forecast bars), and the situation check leaves out bars whose 72-bar return cannot be computed inside their window.
- Size: unusual move -0.13 % per case over 72 bars, -0.016 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.28 %; 4912 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h`
Measure: `measure.py`
