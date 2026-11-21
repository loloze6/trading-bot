---
plan: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d
idea: 022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of demeaned 5-bar forward return on forecast, pooled 5-bar grid: 0.00025312; OLS slope t: 1.45927 (threshold: confirm if t >= 2 (with the supporting check), reject if t <= -2, otherwise inconclusive)
- Supporting check: book mean daily return minus market-rise gain: -0.000123112, passed: False
- Counts: grid cases with a non-zero forecast: 3416, grid cases: 3419
- Decided by: The slope's t lies between -2 and 2.
- Reading: The regression is OLS with an intercept on every grid bar with a full 5-bar forward return, zero forecasts included; the coin's mean 5-bar return is the mean of its grid returns over all windows; the book's daily return is the change in postRebalance_total_value per coin, averaged across coins each day, and its market gain is the previous bar's allocation times the coin's mean daily return.
- Size: unusual move +0.18 % per case over 5 bars, 0.015 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.17 %; 3399 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.d2_daily-move-continues-five-days_1d`
Measure: `measure.py`
