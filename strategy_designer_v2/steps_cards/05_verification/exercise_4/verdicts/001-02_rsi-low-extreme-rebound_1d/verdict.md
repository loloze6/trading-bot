---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: pooled fwd 5-bar return, top-quintile forecast minus zero forecast: -0.00147462; Welch t: -0.139197 (threshold: excess > 0 with t >= 2 and positive in at least 2 of 3 coins to confirm; excess <= 0 and non-positive in at least 2 coins to reject)
- Supporting check: Spearman rank corr of forecast vs fwd 5-bar return (positive forecasts): -0.0562873, passed: False
- Counts: non-overlapping top-quintile cases pooled: 77, top-quintile cases BTCUSD: 36, top-quintile cases ETHUSD: 41, non-overlapping neutral cases pooled: 129, coins with positive excess: 1, coins with non-positive excess: 1, coins in record: 2
- Decided by: Inconclusive: the coins disagree beyond the confirm and reject rules.
- Reading: The top-quintile cut-off is the 80th percentile of all positive forecasts, pooled across coins and windows (bars at or above it count); samples are the grid bars 0, 5, 10, ... of each window; the Spearman check uses the same grid; and since only 2 coins are in the record, the 'at least 2 of the 3 coins' counts are applied literally to the coins present.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
