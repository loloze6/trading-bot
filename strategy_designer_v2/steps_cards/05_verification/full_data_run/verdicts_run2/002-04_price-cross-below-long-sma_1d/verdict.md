---
plan: 002-04_price-cross-below-long-sma_1d
idea: 002-04_price-cross-below-long-sma
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess forward 20-bar return (minus coin-window mean 20-bar return) on forecast, pooled, non-overlapping 20-bar blocks: -0.00642934; OLS t of slope (non-overlapping 20-bar blocks): -4.28964 (threshold: confirm if slope > 0 with t >= 2 (and supporting share > 50%); reject if slope < 0 with t <= -2; inconclusive otherwise or if fewer than 30 non-overlapping 20-bar periods with non-zero forecast)
- Supporting check: share of non-overlapping 20-bar short periods with forward return below coin-window median 20-bar return: 0.458738, passed: False
- Counts: non-overlapping 20-bar periods with non-zero forecast: 412, non-overlapping 20-bar periods with forecast below 0: 412, non-overlapping 20-bar periods in regression: 811
- Decided by: The slope on the forecast is negative with t <= -2: price rises relative to holding the further below the average.
- Reading: The regression uses all bars (including zero forecast) on the 0, 20, 40, ... grid of each window, with the coin's mean and median 20-bar return taken over all overlapping forward returns in that window, and a supporting share not above 50% blocks confirmation.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-04_price-cross-below-long-sma_1d`
Measure: `measure.py`
