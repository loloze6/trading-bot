---
plan: 030-04_heavy-flat-low-close-reverses_1d
idea: 030-04_heavy-flat-low-close-reverses
fit: exact
status: mismatch
---
Situation check: 45 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active bars are heavy, flat, lower-half-close days with a long forecast: the config's forecast does not bet only long on the plan's situation.
- Reading: The situation is a day with volume >= 2x its prior 20-day mean, body <= 1/3 of range and the close in the lower half of the range (close location < 0), expected side long; bars without 20 prior bars in their window use the recorded regime for the volume rule; cases are bets of both signs, the first bet in each 5-bar grid cell, weighted by the signed forecast at the case bar.
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-04_heavy-flat-low-close-reverses_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-04_heavy-flat-low-close-reverses_1d`
Measure: `measure.py`
