---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess forward 10-bar log return on forecast (short bars, non-overlapping blocks): -0.000745799; OLS slope t: -0.241659 (threshold: slope t >= +2 (with mean excess < 0 and higher decline share) confirms; slope t <= -2 rejects)
- Supporting check: decline share on short blocks minus decline share on all blocks: 0.00265781, passed: True
- Counts: non-overlapping 10-bar blocks with forecast < 0: 43, non-overlapping 10-bar blocks, all: 70
- Decided by: Slope t-statistic lies between -2 and +2.
- Reading: The baseline is the mean forward 10-bar log return over every tested bar with a within-window forward return, blocks are rows 0, 10, 20, ... of each window, the slope is OLS of excess log return on the forecast with its ordinary t, and the mean excess in the confirm rule is taken over the short blocks.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
