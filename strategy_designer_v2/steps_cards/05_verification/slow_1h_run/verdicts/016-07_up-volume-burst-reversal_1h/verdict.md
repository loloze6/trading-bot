---
plan: 016-07_up-volume-burst-reversal_1h
idea: 016-07_up-volume-burst-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: excess fwd 72-bar return, top third minus bottom third of |post_pipeline_value|: -0.00439564; Welch t: -1.09947 (threshold: confirm t <= -2 (with top-third mean < 0); reject t >= +2)
- Supporting check: top third mean excess fwd 72-bar return < 0: 0.000702909, passed: False
- Counts: grid samples in top third: 972, grid samples in middle third: 972, grid samples in bottom third: 972
- Decided by: Welch t lies between -2 and +2.
- Reading: Risen-regime bars are grid bars with regime 'mean_reversion' and a recorded post_pipeline_value; the coin's mean 72-bar return is the mean of its forward returns on all grid bars of all windows; thirds are cut by rank of |post_pipeline_value| pooled over coins and windows (N//3 lowest and highest); situation-check bars in a window's first 72 rows are left out.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-07_up-volume-burst-reversal_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-07_up-volume-burst-reversal_1h`
Measure: `measure.py`
