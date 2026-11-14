---
plan: N4-01_breakout-drift-lasts_1d_oos3
idea: N4-01_breakout-drift-lasts
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar forward return after new-high bars (coin return minus coin's mean 10-bar return): 0.0330511; t of the mean: 1.30374 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; otherwise inconclusive; at least 100 non-overlapping events)
- Supporting check: mean excess 10-bar return of events whose next close is below the new high: 0.000841879, passed: True
- Counts: non-overlapping events: 59, events with next close below the high: 29
- Decided by: Only 59 non-overlapping new-high events pooled across coins and windows, fewer than the plan's minimum of 100.
- Reading: New-high bars are those with recorded since_high equal to 20 and a forward 10-bar return inside the window, an event is skipped when it falls fewer than 10 bars after the last counted event in the same window, the new high is that bar's close, the coin's mean is taken over all its overlapping 10-bar returns pooled across windows, the supporting check is reported but does not change the status, and fewer than 100 events gives 'not observable'.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-01_breakout-drift-lasts_1d_oos3.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-01_breakout-drift-lasts_1d_oos3`
Measure: `measure.py`
