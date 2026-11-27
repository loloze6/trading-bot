---
plan: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted short-side next-day return over short bets: -0.00347581; t of the mean, cases of one day pooled: -1.03076 (threshold: confirm: mean > 0 with day-pooled t >= 2 and slope > 0; reject: mean < 0 with t <= -2; >= 100 cases on >= 50 days)
- Supporting check: OLS slope of drift-adjusted short-side next-day return on |forecast|: 0.00100244, passed: True
- Counts: cases: 403, distinct days: 100
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation checked as 1-day return > 0 and 5-day return < 0 (depth raw value, or prices where not recorded) with a short forecast, bars whose returns cannot be computed inside the window left out, the falling profile not rechecked as its 60-day return is not computable on early recorded bars; cases are short bets (rise of -forecast by >= 2 from its lowest level on the short side since the last bet, from 0 after flat or side change) on every bar (horizon 1), drift is the coin's mean 1-bar return over all its windows, and t is the mean over a standard error with deviations summed per UTC day.
- Size: unusual move -0.35 % (t -1.03, the cases of one day together: 100 days) per case over 1 bars, -0.079 of the coin's usual move (3.93 %); normal drift in its direction +0.02 %, total -0.33 %; 403 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2026/backtests/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d`
Measure: `measure.py`
