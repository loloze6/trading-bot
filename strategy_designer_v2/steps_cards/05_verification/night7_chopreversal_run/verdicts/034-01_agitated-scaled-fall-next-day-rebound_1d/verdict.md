---
plan: 034-01_agitated-scaled-fall-next-day-rebound_1d
idea: 034-01_agitated-scaled-fall-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (forecast > 0, pooled): 0.000489291; t of slope, cases of one day taken together: 1.89384 (threshold: confirm: slope > 0 with t >= 2 and check passes; reject: slope < 0 with t <= -2)
- Supporting check: top third minus bottom third mean next-day excess return (Welch t >= 1): 0.00599139, passed: True
- Counts: cases with forecast > 0: 3753, distinct days: 1449
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Agitated bars are those whose regime is not the detector's 'chop' veto and a fall is a recorded raw component value below 0; cases are forecast > 0 bars with a next-day return inside the window; the slope is OLS with intercept, its t clustered by UTC day (CR1, G/(G-1)); thirds are the floor(n/3) lowest and highest forecasts after a stable sort.
- Size: unusual move +0.34 % (t 1.67, the cases of one day together: 1050 days) per case over 1 bars, 0.076 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.47 %; 2469 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/034-01_agitated-scaled-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/034-01_agitated-scaled-fall-next-day-rebound_1d`
Measure: `measure.py`
