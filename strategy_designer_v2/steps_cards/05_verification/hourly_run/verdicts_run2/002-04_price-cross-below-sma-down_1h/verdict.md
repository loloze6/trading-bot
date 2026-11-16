---
plan: 002-04_price-cross-below-sma-down_1h
idea: 002-04_price-cross-below-sma-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 24-bar excess forward return on forecast: 0.000106768; OLS slope t (non-overlapping 24-bar blocks): 0.655397 (threshold: slope t >= 2 confirms (with fall share > 50%), t <= -2 rejects)
- Supporting check: share of forecast<0 blocks followed by negative 24-bar excess return (> 50%): 0.458333, passed: False
- Counts: non-overlapping 24-bar blocks with forecast < 0: 384, non-overlapping 24-bar blocks: 724
- Decided by: Inconclusive: slope t between -2 and 2.
- Reading: Used non-overlapping 24-bar blocks (bars 0, 24, 48, ... of each window) pooled across all coins and windows with a plain OLS slope t-stat of excess return on forecast (all grid bars, zero forecasts included), the excess taken against the mean 24-bar forward return of all bars of the same window, and the 200-block minimum applied before the confirm/reject rules.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-04_price-cross-below-sma-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-04_price-cross-below-sma-down_1h`
Measure: `measure.py`
