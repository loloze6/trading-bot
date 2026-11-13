---
plan: N1-01_trend-with-rising-month_1d
idea: N1-01_trend-with-rising-month
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 20-bar return after forecast > 0 minus coin's mean 20-bar return: 0.0156461; t of the mean: 0.659015 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; at least 30 non-overlapping active cases)
- Supporting check: OLS slope of forward 20-bar excess return on forecast (active, non-overlapping): 0.00766212, passed: True
- Counts: non-overlapping active 20-bar cases pooled: 251, active bars: 5401
- Decided by: The t-stat lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Situation checked on the recorded raw mom/dist component values (dist >= 0 and mom >= 0, long side), falling back to regime == 'trending' where a value is missing; cases and the coin's baseline mean both use the non-overlapping grid (positions 0, 20, 40, ... of each window), the coin mean pools all its windows, the t is the ordinary t of the pooled mean excess return, the slope is OLS of excess return on forecast over active grid bars, and fewer than 30 cases is reported as not observable.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-01_trend-with-rising-month_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-01_trend-with-rising-month_1d`
Measure: `measure.py`
