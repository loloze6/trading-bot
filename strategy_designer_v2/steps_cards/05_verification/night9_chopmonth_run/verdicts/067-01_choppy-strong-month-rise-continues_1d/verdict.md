---
plan: 067-01_choppy-strong-month-rise-continues_1d
idea: 067-01_choppy-strong-month-rise-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar forward excess return on forecast, cells with forecast > 0: 0.00071782; OLS slope t: 0.858863 (threshold: t >= 2 with mean excess > 0 confirms; t <= -2 rejects; at least 100 cells)
- Supporting check: mean 7-bar forward excess return on the same cells > 0: 0.00305522, passed: True
- Counts: cells: 587
- Decided by: The slope's t is between -2 and 2, on at least 100 cells.
- Reading: Cells are pooled over all coins and windows. The slope is a one-variable OLS with an intercept of the excess return (a fraction) on the forecast. Each coin's mean 7-bar return is the mean over its non-overlapping grid cells of all windows. The situation counts a regime other than the config's trend veto label 'chop' as choppy.
- Size: unusual move +0.55 % (t 0.95, the cases of one day together: 572 days) per case over 7 bars, 0.027 of the coin's usual move (14.34 %); normal drift in its direction +1.13 %, total +1.68 %; 985 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01_choppy-strong-month-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01_choppy-strong-month-rise-continues_1d`
Measure: `measure.py`
