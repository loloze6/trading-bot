---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 20-bar forward return on short bars minus on all bars (pp): -1.75117; Welch t: -0.391872 (threshold: confirm if at most -2 percentage points with t at or below -2; reject if 0 or positive)
- Supporting check: hit rate of negative 20-bar returns, short bars minus all bars (pp): -0.560224, passed: False
- Counts: non-overlapping short cases: 21, non-overlapping all bars: 34, largest-tertile short cases: 7, largest-tertile mean forward return (pp): -0.296375, short-bar hit rate: 0.52381, all-bar hit rate: 0.529412
- Decided by: Reject: the short-bar hit rate is not above the unconditional share.
- Reading: Short bars are grid bars (positions 0, 20, 40, ... of each window, with a full 20-bar forward return inside the window) whose forecast is below 0, compared against all grid bars of the same windows, and the largest-tertile shorts are the ceil(n/3) short cases with the most negative forecast.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
