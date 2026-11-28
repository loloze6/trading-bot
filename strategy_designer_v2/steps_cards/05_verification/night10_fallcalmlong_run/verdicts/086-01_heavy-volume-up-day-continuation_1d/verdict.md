---
plan: 086-01_heavy-volume-up-day-continuation_1d
idea: 086-01_heavy-volume-up-day-continuation
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per case (long), cases of one day together: 0.00287386; t of the mean, cases of one day together: 0.415547 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, heavier half minus lighter half (median volume ratio): 0.0146244, passed: True
- Counts: cases: 220, distinct days: 186
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive. No effect (common/verdicts.md): t in the idea's direction +0.416 (below 1), 220 cases (30 needed).
- Reading: A case is the first long bet (forecast rise >= 2 points from its low since the last bet) in each 5-bar grid cell from each window's first row; the t clusters deviations by UTC day with a G/(G-1) correction; the heavier half is volume ratio above the median, the lighter half at or below it; the plan's 'fewer than 30 cases or 20 days' is reported as not observable; calm is read from the detector's regime.
- Size: unusual move +0.29 % (t 0.42, the cases of one day together: 186 days) per case over 5 bars, 0.025 of the coin's usual move (11.31 %); normal drift in its direction +0.64 %, total +0.93 %; 220 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.416 (below 1), 220 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/086-01_heavy-volume-up-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-01_heavy-volume-up-day-continuation_1d`
Measure: `measure.py`
