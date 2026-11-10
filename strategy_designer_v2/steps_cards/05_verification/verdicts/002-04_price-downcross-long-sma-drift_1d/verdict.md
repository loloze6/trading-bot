---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 20-bar forward return on short bars minus mean over all bars (pp): -1.75117; Welch t: -0.391872 (threshold: confirm if at most -2 percentage points with t-stat at or below -2; reject if 0 or positive)
- Supporting check: short-bar hit rate minus unconditional share of negative 20-bar returns (pp): -0.560224, passed: False
- Counts: non-overlapping short cases: 21, non-overlapping all-bar cases: 34, largest-tertile short cases: 7
- Decided by: The hit rate on short bars is not above the unconditional share of negative 20-bar returns.
- Reading: Short bars are grid bars (positions 0, 20, 40, ... of each window with a full 20-bar forward return inside the window) whose forecast is below 0, the all-bars group is every such grid bar including the short ones, and the largest-tertile shorts are the pooled short cases whose forecast is at or below the 1/3 quantile of the short forecasts (the most negative third).
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
