---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 10-bar excess log return on forecast, short-bar blocks: -0.000745799; OLS slope t: -0.241659 (threshold: confirm if slope t >= +2 with mean excess on short blocks < 0 and decline share higher than on all blocks; reject if slope t <= -2; otherwise inconclusive; inconclusive if fewer than 15 non-overlapping short blocks)
- Supporting check: share of negative 10-bar returns, short blocks minus all blocks: 0.00265781, passed: True
- Counts: non-overlapping 10-bar blocks with forecast < 0: 43, non-overlapping 10-bar blocks, all bars: 70
- Decided by: Slope t-statistic -0.24 lies between -2 and +2: inconclusive.
- Reading: Blocks start at rows 0, 10, 20, ... of each window with the forecast read at the block's first bar, the buy-and-hold baseline is the mean forward 10-bar log return over all blocks on that same grid, and the component's raw column is found by its last_history_value name since the record calls it below_sma200 rather than below_ma.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
