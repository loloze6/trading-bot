---
plan: 031-03.b1_short-horizon-continuation-after-moves_1d
idea: 031-03.b1_short-horizon-continuation-after-moves
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 10-bar forward return minus coin drift on forecast (grid cases): 0.000362049; slope t, SE clustered by day: 0.654597 (threshold: slope t >= 2 confirms (with positive timing part), t <= -2 rejects, else inconclusive)
- Supporting check: timing part of book's mean daily return before costs: 0.000465106, passed: True
- Counts: grid cases: 1691, distinct days: 304
- Decided by: The slope's t is between -2 and 2.
- Reading: Every grid bar (positions 0,10,20,... of each window with a 10-bar forward return inside it) is a case, including zero forecasts, regressed with an intercept and day-clustered SEs with the usual G/(G-1)*(N-1)/(N-K) correction; the drift is the coin's mean grid 10-bar return over all windows; the book's return before costs is the held allocation times the next bar's return, averaged over coins per day, minus the allocation times the coin's mean daily return over all windows.
- Size: unusual move +0.49 % (t 0.90, the cases of one day together: 798 days) per case over 10 bars, 0.031 of the coin's usual move (14.49 %); normal drift in its direction -0.07 %, total +0.43 %; 1519 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.b1_short-horizon-continuation-after-moves_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.b1_short-horizon-continuation-after-moves_1d`
Measure: `measure.py`
