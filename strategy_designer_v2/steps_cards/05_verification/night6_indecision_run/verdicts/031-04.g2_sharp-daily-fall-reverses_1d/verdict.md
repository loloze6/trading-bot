---
plan: 031-04.g2_sharp-daily-fall-reverses_1d
idea: 031-04.g2_sharp-daily-fall-reverses
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day return minus coin mean on forecast (forecast > 0): 0.00032777; slope t, clustered by day: 2.17335 (threshold: confirm if slope t >= 2 and timing gain > 0; reject if t <= -2)
- Supporting check: book timing gain before costs (mean daily): 0.000541055, passed: True
- Counts: bars with forecast > 0: 8514, distinct days among them: 2199
- Decided by: The slope's t is 2 or more and the timing gain is above 0.
- Reading: The slope is an OLS with intercept and day-clustered (CR1) standard errors over bars with forecast > 0 that have a next bar in the same window, and the timing gain is the before-cost daily book (position after trade x next-bar return, averaged over coins per day) minus position x coin mean return.
- Size: unusual move +0.19 % (t 1.51, the cases of one day together: 1704 days) per case over 1 bars, 0.039 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 5665 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-04.g2_sharp-daily-fall-reverses_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-04.g2_sharp-daily-fall-reverses_1d`
Measure: `measure.py`
