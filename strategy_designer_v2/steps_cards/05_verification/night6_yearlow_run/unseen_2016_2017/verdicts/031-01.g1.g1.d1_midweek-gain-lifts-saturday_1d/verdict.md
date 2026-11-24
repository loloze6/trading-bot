---
plan: 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d
idea: 031-01.g1.g1.d1_midweek-gain-lifts-saturday
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of Saturday excess return on forecast (Friday bars, forecast > 0): -0.000289712; slope t, residuals summed per Saturday: -0.448543 (threshold: confirm if slope t >= 2 and forecast-weighted mean excess > 0; reject if slope t <= -2)
- Supporting check: forecast-weighted mean Saturday excess return: -0.00292549, passed: False
- Counts: Friday cases with forecast > 0: 241, distinct Saturdays: 95
- Decided by: Minimum count not reached: 241 Friday cases with forecast > 0 (300 required); 95 distinct Saturdays (100 required).
- Reading: Friday = bar stamped Friday UTC (next bar Saturday); situation from last_history_value > 0 (prices close[t-1]/close[t-4]-1 when not recorded); excess = Saturday return minus the coin's mean 1-bar return over all its windows; slope from pooled OLS with intercept across coins, its t from cluster-robust errors with residual scores summed per Saturday date (G/(G-1) correction); the plan's 'else inconclusive' for too few cases is applied as 'not observable' per the workflow.
- Size: unusual move -0.18 % (t -0.28, the cases of one day together: 88 days) per case over 1 bars, -0.030 of the coin's usual move (7.55 %); normal drift in its direction +0.96 %, total +0.78 %; 222 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d`
Measure: `measure.py`
