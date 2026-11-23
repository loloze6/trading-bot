---
plan: 029-01_failed-breakout-depth-decline_1d
idea: 029-01_failed-breakout-depth-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 5-bar excess return over drift: -0.00125077; t of the mean: -0.294981 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject))
- Supporting check: Spearman rank correlation |forecast| vs short excess return: 0.0568904, passed: True
- Counts: cases: 617
- Decided by: t is between -2 and 2 (or undefined) with at least 30 cases: inconclusive.
- Reading: Situation recomputed from closes (most recent bar 1-3 ago with close above the max of its prior 20 closes, today's close below that max), falling back to a nonzero raw component value where the window's prices are too short; a case is a short bet (|forecast| rising by >= 2 from its lowest size on the short side since the last bet, reset to 0 on flat or side change), the first one per non-overlapping 5-bar cell from each window's first row, with drift the coin's mean 5-bar grid return over all its windows.
- Size: unusual move -0.13 % per case over 5 bars, -0.007 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -0.70 %; 617 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-01_failed-breakout-depth-decline_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-01_failed-breakout-depth-decline_1d`
Measure: `measure.py`
