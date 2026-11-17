---
plan: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d
idea: 010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS t of the slope of excess 7-day return on run length below 50 (pooled grid bars, forecast < 0): 0.000420571; OLS slope t: 1.15358 (threshold: confirm if t <= -2 with supporting check passing; reject if t >= +2; otherwise inconclusive; at least 100 grid cases with forecast < 0)
- Supporting check: mean of forecast/10 x excess 7-day return on the same grid bars > 0: 0.00552096, passed: True
- Counts: grid cases with forecast < 0: 406
- Decided by: The slope's t (1.15) lies between -2 and +2.
- Reading: The coin's mean 7-day return is taken over its non-overlapping 7-bar grid bars of all windows, grid bars without a full 7-bar return inside the window are dropped, the slope's t is the ordinary OLS t pooled over both coins, and the plan's 'fewer than 100 cases' rule is reported as not observable per the workflow.
Plan: `steps_cards/03_test_plan/night_rsi_run/plans/010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d.md`
Record: `steps_cards/04_backtest/night_rsi_run/backtests/010-03_rsi-above-streak-continuation.e2_below-midline-streak-continues-down_1d`
Measure: `measure.py`
