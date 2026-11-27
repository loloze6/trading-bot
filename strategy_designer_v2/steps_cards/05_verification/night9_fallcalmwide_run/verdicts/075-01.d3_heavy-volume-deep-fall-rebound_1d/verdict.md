---
plan: 075-01.d3_heavy-volume-deep-fall-rebound_1d
idea: 075-01.d3_heavy-volume-deep-fall-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return (forecast > 0): 0.00323691; day-clustered t of the weighted mean: 1.94932 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: top third minus bottom third mean next-day excess return: 0.00462881, passed: True
- Counts: bars with forecast > 0: 18271, distinct days: 2413
- Decided by: The t of the main measure lies between -2 and 2.
- Reading: The situation is a bar whose raw component value is below 0 (the day's return sign, the prior close being used only where the raw value is missing) with a long forecast; the main measure's t is the day-clustered t of the weighted mean (per-day sums of weight x deviation from the weighted mean, variance scaled by D/(D-1)); thirds are the n//3 lowest and highest forecasts after a stable sort; the minimum counts use bars with forecast > 0 and a next-day return, and short counts give 'not observable'.
- Size: unusual move +0.15 % (t 1.06, the cases of one day together: 1812 days) per case over 1 bars, 0.031 of the coin's usual move (5.31 %); normal drift in its direction +0.15 %, total +0.30 %; 9995 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/075-01.d3_heavy-volume-deep-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/075-01.d3_heavy-volume-deep-fall-rebound_1d`
Measure: `measure.py`
