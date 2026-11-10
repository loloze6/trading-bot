---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: mismatch
---
Situation check: 0 of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active (non-zero forecast) bars are short bars with SMA50 below SMA200 (raw spread < 0), so the config does not trade the plan's situation on its side.
- Reading: Situation taken as last_history_value (SMA50-SMA200)/SMA200 < 0 with forecast < 0 on every bar with a non-zero forecast.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
