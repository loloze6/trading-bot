---
plan: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 72-bar unusual move (return minus coin's mean 72-bar return): 0.0123563; t of mean of forecast x unusual move: 1.12768 (threshold: confirm: > 0 with t >= 2 and top-minus-bottom third > 0; reject: < 0 with t <= -2)
- Supporting check: top-third minus bottom-third mean unusual move (by forecast): 0.0256499, passed: True
- Counts: cases over all coins and windows: 241
- Decided by: The t is between -2 and 2 (or sign and t disagree), which the plan calls inconclusive.
- Reading: The 30-day return is recomputed from closes 720 bars back inside each window and taken from the recorded regime where the window has fewer than 720 earlier bars; the coin's mean 72-bar return is the mean over all grid bars of all its windows; thirds are formed on all cases pooled across coins, sorted by forecast and split into three near-equal groups with numpy.array_split.
- Size: unusual move -0.07 % per case over 72 bars, -0.003 of the coin's usual move (15.26 %); normal drift in its direction +3.04 %, total +2.97 %; 546 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h`
Measure: `measure.py`
