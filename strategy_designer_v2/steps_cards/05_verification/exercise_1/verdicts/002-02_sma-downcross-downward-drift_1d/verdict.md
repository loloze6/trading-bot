---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 10-bar fwd return on short blocks minus all blocks (pooled, %): 0.466185 (threshold: confirm if <= -1.0% per 10 bars with t <= -2 (Welch, non-overlapping blocks); reject if >= 0; inconclusive in between or |t| < 2)
- Supporting check: falling share on short blocks minus unconditional (points, need >= 10): 3.15271, passed: False
- Cases: 29
- Decided by: Rejected: the conditional-minus-unconditional difference is 0 or above, or the falling share on short bars is not above the unconditional share.
- Reading: Non-overlapping 10-bar blocks start at each window's first bar, a block is short when the forecast at its start bar is below 0, the t-stat is Welch's t between short-block and all-block returns, and a downward cross is a forecast move from >= 0 to < 0 inside a window.
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
