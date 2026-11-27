---
plan: 086-01.c1_first-dip-falls-over-week_1d
idea: 086-01.c1_first-dip-falls-over-week
fit: adapted
status: no effect
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual 7-bar move: -0.0150377; t of the mean, cases of one day taken together: -0.89251 (threshold: mean > 0 with day-clustered t >= 2 to confirm (with slope > 0, t >= 2); mean < 0 with t <= -2 or slope < 0 with t <= -2 to reject)
- Supporting check: OLS slope of unusual move on |forecast|: -0.00149393, passed: False
- Counts: cases: 257, distinct days: 195
- Decided by: Inconclusive: the mean or slope has |t| below 2, meeting neither confirm nor reject. No effect (common/verdicts.md): t in the idea's direction -0.893 (below 1), 257 cases (30 needed).
- Reading: Profile on a bar is read from the detector's recorded regime (not 'chop'), since its components are not recorded and their 365-bar lookback cannot be rebuilt inside a window; the streak is the recorded raw value of broken_up_run, else recomputed from closes; the case's first bet in each 7-bar grid cell is kept; the slope's t is the ordinary OLS t; the plan's 'fewer than 40 cases or days' minimum is reported as 'not observable'.
- Size: unusual move -1.50 % (t -0.89, the cases of one day together: 195 days) per case over 7 bars, -0.108 of the coin's usual move (14.39 %); normal drift in its direction -0.83 %, total -2.33 %; 257 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.893 (below 1), 257 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/086-01.c1_first-dip-falls-over-week_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-01.c1_first-dip-falls-over-week_1d`
Measure: `measure.py`
