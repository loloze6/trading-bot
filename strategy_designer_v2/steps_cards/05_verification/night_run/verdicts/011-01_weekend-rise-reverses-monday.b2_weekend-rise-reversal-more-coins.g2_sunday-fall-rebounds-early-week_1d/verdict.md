---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 2-bar return on forecast, Sunday-fall cases: 0.000283662; OLS slope t: 1.11911 (threshold: confirm: slope > 0 with t >= 2 and mean excess > 0; reject: slope < 0 with t <= -2; at least 300 cases)
- Supporting check: mean excess 2-bar return above 0: 0.00229976, passed: True
- Counts: Sunday-fall cases: 2665
- Decided by: The slope's t lies between -2 and 2.
- Reading: Cases are bars with regime mean_reversion and forecast > 0 whose t+2 close lies in the same window; the coin mean is over non-overlapping 2-bar returns on a grid from each window's first row, pooled over all its windows; the slope's t is the OLS slope over its standard error; fewer than 300 cases is reported as not observable.
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g2_sunday-fall-rebounds-early-week_1d`
Measure: `measure.py`
