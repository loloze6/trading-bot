---
plan: 001-02_rsi-low-extreme-rebound_1d
idea: 001-02_rsi-low-extreme-rebound
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: top-quintile forecast fwd 5-bar return minus flat-bar fwd 5-bar return: -0.00147462; Welch t: -0.139197 (threshold: excess above 0 with t >= 2 and positive in at least 2 of the coins)
- Supporting check: Spearman rank correlation of forecast vs fwd 5-bar return on positive-forecast bars: -0.0562873, passed: False
- Counts: pooled non-overlapping top-quintile cases: 77, non-overlapping flat cases: 129, coins with positive excess: 1, coins with non-positive excess: 1, top-quintile cases BTCUSD: 36, top-quintile cases ETHUSD: 41
- Decided by: Inconclusive: the excess return is positive with a t below 2, or the coins disagree beyond the confirm and reject rules.
- Reading: The top quintile is the forecast at or above the 80th percentile of all positive forecasts, pooled over coins and windows; samples (also for the Spearman check) are the bars at positions 0, 5, 10, ... of each window; and since only BTC and ETH ran, 'at least 2 of the 3 coins' and the 8-per-coin minimum are applied to the coins present.
Plan: `steps_cards/03_test_plan/plans/001-02_rsi-low-extreme-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/001-02_rsi-low-extreme-rebound_1d`
Measure: `measure.py`
