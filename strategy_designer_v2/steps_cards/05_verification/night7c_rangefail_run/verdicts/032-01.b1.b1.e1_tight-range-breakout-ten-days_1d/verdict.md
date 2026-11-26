---
plan: 032-01.b1.b1.e1_tight-range-breakout-ten-days_1d
idea: 032-01.b1.b1.e1_tight-range-breakout-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-day return of breakout cases over the coin's normal 10-day drift: 0.0482443; t of the mean, cases of one day summed: 3.41634 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: t <= -2; else inconclusive; fewer than 30 independent cases: not observable)
- Supporting check: OLS slope of excess 10-day return on tight post_pipeline_value: 0.00531064, passed: True
- Counts: independent cases: 259, cases: 349
- Decided by: the mean excess 10-day return is above 0 with t >= 2 and the slope on tight is above 0
- Reading: the situation is recomputed from prices (close above the max high of the 60 prior bars, 60-bar efficiency ratio smoothed by a 5-bar simple mean <= 0.3) on the active bars that have 64 prior bars inside their window, the expected side being long; a case is a bar whose forecast is >= 2 while the previous bar's forecast in the same window is 0 (a window's first bar cannot be one), the first case of each 10-bar grid cell counting from the window's first row, cases without 10 bars ahead in their window left out, and the independent cases are the distinct UTC days the cases fall on.
- Size: unusual move +4.80 % (t 3.42, the cases of one day together: 261 days) per case over 10 bars, 0.251 of the coin's usual move (16.61 %); normal drift in its direction +1.42 %, total +6.23 %; 352 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.02844 on the check folds against +0.04824 on every fold
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-01.b1.b1.e1_tight-range-breakout-ten-days_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-01.b1.b1.e1_tight-range-breakout-ten-days_1d`
Measure: `measure.py`
