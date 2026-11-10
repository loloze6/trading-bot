---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 5-bar fwd return after extreme minus after neutral bars (pooled): -0.000700598 (threshold: positive with t-statistic >= 2 (reject if t <= 0))
- Supporting check: strategy return minus exposure-scaled buy-and-hold, pooled over coins: 0.467728, passed: True
- Cases: 42
- Decided by: Rejected: pooled extreme-minus-neutral difference is zero or negative (t <= 0). (t=-0.05569658268715827, extreme n=42, neutral n=180, coins positive=1/2)
- Reading: Non-overlapping returns are taken on a fixed grid t=0,5,10,... within each window; the top-20% cut-off is the 80th percentile of non-zero forecasts pooled over all coins and windows; t is Welch's two-sample t; with only 2 coins present the 'at least 2 of 3 coins' rule requires both positive; the supporting excess sums per-bar returns with exposure = mean allocation per coin, and 'cases' counts the non-overlapping extreme cases.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
