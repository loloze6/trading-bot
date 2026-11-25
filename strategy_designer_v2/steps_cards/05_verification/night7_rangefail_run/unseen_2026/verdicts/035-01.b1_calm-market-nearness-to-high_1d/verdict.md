---
plan: 035-01.b1_calm-market-nearness-to-high_1d
idea: 035-01.b1_calm-market-nearness-to-high
fit: exact
status: not observable
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered slope of 5-bar excess return on forecast: None (threshold: slope > 0 with t >= 2 confirms (with tercile difference > 0); t <= -2 rejects)
- Supporting check: top-minus-bottom forecast tercile mean excess 5-bar return: None, passed: None
- Counts: grid cases: 751, distinct days: 62
- Decided by: the plan's minimum of 200 grid cases on at least 100 distinct days is not reached
- Reading: Cases are the non-overlapping 5-bar grid bars (positions 0, 5, 10, ... of each window) with near_high recorded, excess return = 5-bar return minus the coin's mean 5-bar grid return over all its windows; 'cases of one day summed together' is read as an OLS slope with standard errors clustered by day; terciles are three equal-count groups of the pooled cases ranked by forecast (ties by order).
- Size: unusual move +1.92 % (t 2.48, the cases of one day together: 179 days) per case over 5 bars, 0.181 of the coin's usual move (9.44 %); normal drift in its direction +0.04 %, total +1.95 %; 470 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-01.b1_calm-market-nearness-to-high_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2026/backtests/035-01.b1_calm-market-nearness-to-high_1d`
Measure: `measure.py`
