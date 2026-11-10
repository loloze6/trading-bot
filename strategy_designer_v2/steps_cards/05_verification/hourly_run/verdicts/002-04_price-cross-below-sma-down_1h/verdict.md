---
plan: 002-04_price-cross-below-sma-down_1h
idea: 002-04_price-cross-below-sma-down
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 24-bar excess forward return on forecast, non-overlapping 24-bar blocks pooled: 0.000106768; OLS slope t: 0.655397 (threshold: confirm if slope t >= 2 (with fall share > 50%); reject if slope t <= -2)
- Supporting check: share of forecast<0 bars followed by negative 24-bar excess return, vs 50%: 0.475903, passed: False
- Counts: non-overlapping 24-bar blocks with forecast < 0: 384, non-overlapping 24-bar blocks: 724, bars with forecast < 0: 9109
- Decided by: Slope t lies between -2 and 2: inconclusive.
- Reading: Non-overlapping blocks are the bars at positions 0, 24, 48, ... of each window, pooled over all windows into one OLS with the ordinary slope t; the excess return subtracts the mean 24-bar forward return of all bars of that window; the fall share uses all bars with forecast < 0 (not only grid bars); the block count is the number of grid bars with forecast < 0 and a valid forward return.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-04_price-cross-below-sma-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-04_price-cross-below-sma-down_1h`
Measure: `measure.py`
