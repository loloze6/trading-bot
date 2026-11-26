---
plan: 034-01.d1_wide-range-low-close-rebound_1d
idea: 034-01.d1_wide-range-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (agitated, forecast > 0): 6.50367e-05; OLS t, errors clustered by day: 0.140789 (threshold: positive with t >= 2 (and top-quintile mean > 0) confirms; negative with t <= -2 rejects)
- Supporting check: mean next-day excess return of top-quintile forecasts (agitated bars): 0.00352929, passed: True
- Counts: agitated bars with forecast > 0: 747, distinct days: 254, top-quintile agitated bars: 150
- Decided by: The slope has |t| < 2.
- Reading: The agitated regime is read from the recorded `regime` (mean_reversion), since the detector's 365-day volatility rank cannot be rebuilt inside 120-bar windows; the situation is that regime with the raw low-close range reading above 0 on the long side; the next-day return (every bar, horizon 1) minus the coin's mean 1-day return over all its windows is regressed with OLS on the forecast with day-clustered errors (CR1 small-sample correction); the top quintile is the pooled agitated bars (all coins, forecast 0 included) with forecast at or above the pooled 80th percentile; the minimum counts are agitated bars with forecast > 0 and a next-day return, and the distinct days they fall on.
- Size: unusual move -0.41 % (t -1.16, the cases of one day together: 155 days) per case over 1 bars, -0.065 of the coin's usual move (3.33 %); normal drift in its direction +0.06 %, total -0.35 %; 298 cases
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/034-01.d1_wide-range-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/unseen_2026/backtests/034-01.d1_wide-range-low-close-rebound_1d`
Measure: `measure.py`
