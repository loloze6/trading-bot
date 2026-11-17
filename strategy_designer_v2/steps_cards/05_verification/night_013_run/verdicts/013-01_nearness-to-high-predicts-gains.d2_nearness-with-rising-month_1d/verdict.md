---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
fit: exact
status: mismatch
---
Situation check: 57 % of the active bars are bars of the plan's situation on its side (90 % needed).
- Decided by: Only 56.9% of active bars are long bars with a positive 30-day return, below the 90% needed for the config to match the plan's situation and side.
- Reading: The situation is read as the gate 'PriceEvolution(30) > 0' with a long side, since 'near the high' has no cut-off and is the graded part of the comparison; the coin's mean 7-bar return is taken over all its non-overlapping grid bars in all windows; the regression is pooled OLS with intercept across coins and windows; the before-cost book is the held allocation times the next bar's return per coin, averaged across coins per day.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d`
Measure: `measure.py`
