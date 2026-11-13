---
plan: N1-01_trend-with-rising-month_1d
idea: N1-01_trend-with-rising-month
fit: adapted
status: mismatch
---
Situation check: 0 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active bars are long bars with close at or above its 200-day SMA and a non-negative 20-bar return, as the plan's situation requires.
- Reading: The coin's mean 20-bar return is the mean of every bar's in-window forward 20-bar return across all its windows; cases are bars with forecast > 0 at grid positions 0, 20, 40, ... of each window, pooled across coins; the minimum of 30 such cases is treated as an observability minimum; the supporting slope is an OLS of excess return on forecast over those same cases and passes if positive.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-01_trend-with-rising-month_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-01_trend-with-rising-month_1d`
Measure: `measure.py`
