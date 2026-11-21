---
plan: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d
idea: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 7-bar excess forward return on forecast: 0.000461795; OLS slope t: 1.94246 (threshold: confirm if t >= 2 with top-minus-bottom tercile > 0; reject if t <= -2)
- Supporting check: top-minus-bottom forecast tercile mean excess 7-bar return: 0.00754352, passed: True
- Counts: independent non-overlapping cases: 2443, top tercile cases: 815, bottom tercile cases: 815
- Decided by: The slope t lies between -2 and 2 (inconclusive rule).
- Reading: The coin's mean 7-bar return is taken over its non-overlapping samples from all windows. The OLS includes an intercept and uses the ordinary OLS standard error. Terciles are cut at the pooled 1/3 and 2/3 forecast quantiles (bottom <= q1/3, top >= q2/3).
- Size: unusual move +0.56 % per case over 7 bars, 0.033 of the coin's usual move (12.44 %); normal drift in its direction -0.21 %, total +0.35 %; 2208 cases
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g1_volume-surge-predicts-weekly-return_1d`
Measure: `measure.py`
