---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forward 5-bar return after extreme bars minus after neutral bars (pooled, before costs): -0.00717955; Welch t: -0.560234 (threshold: positive with t >= 2 and positive in at least 2 of the coins to confirm; negative with t <= -2 to reject)
- Supporting check: coins where strategy minus buy-and-hold return on non-zero-forecast bars is positive: 1, passed: False
- Counts: non-overlapping extreme cases: 42, neutral cases: 149, coins with positive difference: 1, coins: 2
- Decided by: Inconclusive rule met: t lies between -2 and 2.
- Reading: The top 20% cut-off is the 80th percentile of all positive forecasts pooled over coins and windows (extreme = forecast at or above it), neutral bars have |raw value| <= 4, both groups are then taken on the 0,5,10,... grid of each window, the 'at least 2 of the 3 coins' rules are applied as at least 2 of the coins present, and the supporting check is reported but not used in the decision since the confirm rule does not name it.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
