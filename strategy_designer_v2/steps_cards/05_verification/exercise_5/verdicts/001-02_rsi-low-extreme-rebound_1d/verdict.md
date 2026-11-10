---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: Top-quintile minus zero-forecast mean forward 5-bar return (non-overlapping, pooled): -0.00147462; Welch t: -0.139197 (threshold: excess > 0 with t >= 2 and positive in at least 2 of the coins to confirm; <= 0 and non-positive in at least 2 coins to reject)
- Supporting check: Spearman rank correlation of forecast vs forward 5-bar return on positive-forecast bars: -0.0562873, passed: False
- Counts: non-overlapping top-quintile cases pooled: 77, non-overlapping zero-forecast cases pooled: 129, coins: 2, coins with positive excess: 1, coins with non-positive excess: 1, non-overlapping top-quintile cases BTCUSD: 36, non-overlapping top-quintile cases ETHUSD: 41
- Decided by: Inconclusive: coins disagree beyond the confirm/reject rules.
- Reading: The top-quintile cut-off is the 80th percentile of all positive forecasts pooled across coins and windows, both groups and the Spearman check use the bars at positions 0,5,10,... of each window, and since only 2 coins are in the record the 'at least 2 of the 3 coins' rules are applied as at least 2 of the coins present and the per-coin minimum of 8 to each coin present.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
