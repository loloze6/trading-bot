---
plan: 086-01.c1_forceful-turn-day-continues_1d
idea: 086-01.c1_forceful-turn-day-continues
fit: exact
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of the cases (long): -0.00176964; t of the mean, cases clustered by day: -0.279885 (threshold: mean > 0 with day-clustered t >= 2 to confirm; t <= -2 to reject)
- Supporting check: OLS slope of unusual move on post_pipeline_value of upday: 0.00104761, passed: True
- Counts: cases: 370, distinct days: 245
- Decided by: Inconclusive: the mean t lies between -2 and 2 and the slope t is above -2. No effect (common/verdicts.md): t in the idea's direction -0.280 (below 1), 370 cases (30 needed).
- Reading: Break bars are recomputed from closes inside each window (an up close after at least two strict down closes), bars without three prior closes in the window are left out of the agreement, and the profile vetoes (365-bar volatility percentile) cannot be rebuilt from the recorded bars so only the break and the long side are checked; a case is the first bet in each 3-bar grid cell (positions 0,3,6,... of its window), the drift is the coin's mean non-overlapping 3-bar return over all its windows, the mean's t clusters cases by UTC day (deviations summed per day, G/(G-1) correction), the slope's t is the ordinary least-squares t, and fewer than 30 cases or 30 days gives 'not observable'.
- Size: unusual move -0.18 % (t -0.28, the cases of one day together: 245 days) per case over 3 bars, -0.027 of the coin's usual move (8.55 %); normal drift in its direction +0.40 %, total +0.22 %; 370 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction -0.280 (below 1), 370 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_riseagilong_run/plans/086-01.c1_forceful-turn-day-continues_1d.md`
Record: `steps_cards/04_backtest/night10_riseagilong_run/backtests/086-01.c1_forceful-turn-day-continues_1d`
Measure: `measure.py`
