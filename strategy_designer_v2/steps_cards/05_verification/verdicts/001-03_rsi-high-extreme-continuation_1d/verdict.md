---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: extreme minus neutral forward 5-bar return, pooled, before costs: -0.00717955; Welch t: -0.560234 (threshold: positive with t >= 2 and positive in at least 2 of 3 coins to confirm; negative with t <= -2 to reject)
- Supporting check: strategy minus buy-and-hold return on non-zero-forecast bars, coins positive: 1, passed: False
- Counts: non-overlapping extreme cases: 42, neutral cases: 149, coins with positive difference: 1, coins with negative difference: 1, coins in record: 2
- Decided by: Inconclusive: t lies between -2 and 2.
- Reading: Extreme bars are grid bars whose forecast is at or above the 80th percentile of all positive forecasts pooled over coins and windows, neutral bars are grid bars with |component value| <= 4, 'at least 2 of the 3 coins' is applied as at least 2 of the coins present (the same count of 2 negative coins is required for a rejection to be supported in more than one coin), and the supporting check sums per-bar strategy and coin returns over each coin's non-zero-forecast bars.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
