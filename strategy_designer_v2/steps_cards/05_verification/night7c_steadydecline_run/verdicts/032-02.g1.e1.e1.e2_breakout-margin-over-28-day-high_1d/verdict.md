---
plan: 032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high_1d
idea: 032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high
fit: exact
status: mismatch
---
Situation check: 0 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: The plan expects a long forecast on every fresh 28-day closing high, but the record has no bar with a non-zero forecast (the config gives the 'trending' regime no strategy), so the situation is never traded.
- Reading: With no active bar the agreement share is taken as 0.
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e1.e2_breakout-margin-over-28-day-high_1d`
Measure: `measure.py`
