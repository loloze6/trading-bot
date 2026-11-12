---
plan: 002-02_sma-cross-down-drift-down_1h
idea: 002-02_sma-cross-down-drift-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-stat of mean of (forecast/10 x block forward 24-bar excess return over window mean 24-bar return): 0.00048375; t of the mean: 0.431124 (threshold: t-stat >= 2 confirms, <= -2 rejects, strictly between is inconclusive; fewer than 100 active blocks is inconclusive)
- Supporting check: share of active blocks with negative 24-bar excess return vs 50%: 0.5, passed: False
- Counts: non-overlapping active blocks (forecast < 0): 376, non-overlapping blocks: 724
- Decided by: Inconclusive: the main-measure t-stat is strictly between -2 and 2.
- Reading: Blocks start at positions 0, 24, 48, ... of each window with a full 24-bar forward return inside it, all blocks (including forecast 0) enter the products, the window's mean 24-bar return is the mean of the forward 24-bar returns from every bar of that window, and the supporting check passes when the negative share exceeds 50%.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-02_sma-cross-down-drift-down_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-02_sma-cross-down-drift-down_1h`
Measure: `measure.py`
