---
plan: 035-01.b1_calm-market-nearness-to-high_1d
idea: 035-01.b1_calm-market-nearness-to-high
fit: exact
status: confirmed
---
Situation check: 97 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered slope of 5-bar excess return on forecast: 0.00227773; day-clustered OLS slope t: 2.53733 (threshold: slope > 0 with t >= 2 confirms (with tercile difference > 0); t <= -2 rejects)
- Supporting check: top-minus-bottom forecast tercile mean excess 5-bar return: 0.0152444, passed: True
- Counts: grid cases: 5017, distinct days: 675
- Decided by: the slope is positive with t >= 2 and the top-minus-bottom tercile difference is above 0
- Reading: Cases are the non-overlapping 5-bar grid bars (positions 0, 5, 10, ... of each window) with near_high recorded, excess return = 5-bar return minus the coin's mean 5-bar grid return over all its windows; 'cases of one day summed together' is read as an OLS slope with standard errors clustered by day; terciles are three equal-count groups of the pooled cases ranked by forecast (ties by order).
- Size: unusual move +1.09 % (t 3.46, the cases of one day together: 1430 days) per case over 5 bars, 0.095 of the coin's usual move (11.71 %); normal drift in its direction +0.18 %, total +1.27 %; 3343 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-01.b1_calm-market-nearness-to-high_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/common/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Measure: `measure.py`
