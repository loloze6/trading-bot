---
plan: 002-04_price-downcross-long-sma-drift_1d
idea: 002-04_price-downcross-long-sma-drift
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess forward 10-bar log return on forecast, short-bar non-overlapping blocks: -0.000745799; OLS slope t: -0.241659 (threshold: slope t >= +2 (with mean excess < 0 and higher decline share) confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: decline share on short blocks minus decline share on all blocks: 0.00265781, passed: True
- Counts: non-overlapping 10-bar blocks with forecast < 0: 43, non-overlapping 10-bar blocks, all: 70
- Decided by: Slope t-statistic lies between -2 and +2, which the plan defines as inconclusive.
- Reading: Situation taken as raw SMA200 distance < 0 with forecast < 0; baseline is the mean forward 10-bar log return over every bar with a valid in-window forward return; short blocks are grid bars (positions 0,10,20,... per window) with forecast < 0 and the regression uses forecast as x; the plan's minimum of 15 short blocks is applied as 'not observable'.
Plan: `steps_cards/03_test_plan/plans/002-04_price-downcross-long-sma-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-downcross-long-sma-drift_1d`
Measure: `measure.py`
