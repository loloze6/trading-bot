---
plan: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d
idea: 003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar forward return of cases with forecast >= 2 (vs coin mean on the same grid): 0.0158205; t of the mean: 0.722986 (threshold: confirm if t >= 2 and supporting difference > 0; reject if t <= -2; at least 30 cases)
- Supporting check: mean excess of cases above median forecast minus below median: None, passed: None
- Counts: cases: 76, cases above median forecast: 0, cases below median forecast: 36, active bars: 1501
- Decided by: t lies between -2 and 2, which the plan calls inconclusive whatever the supporting check shows.
- Reading: The coin's mean is taken over every grid bar with a full 5-bar return in all its windows, cases are grid bars with forecast >= 2 and a full return inside the window, cases equal to the median forecast are left out of the supporting split, and fewer than 30 cases gives 'not observable' as the workflow requires.
- Size: unusual move +1.49 % (t 0.89, the cases of one day together: 198 days) per case over 5 bars, 0.096 of the coin's usual move (18.32 %); normal drift in its direction +4.75 %, total +6.24 %; 291 cases
Plan: `steps_cards/03_test_plan/volume_run/plans/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d.md`
Record: `steps_cards/04_backtest/volume_run/unseen_2016_2017/backtests/003-02_thin-volume-drop-rebounds.g1_heavy-volume-up-moves-continue_1d`
Measure: `measure.py`
