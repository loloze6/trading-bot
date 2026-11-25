---
plan: 035-01_falling-agitated-scaled-fall-rebound_1d
idea: 035-01_falling-agitated-scaled-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on the forecast, bars with forecast > 0: 0.0010552; t of the OLS slope, day-clustered (CR1): 2.62033 (threshold: confirm if slope t >= 2 and top-third check passes; reject if slope t <= -2)
- Supporting check: mean excess next-day return, top third of positive forecasts: 0.0138326, passed: True
- Counts: bars with forecast > 0: 1468, distinct days: 702, bars in top third: 490
- Decided by: The slope's t is 2 or more and the top-third mean excess return is above 0.
- Reading: The falling, agitated profile is read as the bars whose regime is 'unknown' (both chop vetoes off), the fall as the recorded raw scaled return (else the price return) below zero, the expected side long; cases are bars with forecast > 0 and a next-day close in the same window; the coin's mean daily return is the pooled mean of all its in-window close-to-close returns; the slope's t uses a CR1 day-clustered standard error; the top third is the positive forecasts at or above their 2/3 quantile; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.99 % (t 3.34, the cases of one day together: 478 days) per case over 1 bars, 0.212 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.12 %; 975 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0007151 on the check folds against +0.001055 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/035-01_falling-agitated-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/035-01_falling-agitated-scaled-fall-rebound_1d`
Measure: `measure.py`
