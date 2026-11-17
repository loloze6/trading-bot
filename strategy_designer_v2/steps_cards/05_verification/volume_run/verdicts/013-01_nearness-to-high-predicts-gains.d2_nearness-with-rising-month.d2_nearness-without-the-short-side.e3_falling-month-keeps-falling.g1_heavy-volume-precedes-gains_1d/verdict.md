---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
fit: exact
status: mismatch
---
Situation check: 63 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: The forecast's sign does not follow the plan's situation (long when the day's volume is above its usual ratio to the 30-day average, short when below) on at least 90% of active bars.
- Reading: Usual volume level taken as the ratio's mean over its past 60 values (or 1 without enough history, or 10 if the recorded value is already standardised).
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d`
Measure: `measure.py`
