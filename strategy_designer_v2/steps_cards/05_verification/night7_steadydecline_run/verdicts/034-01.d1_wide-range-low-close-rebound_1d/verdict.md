---
plan: 034-01.d1_wide-range-low-close-rebound_1d
idea: 034-01.d1_wide-range-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (agitated, forecast > 0): 0.000624062; OLS t, errors clustered by day: 3.69206 (threshold: positive with t >= 2 (and top-quintile mean > 0) confirms; negative with t <= -2 rejects)
- Supporting check: mean next-day excess return of top-quintile forecasts (agitated bars): 0.00728292, passed: True
- Counts: agitated bars with forecast > 0: 7650, distinct days: 2211, top-quintile agitated bars: 1543
- Decided by: The slope is positive with t >= 2 and the top-quintile mean excess return is above 0.
- Reading: The agitated regime is read from the recorded `regime` (mean_reversion), since the detector's 365-day volatility rank cannot be rebuilt inside 120-bar windows; the situation is that regime with the raw low-close range reading above 0 on the long side; the next-day return (every bar, horizon 1) minus the coin's mean 1-day return over all its windows is regressed with OLS on the forecast with day-clustered errors (CR1 small-sample correction); the top quintile is the pooled agitated bars (all coins, forecast 0 included) with forecast at or above the pooled 80th percentile; the minimum counts are agitated bars with forecast > 0 and a next-day return, and the distinct days they fall on.
- Size: unusual move +0.27 % (t 1.55, the cases of one day together: 1322 days) per case over 1 bars, 0.060 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.40 %; 3048 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003836 on the check folds against +0.0006241 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/034-01.d1_wide-range-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/034-01.d1_wide-range-low-close-rebound_1d`
Measure: `measure.py`
