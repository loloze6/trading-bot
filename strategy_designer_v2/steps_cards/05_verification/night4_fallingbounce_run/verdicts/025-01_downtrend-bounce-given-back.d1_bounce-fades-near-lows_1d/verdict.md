---
plan: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d
idea: 025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move in the short direction: 0.0029277; t of the mean: 1.08218 (threshold: confirm: mean > 0 with t >= 2 over at least 30 cases; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: None, passed: False
- Counts: cases: 1337, larger half: 0, smaller half: 1337
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The 90-day return is recomputed from in-window closes where 90 prior bars exist and taken from the recorded regime otherwise; a case is the first short bet (a rise of the short forecast's size of at least 2 points from its lowest size since the last bet, reset at flat or side change) in each 5-bar grid cell of its window, with its 5-bar return inside the window; the larger half is abs forecast above the median and the smaller half at or below it.
- Size: unusual move +0.29 % per case over 5 bars, 0.029 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.30 %; 1337 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-01_downtrend-bounce-given-back.d1_bounce-fades-near-lows_1d`
Measure: `measure.py`
