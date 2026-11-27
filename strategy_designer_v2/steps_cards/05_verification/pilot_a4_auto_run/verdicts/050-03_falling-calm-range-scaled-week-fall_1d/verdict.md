---
plan: 050-03_falling-calm-range-scaled-week-fall_1d
idea: 050-03_falling-calm-range-scaled-week-fall
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move in the short direction: 0.000743912; t of the mean (per-day summed deviations): 0.189268 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: mean unusual move, larger-|forecast| half minus smaller half: 0.00120703, passed: True
- Counts: distinct case days: 414, cases: 649
- Decided by: The t of the mean unusual move lies between -2 and 2 (or its sign disagrees with the mean). No effect (common/verdicts.md): t in the idea's direction +0.189 (below 1), 414 cases (30 needed).
- Reading: Situation = 7-day close-to-close return below 0 inside the window (the raw scaled_fall sign where the 7 prior bars are not in the window) on bars whose regime is 'trending' (the profile vetoes give 'chop'), side short; cases are short-side bets of >= 2 forecast points, the first one per 3-bar grid cell from each window's first row; the mean unusual move is the mean over cases and its t is over per-day summed deviations; the median split puts |forecast| above the median in the larger half, the rest in the smaller.
- Size: unusual move +0.07 % (t 0.19, the cases of one day together: 414 days) per case over 3 bars, 0.007 of the coin's usual move (8.29 %); normal drift in its direction -0.18 %, total -0.10 %; 649 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.189 (below 1), 414 cases (30 needed)
Plan: `steps_cards/03_test_plan/pilot_a4_auto_run/plans/050-03_falling-calm-range-scaled-week-fall_1d.md`
Record: `steps_cards/04_backtest/pilot_a4_auto_run/backtests/050-03_falling-calm-range-scaled-week-fall_1d`
Measure: `measure.py`
