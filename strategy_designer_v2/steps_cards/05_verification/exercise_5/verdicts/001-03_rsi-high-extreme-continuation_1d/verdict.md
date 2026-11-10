---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 5-bar forward return, extreme minus neutral bars: -0.000700598; Welch t: -0.0556966 (threshold: positive with t >= 2 to confirm; t <= 0 rejects)
- Supporting check: strategy return minus exposure-scaled buy-and-hold, pooled, before costs: 0.467728, passed: True
- Counts: non-overlapping extreme cases pooled: 42, neutral cases pooled: 180, coins with positive difference: 1, coins present: 2
- Decided by: Rejected: the pooled extreme-minus-neutral difference is zero or negative (t <= 0).
- Reading: Extreme bars are those whose forecast is at or above the 80th percentile of that coin's non-zero forecasts over all its bars and windows, and neutral bars have forecast < 1. Returns are sampled on the grid 0, 5, 10, ... of each window. With only 2 coins present, 'at least 2 of the 3 coins' is read literally as at least 2 coins, so both must be positive. The supporting excess is computed per coin as the sum of bar gains minus the coin's mean allocation times the sum of the coin's bar returns, then summed over coins.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
