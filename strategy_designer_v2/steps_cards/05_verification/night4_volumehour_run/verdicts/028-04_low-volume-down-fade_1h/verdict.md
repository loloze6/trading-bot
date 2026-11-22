---
plan: 028-04_low-volume-down-fade_1h
idea: 028-04_low-volume-down-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move after forecast rises >= 2 (long): 0.000352964; t of the mean: 1.39557 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, cases at/above median forecast minus below: -0.000216252, passed: False
- Counts: cases over both coins: 6854, cases at or above median: 3427, cases below median: 3427
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Volume ratio recomputed from the window's volume over the prior 720 bars (the recorded regime used where fewer than 720 prior bars exist in the window), the fall is the raw component < 0; cases are bets (forecast rise >= 2 from its lowest long level since the last bet, from 0 after flat), the first per 6-bar grid cell of each window, both coins pooled, drift per coin from grid 6-bar returns over all its windows; the plan's 'fewer than 30 cases' minimum is applied as not observable; a supporting check with an empty half counts as failed.
- Size: unusual move +0.04 % per case over 6 bars, 0.017 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.07 %; 6854 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade_1h`
Measure: `measure.py`
