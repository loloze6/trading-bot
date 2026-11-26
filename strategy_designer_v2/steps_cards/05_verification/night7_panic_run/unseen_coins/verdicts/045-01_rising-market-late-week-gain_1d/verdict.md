---
plan: 045-01_rising-market-late-week-gain_1d
idea: 045-01_rising-market-late-week-gain
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess position gain: position x (next-day return - coin's mean daily return), cases of a day summed across coins: 0.0201076; t of the mean (daily sums): 3.25691 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; else inconclusive; at least 100 distinct days with a position)
- Supporting check: OLS slope of excess next-day return on forecast: 0.000814182, passed: True
- Counts: distinct days with a position: 494, bars with a position: 2032
- Decided by: The mean excess position gain is above 0 with t >= 2 and the slope on the forecast is above 0.
- Reading: Situation = coming bar (timestamp + 1 day) is a Friday or Saturday and the 60-bar return (trend60 raw value, or recomputed from closes where not recorded) is above 0, side long; 'bars with a position' = bars with a non-zero post-rebalance allocation and a next close in the same window; the coin's mean daily return is the mean of all its next-day returns over all windows; the slope is an OLS of the excess next-day return on the forecast on those bars.
- Size: unusual move +0.82 % (t 2.34, the cases of one day together: 338 days) per case over 1 bars, 0.138 of the coin's usual move (5.55 %); normal drift in its direction +0.18 %, total +1.00 %; 1241 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.02671 on the check folds against +0.02011 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/045-01_rising-market-late-week-gain_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/unseen_coins/backtests/045-01_rising-market-late-week-gain_1d`
Measure: `measure.py`
