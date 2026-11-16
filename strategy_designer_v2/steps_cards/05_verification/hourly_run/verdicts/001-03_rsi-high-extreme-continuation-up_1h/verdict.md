---
plan: 001-03_rsi-high-extreme-continuation-up_1h
idea: 001-03_rsi-high-extreme-continuation-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: 6-bar return after top-decile forecast bars minus after neutral RSI (45-55) bars: -0.000696049; Welch t: -1.03761 (threshold: difference > 0 with t >= 2 to confirm; difference < 0 with t <= -2 to reject)
- Supporting check: coins with positive top-decile excess over unconditional 6-bar mean: 0, passed: False
- Counts: top_decile_cases: 782, neutral_cases: 1998, coins: 2
- Decided by: The t-statistic lies strictly between -2 and 2, so the plan rules the test inconclusive.
- Reading: Top decile is forecast >= the 90th percentile of all forecast values pooled over coins and windows (and > 0), cases and the unconditional mean use the non-overlapping 6-bar grid from each window's first row, neutral is raw value in [-2, 2] inclusive, and with only 2 coins in the record the '2 of 3 coins' rule requires both coins positive.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-03_rsi-high-extreme-continuation-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-03_rsi-high-extreme-continuation-up_1h`
Measure: `measure.py`
