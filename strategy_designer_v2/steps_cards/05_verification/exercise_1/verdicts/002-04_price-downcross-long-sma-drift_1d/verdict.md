---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 20-bar fwd return on short bars minus mean over all bars (pp), sampled every 20 bars: -1.75117 (threshold: confirm at or below -2 pp with t-stat <= -2; reject at 0 or above)
- Supporting check: hit rate short bars minus unconditional negative share (pp): -0.560224, passed: False
- Cases: 21
- Decided by: Reject: the short-bar hit rate is not above the unconditional share.
- Reading: Sampled bars at offsets 0, 20, 40, ... within each window (return to t+20 inside the window), used all sampled bars as the unconditional set and sampled bars with forecast < 0 as short cases; t-stat is the one-sample t of short-bar returns against the unconditional mean (difference / (std of short returns / sqrt(n))); differences are in percentage points; largest-tertile shorts are the short cases with forecast at or below the 1/3 quantile of their forecasts.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
