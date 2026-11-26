---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, pooled over coins and windows (1-bar grid): 0.000285389; OLS slope t: 5.09242 (threshold: confirm: slope > 0 with t >= 2 and supporting check passing; reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return, top fifth of forecast bars minus bottom fifth: 0.00346141, passed: True
- Counts: bars with a forecast above 0: 2181, bars in the regression: 17380, bars per fifth: 3476
- Decided by: The slope is positive with t >= 2 and the top-minus-bottom fifth difference is above 0.
- Reading: Situation taken as the graded product (high-close)/(high-low) x volume / prior-20-day mean volume being above 0 with a long forecast (raw value recomputed from prices where not recorded); top and bottom fifths are the pooled bars ranked by forecast (stable sort, ties kept in record order), n//5 bars each; the 1000-bar minimum counts bars with forecast > 0 that have a next-day return, and failing it gives 'not observable'.
- Size: unusual move +0.30 % per case over 1 bars, 0.059 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.42 %; 1717 cases
Plan: `steps_cards/03_test_plan/book_reflects_idea_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d.md`
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close_1d`
Measure: `measure.py`
