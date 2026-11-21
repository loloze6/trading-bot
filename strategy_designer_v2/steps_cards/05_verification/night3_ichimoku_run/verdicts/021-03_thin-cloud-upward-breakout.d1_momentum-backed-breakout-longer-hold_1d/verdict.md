---
plan: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d
idea: 021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of unusual 40-bar move on case forecast: 0.00251812; OLS slope t: 0.136594 (threshold: confirm: slope > 0 with t >= 2 and mean unusual move > 0; reject: slope < 0 with t <= -2; at least 30 cases)
- Supporting check: mean unusual 40-bar move over cases > 0: 0.189467, passed: True
- Counts: cases: 64
- Decided by: The slope's t lies between -2 and 2.
- Reading: Situation recomputed from prices as an Ichimoku (9,26,52,26) close first above the cloud whose last outside state was below, using the recorded regime 'trending' where the window lacks the history to compute it; a case is the first long bet (forecast rise >= 2 from its low since the last bet, from 0 after flat) in each 40-bar grid cell of a window, cases without 40 forward bars in the window are dropped, drift is the coin's mean 40-bar return on the window grids, and the count of 30 is treated as a minimum count (not observable if unmet).
- Size: unusual move +18.95 % per case over 40 bars, 0.429 of the coin's usual move (30.89 %); normal drift in its direction +4.77 %, total +23.71 %; 64 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-03_thin-cloud-upward-breakout.d1_momentum-backed-breakout-longer-hold_1d`
Measure: `measure.py`
