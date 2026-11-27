---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return on forecast > 0 bars: 0.00364622; ordinary t of the mean: 6.11559 (threshold: confirm: mean > 0 with t >= 2 and slope t >= 1; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of next-day excess return on forecast: 7.66487, passed: True
- Counts: active bars: 10218
- Decided by: Mean next-day excess return above 0 with t >= 2 and a positive slope with t >= 1.
- Reading: Active bars counted as bars with forecast > 0 and a next-day close in the same window; the coin's mean daily return is over all its close-to-close returns in all windows; the plan's 'fewer than 200 is inconclusive' is reported as 'not observable' per the workflow.
- Size: unusual move +0.27 % (t 1.68, the cases of one day together: 2072 days) per case over 1 bars, 0.049 of the coin's usual move (5.44 %); normal drift in its direction +0.15 %, total +0.41 %; 8417 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/common/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound_1d`
Measure: `measure.py`
