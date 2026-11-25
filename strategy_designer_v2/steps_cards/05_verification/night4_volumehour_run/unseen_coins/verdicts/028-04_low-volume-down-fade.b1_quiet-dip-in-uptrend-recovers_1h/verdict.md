---
plan: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h
idea: 028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move of long bets (return minus coin's mean 6-bar return): 0.00107454; t of the mean: 5.72622 (threshold: confirm: mean > 0 with t >= 2 and check passes; reject: mean < 0 with t <= -2; fewer than 30 cases inconclusive)
- Supporting check: correlation of signal forecast with unusual move > 0: 0.000171775, passed: True
- Counts: cases: 22563, cases AAVEUSD: 1119, cases ADAUSD: 1800, cases AVAXUSD: 895, cases DOGEUSD: 1330, cases INJUSD: 979, cases LINKUSD: 1911, cases LTCUSD: 2306, cases NEARUSD: 807, cases ONDOUSD: 365, cases SOLUSD: 1396, cases SUIUSD: 589, cases TAOUSD: 391, cases TRXUSD: 1343, cases UNIUSD: 1262, cases XMRUSD: 2318, cases XRPUSD: 2108, cases ZECUSD: 1644
- Decided by: Mean unusual move above 0 with t >= 2 and a positive forecast/move correlation (confirm rule).
- Reading: Situation = regime 'mean_reversion' (volume band) with raw dip_in_rise > 0, a falling close and a positive 168-bar return where computable in the window, on a positive forecast; a case is the first bet (forecast rise >= 2 from its lowest long level since the last bet) in each 6-bar grid cell from each window's first row; drift is the coin's mean 6-bar grid return over all its windows; the plan's 'fewer than 30 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.11 % (t 3.28, the cases of one day together: 2343 days) per case over 6 bars, 0.038 of the coin's usual move (2.81 %); normal drift in its direction +0.04 %, total +0.15 %; 22563 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0007379 on the check folds against +0.001075 on every fold
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/unseen_coins/backtests/028-04_low-volume-down-fade.b1_quiet-dip-in-uptrend-recovers_1h`
Measure: `measure.py`
