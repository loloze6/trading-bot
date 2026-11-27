---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of demeaned 7-bar forward return on raw 7-day return, trending bars: 0.000184601; OLS slope t: 2.25236 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, with at least 100 independent cases)
- Supporting check: timing part of book's mean daily gain above 0: 0.000832235, passed: True
- Counts: independent grid cases in the regime: 3634
- Decided by: The slope's t is 2 or more with at least 100 independent cases and the timing gain is above 0.
- Reading: Grid bars are positions 0,7,14,... of each window kept when regime is 'trending' with a 7-bar forward return inside the window, the coin mean is the mean of all its grid 7-bar returns over all windows, the book of each coin is its postRebalance_total_value at each day's last bar averaged across coins per day, and the plan's 'fewer than 100 cases' is reported as not observable.
- Size: unusual move +1.14 % (t 2.20, the cases of one day together: 1273 days) per case over 7 bars, 0.070 of the coin's usual move (14.68 %); normal drift in its direction +1.16 %, total +2.30 %; 3311 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d`
Measure: `measure.py`
