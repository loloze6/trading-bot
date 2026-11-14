---
plan: N4-01_breakout-drift-lasts_1d_volt
idea: N4-01_breakout-drift-lasts
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar forward return after new-high bars (event minus coin's mean 10-bar return): 0.0159453; t of the mean: 2.04871 (threshold: confirm if mean > 0 with t >= 2; reject if mean < 0 with t <= -2; at least 100 non-overlapping events)
- Supporting check: mean excess 10-bar return, events whose next bar closes below the new high: -0.0267688, passed: False
- Counts: non-overlapping events: 559, events with next close below the high: 299
- Decided by: The mean excess 10-bar return after non-overlapping new highs is above 0 with t >= 2 (confirm rule).
- Reading: A new-high bar is a recorded since_high value equal to 20 with a full 10-bar forward return in its window, an event is skipped if it lies fewer than 10 bars after the last counted event in the same window, the coin's mean is over the overlapping 10-bar forward returns of all its bars in all windows, 'closes below the new high' means the next close is below the event bar's close, and the supporting check is reported without changing the status, which the main measure alone decides.
Plan: `steps_cards/03_test_plan/overnight_run/plans_diag/N4-01_breakout-drift-lasts_1d_volt.md`
Record: `steps_cards/04_backtest/overnight_run/backtests_diag/N4-01_breakout-drift-lasts_1d_volt`
Measure: `measure.py`
