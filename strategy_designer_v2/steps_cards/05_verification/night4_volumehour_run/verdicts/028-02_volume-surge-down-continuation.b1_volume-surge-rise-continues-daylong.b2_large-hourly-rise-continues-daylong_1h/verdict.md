---
plan: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h
idea: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 24-bar excess return of forecast-rise cases (one per 24-bar grid cell): 0.000949523; t of the mean: 1.48708 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess return above-median forecast minus at-or-below-median: 6.83774e-06, passed: True
- Counts: cases: 4454, active bars: 21568
- Decided by: The t lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: Situation = positive hourly return (raw 'rise' value, else close-to-close) on volume >= mean of prior 720 bars recomputed in-window (recorded regime used where 720 prior bars are absent), side long; a case is the first forecast rise of >= 2 points (from its lowest long level since the last bet, 0 after flat) in each 24-bar cell of each window, cases whose 24-bar return leaves the window are dropped, both coins pooled, each coin's drift from its non-overlapping 24-bar grid returns over all windows, and the plan's 'fewer than 30 cases' is reported as not observable.
- Size: unusual move +0.09 % per case over 24 bars, 0.021 of the coin's usual move (4.12 %); normal drift in its direction +0.15 %, total +0.24 %; 4454 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.b2_large-hourly-rise-continues-daylong_1h`
Measure: `measure.py`
