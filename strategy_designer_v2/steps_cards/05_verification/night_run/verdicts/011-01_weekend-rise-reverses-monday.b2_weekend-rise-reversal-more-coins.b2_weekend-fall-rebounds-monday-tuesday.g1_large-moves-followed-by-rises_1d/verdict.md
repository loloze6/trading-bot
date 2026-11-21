---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess next-2-bar return on forecast: 0.000348647; OLS slope t: 4.02028 (threshold: slope > 0 with t >= 2 (confirm, with supporting check); slope < 0 with t <= -2 (reject))
- Supporting check: mean excess 2-bar return in top fifth of forecast > 0: 0.00411801, passed: True
- Counts: non-overlapping cases: 18386, cases in the top fifth: 3678
- Decided by: The slope is positive with t >= 2 and the top-fifth mean excess return is above 0.
- Reading: The coin's mean 2-bar return is the mean of its non-overlapping grid returns over all its windows; the OLS has an intercept; the top fifth is grid bars with forecast at or above the pooled 80th percentile of grid forecasts; the situation is a nonzero component value (or nonzero 1-day price move where it is not recorded) with a positive forecast.
- Size: unusual move +0.18 % per case over 2 bars, 0.020 of the coin's usual move (7.48 %); normal drift in its direction +0.30 %, total +0.48 %; 11406 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_large-moves-followed-by-rises_1d`
Measure: `measure.py`
