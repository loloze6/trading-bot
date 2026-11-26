---
plan: 038-01_calm-scaled-weekly-rise-continues_1d
idea: 038-01_calm-scaled-weekly-rise-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 5-day forward return net of the coin's drift on the forecast (grid, forecast > 0): 1.4567; OLS slope t: 1.4567 (threshold: confirm if slope t >= 2 and mean unusual move > 0; reject if slope t <= -2; at least 100 grid cases)
- Supporting check: mean unusual 5-day move (net of coin drift) > 0: 0.00210126, passed: True
- Counts: grid cases with forecast > 0: 941
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Cases from all coins are pooled in one OLS regression of the drift-removed 5-day forward return on the forecast at the grid bar (positions 0,5,10,... of each window with a full 5-bar return), each coin's drift being the mean of its non-overlapping 5-bar returns over all its windows, and the plan's 'fewer than 100 cases' is reported as 'not observable' per the minimum-count rule.
- Size: unusual move +0.27 % (t 0.68, the cases of one day together: 645 days) per case over 5 bars, 0.020 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +0.91 %; 1166 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/038-01_calm-scaled-weekly-rise-continues_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/038-01_calm-scaled-weekly-rise-continues_1d`
Measure: `measure.py`
