---
plan: N4-01_breakout-drift-lasts_1d_oos2
idea: N4-01_breakout-drift-lasts
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar forward return after new 20-day closing highs (vs coin mean 10-bar return): 0.0687245; t of the mean: 1.34071 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 100 non-overlapping events)
- Supporting check: mean excess 10-bar return of events whose next close is below the new high (must be > 0): 0.0369813, passed: True
- Counts: non-overlapping events: 105, events with next close below the new high: 59
- Decided by: Inconclusive rule met: the t of the mean excess 10-bar return lies between -2 and 2 with at least 100 events.
- Reading: A new-high event is a bar whose recorded countdown equals 20 and has a 10-bar forward return in its window; events are kept greedily per window and one less than 10 bars after the last counted event is skipped; the coin mean uses every bar with a 10-bar forward return across all its windows; 'closes below the new high' means close[t+1] < close[t]; the supporting check does not change the status.
Plan: `steps_cards/03_test_plan/overnight_run/plans_oos/N4-01_breakout-drift-lasts_1d_oos2.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_oos/N4-01_breakout-drift-lasts_1d_oos2`
Measure: `measure.py`
