---
plan: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d
idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess Sunday-to-Wednesday 3-bar return on forecast: 0.00136272; OLS slope t: 4.21733 (threshold: t >= 2 with a positive supporting check confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: forecast-weighted mean excess 3-bar return of Sunday bars with forecast > 0: 0.00856287, passed: True
- Counts: Sunday bars with forecast > 0: 1176, Sunday bars in total: 2441
- Decided by: The slope's t is 2 or more and the forecast-weighted mean excess return of Sunday bars with forecast > 0 is positive.
- Reading: Sunday bars for the measure are the bars with regime 'trending' that have a full 3-bar return inside their window, the coin mean is over the non-overlapping 3-bar grid of all its windows, the regression includes zero-forecast Sunday bars, and the situation check takes Sunday as a bar starting on Sunday UTC with a negative raw wkd_fall value and a positive forecast.
- Size: unusual move +0.70 % per case over 3 bars, 0.093 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +1.05 %; 994 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week_1d`
Measure: `measure.py`
