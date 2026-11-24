---
plan: 033-01.b1_range-position-more-coins_1d
idea: 033-01.b1_range-position-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-bar excess return on forecast: 0.000424386; t, same-day cases summed (day-clustered): 1.3861 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2; else inconclusive; minimum 500 grid cases on 100 distinct days)
- Supporting check: mean excess return, forecast > +10 minus forecast < -10: 0.0108572, passed: True
- Counts: grid cases: 7270, distinct days: 617
- Decided by: The slope's t lies between -2 and 2.
- Reading: Every grid bar (positions 0, 5, 10, ... of each window that have a close 5 bars later) with a forecast is a case. The slope is OLS with an intercept, and its t uses residual scores summed per UTC day with a G/(G-1) correction. The drift is each coin's mean grid 5-bar return over all its windows. A supporting check with an empty group fails.
- Size: unusual move +0.55 % (t 1.92, the cases of one day together: 1770 days) per case over 5 bars, 0.041 of the coin's usual move (12.35 %); normal drift in its direction -0.06 %, total +0.49 %; 6244 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-01.b1_range-position-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-01.b1_range-position-more-coins_1d`
Measure: `measure.py`
