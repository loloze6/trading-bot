---
plan: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h
idea: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 72-bar move per long case (return minus coin's normal 72-bar drift): 0.00644859; t of the mean: 3.53004 (threshold: t >= 2 confirms (with check > 0); t <= -2 rejects)
- Supporting check: mean unusual move with rise30_rec above its median minus below: 0.00941209, passed: True
- Counts: independent cases: 2442, cases above median: 1221, cases below median: 1221
- Decided by: The mean unusual move has a t of at least 2 and the supporting check is above 0.
- Reading: Cases are the first long bet per 72-bar grid cell of each window (cells from the window's first row, cases whose 72-bar return leaves the window dropped), the rise30_rec median is pooled over all cases with cases at the median left out, and fewer than 30 cases is reported as not observable.
- Size: unusual move +0.64 % per case over 72 bars, 0.074 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +1.05 %; 2442 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h`
Measure: `measure.py`
