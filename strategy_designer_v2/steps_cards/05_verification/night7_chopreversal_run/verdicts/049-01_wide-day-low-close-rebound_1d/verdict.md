---
plan: 049-01_wide-day-low-close-rebound_1d
idea: 049-01_wide-day-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day return minus coin mean on forecast (pooled, every bar): 0.000373757; OLS slope t, clustered by day: 3.47545 (threshold: t >= 2 confirms (with the check passing), t <= -2 rejects)
- Supporting check: mean next-day excess return in the top fifth of the forecast > 0: 0.00447067, passed: True
- Counts: bars with a forecast: 17216, distinct days of bars with a forecast: 2897, bars in the top fifth: 3476
- Decided by: the slope's t is 2 or more and the top-fifth mean excess return is above 0.
- Reading: Regression with intercept over every bar with a next-day return in its window, t from day-clustered (UTC day) standard errors with a G/(G-1) correction; 'bars with a forecast' are bars with a non-zero forecast; the top fifth is bars at or above the pooled 80th percentile of the forecast (non-zero only if that percentile is 0).
- Size: unusual move +0.10 % (t 0.95, the cases of one day together: 2050 days) per case over 1 bars, 0.023 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.22 %; 6991 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001439 on the check folds against +0.0003738 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/049-01_wide-day-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/049-01_wide-day-low-close-rebound_1d`
Measure: `measure.py`
