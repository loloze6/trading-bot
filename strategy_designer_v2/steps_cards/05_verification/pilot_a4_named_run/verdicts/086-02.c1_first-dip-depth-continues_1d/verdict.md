---
plan: 086-02.c1_first-dip-depth-continues_1d
idea: 086-02.c1_first-dip-depth-continues
fit: exact
status: no effect
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual move over 5 bars: -0.00861472; t of the mean, cases grouped by day: -0.56422 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: mean unusual move above minus below the median |forecast|: 0.0275589, passed: True
- Counts: days carrying cases: 191, cases: 252, active bars: 324
- Decided by: The t of the main measure lies between -2 and 2. No effect (common/verdicts.md): t in the idea's direction -0.564 (below 1), 191 cases (30 needed).
- Reading: The up run is recomputed from closes inside each window (strict up closes, ties break it), the rising agitated profile is read from the detector's regime 'mean_reversion' since its 60-bar trend and 365-bar volatility percentile cannot be rebuilt inside a window; a case is the first short bet (forecast rising by 2+ points on the short side) of each 5-bar grid cell; the day-grouped t uses clustered errors with a G/(G-1) correction; cases at the median |forecast| are left out of the supporting check; the plan's 30-day minimum is applied as 'not observable'.
- Size: unusual move -0.86 % (t -0.57, the cases of one day together: 191 days) per case over 5 bars, -0.078 of the coin's usual move (11.89 %); normal drift in its direction -0.60 %, total -1.46 %; 252 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.564 (below 1), 191 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_named_run/plans/086-02.c1_first-dip-depth-continues_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_named_run/backtests/086-02.c1_first-dip-depth-continues_1d`
Measure: `measure.py`
