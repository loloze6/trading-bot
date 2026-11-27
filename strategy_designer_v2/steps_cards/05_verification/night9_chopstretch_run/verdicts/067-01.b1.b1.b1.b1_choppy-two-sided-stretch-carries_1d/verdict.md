---
plan: 067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries_1d
idea: 067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of the 10-bar forward return minus the coin's normal 10-bar drift on the recorded forecast: 0.000566707; slope t, cases of one day clustered: 0.726486 (threshold: slope t >= 2 confirms (with both sides' mean unusual move > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: smaller of the two sides' mean unusual move in the forecast's direction (long -0.0035017386616689973, short 0.007227726060878583), must be > 0: -0.00350174, passed: False
- Counts: cases in total: 408, cases with forecast > 0: 208, cases with forecast < 0: 200, days: 187
- Decided by: The slope's t lies between -2 and 2.
- Reading: The choppy situation is |60-bar close return| <= 10 % recomputed inside each window, falling back on the recorded regime (not 'chop') for bars without 60 prior bars in the window, and the side is the sign of the raw stretch; the drift is the coin's mean 10-bar return on the non-overlapping grid of all its windows; the slope's t uses day-clustered (CR1) standard errors on cases grouped by UTC date; the plan's 'fewer cases than the minimum' is reported as not observable.
- Size: unusual move -0.05 % (t -0.09, the cases of one day together: 536 days) per case over 10 bars, -0.016 of the coin's usual move (14.49 %); normal drift in its direction +0.01 %, total -0.04 %; 717 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-01.b1.b1.b1.b1_choppy-two-sided-stretch-carries_1d`
Measure: `measure.py`
