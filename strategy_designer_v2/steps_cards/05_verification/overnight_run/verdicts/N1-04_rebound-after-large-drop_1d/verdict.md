---
plan: N1-04_rebound-after-large-drop_1d
idea: N1-04_rebound-after-large-drop
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: share of positive next-bar returns on bars with forecast >= 16 minus all-bar share, pooled over coins: 0.102019; two-proportion z (pooled variance): 7.04569 (threshold: confirm if hit-rate excess > 0 with z >= 2, reject if excess < 0 with z <= -2, over at least 100 qualifying bars; otherwise inconclusive)
- Supporting check: mean next-bar return on qualifying bars minus mean of all bars (Welch t): 0.00622086, passed: None
- Counts: qualifying bars: 1280
- Decided by: Confirm rule met: the hit-rate excess is positive with z >= 2 over at least 100 qualifying bars.
- Reading: Qualifying bars and the baseline (all bars with a next close in the same window) are each pooled over all coins and windows, a positive return is strictly > 0, the baseline includes the qualifying bars, the supporting check has no threshold so its passed is null, and the plan's '<100 bars' case is reported as not observable per the instructions.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-04_rebound-after-large-drop_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-04_rebound-after-large-drop_1d`
Measure: `measure.py`
