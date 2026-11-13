---
plan: N4-01_breakout-drift-lasts_1d
idea: N4-01_breakout-drift-lasts
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar return after new 20-day closing highs: 0.0159453; t of the mean: 2.04871 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects; at least 100 events)
- Supporting check: mean excess 10-bar return, events whose next close is below the new high: -0.0267688, passed: False
- Counts: non-overlapping events: 559, events with next close below the high: 299
- Decided by: The mean excess 10-bar return is above 0 with t >= 2 on non-overlapping events.
- Reading: Situation bars are those with the recorded countdown above 0 and the expected side is long; a new-high event is a bar whose recorded value equals 20; events are made non-overlapping per coin and window by keeping an event only if it is at least 10 bars after the last kept one; the coin's mean 10-bar return is taken over every bar with a within-window 10-bar return, across all its windows; the supporting check takes events whose next close is below the new-high close.
Plan: `steps_cards/03_test_plan/overnight_run/plans_rerun/N4-01_breakout-drift-lasts_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-01_breakout-drift-lasts_1d`
Measure: `measure.py`
