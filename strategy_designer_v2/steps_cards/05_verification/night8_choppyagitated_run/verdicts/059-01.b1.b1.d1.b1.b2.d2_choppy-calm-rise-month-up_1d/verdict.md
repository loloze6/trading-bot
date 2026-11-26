---
plan: 059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up_1d
idea: 059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 7-bar forward return (forecast > 0): 0.00916459; t of the weighted mean, cases of one day taken together: 0.703529 (threshold: above 0 with day-clustered t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: top third minus bottom third by forecast, mean excess 7-bar return (Welch t): 0.0379358, passed: True
- Counts: cases: 278, distinct days: 130
- Decided by: The t lies between -2 and +2 (or its sign disagrees with the mean), which is inconclusive.
- Reading: Cases are grid bars (positions 0, 7, 14, ... of each window) with forecast > 0 and a 7-bar forward close inside the window; the coin's mean is over all its windows' grid returns; thirds are floor(n/3) cases sorted by forecast (ties by coin and time); the supporting check passes on a difference above 0, with its Welch t reported.
- Size: unusual move +0.82 % (t 1.21, the cases of one day together: 368 days) per case over 7 bars, 0.059 of the coin's usual move (12.84 %); normal drift in its direction +0.96 %, total +1.78 %; 550 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b2.d2_choppy-calm-rise-month-up_1d`
Measure: `measure.py`
