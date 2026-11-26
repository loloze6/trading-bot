---
plan: 034-01.d1_wide-range-low-close-rebound_1d
idea: 034-01.d1_wide-range-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (agitated, forecast > 0): -0.000129475; OLS t, errors clustered by day: -0.265984 (threshold: positive with t >= 2 (and top-quintile mean > 0) confirms; negative with t <= -2 rejects)
- Supporting check: mean next-day excess return of top-quintile forecasts (agitated bars): 0.00205131, passed: True
- Counts: agitated bars with forecast > 0: 953, distinct days: 459, top-quintile agitated bars: 193
- Decided by: The slope has |t| < 2.
- Reading: The agitated regime is read from the recorded `regime` (mean_reversion), since the detector's 365-day volatility rank cannot be rebuilt inside 120-bar windows; the situation is that regime with the raw low-close range reading above 0 on the long side; the next-day return (every bar, horizon 1) minus the coin's mean 1-day return over all its windows is regressed with OLS on the forecast with day-clustered errors (CR1 small-sample correction); the top quintile is the pooled agitated bars (all coins, forecast 0 included) with forecast at or above the pooled 80th percentile; the minimum counts are agitated bars with forecast > 0 and a next-day return, and the distinct days they fall on.
- Size: unusual move -0.55 % (t -1.43, the cases of one day together: 243 days) per case over 1 bars, -0.069 of the coin's usual move (6.78 %); normal drift in its direction +0.84 %, total +0.29 %; 360 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/034-01.d1_wide-range-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2016_2017/backtests/034-01.d1_wide-range-low-close-rebound_1d`
Measure: `measure.py`
