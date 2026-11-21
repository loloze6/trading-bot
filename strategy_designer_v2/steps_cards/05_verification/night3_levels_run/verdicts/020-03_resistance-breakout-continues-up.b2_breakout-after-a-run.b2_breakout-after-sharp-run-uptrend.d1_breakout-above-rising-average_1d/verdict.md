---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar unusual move (return minus coin's normal 5-bar drift, in signal direction): 0.00696569; t of the mean: 1.79426 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and Spearman > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: Spearman(forecast, unusual move) > 0: 0.0347213, passed: True
- Counts: cases: 990
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: ret60 is recomputed from closes inside the window where 60 prior bars exist, else taken from the recorded regime being 'trending'; break and ma_dist conditions use their recorded raw values; a case is the first bet bar (forecast rise of >= 2 points on its side from its lowest level since the last bet, from 0 after flat) in each 5-bar grid cell of a window, with a full 5-bar forward return inside that window; drift is the coin's mean 5-bar return on the grid positions 0,5,10,... of all its windows.
- Size: unusual move +0.70 % per case over 5 bars, 0.059 of the coin's usual move (10.60 %); normal drift in its direction +0.57 %, total +1.27 %; 990 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b2_breakout-after-sharp-run-uptrend.d1_breakout-above-rising-average_1d`
Measure: `measure.py`
