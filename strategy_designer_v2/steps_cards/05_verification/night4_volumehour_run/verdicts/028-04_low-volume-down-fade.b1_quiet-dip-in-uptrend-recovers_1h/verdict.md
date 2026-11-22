---
plan: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
idea: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move of long bets (return minus coin's mean 6-bar return): 0.00126412; t of the mean: 4.59169 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive)
- Supporting check: correlation of signal forecast with unusual move > 0: 0.0102587, passed: True
- Counts: cases: 4986, cases BTCUSD: 2534, cases ETHUSD: 2452
- Decided by: Mean unusual move above 0 with t >= 2 and a positive forecast/move correlation (confirm rule).
- Reading: Situation = regime 'mean_reversion' (volume band) with raw dip_in_rise > 0, a falling close and a positive 168-bar return where computable in the window, on a positive forecast; a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet) in each 6-bar grid cell from each window's first row; drift is the coin's mean 6-bar grid return over all its windows; the plan's 'fewer than 30 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.13 % per case over 6 bars, 0.063 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.16 %; 4986 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Measure: `measure.py`
