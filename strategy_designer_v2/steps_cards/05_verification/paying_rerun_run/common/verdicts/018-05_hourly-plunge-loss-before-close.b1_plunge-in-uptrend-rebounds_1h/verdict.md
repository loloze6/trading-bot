---
plan: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h
idea: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 72-bar move per long case (return minus coin's normal 72-bar drift): 0.00790131; t of the mean: 5.01463 (threshold: t >= 2 confirms (with check > 0); t <= -2 rejects)
- Supporting check: mean unusual move with rise30_rec above its median minus below: 0.0135983, passed: True
- Counts: independent cases: 4924, cases above median: 2462, cases below median: 2462
- Decided by: The mean unusual move has a t of at least 2 and the supporting check is above 0.
- Reading: Cases are the first long bet per 72-bar grid cell of each window (cells from the window's first row, cases whose 72-bar return leaves the window dropped), the rise30_rec median is pooled over all cases with cases at the median left out, and fewer than 30 cases is reported as not observable.
- Size: unusual move +0.79 % (t 3.16, the cases of one day together: 1728 days) per case over 72 bars, 0.080 of the coin's usual move (9.32 %); normal drift in its direction +0.66 %, total +1.45 %; 4924 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h`
Measure: `measure.py`
