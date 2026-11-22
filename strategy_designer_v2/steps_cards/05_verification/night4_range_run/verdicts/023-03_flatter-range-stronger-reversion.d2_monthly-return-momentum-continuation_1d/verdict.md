---
plan: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 5-bar forward return on forecast, pooled: 0.000385566; OLS slope t: 2.354 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 200 non-overlapping grid cases)
- Supporting check: none
- Counts: non-overlapping grid cases with a recorded forecast: 3419
- Decided by: The slope is positive with t >= 2 over at least 200 grid cases (confirm rule).
- Reading: Cases are grid bars 0,5,10,... of each window with t+5 in the window and a non-missing forecast (zero forecasts included); each coin's drift is the mean of its grid 5-bar returns over all its windows; the slope and its t come from a pooled OLS with an intercept.
- Size: unusual move +0.58 % per case over 5 bars, 0.048 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.56 %; 2409 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation_1d`
Measure: `measure.py`
