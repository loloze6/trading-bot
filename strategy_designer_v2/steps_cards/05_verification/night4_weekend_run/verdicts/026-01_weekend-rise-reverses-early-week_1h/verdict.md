---
plan: 026-01_weekend-rise-reverses-early-week_1h
idea: 026-01_weekend-rise-reverses-early-week
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed unusual 48-bar move after a weekend-gain short (short direction, net of coin drift): -0.00021373; t of the mean: -0.0957287 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; at least 100 cases)
- Supporting check: OLS slope of signed unusual move on |forecast|: 0.000453937, passed: True
- Counts: cases: 1123
- Decided by: The t-statistic lies between -2 and 2.
- Reading: A case is a bar stamped Sunday 23:00 UTC (closing at Monday 00:00) with a negative forecast that is a bet under the 2-point band rule, its 48-bar return taken by row inside its window and the coin's drift from the 0,48,96,... grid of all its windows; the plan's fewer-than-100-cases rule is reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move -0.02 % per case over 48 bars, -0.000 of the coin's usual move (6.56 %); normal drift in its direction -0.27 %, total -0.29 %; 1124 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week_1h`
Measure: `measure.py`
