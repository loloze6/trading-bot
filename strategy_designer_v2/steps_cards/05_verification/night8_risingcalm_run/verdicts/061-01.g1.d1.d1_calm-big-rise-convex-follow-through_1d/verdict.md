---
plan: 061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d
idea: 061-01.g1.d1.d1_calm-big-rise-convex-follow-through
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-day return of long cases over the coin's mean 5-day return: -0.00198416; t of the mean, cases of one day together: -0.315348 (threshold: above 0 with t >= 2 to confirm, below 0 with t <= -2 to reject, over at least 30 cases)
- Supporting check: least-squares slope of excess 5-day return on forecast: 0.0127769, passed: True
- Counts: cases: 314, days: 228
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is checked as the raw volatility-scaled 1-day return (recorded big_day value, recomputed from closes where missing) at least 1.0 with a positive forecast, the choppy-calm profile not being recomputable from the record; a case is the first long bet (forecast rise of at least 2 points from its low on the long side) in each non-overlapping 5-bar grid cell of a window, its forecast is the signal bar's forecast, and the t clusters cases by UTC day with a G/(G-1) correction.
- Size: unusual move -0.20 % (t -0.32, the cases of one day together: 228 days) per case over 5 bars, -0.040 of the coin's usual move (10.60 %); normal drift in its direction +0.61 %, total +0.42 %; 314 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d1_calm-big-rise-convex-follow-through_1d`
Measure: `measure.py`
