---
plan: 086-02.c2_deep-down-day-continues_1d
idea: 086-02.c2_deep-down-day-continues
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move in the short direction over the cases: -0.00160297; t of the mean, cases summed per day: -0.0987658 (threshold: t >= +2 confirms (with deeper-minus-shallower > 0); t <= -2 rejects; fewer than 30 distinct case days is not observable)
- Supporting check: deeper half minus shallower half mean unusual move: -0.0113399, passed: False
- Counts: cases: 288, distinct case days: 218
- Decided by: The main t lies between -2 and +2. No effect (common/verdicts.md): t in the idea's direction -0.099 (below 1), 218 cases (30 needed).
- Reading: Profile taken as the recorded regime 'unknown' (not vetoed to chop), down day as the scaled_fall raw value < 0; a case is the first short bet in each 10-bar grid cell of its window, the t clusters cases by UTC day with a D/(D-1) correction, and the median split puts cases strictly above the median of |forecast| in the deeper half, at or below in the shallower.
- Size: unusual move -0.16 % (t -0.10, the cases of one day together: 218 days) per case over 10 bars, -0.010 of the coin's usual move (17.84 %); normal drift in its direction -1.16 %, total -1.32 %; 288 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.099 (below 1), 218 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/086-02.c2_deep-down-day-continues_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-02.c2_deep-down-day-continues_1d`
Measure: `measure.py`
