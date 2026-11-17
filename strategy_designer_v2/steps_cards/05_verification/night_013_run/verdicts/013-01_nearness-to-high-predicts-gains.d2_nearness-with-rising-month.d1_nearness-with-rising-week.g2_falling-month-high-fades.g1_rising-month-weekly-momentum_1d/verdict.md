---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of demeaned 7-bar forward return on raw 7-day return, trending bars: 0.000480893; OLS slope t: 3.46685 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, with at least 100 independent cases)
- Supporting check: timing part of book's mean daily gain above 0: 0.000397192, passed: True
- Counts: independent grid cases in the regime: 1215
- Decided by: The slope's t is 2 or more with at least 100 independent cases and the timing gain is above 0.
- Reading: Grid bars are positions 0,7,14,... of each window kept when regime is 'trending' with a 7-bar forward return inside the window, the coin mean is the mean of all its grid 7-bar returns over all windows, the book of each coin is its postRebalance_total_value at each day's last bar averaged across coins per day, and the plan's 'fewer than 100 cases' is reported as not observable.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d`
Measure: `measure.py`
