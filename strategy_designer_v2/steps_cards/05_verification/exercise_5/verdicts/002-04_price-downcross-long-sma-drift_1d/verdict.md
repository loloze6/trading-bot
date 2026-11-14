---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 20-bar forward return on short bars minus on all bars (pp): -1.75117; Welch t: -0.391872 (threshold: confirm if at most -2 percentage points with t-stat at or below -2; reject if 0 or positive)
- Supporting check: short-bar hit rate minus unconditional share of negative 20-bar returns (points): -0.560224, passed: False
- Counts: non-overlapping short cases: 21, non-overlapping all-bar cases: 34, largest-tertile short cases: 7
- Decided by: Reject rule met: the short hit rate is not above the unconditional share.
- Reading: Short bars are non-overlapping grid bars (positions 0, 20, 40, ... of each window, with a full 20-bar forward return inside the window) whose forecast is below 0, compared with all grid bars of the same windows via Welch t; the largest-tertile shorts are the ceil(n/3) short cases with the most negative forecast, and the fewer-than-15 rule is applied before the confirm and reject rules.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
