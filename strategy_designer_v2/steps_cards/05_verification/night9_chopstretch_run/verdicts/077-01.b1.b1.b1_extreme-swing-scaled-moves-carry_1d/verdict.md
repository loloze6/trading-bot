---
plan: 077-01.b1.b1.b1_extreme-swing-scaled-moves-carry_1d
idea: 077-01.b1.b1.b1_extreme-swing-scaled-moves-carry
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: |forecast|-weighted mean signed unusual 7-day move: 0.00832368; t, cases of one day together: 0.524582 (threshold: above 0 with day-clustered t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: top third minus bottom third of |forecast|: mean signed unusual move (Welch t >= 1): 0.170093, passed: False
- Counts: grid cases: 773, distinct days: 228, top third cases: 257, bottom third cases: 257
- Decided by: The day-clustered t of the weighted mean signed unusual move lies between -2 and 2.
- Reading: The choppy calm profile is read from the recorded `regime` column (regime 'unknown' = no veto fired = the profile, since the detector's 365-day components cannot be rebuilt inside the windows), the situation's side is the sign of the raw swing-scaled 14-day move, the coin's mean 7-day return is taken over every window's non-overlapping 7-bar grid, the day-clustered t sums |forecast|-weighted deviations per UTC day with a D/(D-1) correction, and the thirds are the floor(n/3) cases with the largest and smallest |forecast|.
- Size: unusual move +0.20 % (t 0.31, the cases of one day together: 572 days) per case over 7 bars, 0.013 of the coin's usual move (12.84 %); normal drift in its direction +0.11 %, total +0.31 %; 908 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-01.b1.b1.b1_extreme-swing-scaled-moves-carry_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1.b1.b1_extreme-swing-scaled-moves-carry_1d`
Measure: `measure.py`
