---
plan: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
idea: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move of long bets (return minus coin's mean 6-bar return): 0.00111898; t of the mean: 6.57897 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive)
- Supporting check: correlation of signal forecast with unusual move > 0: 0.00438511, passed: True
- Counts: cases: 26047, cases AAVEUSD: 1119, cases ADAUSD: 1800, cases AVAXUSD: 895, cases BTCUSD: 3483, cases DOGEUSD: 1330, cases ETHUSD: 3160, cases INJUSD: 979, cases LTCUSD: 2757, cases NEARUSD: 765, cases ONDOUSD: 365, cases SUIUSD: 589, cases TAOUSD: 285, cases TRXUSD: 1343, cases XMRUSD: 2757, cases XRPUSD: 2408, cases ZECUSD: 2012
- Decided by: Mean unusual move above 0 with t >= 2 and a positive forecast/move correlation (confirm rule).
- Reading: Situation = regime 'mean_reversion' (volume band) with raw dip_in_rise > 0, a falling close and a positive 168-bar return where computable in the window, on a positive forecast; a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet) in each 6-bar grid cell from each window's first row; drift is the coin's mean 6-bar grid return over all its windows; the plan's 'fewer than 30 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.11 % (t 3.91, the cases of one day together: 3057 days) per case over 6 bars, 0.042 of the coin's usual move (2.75 %); normal drift in its direction +0.05 %, total +0.17 %; 26047 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/common/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Measure: `measure.py`
