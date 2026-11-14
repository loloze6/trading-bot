---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 5-bar forward return, extreme minus neutral bars: -0.000700598; Welch t: -0.0556966 (threshold: positive with t >= 2 confirms; t <= 0 rejects (t <= -2 rejects as reversal); 0 < t < 2 inconclusive)
- Supporting check: strategy minus exposure-scaled buy-and-hold, pooled, before costs: 0.467728, passed: True
- Counts: non-overlapping extreme cases pooled: 42, neutral cases: 180, coins with positive difference: 1, coins in record: 2
- Decided by: The pooled extreme-minus-neutral difference is zero or negative (t <= 0), which rejects.
- Reading: The top-20% cut is the 80th percentile of all non-zero forecasts pooled over every bar of all coins and windows (extreme = forecast >= it), neutral = forecast < 1 including zeros, both sampled on the 0,5,10,... grid of each window; 'at least 2 of the 3 coins' is applied literally as at least 2 positive coins among those present; the supporting excess is, per coin, the summed per-bar strategy gain minus that coin's mean allocation times its summed per-bar return, added over coins; t >= 2 with a failing coin or supporting condition is treated as inconclusive.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
