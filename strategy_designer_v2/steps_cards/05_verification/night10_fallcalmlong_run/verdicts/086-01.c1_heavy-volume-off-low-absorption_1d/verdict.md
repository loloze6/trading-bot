---
plan: 086-01.c1_heavy-volume-off-low-absorption_1d
idea: 086-01.c1_heavy-volume-off-low-absorption
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move after each case, long, before costs: -0.00412288; t of the mean, cases of one day clustered: -0.709158 (threshold: confirm: mean > 0 with t >= 2 (and check passes); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, upper half minus lower half of entry forecast (> 0): 0.00720765, passed: True
- Counts: cases: 340, distinct days: 268
- Decided by: Inconclusive rule: the t lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.709 (below 1), 340 cases (30 needed).
- Reading: Situation = volume >= 1.5x the mean of the prior 20 bars of the window and close above the low, long side, with the recorded regime used where 20 prior bars are not in the window; a case is the first bet bar (long forecast rise >= 2 points from its low since the last bet) in each 5-bar cell of a window's grid; the minimum counts are read as at least 30 cases and at least 20 distinct days, either short giving not observable; the day-clustered t uses a D/(D-1) factor; the upper half is forecasts strictly above the median, the lower half the rest.
- Size: unusual move -0.41 % (t -0.71, the cases of one day together: 268 days) per case over 5 bars, -0.036 of the coin's usual move (11.31 %); normal drift in its direction +0.60 %, total +0.19 %; 340 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.709 (below 1), 340 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/086-01.c1_heavy-volume-off-low-absorption_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-01.c1_heavy-volume-off-low-absorption_1d`
Measure: `measure.py`
