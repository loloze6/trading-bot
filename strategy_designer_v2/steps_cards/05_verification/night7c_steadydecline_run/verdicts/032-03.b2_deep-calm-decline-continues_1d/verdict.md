---
plan: 032-03.b2_deep-calm-decline-continues_1d
idea: 032-03.b2_deep-calm-decline-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-bar excess forward return on forecast (thin-volume short cases): 0.00097939; OLS slope t, clustered by day: 0.675951 (threshold: confirm if cluster-by-day t >= 2 with supporting mean > 0; reject if t <= -2)
- Supporting check: mean excess 10-bar return in the short's direction: 0.00736879, passed: True
- Counts: cases: 532, distinct days: 201
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Thin-volume situation taken from the recorded regime (trending = vr<1) since vr cannot be rebuilt in-window; coin mean 10-bar return taken on the non-overlapping grid of all its windows; slope t from OLS with intercept and CR1 standard errors clustered by UTC day; supporting check read as the mean of minus (return minus coin mean); the plan's 'fewer than 30 cases or 20 days' treated as minimum counts giving 'not observable'.
- Size: unusual move +0.56 % (t 0.73, the cases of one day together: 398 days) per case over 10 bars, 0.051 of the coin's usual move (14.49 %); normal drift in its direction -1.28 %, total -0.72 %; 619 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-03.b2_deep-calm-decline-continues_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-03.b2_deep-calm-decline-continues_1d`
Measure: `measure.py`
