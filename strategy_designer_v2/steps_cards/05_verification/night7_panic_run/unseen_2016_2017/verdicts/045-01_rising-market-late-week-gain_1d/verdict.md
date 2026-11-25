---
plan: 045-01_rising-market-late-week-gain_1d
idea: 045-01_rising-market-late-week-gain
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess position gain: position x (next-day return - coin's mean daily return), cases of a day summed across coins: -0.00148199; t of the mean (daily sums): -0.265267 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2; else inconclusive; at least 100 distinct days with a position)
- Supporting check: OLS slope of excess next-day return on forecast: 0.00025758, passed: True
- Counts: distinct days with a position: 209, bars with a position: 522
- Decided by: The t of the mean excess position gain lies between -2 and 2.
- Reading: Situation = coming bar (timestamp + 1 day) is a Friday or Saturday and the 60-bar return (trend60 raw value, or recomputed from closes where not recorded) is above 0, side long; 'bars with a position' = bars with a non-zero post-rebalance allocation and a next close in the same window; the coin's mean daily return is the mean of all its next-day returns over all windows; the slope is an OLS of the excess next-day return on the forecast on those bars.
- Size: unusual move -0.61 % (t -0.91, the cases of one day together: 120 days) per case over 1 bars, -0.095 of the coin's usual move (7.81 %); normal drift in its direction +0.97 %, total +0.36 %; 283 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/045-01_rising-market-late-week-gain_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2016_2017/backtests/045-01_rising-market-late-week-gain_1d`
Measure: `measure.py`
