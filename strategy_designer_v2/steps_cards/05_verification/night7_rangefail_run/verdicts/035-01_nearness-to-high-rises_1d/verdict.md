---
plan: 035-01_nearness-to-high-rises_1d
idea: 035-01_nearness-to-high-rises
fit: exact
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast, pooled grid cells: 0.00151006; OLS slope t, clustered by day: 1.57748 (threshold: confirm t >= 2 (with positive non-rising-market slope); reject t <= -2)
- Supporting check: slope on cells with 60-day return <= +10 %: 0.00316484, passed: True
- Counts: grid cases: 7270, distinct days: 617, non-rising-market cells: 2140
- Decided by: The main slope has t between -2 and 2.
- Reading: All grid cells with a full 5-bar forward return are regressed with an intercept (including forecast-0 cells), the t uses standard errors clustered by calendar day, the normal drift is the coin's mean grid-cell 5-bar return, and cells before bar 60 of a window have no 60-day return and are left out of the supporting check.
- Size: unusual move +1.03 % (t 3.27, the cases of one day together: 1600 days) per case over 5 bars, 0.083 of the coin's usual move (12.35 %); normal drift in its direction +0.20 %, total +1.24 %; 4354 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-01_nearness-to-high-rises_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/035-01_nearness-to-high-rises_1d`
Measure: `measure.py`
