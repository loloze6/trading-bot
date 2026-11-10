---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: forward 5-bar return, top-quintile forecast minus zero-forecast bars: -0.00147462; Welch t: -0.139197 (threshold: excess above 0 with t >= 2 and positive in at least 2 of the 3 coins)
- Supporting check: Spearman rank correlation of forecast vs forward 5-bar return on positive-forecast bars: -0.0562873, passed: False
- Counts: pooled non-overlapping top-quintile cases: 77, top-quintile cases BTCUSD: 36, top-quintile cases ETHUSD: 41, neutral (forecast 0) cases: 129, coins with positive excess return: 1, coins with non-positive excess return: 1, coins in record: 2
- Decided by: Inconclusive: positive excess return with t below 2, or coins disagree beyond the confirm/reject rules.
- Reading: The top quintile is cut at the 80th percentile of all positive forecasts pooled across coins and windows, the supporting check uses the same non-overlapping grid, and with only 2 coins in the record the 'at least 2 of the 3 coins' rules are applied to the coins present.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
