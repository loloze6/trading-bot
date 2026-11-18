---
plan: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
idea: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of OLS slope of excess 10-bar forward return on forecast (forecast > 0 grid samples): 1.79402; OLS slope t: 1.79402 (threshold: confirm if slope t >= +2 on >= 30 cases and mean excess > 0; reject if slope t <= -2 on >= 30 cases; else inconclusive)
- Supporting check: mean excess 10-bar return over forecast > 0 samples above 0: 0.0643077, passed: True
- Counts: forecast > 0 grid samples: 108
- Decided by: The slope's t lies between -2 and +2.
- Reading: The coin's mean 10-bar return is the mean of all its non-overlapping 10-bar grid returns over all windows (not only forecast > 0 samples), the slope t is the ordinary OLS t with intercept, and the situation is read from the raw component value > 0 (price-based prior 20-bar high where it is missing).
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d`
Measure: `measure.py`
