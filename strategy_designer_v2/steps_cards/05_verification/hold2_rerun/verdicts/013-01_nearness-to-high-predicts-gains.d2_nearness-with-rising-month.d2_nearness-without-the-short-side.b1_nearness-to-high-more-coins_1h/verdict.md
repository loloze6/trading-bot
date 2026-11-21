---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope t of excess 168-bar forward return on forecast (non-overlapping grid): 0.00172898; OLS slope t: 5.2926 (threshold: confirm if t >= 2 and supporting check passes; reject if t <= -2; else inconclusive; needs >= 300 grid cases with forecast > 0)
- Supporting check: mean excess 168-bar forward return on grid bars with forecast > 0 above 0: 0.00688644, passed: True
- Counts: non-overlapping grid cases with forecast > 0: 2201, non-overlapping grid cases (all): 4530
- Decided by: The slope's t is >= 2 and the mean excess return on forecast > 0 grid bars is above 0.
- Reading: The 720-bar return is recomputed from each window's closes and, on bars without 720 bars of history in the window, its sign is taken from the raw HPM value; the coin's benchmark is the mean of all its non-overlapping 168-bar grid returns over all its windows; the slope's t is the ordinary OLS t with an intercept; the plan's 'fewer than 300 cases' rule is reported as not observable per the workflow.
Plan: `steps_cards/03_test_plan/hold2_rerun/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h.md`
Record: `steps_cards/04_backtest/hold2_rerun/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h`
Measure: `measure.py`
