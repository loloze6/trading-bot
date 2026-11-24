---
plan: 031-01.g1.g1.g1.g1_two-week-run-carries-saturday_1d
idea: 031-01.g1.g1.g1.g1_two-week-run-carries-saturday
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of Saturday's excess return on the Friday run14 forecast: 0.000466841; slope t (clustered by Saturday): 3.52009 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 300 Friday cases and 100 distinct Saturdays)
- Supporting check: none
- Counts: Friday cases: 2478, distinct Saturdays: 414
- Decided by: Confirm rule met: the slope is positive with t >= 2 over at least 300 Friday cases.
- Reading: Friday-close bars are bars stamped Friday (dayofweek 4) whose regime is 'trending'; the regression has an intercept and the slope's t uses standard errors clustered by Saturday (score contributions summed per day across coins, with a G/(G-1) correction); the coin's mean daily return is over all its windows' within-window daily returns.
- Size: unusual move +0.50 % (t 3.55, the cases of one day together: 413 days) per case over 1 bars, 0.102 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.50 %; 2143 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.g1_two-week-run-carries-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.g1_two-week-run-carries-saturday_1d`
Measure: `measure.py`
