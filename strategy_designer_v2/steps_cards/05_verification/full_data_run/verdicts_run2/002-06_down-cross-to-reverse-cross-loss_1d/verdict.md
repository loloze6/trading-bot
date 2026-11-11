---
plan: 002-06_down-cross-to-reverse-cross-loss_1d
idea: 002-06_down-cross-to-reverse-cross-loss
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled mean excess return of position x (next-bar return - window mean daily return): -0.000889728; Newey-West t (lag 10): -3.8054 (threshold: mean > 0 with t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: share of completed down-cross spans below the coin's median same-length span return: 0.0666667, passed: False
- Counts: bars with a non-zero position: 9754, distinct down-cross spans: 130, completed down-cross spans: 15
- Decided by: Mean excess return below 0 with t <= -2: rejected (reversal).
- Reading: Excess returns use every bar (zero positions included) with the coin's mean next-bar return in that window, pooled with Newey-West autocovariances taken within each coin-window only; a span is a run of raw spread < 0 inside one window, counted for the minimum whether or not it is completed, and a completed span (cross down and back up both seen) returns close at the up-cross bar over close at its first negative bar, compared with the median of all same-length close-to-close returns of that coin pooled over its windows.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-06_down-cross-to-reverse-cross-loss_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-06_down-cross-to-reverse-cross-loss_1d`
Measure: `measure.py`
