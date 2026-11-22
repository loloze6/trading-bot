---
plan: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d
idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of the short bets, short direction: 0.00542895; t of the mean: 2.77943 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: slope of unusual move (short) on |forecast|: 0.000204429, passed: True
- Counts: cases: 2913
- Decided by: The mean unusual move is positive with t >= 2 over at least 30 cases and the slope on |forecast| is above 0.
- Reading: The 90-bar return is recomputed from closes inside the window where 90 prior bars exist and taken from the recorded regime otherwise; a case is the first short bet (forecast falling >= 2 points below its least negative level since the last bet, from 0 after flat or a side change) in each 5-bar grid cell from each window's first row, cases whose 5-bar return leaves the window are dropped, and the drift is the coin's mean non-overlapping 5-bar return over all its windows.
- Size: unusual move +0.54 % per case over 5 bars, 0.040 of the coin's usual move (12.24 %); normal drift in its direction -0.75 %, total -0.21 %; 2913 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows.b1_bounce-fade-all-coins_1d`
Measure: `measure.py`
