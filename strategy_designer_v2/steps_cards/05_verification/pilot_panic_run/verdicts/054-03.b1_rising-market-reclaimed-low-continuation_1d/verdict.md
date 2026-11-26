---
plan: 054-03.b1_rising-market-reclaimed-low-continuation_1d
idea: 054-03.b1_rising-market-reclaimed-low-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed (short) unusual 10-bar move vs coin's normal drift: 0.0262594; t of the mean, same-day cases as one: 1.10596 (threshold: confirm: mean > 0 with t >= 2 and depth slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: slope of signed unusual move on |forecast|: 0.00313485, passed: True
- Counts: cases: 52, distinct days: 43
- Decided by: Inconclusive: the t lies between -2 and 2.
- Reading: Rising profile recomputed as 60-bar close change > 10% inside the window (regime column used where 60 prior bars are missing), pierce from the recorded raw value else from prices; a case is the first short-side bet (forecast rise of >= 2 points) in each 10-bar grid cell with a full 10-bar return in its window, day-clustered t uses summed deviations per UTC day with a G/(G-1) correction.
- Size: unusual move +2.63 % (t 1.12, the cases of one day together: 43 days) per case over 10 bars, 0.158 of the coin's usual move (14.49 %); normal drift in its direction -1.16 %, total +1.46 %; 52 cases
Plan: `steps_cards/03_test_plan/pilot_panic_run/plans/054-03.b1_rising-market-reclaimed-low-continuation_1d.md`
Record: `steps_cards/04_backtest/pilot_panic_run/backtests/054-03.b1_rising-market-reclaimed-low-continuation_1d`
Measure: `measure.py`
