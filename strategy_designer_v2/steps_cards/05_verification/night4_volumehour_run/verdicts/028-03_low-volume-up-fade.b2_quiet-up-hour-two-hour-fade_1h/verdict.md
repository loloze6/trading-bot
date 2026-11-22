---
plan: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move in the short direction on short bets: 0.00029966; t of the mean: 2.60388 (threshold: positive with t >= 2 to confirm, negative with t <= -2 to reject, over at least 30 cases)
- Supporting check: OLS slope of unusual move on |forecast|: -1.32385e-05, passed: False
- Counts: cases: 11338
- Decided by: t >= 2 but the supporting slope is not above 0.
- Reading: Situation bars are bars with regime 'mean_reversion' (the recorded detector decision for the 720-bar volume ratio between 0.67 and 1.5) whose raw 'rise' value is above 0, expected side short; a case is the first short bet (forecast falling at least 2 points below its least-negative level since the last bet, reset at flat or side change) in each 2-bar grid cell from each window's first row, and the unusual move is -(r - drift) with drift the coin's mean non-overlapping 2-bar return pooled over all its windows, following the workflow's 'minus drift, in the signal direction' and the reject rule's 'beyond drift'.
- Size: unusual move +0.03 % per case over 2 bars, 0.026 of the coin's usual move (1.16 %); normal drift in its direction -0.01 %, total +0.02 %; 11338 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade_1h`
Measure: `measure.py`
