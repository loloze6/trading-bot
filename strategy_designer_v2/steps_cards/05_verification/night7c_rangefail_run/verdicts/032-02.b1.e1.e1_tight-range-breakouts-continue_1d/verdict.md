---
plan: 032-02.b1.e1.e1_tight-range-breakouts-continue_1d
idea: 032-02.b1.e1.e1_tight-range-breakouts-continue
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 20-day unusual move on the case's forecast: -0.00338844; slope t, clustered by day: -0.567362 (threshold: slope > 0 with t >= 2 confirms (with mean unusual move > 0); slope < 0 with t <= -2 rejects)
- Supporting check: mean unusual 20-day move over all cases > 0: 0.0482886, passed: True
- Counts: cases: 255, distinct days: 196
- Decided by: The slope t lies between -2 and 2: inconclusive.
- Reading: The breakout is recomputed from the window's own closes where 60 prior closes exist in the window and read from the recorded regime ('trending') on earlier bars; a case is the first bet (a rise of the long forecast of at least the default 2-point band from its low since the last bet) in each 20-bar grid cell of a window, on a break bar, with a full 20-bar return inside the window; the normal drift is the coin's mean 20-bar return on the grid of all its windows; the slope t uses OLS with standard errors clustered by UTC day; the plan's 'fewer than 30 cases or days' rule is reported as 'not observable'.
- Size: unusual move +4.83 % (t 2.04, the cases of one day together: 196 days) per case over 20 bars, 0.179 of the coin's usual move (21.24 %); normal drift in its direction +2.53 %, total +7.35 %; 255 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1_tight-range-breakouts-continue_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1_tight-range-breakouts-continue_1d`
Measure: `measure.py`
