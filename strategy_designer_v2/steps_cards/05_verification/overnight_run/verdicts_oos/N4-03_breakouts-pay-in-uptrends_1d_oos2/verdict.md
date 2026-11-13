---
plan: N4-03_breakouts-pay-in-uptrends_1d_oos2
idea: N4-03_breakouts-pay-in-uptrends
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean of sign(forecast) x (10-bar forward return - coin holding mean) on |forecast|>=10, non-overlapping: 0.167799; t of the mean: 1.27225 (threshold: confirm if mean > 0 and t >= 2; reject if mean < 0 and t <= -2; else inconclusive; needs >= 30 cases pooled and >= 10 per regime)
- Supporting check: per-regime signed excess return: trending mean=0.208191 t=1.313; mean_reversion mean=-0.024064 t=-0.528; value = smaller t: -0.528248, passed: False
- Counts: non-overlapping cases: 23, trending cases: 19, mean_reversion cases: 4
- Decided by: Fewer than 30 non-overlapping cases in the pool.
- Reading: Holding is each coin's mean of all overlapping 10-bar forward returns across its windows. Cases are the window-grid bars 0, 10, 20, ... with |forecast| >= 10 and a full 10-bar return inside the window, split by the recorded regime label. The supporting check passes when both regimes have a positive mean and is not part of the decision.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-03_breakouts-pay-in-uptrends_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-03_breakouts-pay-in-uptrends_1d_oos2`
Measure: `measure.py`
