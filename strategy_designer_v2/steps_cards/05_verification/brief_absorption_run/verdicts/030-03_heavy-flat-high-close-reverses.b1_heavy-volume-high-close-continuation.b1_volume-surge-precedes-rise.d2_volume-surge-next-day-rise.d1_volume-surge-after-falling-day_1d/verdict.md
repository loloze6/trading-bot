---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return on forecast > 0 bars: 0.00401162; t of the weighted mean: 4.88004 (threshold: confirm: > 0 with t >= 2 (and upper half beats lower half); reject: < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean next-day excess return: 0.00350968, passed: True
- Counts: bars with forecast > 0: 8514, upper half bars: 4257, lower half bars: 4257
- Decided by: The forecast-weighted mean excess return is above 0 with t >= 2 and the upper half beats the lower half.
- Reading: Down day read as a negative raw component value (price return where missing); t is the weighted mean over its weighted standard error (sqrt(n/(n-1)) * sqrt(sum w^2 (x-m)^2) / sum w); the upper half is forecast > median, the lower half forecast <= median; with a 1-bar horizon every bar is a grid cell.
- Size: unusual move +0.23 % per case over 1 bars, 0.047 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.35 %; 4744 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d`
Measure: `measure.py`
