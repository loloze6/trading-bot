---
plan: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h
idea: 018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean 72-bar unusual move (return minus coin's mean 72-bar return): 0.0131931; t of mean of forecast x unusual move: 4.05407 (threshold: confirm: > 0 with t >= 2 and top-minus-bottom third > 0; reject: < 0 with t <= -2)
- Supporting check: top-third minus bottom-third mean unusual move (by forecast): 0.0275597, passed: True
- Counts: cases over all coins and windows: 1251
- Decided by: The weighted mean unusual move is > 0 with t >= 2 and the top-minus-bottom-third difference is > 0.
- Reading: The 30-day return is recomputed from closes 720 bars back inside each window and taken from the recorded regime where the window has fewer than 720 earlier bars; the coin's mean 72-bar return is the mean over all grid bars of all its windows; thirds are formed on all cases pooled across coins, sorted by forecast and split into three near-equal groups with numpy.array_split.
- Size: unusual move +0.44 % per case over 72 bars, 0.053 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.85 %; 3181 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.d1_sharp-dip-in-uptrend-rebounds.e1_dip-depth-in-uptrend-rebounds_1h`
Measure: `measure.py`
