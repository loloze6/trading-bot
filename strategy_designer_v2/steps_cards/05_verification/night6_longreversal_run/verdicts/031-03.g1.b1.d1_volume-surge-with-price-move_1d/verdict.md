---
plan: 031-03.g1.b1.d1_volume-surge-with-price-move_1d
idea: 031-03.g1.b1.d1_volume-surge-with-price-move
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 14-bar move over the cases, in the signal's direction: 0.0112724; day-clustered t: 1.69814 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, |forecast| >= median minus below median: 0.012317, passed: True
- Counts: cases: 2072, distinct days: 1038
- Decided by: The day-clustered t lies strictly between -2 and 2 (or its sign disagrees with the mean), which the plan rules inconclusive.
- Reading: ret14 is recomputed as close[t]/close[t-14]-1 inside the window and the volume ratio is the recorded last_history_value (recomputed from volume where missing), active bars where ret14 cannot be computed are left out of the agreement; a bet starts from 0 at each window's start, the first bet of each 14-bar grid cell is the case and is dropped if its 14-bar forward return leaves the window; the day-clustered t uses the per-day summed deviations without small-sample correction; the supporting check splits the cases at the median of |forecast| on the signal bar.
- Size: unusual move +1.13 % (t 1.70, the cases of one day together: 1038 days) per case over 14 bars, 0.050 of the coin's usual move (20.98 %); normal drift in its direction -0.33 %, total +0.79 %; 2072 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d1_volume-surge-with-price-move_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d1_volume-surge-with-price-move_1d`
Measure: `measure.py`
