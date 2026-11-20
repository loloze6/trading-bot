---
plan: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 2-bar return on forecast (Sunday falls): 0.000103137; OLS slope t: 0.285031 (threshold: slope t >= 2 with positive forecast-weighted mean excess 2-bar return confirms; slope t <= -2 rejects; at least 200 cases)
- Supporting check: forecast-weighted mean excess 2-bar return > 0: 0.00333825, passed: True
- Counts: Sunday-fall cases: 1196
- Decided by: The slope's t is between -2 and 2.
- Reading: Sunday is the bar whose UTC start timestamp is a Sunday; the coin's mean 2-bar return is pooled over all its windows on each window's grid of rows 0, 2, 4, ...; the regression is ordinary least squares with an intercept on all pooled cases.
- Size: unusual move +0.34 % per case over 2 bars, 0.055 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.57 %; 1011 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d`
Measure: `measure.py`
