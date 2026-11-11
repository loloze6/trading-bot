---
plan: 002-06_down-cross-to-reverse-cross-loss_1d
idea: 002-06_down-cross-to-reverse-cross-loss
fit: adapted
status: rejected
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess return: position x (next-bar return - coin's window mean daily return), pooled: -0.000889728; Newey-West t (lag 10): -3.79844 (threshold: confirm: mean > 0 with t >= 2 and supporting share > 50%; reject: mean < 0 with t <= -2)
- Supporting check: share of completed down-cross spans returning below the coin's same-length span median: 0.0666667, passed: False
- Counts: bars with a non-zero position: 9754, distinct down-cross spans: 130, completed down-cross spans: 15
- Decided by: Mean excess return below 0 with t <= -2 (reversal after down crosses): rejected.
- Reading: Excess returns use every bar (zero-position bars add zero) pooled in coin then window order for one Newey-West series, the window mean is the mean of all next-bar returns in that window; a down-cross span is a maximal run of bars with raw spread < 0 inside one window (all runs count toward the 10), a completed span is bounded by non-negative spread on both sides and its return runs from the cross bar's close to the close of the up-cross bar, compared with the median of all same-length close-to-close returns of that coin across its windows.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-06_down-cross-to-reverse-cross-loss_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-06_down-cross-to-reverse-cross-loss_1d`
Measure: `measure.py`
