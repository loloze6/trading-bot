---
plan: 001-03_rsi-high-extreme-continuation-up_1h
idea: 001-03_rsi-high-extreme-continuation-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: 6-bar forward return after top-decile forecast minus after neutral RSI (45-55): -0.000696049; Welch t: -1.03761 (threshold: difference > 0 with t >= 2 to confirm; difference < 0 with t <= -2 to reject)
- Supporting check: coins with positive top-decile excess over unconditional mean 6-bar return: 0, passed: False
- Counts: top-decile cases: 782, neutral cases: 1998, coins with positive excess: 0, coins: 2
- Decided by: Inconclusive: the t-statistic lies strictly between -2 and 2.
- Reading: Top decile is forecast at or above the 90th percentile of all forecast values pooled over coins, windows and bars (and strictly positive), neutral is raw component in [-2, 2], the supporting check uses the same non-overlapping grid with the unconditional mean over all grid bars of the coin, and '2 of the 3 coins' is read as at least 2 coins positive among the coins present.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-03_rsi-high-extreme-continuation-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-03_rsi-high-extreme-continuation-up_1h`
Measure: `measure.py`
