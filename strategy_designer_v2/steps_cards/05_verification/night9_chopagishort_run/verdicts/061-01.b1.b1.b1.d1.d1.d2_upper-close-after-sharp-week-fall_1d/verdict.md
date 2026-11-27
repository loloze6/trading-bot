---
plan: 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall_1d
idea: 061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction 3-bar return minus the coin's normal 3-bar drift: 0.00437401; t of the mean, cases pooled by day: 0.783645 (threshold: mean > 0 with day-pooled t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: excess return of cases with |forecast| above median minus below median: -0.0059064, passed: False
- Counts: cases: 1255, cases on distinct days: 423, cases above median |forecast|: 627, cases below median |forecast|: 627
- Decided by: The day-pooled t lies between -2 and 2 (or its sign disagrees with the mean's), meeting neither rule.
- Reading: A case is the first short bet (forecast magnitude rising >= 2 points from its lowest level since the last bet, reset at flat) in each non-overlapping 3-bar grid cell of a window, measured from its close to the close 3 bars later within the window, drift being the coin's mean non-overlapping 3-bar return over all its windows; the t uses day-clustered deviations with a D/(D-1) correction; median ties are left out of the supporting check; and the plan's 'fewer than 30 cases on distinct days' is applied as the minimum count giving 'not observable'.
- Size: unusual move +0.44 % (t 0.78, the cases of one day together: 423 days) per case over 3 bars, 0.061 of the coin's usual move (9.14 %); normal drift in its direction -0.48 %, total -0.04 %; 1255 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d1.d1.d2_upper-close-after-sharp-week-fall_1d`
Measure: `measure.py`
