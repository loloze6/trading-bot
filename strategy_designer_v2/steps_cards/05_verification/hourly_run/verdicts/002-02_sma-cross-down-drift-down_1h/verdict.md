---
plan: 002-02_sma-cross-down-drift-down_1h
idea: 002-02_sma-cross-down-drift-down
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: t-stat of mean of (forecast/10 x forward 24-bar excess return over window mean) on non-overlapping 24-bar blocks: 0.00048375; t of the mean: 0.431124 (threshold: confirm if t >= 2, reject if t <= -2, inconclusive otherwise or if fewer than 100 active (forecast < 0) blocks)
- Supporting check: share of active blocks with negative forward 24-bar excess return (vs 50%): 0.5, passed: False
- Counts: non-overlapping active blocks (forecast < 0): 376, non-overlapping blocks: 724
- Decided by: The main-measure t-stat lies strictly between -2 and 2, which neither confirms nor rejects.
- Reading: Each window's mean 24-bar return is the mean of the forward 24-bar returns from every bar of that window; all grid blocks (including forecast 0, whose product is 0) enter the t-stat; the supporting check passes when the share exceeds 50%.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-02_sma-cross-down-drift-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-02_sma-cross-down-drift-down_1h`
Measure: `measure.py`
