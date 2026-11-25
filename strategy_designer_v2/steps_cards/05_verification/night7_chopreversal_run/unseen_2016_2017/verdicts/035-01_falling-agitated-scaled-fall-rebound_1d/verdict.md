---
plan: 035-01_falling-agitated-scaled-fall-rebound_1d
idea: 035-01_falling-agitated-scaled-fall-rebound
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on the forecast, bars with forecast > 0: 0.000600588; t of the OLS slope, day-clustered (CR1): 0.291901 (threshold: confirm if slope t >= 2 and top-third check passes; reject if slope t <= -2)
- Supporting check: mean excess next-day return, top third of positive forecasts: 0.00332911, passed: True
- Counts: bars with forecast > 0: 19, distinct days: 19, bars in top third: 7
- Decided by: The plan's minimum of 30 bars with forecast > 0 on at least 20 distinct days is not reached (19 bars, 19 days).
- Reading: The falling, agitated profile is read as the bars whose regime is 'unknown' (both chop vetoes off), the fall as the recorded raw scaled return (else the price return) below zero, the expected side long; cases are bars with forecast > 0 and a next-day close in the same window; the coin's mean daily return is the pooled mean of all its in-window close-to-close returns; the slope's t uses a CR1 day-clustered standard error; the top third is the positive forecasts at or above their 2/3 quantile; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.00 % (t 0.01, the cases of one day together: 12 days) per case over 1 bars, -0.030 of the coin's usual move (6.78 %); normal drift in its direction +0.86 %, total +0.87 %; 12 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/035-01_falling-agitated-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/unseen_2016_2017/backtests/035-01_falling-agitated-scaled-fall-rebound_1d`
Measure: `measure.py`
