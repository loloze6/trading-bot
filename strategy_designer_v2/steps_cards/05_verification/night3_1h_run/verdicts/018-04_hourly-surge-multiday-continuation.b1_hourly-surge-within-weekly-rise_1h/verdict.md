---
plan: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h
idea: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move of the bets (return minus the coin's normal 120-bar drift): 0.00116173; t of the mean: 0.518562 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: t <= -2 over at least 30 cases)
- Supporting check: above-median minus below-median 168-bar-return half, in unusual move (Welch t): 0.0042032, passed: True
- Counts: cases: 2455, above-median half: 1124, below-median half: 1124
- Decided by: Inconclusive rule: the main t is between -2 and 2.
- Reading: Situation bars are those with a positive 168-bar return recomputed from closes (the recorded regime where fewer than 168 past closes exist in the window) and a positive 24-bar surge, on the long side; cases are the first bet of each 120-bar grid cell per window, pooled over all coins with each coin's own drift; the halves are cases with 168-bar return strictly above the median versus at or below it; the plan's minimum counts (30 cases, 15 per half) not reached give 'not observable' as the workflow requires.
- Size: unusual move +0.12 % per case over 120 bars, 0.007 of the coin's usual move (10.37 %); normal drift in its direction +0.64 %, total +0.76 %; 2455 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h`
Measure: `measure.py`
