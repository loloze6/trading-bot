---
plan: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return of cases with forecast >= 2 (vs coin mean on the same grid): 0.016876; t of the mean: 2.97614 (threshold: confirm if t >= 2 and supporting difference > 0; reject if t <= -2; at least 30 cases)
- Supporting check: mean excess of cases above median forecast minus below median: 0.00473143, passed: True
- Counts: cases: 511, cases above median forecast: 255, cases below median forecast: 255, active bars: 8793
- Decided by: The mean excess 5-bar return has t >= 2 and the above-median minus below-median difference is above 0.
- Reading: The coin's mean is taken over every grid bar with a full 5-bar return in all its windows, cases are grid bars with forecast >= 2 and a full return inside the window, cases equal to the median forecast are left out of the supporting split, and fewer than 30 cases gives 'not observable' as the workflow requires.
- Size: unusual move +0.32 % per case over 5 bars, 0.020 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.91 %; 1672 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d`
Measure: `measure.py`
