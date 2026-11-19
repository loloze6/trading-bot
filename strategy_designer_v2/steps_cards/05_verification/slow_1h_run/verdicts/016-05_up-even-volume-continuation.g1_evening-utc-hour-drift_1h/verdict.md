---
plan: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20:00-22:00 2-bar return minus mean other-hour 2-bar return: 0.000526115; Welch t: 4.4195 (threshold: confirm: difference > 0 with Welch t >= 2 (and slope t >= 2); reject: Welch t <= -2 or slope t <= -2)
- Supporting check: t of slope of 20:00-22:00 return on vol7d at 19:00 bar (must be >= 2): 9.34557, passed: True
- Counts: daily 20:00-22:00 cases: 17241, other-hour cases: 188355, regression cases: 17233
- Decided by: Confirm rule met: the main difference is positive with Welch t >= 2 and the volatility slope has t >= 2.
- Reading: Cases are 2-bar returns on bars starting at odd UTC hours (closes on even hours) within each window with exactly 2 hours between the two closes, the bar starting at 19:00 giving the 20:00-22:00 case and all other such blocks the other-hour cases; vol7d is the recorded last_history_value at the 19:00 bar (recomputed as the std of 168 hourly returns only if it is not recorded on most of those bars, rows missing it left out). Recorded vol7d used.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h`
Measure: `measure.py`
