---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: extreme minus neutral forward 5-bar return (pooled, non-overlapping): -0.00717955; Welch t: -0.560234 (threshold: extreme-minus-neutral difference positive with Welch t >= 2 and positive in at least 2 of 3 coins confirms; negative with t <= -2 rejects; at least 30 non-overlapping extreme and 30 neutral cases)
- Supporting check: coins where strategy minus buy-and-hold on active bars is positive (need >= 2): 1, passed: False
- Counts: non-overlapping extreme cases: 42, neutral cases: 149, coins with positive difference: 1, coins in record: 2
- Decided by: Inconclusive: t lies between -2 and 2.
- Reading: Extreme bars are grid bars whose forecast is positive and at or above the 80th percentile of all positive forecasts pooled over coins and windows, neutral bars are grid bars with |raw value| <= 4, 'at least 2 of the 3 coins' is applied as at least 2 coins among those present, and the supporting check sums per-bar (position return minus coin return) over active bars per coin.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
