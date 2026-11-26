---
plan: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
idea: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast: 0.00110534; OLS slope t: 3.71133 (threshold: slope t >= 2 with positive mean excess confirms; slope t <= -2 rejects)
- Supporting check: mean excess next-day return over cases > 0: 0.00418438, passed: True
- Counts: cases: 1355
- Decided by: The slope's t is 2 or more and the mean excess return over the cases is positive.
- Reading: The situation is a bar whose raw fall_z value (return over 30-day volatility) is below 0, falling back to the price return where the raw value is missing; the coin's mean daily return is the mean of all next-day returns pooled over all windows; with a 1-bar horizon every bar is on the grid; the slope's t is the ordinary least-squares t of the slope; fewer than 100 cases is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.61 % (t 3.62, the cases of one day together: 793 days) per case over 1 bars, 0.130 of the coin's usual move (4.65 %); normal drift in its direction +0.11 %, total +0.71 %; 793 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d`
Measure: `measure.py`
