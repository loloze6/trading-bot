---
plan: 006-04_upside-squeeze-break-continuation_1d
idea: 006-04_upside-squeeze-break-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar return on forecast, break-bar grid cases: -0.00203816; OLS slope t: -1.45773 (threshold: confirm: t >= 2 and mean excess > 0; reject: t <= -2; else inconclusive; min 100 cases)
- Supporting check: mean excess 3-bar return on break-bar cases > 0: 0.0113804, passed: True
- Counts: break-bar cases: 299
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is rebuilt per window as close > max(high of the 20 prior bars). Each window's first 20 bars cannot be rebuilt and are left out of the agreement. The cases are pooled across all coins and windows into one OLS regression. Each coin's baseline is its mean 3-bar return on the non-overlapping grid of all its windows. The plan's 'fewer than 100 break-bar cases' minimum is treated as a minimum count, which gives 'not observable'.
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation_1d`
Measure: `measure.py`
