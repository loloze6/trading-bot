---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: mean 5-bar forward return, extreme minus neutral bars (pooled), t-statistic: 0.2823 (threshold: t >= 2 confirms (with other conditions); t <= 0 rejects; 0 < t < 2 inconclusive)
- Supporting check: strategy return minus exposure-scaled buy-and-hold, summed over coins, before costs: 0.467728, passed: True
- Cases: 51
- Decided by: Inconclusive: t is between 0 and 2.
- Reading: The top-20% cut-off is the 80th percentile of all non-zero forecasts pooled over the record; non-overlapping samples are taken greedily per category inside each window (a bar is used only if it starts at least 5 bars after the previous sample of its category); the t-statistic is Welch's two-sample t; 'positive in at least 2 of the 3 coins' is applied as at least 2 positive coins among those present; the supporting excess per coin is the sum of per-bar strategy gains minus the coin's mean allocation times the sum of its per-bar returns, pooled as the sum over coins; cases counts the non-overlapping extreme samples (neutral samples: 204; diff: 0.0036862440486889678; per-coin: {'BTCUSD': 0.01026187623118349, 'ETHUSD': -0.002194219773633656}).
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
