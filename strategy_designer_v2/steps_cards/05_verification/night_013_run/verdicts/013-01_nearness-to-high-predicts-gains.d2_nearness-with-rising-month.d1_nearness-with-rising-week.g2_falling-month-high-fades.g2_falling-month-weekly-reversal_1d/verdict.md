---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 7-bar forward return on forecast, mean_reversion grid bars: 6.31695e-05; OLS slope t: 0.181881 (threshold: t >= 2 confirms (with timing gain > 0); t <= -2 rejects; otherwise inconclusive; at least 100 grid cases)
- Supporting check: book mean daily timing gain > 0: -0.000229198, passed: False
- Counts: independent grid cases in mean_reversion: 1226
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The 30-bar return for the situation check is recomputed from closes inside each window (first 30 bars left out); the coin mean subtracted is the mean 7-bar forward return over all its windows' grid bars; the slope t is the OLS slope over its standard error; the timing gain uses each coin's book value after rebalance, daily returns averaged across coins per day, minus the held allocation times the coin's mean daily return.
- Size: unusual move -0.04 % per case over 7 bars, -0.001 of the coin's usual move (12.44 %); normal drift in its direction +0.21 %, total +0.17 %; 1467 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g2_falling-month-weekly-reversal_1d`
Measure: `measure.py`
