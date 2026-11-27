---
plan: 035-01_falling-agitated-scaled-fall-rebound_1d
idea: 035-01_falling-agitated-scaled-fall-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on the forecast, bars with forecast > 0: 0.000657505; t of the OLS slope, day-clustered (CR1): 1.72684 (threshold: confirm if slope t >= 2 and top-third check passes; reject if slope t <= -2)
- Supporting check: mean excess next-day return, top third of positive forecasts: 0.00681244, passed: True
- Counts: bars with forecast > 0: 4200, distinct days: 1013, bars in top third: 1400
- Decided by: The slope's t is between -2 and 2, which the plan calls inconclusive.
- Reading: The falling, agitated profile is read as the bars whose regime is 'unknown' (both chop vetoes off), the fall as the recorded raw scaled return (else the price return) below zero, the expected side long; cases are bars with forecast > 0 and a next-day close in the same window; the coin's mean daily return is the pooled mean of all its in-window close-to-close returns; the slope's t uses a CR1 day-clustered standard error; the top third is the positive forecasts at or above their 2/3 quantile; the plan's minimum counts, when not reached, give 'not observable'.
- Size: unusual move +0.37 % (t 1.43, the cases of one day together: 736 days) per case over 1 bars, 0.072 of the coin's usual move (5.12 %); normal drift in its direction +0.11 %, total +0.48 %; 2677 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/035-01_falling-agitated-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/common/backtests/035-01_falling-agitated-scaled-fall-rebound_1d`
Measure: `measure.py`
