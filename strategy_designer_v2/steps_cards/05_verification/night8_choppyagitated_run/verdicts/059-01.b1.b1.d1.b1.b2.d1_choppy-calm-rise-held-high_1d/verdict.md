---
plan: 059-01.b1.b1.d1.b1.b2.d1_choppy-calm-rise-held-high_1d
idea: 059-01.b1.b1.d1.b1.b2.d1_choppy-calm-rise-held-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 7-bar move per long case (day-pooled): 0.00305436; t of the mean, cases pooled by day: 0.416961 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2)
- Supporting check: unusual move upper half minus lower half of forecast (Welch t >= 1): 0.0112936, passed: True
- Counts: cases: 536, distinct case days: 343
- Decided by: The main t lies between -2 and 2.
- Reading: A case is the first long bet (forecast rise of >= 2 points from its lowest level since the last bet, from 0 after a flat) in each 7-bar grid cell of a window with a full 7-bar forward return; the halves split at the median case forecast (above vs at-or-below); the plan's minimum of 30 distinct case days is applied as 'not observable'; active bars without a computable 7-bar high or rise are left out of the agreement share.
- Size: unusual move +0.31 % (t 0.42, the cases of one day together: 343 days) per case over 7 bars, 0.018 of the coin's usual move (12.84 %); normal drift in its direction +0.96 %, total +1.27 %; 536 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b2.d1_choppy-calm-rise-held-high_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b2.d1_choppy-calm-rise-held-high_1d`
Measure: `measure.py`
