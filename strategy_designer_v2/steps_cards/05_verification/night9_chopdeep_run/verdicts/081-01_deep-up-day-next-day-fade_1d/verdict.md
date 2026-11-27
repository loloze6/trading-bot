---
plan: 081-01_deep-up-day-next-day-fade_1d
idea: 081-01_deep-up-day-next-day-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean daily timing gain (position x (next-day return - coin mean daily return)), summed per day across coins: 0.00951687; t of the mean (daily sums): 2.94575 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: Welch t of next-day excess return, deepest third minus shallowest third by depth (pass: difference < 0 and t <= -1): -3.33071, passed: True
- Counts: up-day cases: 14361, distinct days: 2273
- Decided by: Mean daily timing gain positive with t >= 2 and the deepest-minus-shallowest Welch t <= -1.
- Reading: Up day = close above the prior close in the same window (first bar: recorded regime); position = postRebalance_current_allocation; days with no case are left out of the daily series; terciles are pooled over all coins on the raw depth (last_history_value, most negative = deepest); the minimum is read as at least 300 cases and at least 100 distinct days, either failing gives not observable.
- Size: unusual move +0.36 % (t 2.76, the cases of one day together: 1648 days) per case over 1 bars, 0.069 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.20 %; 8045 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.005093 on the check folds against +0.009517 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/081-01_deep-up-day-next-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/081-01_deep-up-day-next-day-fade_1d`
Measure: `measure.py`
