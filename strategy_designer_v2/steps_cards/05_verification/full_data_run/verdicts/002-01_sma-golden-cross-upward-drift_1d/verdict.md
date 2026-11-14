---
plan: 002-01_sma-golden-cross-upward-drift_1d
idea: 002-01_sma-golden-cross-upward-drift
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 10-bar return minus coin holding mean on forecast: 0.000202171; OLS slope t: 0.370976 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: share of positive 10-bar returns when forecast > 0 minus coin's share over all bars: -0.0214105, passed: False
- Counts: non-overlapping blocks with forecast > 0: 832, non-overlapping blocks (all): 1657
- Decided by: The t of the slope lies between -2 and 2 (inconclusive rule).
- Reading: Non-overlapping samples are positions 0,10,20,... of each window; holding is the coin's mean of those samples over all its windows; the regression is OLS with intercept on the pooled samples; the supporting check is pooled as the mean over forecast>0 samples of (positive indicator minus that coin's all-sample positive share) and passes if above zero; fewer than 100 forecast>0 blocks gives 'not observable'.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-01_sma-golden-cross-upward-drift_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-01_sma-golden-cross-upward-drift_1d`
Measure: `measure.py`
