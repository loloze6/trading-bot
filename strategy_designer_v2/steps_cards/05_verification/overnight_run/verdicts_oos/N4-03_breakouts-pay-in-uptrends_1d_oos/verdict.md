---
plan: N4-03_breakouts-pay-in-uptrends_1d_oos
idea: N4-03_breakouts-pay-in-uptrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean signed 10-bar excess return over holding, |forecast|>=10: 0.00895445; t of the mean: 0.569435 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2)
- Supporting check: per-regime mean: trending excess, mean_reversion negative excess: 0.0149591, passed: False
- Counts: non-overlapping cases: 96, trending cases: 63, mean_reversion cases: 33
- Decided by: Inconclusive: the pooled t lies between -2 and 2.
- Reading: Cases are grid bars 0,10,20,... of each window with |forecast|>=10 and a full in-window 10-bar return; holding is the coin's mean of all in-window 10-bar returns (every bar) pooled over its windows; regimes are split on the `regime` column, the situation is a raw Donchian position > 0, and the supporting check passes when both regime means are positive.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-03_breakouts-pay-in-uptrends_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-03_breakouts-pay-in-uptrends_1d_oos`
Measure: `measure.py`
