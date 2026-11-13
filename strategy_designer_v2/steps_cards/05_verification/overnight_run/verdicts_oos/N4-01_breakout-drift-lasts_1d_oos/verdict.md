---
plan: N4-01_breakout-drift-lasts_1d_oos
idea: N4-01_breakout-drift-lasts
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar forward return after new-high bars (minus coin's mean 10-bar return), non-overlapping, pooled: 0.0213517; t of the mean: 2.22898 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 100 non-overlapping events)
- Supporting check: mean excess 10-bar return of events whose next close is below the new high: -0.0366313, passed: False
- Counts: non-overlapping events: 384, events with next close below the new high: 188
- Decided by: Mean excess 10-bar return 0.0214 > 0 with t = 2.23 >= 2 over 384 non-overlapping events.
- Reading: A new-high bar is a bar whose recorded countdown equals 20 and that has a 10-bar forward return inside its window; within each window, events are taken in time order and one less than 10 bars after the last counted event is skipped; the coin's mean is over every bar with a 10-bar return in all its windows; the new high is that bar's close; the supporting check is reported only and does not change the status.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-01_breakout-drift-lasts_1d_oos.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-01_breakout-drift-lasts_1d_oos`
Measure: `measure.py`
