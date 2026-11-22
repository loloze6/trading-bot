---
plan: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d
idea: 029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 5-bar move: 0.00690228; t of the mean: 1.05986 (threshold: mean short-direction unusual move > 0 with t >= 2 over at least 30 cases (reject: < 0 with t <= -2))
- Supporting check: larger-half minus smaller-half mean unusual move (by abs forecast): None, passed: None
- Counts: cases: 221, larger half cases: 0, smaller half cases: 221
- Decided by: The t of the mean short-direction unusual move lies between -2 and 2.
- Reading: Cases are the first short-side forecast rise of at least 2 points in each 5-bar grid cell (positions 0,5,10,... of each window) with a full 5-bar return inside the window; the larger half is abs(forecast) strictly above the median and the smaller half at or below it; situation bars in the first 23 bars of a window, where the 20-day high cannot be rebuilt from recorded prices, are judged by raw value > 0.
- Size: unusual move +0.69 % per case over 5 bars, 0.083 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.10 %; 221 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-01_failed-breakout-depth-decline.d1_thin-volume-failed-breakout-falls_1d`
Measure: `measure.py`
