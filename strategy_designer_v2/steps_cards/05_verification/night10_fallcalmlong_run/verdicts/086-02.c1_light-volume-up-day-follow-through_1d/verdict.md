---
plan: 086-02.c1_light-volume-up-day-follow-through_1d
idea: 086-02.c1_light-volume-up-day-follow-through
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of the cases: 0.00184283; t of the mean, cases of one day pooled: 0.409461 (threshold: confirm: mean > 0 with t >= 2 (and check > 0); reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half (by forecast) mean unusual move: 0.00132069, passed: True
- Counts: cases: 568, distinct days with cases: 408
- Decided by: The main t lies between -2 and 2 and no reject rule is met. No effect (common/verdicts.md): t in the idea's direction +0.409 (below 1), 408 cases (30 needed).
- Reading: The falling-calm profile is read from the detector's regime ('mean_reversion', since the profile components are not recorded), the up day from close above the prior close, light volume from the lightness raw value below 0 (recomputed from volume when missing), active bars whose up day or ratio cannot be computed are left out; a case is the first bet (forecast rise of >= 2 from its low since the last bet) in each 5-bar grid cell with its 5-bar return from that bar's close, the day t is cluster-robust by signal date with G/(G-1) correction, the halves are strictly above/below the median case forecast, and the plan's 'fewer than 30 distinct days' minimum is reported as 'not observable' per the workflow.
- Size: unusual move +0.18 % (t 0.41, the cases of one day together: 408 days) per case over 5 bars, 0.017 of the coin's usual move (11.31 %); normal drift in its direction +0.60 %, total +0.78 %; 568 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.409 (below 1), 408 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/086-02.c1_light-volume-up-day-follow-through_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/086-02.c1_light-volume-up-day-follow-through_1d`
Measure: `measure.py`
