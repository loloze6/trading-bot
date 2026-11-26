---
plan: 031-03.g1_volume-surge-leads-two-week-drift_1d
idea: 031-03.g1_volume-surge-leads-two-week-drift
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of the coin's demeaned 14-bar forward return on the forecast: 0.000798964; OLS slope t: 1.52533 (threshold: confirm: slope t >= 2 with timing gain > 0; reject: t <= -2; otherwise inconclusive; at least 300 grid cases with non-zero forecast)
- Supporting check: timing gain: book mean daily return minus position x coin mean daily return: 0.000437933, passed: True
- Counts: grid cases with a non-zero forecast: 1152, grid cases: 1152
- Decided by: The slope's t lies between -2 and 2.
- Reading: The regression is an OLS with intercept over every grid bar of each window (positions 0, 14, 28, ... with a full 14-bar return inside the window, zero-forecast bars included), each coin's mean 14-bar return is taken over those same grid samples of all its windows, and the timing gain averages the coins per UTC day before averaging over days.
- Size: unusual move +0.03 % (t 0.04, the cases of one day together: 699 days) per case over 14 bars, -0.005 of the coin's usual move (18.06 %); normal drift in its direction -0.10 %, total -0.06 %; 1077 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1_volume-surge-leads-two-week-drift_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1_volume-surge-leads-two-week-drift_1d`
Measure: `measure.py`
