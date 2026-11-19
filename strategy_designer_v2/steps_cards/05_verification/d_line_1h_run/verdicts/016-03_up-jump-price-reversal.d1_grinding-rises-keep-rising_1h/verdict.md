---
plan: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 72-bar excess forward return on the forecast: -0.000325995; OLS slope t: -0.650931 (threshold: confirm if t >= 2 with forecast-weighted mean excess > 0; reject if t <= -2)
- Supporting check: forecast-weighted mean excess 72-bar forward return > 0: 0.00804094, passed: True
- Counts: independent grid cases with forecast > 0: 947
- Decided by: The slope's t lies between -2 and 2.
- Reading: Grid is positions 0, 72, 144, ... of each window from its first row; the coin's mean 72-bar return is the mean over that grid in all of the coin's windows; the slope's t is the ordinary OLS t with an intercept; and a count below the plan's minimum of 100 is reported as not observable, as the workflow requires.
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h`
Measure: `measure.py`
