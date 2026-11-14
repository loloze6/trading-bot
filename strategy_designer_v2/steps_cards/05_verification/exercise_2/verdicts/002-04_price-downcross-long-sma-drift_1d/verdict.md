---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 20-bar forward return on short bars minus on all bars (pp): -1.75117 (threshold: confirm at or below -2 percentage points with t-stat at or below -2; reject at 0 or above)
- Supporting check: short-bar negative-return hit rate minus unconditional share (pp): -0.560224, passed: False
- Cases: 21
- Decided by: Reject: the short-bar hit rate is not above the unconditional share.
- Reading: Bars are sampled at every 20th row from each window's first row (only where the return fits in the window). The t-stat is the one-sample t of short-bar returns against the pooled all-bar mean. The largest-tertile shorts are the sampled short bars with forecast at or below the 1/3 quantile of short forecasts. Any reject condition takes precedence over confirm.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
