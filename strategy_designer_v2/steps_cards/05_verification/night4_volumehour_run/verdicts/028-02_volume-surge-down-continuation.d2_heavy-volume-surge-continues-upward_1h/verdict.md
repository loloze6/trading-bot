---
plan: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h
idea: 028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move after a long bet (BTC and ETH pooled): -0.000284872; ordinary t of the mean: -1.37533 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, top half minus bottom half by entry forecast: None, passed: False
- Counts: cases in total: 11507, top half cases: 0, bottom half cases: 11507
- Decided by: The t lies between -2 and 2, which the plan reads as inconclusive.
- Reading: A case is the first long bet (forecast rise of >= 2 points from its lowest level since the last bet, from 0 after a flat) in each 6-bar grid cell counted from each window's first row, the drift is the coin's mean non-overlapping 6-bar return over all its windows, the supporting split puts cases above the median entry forecast in the top half and those at or below it in the bottom half, and fewer than 30 cases is read as the plan's minimum count, so not observable.
- Size: unusual move -0.03 % per case over 6 bars, -0.015 of the coin's usual move (1.98 %); normal drift in its direction +0.03 %, total +0.01 %; 11507 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.d2_heavy-volume-surge-continues-upward_1h`
Measure: `measure.py`
