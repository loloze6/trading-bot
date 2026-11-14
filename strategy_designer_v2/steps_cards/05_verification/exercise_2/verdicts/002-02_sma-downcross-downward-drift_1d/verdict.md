---
plan: 002-02_sma-downcross-downward-drift_1d
idea: 002-02_sma-downcross-downward-drift
fit: adapted
status: rejected
---
Evidence:
- Main measure: mean 10-bar fwd return on short bars minus mean over all bars (non-overlapping blocks): 0.00466185 (threshold: at most -1.0% per 10 bars with t-stat <= -2 to confirm; 0 or above rejects)
- Supporting check: falling share on short blocks minus falling share on all blocks: 0.0315271, passed: False
- Cases: 29
- Decided by: Rejected: the conditional-minus-unconditional difference is 0 or above, or the falling share on short bars is not above the unconditional share.
- Reading: Blocks are non-overlapping 10-bar returns starting at bars 0,10,20,... of each window, a block is short when the forecast at its start bar is below 0, the t-stat is the difference divided by the standard error of the short-block returns, a downward cross is each entry of the forecast into negative values within a window (including a window opening short), minimum counts are checked before confirm, and reject takes precedence over the |t|<2 inconclusive rule (t-stat = 0.296, all blocks = 70, crosses = 5).
Plan: `steps_cards/03_test_plan/plans/002-02_sma-downcross-downward-drift_1d.md`
Record: `steps_cards/04_backtest/backtests/002-02_sma-downcross-downward-drift_1d`
Measure: `measure.py`
