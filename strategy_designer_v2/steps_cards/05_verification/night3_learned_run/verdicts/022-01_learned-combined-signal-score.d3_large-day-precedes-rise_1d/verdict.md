---
plan: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d
idea: 022-01_learned-combined-signal-score.d3_large-day-precedes-rise
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: top-third minus bottom-third mean excess 5-day return: 0.00771986; Welch t: 1.63528 (threshold: confirm if difference > 0 with Welch t >= 2 and top third beats holding; reject if difference < 0 with Welch t <= -2)
- Supporting check: top-third mean excess 5-day return > 0: 0.00667229, passed: True
- Counts: grid cases in top third: 1139, grid cases in bottom third: 1139, grid cases in total: 3419
- Decided by: Welch t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Thirds are taken by rank of the pooled grid forecasts (stable sort, floor(n/3) cases each, ties broken by coin, window and position), grid points with forecast 0 included, and the drift is each coin's mean of its non-overlapping 5-day grid returns over all its windows.
- Size: unusual move +0.09 % per case over 5 bars, 0.009 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.68 %; 3187 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d3_large-day-precedes-rise_1d`
Measure: `measure.py`
