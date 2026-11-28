---
plan: 086-02.c1_forceful-break-day-continues_1d
idea: 086-02.c1_forceful-break-day-continues
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move of the bets: -0.00118789; t clustered by day: -0.127127 (threshold: positive with t >= 2 to confirm; t <= -2 to reject)
- Supporting check: unusual move above-median forecast minus at-or-below (Welch t 0.217): 0.00356357, passed: True
- Counts: cases: 338, distinct days: 228, cases above median: 169, cases at or below median: 169
- Decided by: Inconclusive: the numbers meet neither the confirm nor the reject rule. No effect (common/verdicts.md): t in the idea's direction -0.127 (below 1), 169 cases (30 needed).
- Reading: A case is the first bet (forecast rise of at least 2 from its low since the last bet) in each 5-bar grid cell from each window's first row, the day t uses the day-clustered standard error with a G/(G-1) correction, the plan's minimum of 30 cases on 30 days gives 'not observable' when not met, and active bars in a window's first 3 bars are left out of the situation check.
- Size: unusual move -0.12 % (t -0.13, the cases of one day together: 228 days) per case over 5 bars, -0.024 of the coin's usual move (11.39 %); normal drift in its direction +0.66 %, total +0.54 %; 338 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.127 (below 1), 169 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_riseagilong_run/plans/086-02.c1_forceful-break-day-continues_1d.md`
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/086-02.c1_forceful-break-day-continues_1d`
Measure: `measure.py`
