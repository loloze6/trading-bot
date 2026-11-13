---
plan: N4-01_breakout-drift-lasts_1d
idea: N4-01_breakout-drift-lasts
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar forward return after new-high bars (event return minus coin's mean 10-bar return): 0.0159453; t of the mean: 2.04871 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; else inconclusive; minimum 100 non-overlapping events)
- Supporting check: mean excess 10-bar return of events whose next close is below the new high (must be > 0): -0.0267688, passed: False
- Counts: non-overlapping events: 559, events with next close below the new high: 299
- Decided by: The mean excess 10-bar return is above 0 with t >= 2 on non-overlapping events (confirm rule).
- Reading: A new-high bar is a bar whose recorded since_high value equals 20, events are taken in time order per coin and window with a new one counted only if it is at least 10 bars after the last counted event (so 10-bar returns do not overlap) and has a full 10-bar forward return inside its window, the coin mean is over all overlapping 10-bar returns of that coin in all its windows, the plan's 'fewer than 100 events' is treated as the minimum count giving 'not observable', and the supporting check is reported but does not change the status since the confirm and reject rules name only the main measure.
Plan: `steps_cards/03_test_plan/overnight_run/plans_rerun/N4-01_breakout-drift-lasts_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N4-01_breakout-drift-lasts_1d`
Measure: `measure.py`
