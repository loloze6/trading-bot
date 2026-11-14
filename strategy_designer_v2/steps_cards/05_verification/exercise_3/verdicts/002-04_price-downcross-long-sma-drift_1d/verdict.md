---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 20-bar forward return on short bars minus on all bars (pp): -1.75117; Welch t: -0.391872 (threshold: confirm if difference <= -2 percentage points with t <= -2; reject if difference >= 0)
- Supporting check: hit rate on short bars minus unconditional share of negative 20-bar returns (pp): -0.560224, passed: False
- Counts: non-overlapping short cases pooled across windows: 21, non-overlapping all-bar cases pooled across windows: 34, largest-tertile short cases: 7, largest-tertile mean forward return: -0.00296375, windows: 6
- Decided by: Reject: the short-bar hit rate is not above the unconditional share.
- Reading: Short bars are grid bars (positions 0, 20, 40, ... of each window) with forecast < 0 compared against all grid bars of the same windows, both groups taking the Welch t, and the 'largest-tertile shorts' are the ceil(n/3) short cases with the most negative forecast; the minimum-count rule is applied before the reject and confirm rules.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
