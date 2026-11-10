---
plan: 003-05_up-move-retrace-by-volume_1d
idea: 003-05_up-move-retrace-by-volume
fit: adapted
status: mismatch
---
Situation check: 0.189542 of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active bars are top-decile one-bar up moves with long on volume at/above its 20-bar mean and short below it, so the config does not do what the Fidelity says.
- Reading: Percentile ranks and 20-bar volume means are computed from in-window history only (bars without 20 bars of history are skipped).
Plan: `steps_cards/03_test_plan/plans/003-05_up-move-retrace-by-volume_1d.md`
Record: `steps_cards/04_backtest/backtests/003-05_up-move-retrace-by-volume_1d`
Measure: `measure.py`
