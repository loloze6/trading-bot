---
plan: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d
idea: 074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted short-side next-day return over short bets: 0.00120531 (threshold: confirm: mean > 0 with day-pooled t >= 2 and slope > 0; reject: mean < 0 with t <= -2; >= 100 cases on >= 50 days)
- Supporting check: none
- Counts: cases: 64, distinct days: 58
- Decided by: The plan's minimum of 100 cases on at least 50 distinct days is not reached (64 cases on 58 days).
- Reading: Situation checked as 1-day return > 0 and 5-day return < 0 (depth raw value, or prices where not recorded) with a short forecast, bars whose returns cannot be computed inside the window left out, the falling profile not rechecked as its 60-day return is not computable on early recorded bars; cases are short bets (rise of -forecast by >= 2 from its lowest level on the short side since the last bet, from 0 after flat or side change) on every bar (horizon 1), drift is the coin's mean 1-bar return over all its windows, and t is the mean over a standard error with deviations summed per UTC day.
- Size: unusual move +0.12 % (t 0.20, the cases of one day together: 58 days) per case over 1 bars, 0.026 of the coin's usual move (7.55 %); normal drift in its direction -0.98 %, total -0.86 %; 64 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/unseen_2016_2017/backtests/074-01.b1.b1.b1.b1.d1.d1_graded-still-down-bounce-fade_1d`
Measure: `measure.py`
