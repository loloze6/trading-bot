---
plan: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
idea: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move of long bets (return minus coin's mean 6-bar return): -1.06701e-05; t of the mean: -0.0147854 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive)
- Supporting check: correlation of signal forecast with unusual move > 0: 0.0159484, passed: True
- Counts: cases: 1283, cases BTCUSD: 771, cases ETHUSD: 512
- Decided by: t between -2 and 2 (inconclusive rule).
- Reading: Situation = regime 'mean_reversion' (volume band) with raw dip_in_rise > 0, a falling close and a positive 168-bar return where computable in the window, on a positive forecast; a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet) in each 6-bar grid cell from each window's first row; drift is the coin's mean 6-bar grid return over all its windows; the plan's 'fewer than 30 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move -0.00 % per case over 6 bars, -0.008 of the coin's usual move (2.54 %); normal drift in its direction +0.18 %, total +0.18 %; 1283 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/unseen_2016_2017/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Measure: `measure.py`
