---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess forward 10-bar log return on forecast, short-bar non-overlapping blocks: -0.000745799; OLS slope t: -0.241659 (threshold: slope t >= +2 confirms (with mean excess < 0 and higher decline share); t <= -2 rejects; else inconclusive; < 15 short blocks inconclusive)
- Supporting check: share of negative 10-bar returns: short blocks minus all blocks: 0.00265781, passed: True
- Counts: non-overlapping 10-bar blocks with forecast < 0: 43, all non-overlapping 10-bar blocks: 70
- Decided by: The slope t-statistic lies between -2 and +2, which the plan calls inconclusive.
- Reading: The baseline is the mean forward 10-bar log return over every bar with a full in-window forward return, the regression and the shares use the per-window grid at positions 0, 10, 20, ..., the slope t is the OLS slope over its standard error, the mean excess in the confirm rule is taken on the short grid blocks, and a t >= +2 that fails the other confirm conditions is treated as inconclusive.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
