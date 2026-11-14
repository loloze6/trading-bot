---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Evidence:
- Main measure: top-quintile minus neutral mean forward 5-bar return: -0.00147462; Welch t: -0.139197 (threshold: excess return above 0 with t of at least 2, positive in at least 2 of the 3 coins)
- Supporting check: Spearman rank correlation forecast vs forward 5-bar return (positive forecasts): -0.0562873, passed: False
- Counts: pooled non-overlapping top-quintile cases: 77, pooled non-overlapping neutral cases: 129, top-quintile cases BTCUSD: 36, neutral cases BTCUSD: 64, top-quintile cases ETHUSD: 41, neutral cases ETHUSD: 65, coins with positive excess return: 1, coins with non-positive excess return: 1, coins in record: 2
- Decided by: Inconclusive: positive excess return with t below 2, or coins disagree beyond the confirm/reject rules.
- Reading: Top quintile is set per coin as forecast at or above the 80th percentile of that coin's positive forecasts over all its rows and windows; the forward 5-bar returns are taken on the per-window grid 0,5,10,... (as is the supporting correlation); and because only 2 of the plan's 3 coins are in the record, the 'at least 2 coins' rules are applied to the coins present.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
