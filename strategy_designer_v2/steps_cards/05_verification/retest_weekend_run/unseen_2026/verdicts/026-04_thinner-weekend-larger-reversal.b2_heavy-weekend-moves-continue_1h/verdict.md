---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
fit: exact
status: mismatch
---
Situation check: 89 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the nonzero-forecast bars are Sunday 23:00 bars with weekend volume above the prior weekdays' mean and a forecast sign equal to the 48-bar weekend return's sign.
- Reading: The situation bar is the bar starting Sunday 23:00 UTC (closing Monday 00:00), the volume ratio is mean volume of bars t-47..t over bars t-167..t-48 by row position in the window.
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/unseen_2026/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Measure: `measure.py`
