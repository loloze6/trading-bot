---
plan: 017-04_postsettle-decline-after-downtrend_1h
idea: 017-04_postsettle-decline-after-downtrend
fit: adapted
status: rejected
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean per-event gain -(forecast/10) x excess 2-bar return after settlements, forecast < 0: -0.000865296; ordinary t of the mean: -5.88589 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean excess 2-bar return, largest third of |forecast| minus smallest third: -0.000987969, passed: True
- Counts: events with forecast below 0: 25389
- Decided by: The mean gain is negative with t <= -2.
- Reading: Events are the bars whose close (timestamp + 1h) is at 00:00, 08:00 or 16:00 UTC with a 2-bar forward return inside the window, pooled over all coins and windows, each coin's excess taken against its own all-window mean on the non-overlapping 2-bar grid, and thirds formed by rank of |forecast| over the pooled events; the situation is a negative 72-bar change on the held bars two hours after a settlement.
Plan: `steps_cards/03_test_plan/intraday_1h_run/plans/017-04_postsettle-decline-after-downtrend_1h.md`
Record: `steps_cards/04_backtest/intraday_1h_run/backtests/017-04_postsettle-decline-after-downtrend_1h`
Measure: `measure.py`
