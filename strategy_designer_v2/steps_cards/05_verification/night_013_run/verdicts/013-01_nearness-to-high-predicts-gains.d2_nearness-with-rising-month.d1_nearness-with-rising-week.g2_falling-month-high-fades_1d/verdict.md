---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades
fit: exact
status: inconclusive
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 7-bar return on forecast, pooled: 0.000305746; OLS slope t: 0.423318 (threshold: t >= 2 (with supporting check) confirms; t <= -2 rejects; at least 100 cases)
- Supporting check: mean excess return, nearest third minus farthest third (must be < 0): -0.00813416, passed: True
- Counts: cases: 1177
- Decided by: The slope t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is the 30-bar close change below 0 recomputed inside each window (the detector's regime is used only on bars with fewer than 30 prior bars in the window), and the graded side is checked as the forecast rising when the bar-to-bar distance below the 364-bar high rises; the grid keeps rows with regime 'mean_reversion', each coin's mean 7-bar return is the mean of all its grid forward returns over all windows, the slope t is the OLS t of excess return on forecast, and the thirds are split by forecast rank into three equal-sized groups.
- Size: unusual move -0.12 % per case over 7 bars, -0.011 of the coin's usual move (12.44 %); normal drift in its direction +0.98 %, total +0.86 %; 754 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades_1d`
Measure: `measure.py`
