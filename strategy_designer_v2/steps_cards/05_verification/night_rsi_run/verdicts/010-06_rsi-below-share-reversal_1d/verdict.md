---
plan: 010-06_rsi-below-share-reversal_1d
idea: 010-06_rsi-below-share-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-demeaned forward 14-bar return on forecast (pooled, non-overlapping grid, non-zero forecast): -0.00118394; OLS slope t: -1.6513 (threshold: confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2; at least 100 cases)
- Supporting check: book timing gain before costs (mean daily book return minus position x coin mean daily return): -0.00102943, passed: False
- Counts: non-overlapping cases with a non-zero forecast: 373, active bars: 5694
- Decided by: The slope's t lies between -2 and 2.
- Reading: The coin's mean 14-bar return is the mean over all its non-overlapping grid returns in all windows (any forecast), the regression is OLS with an intercept on the raw forecast, and the book's daily return is the change of postRebalance_total_value per coin averaged across coins per day, with the market part as the previous day's position times the coin's mean daily close return.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-06_rsi-below-share-reversal_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-06_rsi-below-share-reversal_1d`
Measure: `measure.py`
