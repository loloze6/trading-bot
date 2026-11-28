---
plan: 086-01_down-day-volume-share-drift_1d
idea: 086-01_down-day-volume-share-drift
fit: adapted
status: no effect
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar forward return minus coin mean 5-bar return on the raw centred down-day volume share: -0.00753226; OLS slope t, cells of the same day clustered: -0.267208 (threshold: confirm: slope < 0 with t <= -2 (and check passes); reject: slope > 0 with t >= +2)
- Supporting check: mean unusual 5-bar move in the short direction over grid cells with forecast < 0: -0.00177628, passed: False
- Counts: in-profile grid cells: 567, in-profile grid cells with forecast < 0: 361, days of the in-profile grid cells: 246
- Decided by: Inconclusive: the slope's t lies between -2 and +2. No effect (common/verdicts.md): t in the idea's direction +0.267 (below 1), 246 cases (30 needed).
- Reading: In-profile means regime 'unknown' (the falling calm profile not vetoed, as the detector's components are not recorded); grid cells are positions 0,5,10,... of each window with a 5-bar return inside the window, the coin's mean is over all its grid cells in all windows, the slope is OLS with an intercept and a day-clustered (CR1, G/(G-1)) standard error, and the plan's 'too few cells' case is reported as not observable.
- Size: unusual move -0.19 % (t -0.40, the cases of one day together: 358 days) per case over 5 bars, -0.015 of the coin's usual move (10.68 %); normal drift in its direction -0.51 %, total -0.70 %; 479 cases
- Effect check (common/verdicts.md): no effect: t in the idea's direction +0.267 (below 1), 246 cases (30 needed)
Plan: `steps_cards/03_test_plan/night10_fallcalmshort_run/plans/086-01_down-day-volume-share-drift_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmshort_run/backtests/086-01_down-day-volume-share-drift_1d`
Measure: `measure.py`
