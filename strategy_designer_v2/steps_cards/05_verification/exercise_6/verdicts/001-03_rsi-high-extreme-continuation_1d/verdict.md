---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 5-bar forward return, extreme minus neutral bars, pooled: -0.000700598; Welch t: -0.0556966 (threshold: positive with t >= 2 confirms (with >= 2 of 3 coins positive and positive pooled support); t <= 0 rejects)
- Supporting check: strategy return minus exposure-scaled buy-and-hold, summed over coins: 0.467728, passed: True
- Counts: non-overlapping extreme cases: 42, neutral cases: 180, coins with positive difference: 1, coins: 2
- Decided by: Rejected: the pooled extreme-minus-neutral difference is zero or negative (t = -0.06 <= 0).
- Reading: Extreme bars are those whose forecast is at or above the 80th percentile of all non-zero forecasts pooled over every bar of every coin and window, and neutral bars are those whose forecast is below 1, both taken on the 0,5,10,... grid of each window. With only the coins present in the record, the rule 'positive in at least 2 of the 3 coins' is applied as at least 2 positive coins. The supporting excess is computed per coin as the sum of per-bar gains (allocation x next-bar return) minus the mean allocation times the sum of the coin's per-bar returns, all inside each window, and these per-coin excesses are summed to give the pooled value.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
