---
plan: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h
idea: 018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 72-bar move per long case (return minus coin's normal 72-bar drift): 0.00218868; t of the mean: 0.306424 (threshold: t >= 2 confirms (with check > 0); t <= -2 rejects)
- Supporting check: mean unusual move with rise30_rec above its median minus below: 0.0246557, passed: True
- Counts: independent cases: 397, cases above median: 198, cases below median: 198
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Cases are the first long bet per 72-bar grid cell of each window (cells from the window's first row, cases whose 72-bar return leaves the window dropped), the rise30_rec median is pooled over all cases with cases at the median left out, and fewer than 30 cases is reported as not observable.
- Size: unusual move +0.22 % per case over 72 bars, 0.019 of the coin's usual move (15.26 %); normal drift in its direction +3.13 %, total +3.35 %; 397 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-05_hourly-plunge-loss-before-close.b1_plunge-in-uptrend-rebounds_1h`
Measure: `measure.py`
