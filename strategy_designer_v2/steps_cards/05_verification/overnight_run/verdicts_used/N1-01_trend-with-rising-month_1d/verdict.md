---
plan: N1-01_trend-with-rising-month_1d
idea: N1-01_trend-with-rising-month
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess forward 20-bar return after forecast > 0 (non-overlapping, pooled): 0.0150071; t of the mean: 0.631297 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive)
- Supporting check: slope of excess forward 20-bar return on forecast (active, non-overlapping): 0.00765658, passed: True
- Counts: non-overlapping active 20-bar cases pooled: 251
- Decided by: Inconclusive rule met: the t-stat lies between -2 and 2.
- Reading: Situation taken as raw dist >= 0 and mom >= 0 from the strategy components' last_history_value (falling back to regime == 'trending' where those values are missing), side long (forecast > 0); the coin's mean 20-bar return uses every bar's forward 20-bar return in all its windows, cases are the window-grid bars 0, 20, 40, ... with forecast > 0 and a full forward return, the t is the ordinary one-sample t, and the plan's 'fewer than 30 cases' minimum is treated as not observable.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-01_trend-with-rising-month_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-01_trend-with-rising-month_1d`
Measure: `measure.py`
