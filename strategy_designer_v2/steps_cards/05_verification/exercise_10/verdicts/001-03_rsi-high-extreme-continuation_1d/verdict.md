---
plan: 001-03_rsi-high-extreme-continuation_1d
idea: 001-03_rsi-high-extreme-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled forward 5-bar return after extreme bars minus after neutral bars: -0.00717955; Welch t: -0.560234 (threshold: confirm if positive with t >= 2 and positive in at least 2 of the coins; reject if negative with t <= -2)
- Supporting check: coins where strategy minus buy-and-hold return on non-zero-forecast bars is positive: 1, passed: False
- Counts: non-overlapping extreme cases: 42, neutral cases: 149, coins with positive difference: 1, coins in record: 2
- Decided by: Inconclusive rule met: t lies between -2 and 2.
- Reading: Extreme bars are grid bars whose forecast is at or above the 80th percentile of all positive forecasts pooled over coins and windows, neutral bars are grid bars with |raw RSI component| <= 4, the 'at least 2 of the 3 coins' rules are applied as at least 2 of the coins present (only 2 are in the record), per-coin support uses each coin's extreme-minus-neutral difference, and the supporting check sums per-bar returns and is reported without entering the decision.
Plan: `steps_cards/03_test_plan/plans/001-03_rsi-high-extreme-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-03_rsi-high-extreme-continuation_1d`
Measure: `measure.py`
