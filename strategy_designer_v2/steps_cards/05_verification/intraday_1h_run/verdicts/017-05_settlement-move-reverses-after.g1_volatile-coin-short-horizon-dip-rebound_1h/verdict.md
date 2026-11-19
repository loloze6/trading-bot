---
plan: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h
idea: 017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 2-bar forward return on forecast (mean_reversion grid bars, pooled): 0.000128789; OLS slope t: 13.8026 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 grid bars with forecast > 0)
- Supporting check: mean excess 2-bar return over top quintile of positive forecasts > 0: 0.00211878, passed: True
- Counts: grid bars where forecast > 0: 47568, grid bars in mean_reversion regime: 97120, top-quintile grid bars: 9514
- Decided by: The slope is positive with t >= 2, the top-quintile mean excess return is above 0, and there are at least 300 grid bars with forecast > 0.
- Reading: The coin's mean 2-bar return is taken over the non-overlapping 2-bar grid of all its bars in all windows, the regression is OLS with an intercept, the top quintile is positive-forecast grid bars at or above their 80th percentile, and the regime is read from the recorded `regime` column.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-05_settlement-move-reverses-after.g1_volatile-coin-short-horizon-dip-rebound_1h`
Measure: `measure.py`
