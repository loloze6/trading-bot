---
plan: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h
idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week
fit: exact
status: confirmed
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 48-bar return minus drift on the Monday 00:00 forecast: 0.000712275; OLS slope t: 4.32347 (threshold: confirm: slope > 0 with t >= 2 over >= 500 cases and supporting mean > 0; reject: slope < 0 with t <= -2 over >= 500 cases)
- Supporting check: mean of forecast sign x (48-bar return - drift): 0.00448367, passed: True
- Counts: cases: 2429
- Decided by: Confirm: the slope is positive with t >= 2 over at least 500 cases and the supporting mean is above 0.
- Reading: Cases are all coin-week bars closing at Monday 00:00 UTC with a recorded forecast and a 48-row forward return inside the window, pooled across coins in one OLS with its ordinary slope t; drift is each coin's mean 48-bar return on the 0,48,96,... grid of all its windows; the supporting mean counts every case, a zero forecast giving 0.
- Size: unusual move +0.47 % per case over 48 bars, 0.077 of the coin's usual move (6.56 %); normal drift in its direction +0.03 %, total +0.50 %; 1875 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week_1h`
Measure: `measure.py`
