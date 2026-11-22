---
plan: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h
idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 24-bar move after a forecast rise of at least 2 points: 9.13595e-05; t of the mean: 0.214549 (threshold: positive with t >= 2 on at least 30 cases to confirm; negative with t <= -2 on at least 30 cases to reject)
- Supporting check: top-half minus bottom-half mean unusual move, split at median forecast: -2.19672e-05, passed: False
- Counts: cases: 14681, top half cases: 7340, bottom half cases: 7341, cases BTCUSD: 2495, cases ETHUSD: 2513, cases LTCUSD: 2458, cases XMRUSD: 2573, cases XRPUSD: 2342, cases ZECUSD: 2300
- Decided by: The t of the mean unusual move is between -2 and 2.
- Reading: Cases are the first bet bar (forecast rise >= 2 from its lowest positive level since the last bet, reset at 0) in each 24-bar cell counted from each window's first row, with returns only inside the window; drift is the coin's mean non-overlapping 24-bar return over all its windows; the median split puts cases above the median forecast in the top half and the rest in the bottom half.
- Size: unusual move +0.01 % per case over 24 bars, 0.001 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.15 %; 14681 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b1_volume-surge-rise-more-coins_1h`
Measure: `measure.py`
