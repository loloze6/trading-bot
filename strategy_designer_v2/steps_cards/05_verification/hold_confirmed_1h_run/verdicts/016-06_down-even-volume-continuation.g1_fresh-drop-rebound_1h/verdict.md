---
plan: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h
idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 72-bar forward return on forecast (mean_reversion grid bars): 0.000551441; OLS slope t: 2.74545 (threshold: confirm if t >= 2 with the check passing; reject if t <= -2)
- Supporting check: forecast-weighted mean excess 72-bar return > 0: 0.00274667, passed: True
- Counts: grid bars in mean_reversion: 2762, grid bars in mean_reversion with forecast above 0: 1891
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return is above 0.
- Reading: Grid at positions 0, 72, 144, ... of each window with a full 72-bar forward return inside the window; the coin's mean 72-bar return is the mean over all its grid bars across all windows and regimes; the plan's 'fewer cases is inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move -0.25 % per case over 72 bars, -0.030 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.16 %; 4678 cases
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h`
Measure: `measure.py`
