---
plan: 077-03.d1_choppy-agitated-low-close-rebound_1d
idea: 077-03.d1_choppy-agitated-low-close-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean next-day excess return over cases: 0.0033918; t of weighted mean, cases summed per day: 1.19383 (threshold: mean > 0 with t >= 2 (confirm, with positive slope); mean < 0 with t <= -2 (reject))
- Supporting check: OLS slope of next-day excess return on forecast, forecast > 0: 0.000476229, passed: True
- Counts: cases: 770, distinct days: 465
- Decided by: The t of the main mean lies between -2 and 2.
- Reading: A case is a long-side forecast rise of at least 2 points from its lowest level since the last bet (reset to 0 when flat), on every bar since the horizon is 1; the excess return is the next close-to-close return minus the coin's pooled mean daily return over all its windows; the t uses the weighted mean's standard error with weighted deviations summed per UTC day (G/(G-1) factor); the plan's minimum counts map to 'not observable'; the profile is read from the recorded regime 'unknown'.
- Size: unusual move +0.03 % (t 0.15, the cases of one day together: 465 days) per case over 1 bars, 0.006 of the coin's usual move (5.33 %); normal drift in its direction +0.13 %, total +0.17 %; 770 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03.d1_choppy-agitated-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.d1_choppy-agitated-low-close-rebound_1d`
Measure: `measure.py`
