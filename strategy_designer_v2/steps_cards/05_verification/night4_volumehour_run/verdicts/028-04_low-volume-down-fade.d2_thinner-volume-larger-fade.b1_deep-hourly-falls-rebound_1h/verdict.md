---
plan: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h
idea: 028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move after long bets, both coins: 0.000316049; t of the mean: 3.44565 (threshold: confirm: mean > 0 with t >= 2 and top-minus-bottom tercile > 0; reject: mean < 0 with t <= -2)
- Supporting check: top tercile minus bottom tercile mean unusual move: 0.000519506, passed: True
- Counts: non-overlapping cases across both coins: 26615, cases BTCUSD: 13227, cases ETHUSD: 13388
- Decided by: The mean unusual move is positive with t >= 2 and the top tercile beats the bottom tercile.
- Reading: Cases are the first bet (long-forecast rise of >= 2 points from its lowest level since the last bet, reset at 0) in each 3-bar grid cell of each window, counted as the plan's non-overlapping cases; drift is each coin's mean non-overlapping 3-bar return over all its windows; terciles are equal-count splits of the pooled cases ranked by forecast at the signal bar.
- Size: unusual move +0.03 % per case over 3 bars, 0.023 of the coin's usual move (1.41 %); normal drift in its direction +0.02 %, total +0.05 %; 26615 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-04_low-volume-down-fade.d2_thinner-volume-larger-fade.b1_deep-hourly-falls-rebound_1h`
Measure: `measure.py`
