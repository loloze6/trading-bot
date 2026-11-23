---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return on forecast > 0 bars: -0.000431312; ordinary t of the mean: -0.180904 (threshold: confirm: mean > 0 with t >= 2 and slope t >= 1; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess return on forecast: -0.318541, passed: False
- Counts: active bars: 394
- Decided by: The t of the mean next-day excess return lies between -2 and 2.
- Reading: Active bars counted as bars with forecast > 0 and a next-day close in the same window; the coin's mean daily return is over all its close-to-close returns in all windows; the plan's 'fewer than 200 is inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.02 % per case over 1 bars, -0.026 of the coin's usual move (3.33 %); normal drift in its direction +0.00 %, total +0.03 %; 313 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_2026/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d`
Measure: `measure.py`
