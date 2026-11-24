---
plan: 031-01.g1.b2_next-day-down-close-rebound_1d
idea: 031-01.g1.b2_next-day-down-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (next-day return minus coin mean daily return): 0.00165261; t of the mean, cases summed per day: 2.72971 (threshold: t >= 2.0 (with top third above bottom third) confirms; t <= -2.0 rejects)
- Supporting check: top-third minus bottom-third mean excess next-day return (forecast > 0): 0.00645382, passed: True
- Counts: distinct days with forecast > 0: 2220, cases in main measure: 17380, days in main measure: 2898, bars with forecast > 0 and next-day return: 8514
- Decided by: The main measure has t = 2.73 >= 2.0 and the top third's mean excess return is above the bottom third's.
- Reading: Situation = recorded raw scaled return < 0 (down day) with long side (forecast > 0); main t = mean over its standard error with case deviations summed per calendar day (K/(K-1) correction), all bars with a next-day return counted (zero forecasts add 0); thirds of forecast > 0 bars by forecast rank (ties broken by order), top = rank > 2n/3, bottom = rank <= n/3; minimum = distinct UTC days with any forecast > 0, and below it the status is 'not observable'.
- Size: unusual move +0.19 % (t 1.53, the cases of one day together: 1689 days) per case over 1 bars, 0.040 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 5626 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01.g1.b2_next-day-down-close-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.g1.b2_next-day-down-close-rebound_1d`
Measure: `measure.py`
