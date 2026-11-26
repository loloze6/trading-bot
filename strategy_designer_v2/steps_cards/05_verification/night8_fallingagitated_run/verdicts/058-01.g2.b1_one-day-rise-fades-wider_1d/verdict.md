---
plan: 058-01.g2.b1_one-day-rise-fades-wider_1d
idea: 058-01.g2.b1_one-day-rise-fades-wider
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-day return on abs(forecast), short grid bars: -0.0019869; OLS slope t: -4.08535 (threshold: confirm at t <= -2 with the supporting check; reject at t >= +2)
- Supporting check: mean excess 3-day return below 0: -0.00855796, passed: True
- Counts: cases: 889, distinct days: 271
- Decided by: Confirm: the slope's t is -2 or less and the mean excess 3-day return over the cases is below 0.
- Reading: Cases are grid bars (positions 0, 3, 6, ... of each window) with forecast below 0 and a 3-bar forward return inside the window; the coin's mean 3-day return is the mean of its grid returns over all its windows; the slope's t is OLS slope over its standard error; the mean excess return's t is the ordinary t of the mean; the plan's 'fewer than 30 cases or days' rule is reported as not observable.
- Size: unusual move +0.43 % (t 1.01, the cases of one day together: 488 days) per case over 3 bars, 0.048 of the coin's usual move (8.85 %); normal drift in its direction -0.43 %, total -0.00 %; 1357 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure -0.00188 on the check folds against -0.001987 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1_one-day-rise-fades-wider_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1_one-day-rise-fades-wider_1d`
Measure: `measure.py`
