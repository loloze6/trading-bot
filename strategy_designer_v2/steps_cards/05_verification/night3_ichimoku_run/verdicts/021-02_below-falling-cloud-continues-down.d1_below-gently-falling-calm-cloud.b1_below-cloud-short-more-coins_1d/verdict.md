---
plan: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d
idea: 021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of -forecast/10 x (26-bar forward return minus coin's mean 26-bar return), forecast<0, 26-bar grid: -0.00953702; t of the mean: -1.55305 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting difference < 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean excess return, |forecast| above median minus below median, must be < 0: -0.0593559, passed: True
- Counts: non-overlapping cases: 353, cases above median: 176, cases below median: 176
- Decided by: The t of the main mean lies between -2 and 2 (or is undefined), which the plan makes inconclusive.
- Reading: Cloud position recomputed from each window's own prices (cloud at t = spans computed at t-26, below = close under the lower span), cloud-slope sign taken from the recorded slope_size raw value (recomputed from prices if missing), and only active bars where both are computable enter the agreement; drift is the coin's mean 26-bar return on the non-overlapping grid of all its windows; median split is strict (cases equal to the median left out).
- Size: unusual move +4.23 % per case over 26 bars, 0.122 of the coin's usual move (32.35 %); normal drift in its direction -5.65 %, total -1.42 %; 450 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-02_below-falling-cloud-continues-down.d1_below-gently-falling-calm-cloud.b1_below-cloud-short-more-coins_1d`
Measure: `measure.py`
