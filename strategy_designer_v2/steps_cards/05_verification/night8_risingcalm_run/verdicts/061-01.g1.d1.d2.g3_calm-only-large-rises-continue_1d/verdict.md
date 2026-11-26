---
plan: 061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d
idea: 061-01.g1.d1.d2.g3_calm-only-large-rises-continue
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move per long case (minus coin's normal 5-day drift): 0.00387961; t of the mean, cases of one day taken together: 0.866075 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passed; reject: mean < 0 with t <= -2; fewer than 30 distinct days: not observable)
- Supporting check: mean unusual move, upper half minus lower half of entry forecasts: None, passed: None
- Counts: cases: 917, distinct days with cases: 517
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Calm is read as the regime not being the 'chop' veto and the rise from the recorded rise component (recomputed from closes where missing); a case is the first bet bar in each 5-bar grid cell of its window; t uses day-clustered standard errors with a G/(G-1) correction; upper half = cases with entry forecast above the median, lower half = at or below it; the plan's 'fewer than 30 distinct days' minimum is reported as not observable.
- Size: unusual move +0.39 % (t 0.87, the cases of one day together: 517 days) per case over 5 bars, 0.034 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +1.03 %; 917 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.g3_calm-only-large-rises-continue_1d`
Measure: `measure.py`
