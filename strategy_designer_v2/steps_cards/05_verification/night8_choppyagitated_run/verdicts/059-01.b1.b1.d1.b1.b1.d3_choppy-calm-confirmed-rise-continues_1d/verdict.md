---
plan: 059-01.b1.b1.d1.b1.b1.d3_choppy-calm-confirmed-rise-continues_1d
idea: 059-01.b1.b1.d1.b1.b1.d3_choppy-calm-confirmed-rise-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 7-bar forward return on forecast (grid cases, forecast > 0): 0.00360668; OLS slope t: 3.07315 (threshold: confirm if t >= 2 (with mean excess > 0), reject if t <= -2, on at least 100 independent grid cases)
- Supporting check: mean excess 7-bar forward return over the same grid cases > 0: -0.00875301, passed: False
- Counts: independent grid cases: 404
- Decided by: Slope t is 2 or more but the mean excess 7-bar return is at or below 0 (a confirming slope with a failed supporting check).
- Reading: Grid bars are positions 0, 7, 14, ... of each window with a full 7-bar forward return inside the window, the coin's mean 7-bar return is the mean over all such grid bars of all its windows, and the profile part of the situation is read from the detector's 'regime' column since its components are not recorded.
- Size: unusual move -0.33 % (t -0.55, the cases of one day together: 491 days) per case over 7 bars, -0.032 of the coin's usual move (12.84 %); normal drift in its direction +0.97 %, total +0.64 %; 755 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b1.d3_choppy-calm-confirmed-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d3_choppy-calm-confirmed-rise-continues_1d`
Measure: `measure.py`
