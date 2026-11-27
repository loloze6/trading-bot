---
plan: 086-01_heavy-volume-up-day-continuation_1d
idea: 086-01_heavy-volume-up-day-continuation
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move per case over 5 bars (long, minus the coin's normal 5-bar drift): 0.00543097; t of the mean, cases of one day clustered: 0.820502 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: Spearman of heavy_vol raw value vs unusual move: 0.0923903, passed: True
- Counts: cases: 311, days: 231
- Decided by: The t of the mean unusual move lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.821 (below 1), 311 cases (30 needed).
- Reading: The situation is checked as 'close above the previous close and volume above its prior 20-bar mean' on the long side (the falling-calm profile is added by code and not recomputed), using the recorded heavy_vol raw value (ratio minus 1) where present, else the volume recomputed inside the window, else the detector's 'trending' regime on bars without a previous close; cases are bets (forecast rises of at least 2 points from its lowest level since the last bet, from 0 after a flat), the first per 5-bar grid cell of each window, equally weighted, the t clusters cases by UTC day, and fewer than 30 cases gives 'not observable' as the workflow requires.
- Size: unusual move +0.54 % (t 0.82, the cases of one day together: 231 days) per case over 5 bars, 0.052 of the coin's usual move (11.35 %); normal drift in its direction +0.33 %, total +0.87 %; 311 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.821 (below 1), 311 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/086-01_heavy-volume-up-day-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/086-01_heavy-volume-up-day-continuation_1d`
Measure: `measure.py`
