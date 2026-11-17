---
plan: 010-07_rsi-above-streak-reversal_1d
idea: 010-07_rsi-above-streak-reversal
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 14-bar excess return on RSI>50 run length: 0.000672987; OLS slope t: 0.954735 (threshold: confirm if slope < 0 with t <= -2 (and timing gain > 0); reject if slope > 0 with t >= +2)
- Supporting check: book timing gain (mean daily return minus market-rise gain, before costs): -0.000608495, passed: False
- Counts: grid cases with RSI above 50: 199, grid cases with forecast below 0 (regression sample): 199
- Decided by: The slope's t lies between -2 and +2 (inconclusive rule).
- Reading: Pooled the coins present in the record (BNB absent), used grid bars at positions 0,14,28,... of each window with a full forward 14-bar return and forecast < 0, regressed excess return on last_history_value by OLS, counted 'grid cases with RSI above 50' as grid bars with last_history_value > 0, and treated a shortfall of that minimum as 'not observable'.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-07_rsi-above-streak-reversal_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-07_rsi-above-streak-reversal_1d`
Measure: `measure.py`
