---
plan: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 72-bar forward return on forecast, active grid bars: 3.16262; OLS slope t: 3.16262 (threshold: confirm if t >= 2 (with check > 0), reject if t <= -2, at least 200 cases)
- Supporting check: mean excess return above median forecast minus below median: 0.00739528, passed: True
- Counts: active grid cases: 2766
- Decided by: The slope's t is 2 or more and the high-minus-low median split is above 0, with at least 200 cases.
- Reading: The coin's mean 72-bar return is the mean of all its non-overlapping grid 72-bar returns over all windows, the regression is OLS with an intercept, and cases exactly at the median forecast are left out of the median split.
- Size: unusual move -0.25 % per case over 72 bars, -0.030 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.17 %; 4793 cases
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h`
Measure: `measure.py`
