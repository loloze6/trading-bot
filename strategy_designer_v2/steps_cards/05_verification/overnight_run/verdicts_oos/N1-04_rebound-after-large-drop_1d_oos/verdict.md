---
plan: N1-04_rebound-after-large-drop_1d_oos
idea: N1-04_rebound-after-large-drop
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: hit rate of next-bar return on forecast>=16 bars minus all-bar hit rate: 0.035459; two-proportion z: 2.04214 (threshold: positive with z >= 2 to confirm, negative with z <= -2 to reject, over at least 100 qualifying bars)
- Supporting check: mean next-bar return minus coin mean daily return (t = -0.466): -0.000933991, passed: False
- Counts: qualifying bars: 886, all bars: 12922
- Decided by: The hit-rate excess is positive with z >= 2 over at least 100 qualifying bars.
- Reading: Qualifying bars are pooled over all coins in the record (not only 6) and compared by a pooled two-proportion z-test against the share of positive next-bar returns over all bars of all windows of all coins, a zero return counts as not positive, the supporting excess is each bar's return minus its own coin's mean daily return with an ordinary t of the mean and is counted as passed when positive, and fewer than 100 qualifying bars gives 'not observable'.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N1-04_rebound-after-large-drop_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N1-04_rebound-after-large-drop_1d_oos`
Measure: `measure.py`
