---
plan: 002-04_price-cross-below-long-sma_1d
idea: 002-04_price-cross-below-long-sma
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess forward 20-bar return (minus window mean) on forecast, pooled, non-overlapping blocks: -0.00642934; OLS t of slope: -4.28964 (threshold: confirm if slope > 0 with t >= 2 (and supporting share > 50%); reject if slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: share of non-overlapping 20-bar periods with forecast < 0 whose forward return is below the coin's window median: 0.458738, passed: False
- Counts: non-overlapping 20-bar periods with a non-zero forecast: 412, non-overlapping 20-bar periods with forecast below 0: 412, non-overlapping 20-bar periods in the regression: 811
- Decided by: The slope on the forecast is negative with t <= -2, which meets the reject rule (price rises relative to holding the further it sits below the average).
- Reading: I used non-overlapping blocks (bars at positions 0, 20, 40, ... of each window, all forecasts including zero) with an ordinary OLS t, and I took the coin's mean and median 20-bar return in a window over every bar of that window with a complete 20-bar forward return; a positive slope with t >= 2 but a share not above 50% is counted as inconclusive.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-04_price-cross-below-long-sma_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-04_price-cross-below-long-sma_1d`
Measure: `measure.py`
