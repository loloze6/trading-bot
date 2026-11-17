---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high
fit: exact
status: mismatch
---
Situation check: 61 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Fewer than 90% of active bars have a forecast whose sign matches the plan's situation (long when the close is nearer its 52-week high than usual).
- Reading: Situation check: an active bar agrees when the forecast sign matches closeness relative to the coin's usual distance (recorded standardised dist_high plus the recorded offset, positive = nearer than usual, which the Fidelity says is the long side of a graded, centred forecast); quintiles use the 60th/80th percentiles of the forecast pooled over all grid bars with a valid 7-bar return (top = forecast >= 80th percentile, fourth = 60th <= forecast < 80th); holding is each coin's mean 7-bar grid return over all its windows; fewer than 100 top-quintile cases gives 'not observable'.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high_1d`
Measure: `measure.py`
