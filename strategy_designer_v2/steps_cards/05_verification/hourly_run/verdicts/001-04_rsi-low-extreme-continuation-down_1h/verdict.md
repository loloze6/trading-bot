---
plan: 001-04_rsi-low-extreme-continuation-down_1h
idea: 001-04_rsi-low-extreme-continuation-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean fwd 24-bar return, most-short decile minus zero-forecast bars: -0.000357322; Newey-West t (24 lags): -0.276843 (threshold: confirm if negative with t <= -2 and negative in at least 2 of 3 coins; reject if positive with t >= +2)
- Supporting check: HAC slope of demeaned fwd 24-bar return on forecast (must be positive): 1.9859e-05, passed: True
- Counts: non-overlapping extreme episodes BTCUSD: 193, non-overlapping extreme episodes ETHUSD: 200, non-overlapping extreme episodes pooled: 393, coins: 2, coins with negative difference: 1, coins with positive difference: 1
- Decided by: |t| < 2 or the coins split in sign, which the plan calls inconclusive.
- Reading: The most-short decile is the 10% most negative forecasts among all negative-forecast bars pooled over coins and windows, neutral bars are forecast == 0, the Newey-West t is the HAC t of the extreme-dummy slope with lags kept within each coin-window, 'at least 2 of the 3 coins' and 'matching strength' are both applied as at least 2 coins of those present having the difference's sign, and the episode minimums apply to each coin present.
Plan: `steps_cards/03_test_plan/hourly_run/plans/001-04_rsi-low-extreme-continuation-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/001-04_rsi-low-extreme-continuation-down_1h`
Measure: `measure.py`
