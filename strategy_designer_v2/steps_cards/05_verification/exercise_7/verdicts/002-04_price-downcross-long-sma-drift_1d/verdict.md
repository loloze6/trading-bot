---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar forward return on short bars minus on all bars (pp): -1.75117; Welch t: -0.391872 (threshold: Confirm if the difference is <= -2 percentage points with Welch t <= -2; reject if the difference is >= 0)
- Supporting check: short-bar share of negative 20-bar returns minus all-bar share (pp), needs >= 10: -0.560224, passed: False
- Counts: non-overlapping short cases: 21, non-overlapping bars (all): 34
- Decided by: The hit rate on short bars is not above the unconditional share of negative 20-bar returns.
- Reading: Short bars are the 20-bar grid bars (positions 0, 20, 40, ... of each window) with forecast < 0, compared against all grid bars; the largest-tertile shorts are the ceil(n/3) short cases with the most negative forecast; the threshold for 'not above' in the hit rate is a difference of 0 or less; and the minimum count is checked first, then the reject rules, then the confirm rule.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
