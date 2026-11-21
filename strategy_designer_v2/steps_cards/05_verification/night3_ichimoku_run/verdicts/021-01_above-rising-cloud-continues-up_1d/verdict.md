---
plan: 021-01_above-rising-cloud-continues-up_1d
idea: 021-01_above-rising-cloud-continues-up
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 26-bar forward return over coin drift, on grid bars with forecast > 0: 0.0481015; t of the mean: 1.29715 (threshold: confirm if mean > 0 with t >= 2 (and slope t >= 2); reject if mean < 0 with t <= -2 or slope t <= -2)
- Supporting check: OLS slope t of excess return on forecast: 0.0465884, passed: False
- Counts: non-overlapping cases: 149, active bars: 4356
- Decided by: Inconclusive rule: mean excess return t between -2 and 2 and no reject condition met.
- Reading: Cloud position is recomputed from each window's prices (9/26/52, displaced 26, top edge) and the slope taken from the recorded raw slope component, falling back to the detector's 'trending' regime on bars where window history is too short to recompute; normal drift is each coin's mean 26-bar return over all grid bars of all its windows; the plan's minimum of 30 cases is applied as 'not observable' when not met.
- Size: unusual move +2.48 % per case over 26 bars, 0.056 of the coin's usual move (25.48 %); normal drift in its direction +3.88 %, total +6.36 %; 222 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-01_above-rising-cloud-continues-up_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up_1d`
Measure: `measure.py`
