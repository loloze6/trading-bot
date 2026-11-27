---
plan: 086-02_volume-weighted-up-move-continuation_1d
idea: 086-02_volume-weighted-up-move-continuation
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of the signals (return minus normal 5-bar drift): 0.00271663; t of the mean, cases of one day together: 0.506652 (threshold: confirm: mean > 0 with t >= 2 (and supporting difference > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above-median forecast minus below-median: 0.000360513, passed: True
- Counts: cases: 578, distinct days: 360
- Decided by: The t of the mean unusual move lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction +0.507 (below 1), 578 cases (30 needed).
- Reading: The falling-calm profile is read from the recorded regime ('unknown' = no veto fired), since its components are not recorded and their 365-bar lookback cannot be rebuilt in a window, and an up day as a positive raw value; cases are the first long bet (forecast rise >= 2 points from its lowest level since the last bet, reset to 0 after a flat) in each 5-bar grid cell of each window with a 5-bar return inside the window, on every coin of the record; the day-clustered t sums the deviations per UTC day with a D/(D-1) correction; the median split excludes cases equal to the median; the plan's minimum of 30 cases on 30 days, when not reached, gives 'not observable'.
- Size: unusual move +0.27 % (t 0.51, the cases of one day together: 360 days) per case over 5 bars, 0.023 of the coin's usual move (11.35 %); normal drift in its direction +0.32 %, total +0.59 %; 578 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.507 (below 1), 578 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/086-02_volume-weighted-up-move-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/086-02_volume-weighted-up-move-continuation_1d`
Measure: `measure.py`
