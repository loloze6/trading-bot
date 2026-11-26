---
plan: 032-04_calm-decline-rally-sold_1d
idea: 032-04_calm-decline-rally-sold
fit: exact
status: mismatch
---
Situation check: 78 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of the active bars are calm-decline up days on the short side: the plan's situation asks the 28-day mean range to be at most its 120-day mean, while the config's range_calm rule fires when it is at least 1 (gte), i.e. on wide-range days.
- Reading: situation recomputed per window from that window's own bars (28-day return from the recorded fall_depth raw value or the closes, day return, range=(high-low)/close with 28 vs up-to-120-bar means, volume 28-bar mean vs up-to-120 bars before them), agreement taken over the active bars where all four conditions can be computed.
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-04_calm-decline-rally-sold_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-04_calm-decline-rally-sold_1d`
Measure: `measure.py`
