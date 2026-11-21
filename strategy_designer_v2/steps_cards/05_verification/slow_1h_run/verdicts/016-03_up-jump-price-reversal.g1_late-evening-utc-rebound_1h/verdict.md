---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x 2-bar excess return on 19:00 UTC decision bars: 0.00623997; ordinary t: 5.27297 (threshold: confirm if positive with t >= 2 (and supporting difference > 0); reject if negative with t <= -2)
- Supporting check: mean excess return, top fifth of positive forecasts minus zero forecasts: 0.00119329, passed: True
- Counts: decision bars with a forecast above 0: 8652, decision bars: 17404, top-fifth decision bars: 1731, zero-forecast decision bars: 8752
- Decided by: The forecast-weighted mean excess return is positive with t >= 2 and the top-fifth minus zero difference is above 0.
- Reading: The coin's mean 2-bar return is taken on the workflow's non-overlapping grid (positions 0, 2, 4, ... of each window) pooled over all windows, the mean of forecast x excess uses all decision bars including zero forecasts, and the top fifth is the positive decision-bar forecasts at or above their pooled 80th percentile.
- Size: unusual move +0.12 % per case over 2 bars, 0.088 of the coin's usual move (1.47 %); normal drift in its direction +0.01 %, total +0.14 %; 9200 cases
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h`
Measure: `measure.py`
