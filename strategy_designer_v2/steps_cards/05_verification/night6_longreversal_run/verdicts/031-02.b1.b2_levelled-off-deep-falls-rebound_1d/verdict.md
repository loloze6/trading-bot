---
plan: 031-02.b1.b2_levelled-off-deep-falls-rebound_1d
idea: 031-02.b1.b2_levelled-off-deep-falls-rebound
fit: exact
status: mismatch
---
Situation check: 27 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90 % of the bars with a non-zero forecast are mean_reversion-regime bars with a long forecast, while the plan's Fidelity expects a rebound (long) inside the deep-fall situation.
- Reading: The situation is read from the recorded `regime` column because r90's 365-day scale cannot be rebuilt inside the recorded windows, and the expected side is long because the outcome is a rebound.
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-02.b1.b2_levelled-off-deep-falls-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-02.b1.b2_levelled-off-deep-falls-rebound_1d`
Measure: `measure.py`
