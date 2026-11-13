---
plan: N1-04_rebound-after-large-drop_1d
idea: N1-04_rebound-after-large-drop
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: hit rate of next-bar return on bars with forecast >= 16 minus pooled all-bar hit rate: 0.102019; two-proportion z (pooled): 7.04569 (threshold: confirm if excess > 0 with z >= 2, reject if excess < 0 with z <= -2, over at least 100 qualifying bars)
- Supporting check: mean next-bar return on qualifying bars minus pooled all-bar mean daily return (Welch t = 3.704): 0.00622086, passed: True
- Counts: qualifying bars: 1280, all bars: 17260
- Decided by: The hit-rate excess is positive with z >= 2 over at least 100 qualifying bars (confirm rule).
- Reading: The baseline hit rate and mean are pooled over every bar with a next-bar return in all windows of all coins, the qualifying bars are pooled over all coins, the two-proportion z uses the pooled-proportion standard error, the supporting difference uses Welch's t and counts as passed when positive (the plan gives it no threshold), and the situation check counts a drop day (negative raw one-day value) with a positive forecast.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N1-04_rebound-after-large-drop_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N1-04_rebound-after-large-drop_1d`
Measure: `measure.py`
