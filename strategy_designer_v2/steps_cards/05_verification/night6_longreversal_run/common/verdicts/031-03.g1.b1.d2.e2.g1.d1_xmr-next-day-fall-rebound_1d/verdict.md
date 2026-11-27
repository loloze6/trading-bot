---
plan: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d
idea: 031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast: 0.000485617; OLS slope t: 5.84128 (threshold: slope t >= 2 with positive mean excess confirms; slope t <= -2 rejects)
- Supporting check: mean excess next-day return over cases > 0: 0.000760508, passed: True
- Counts: cases: 28021
- Decided by: The slope's t is 2 or more and the mean excess return over the cases is positive.
- Reading: The situation is a bar whose raw fall_z value (return over 30-day volatility) is below 0, falling back to the price return where the raw value is missing; the coin's mean daily return is the mean of all next-day returns pooled over all windows; with a 1-bar horizon every bar is on the grid; the slope's t is the ordinary least-squares t of the slope; fewer than 100 cases is reported as 'not observable' as the workflow requires.
- Size: unusual move +0.07 % (t 0.58, the cases of one day together: 2449 days) per case over 1 bars, 0.013 of the coin's usual move (5.44 %); normal drift in its direction +0.14 %, total +0.22 %; 15367 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/common/backtests/031-03.g1.b1.d2.e2.g1.d1_xmr-next-day-fall-rebound_1d`
Measure: `measure.py`
