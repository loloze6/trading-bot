---
plan: 035-01.b1_calm-market-nearness-to-high_1d
idea: 035-01.b1_calm-market-nearness-to-high
fit: exact
status: not observable
---
Situation check: 96 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered slope of 5-bar excess return on forecast: None (threshold: slope > 0 with t >= 2 confirms (with tercile difference > 0); t <= -2 rejects)
- Supporting check: top-minus-bottom forecast tercile mean excess 5-bar return: None, passed: None
- Counts: grid cases: 170, distinct days: 119
- Decided by: the plan's minimum of 200 grid cases on at least 100 distinct days is not reached
- Reading: Cases are the non-overlapping 5-bar grid bars (positions 0, 5, 10, ... of each window) with near_high recorded, excess return = 5-bar return minus the coin's mean 5-bar grid return over all its windows; 'cases of one day summed together' is read as an OLS slope with standard errors clustered by day; terciles are three equal-count groups of the pooled cases ranked by forecast (ties by order).
- Size: unusual move -0.74 % (t -0.87, the cases of one day together: 110 days) per case over 5 bars, -0.051 of the coin's usual move (17.00 %); normal drift in its direction +1.62 %, total +0.89 %; 130 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-01.b1_calm-market-nearness-to-high_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Measure: `measure.py`
