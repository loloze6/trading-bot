---
plan: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h
idea: 016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess forward 72-bar return on forecast (grid bars, forecast > 0): 0.00036524; OLS t of slope: 1.18933 (threshold: confirm if slope t >= 2 with >= 200 cases and forecast-weighted mean excess > 0; reject if t <= -2 with >= 200 cases)
- Supporting check: forecast-weighted mean excess 72-bar return > 0: 0.00379892, passed: True
- Counts: non-overlapping grid bars with forecast > 0: 2254
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation checked on active bars whose 48- and 72-bar lookbacks lie inside the window; the coin's mean 72-bar return is the mean over all its non-overlapping grid bars (positions 0, 72, 144, ...) in all windows, grid bars without a full 72-bar forward return in the window are dropped, and the slope's t is the ordinary OLS t of the slope with an intercept.
- Size: unusual move +0.03 % per case over 72 bars, 0.004 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.44 %; 4636 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-07_up-volume-burst-reversal.g1_efficient-rises-keep-rising_1h`
Measure: `measure.py`
