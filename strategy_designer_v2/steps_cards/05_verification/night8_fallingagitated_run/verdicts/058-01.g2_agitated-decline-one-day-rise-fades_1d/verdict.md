---
plan: 058-01.g2_agitated-decline-one-day-rise-fades_1d
idea: 058-01.g2_agitated-decline-one-day-rise-fades
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of short cases, in the short direction, before costs: 0.0033148; t of the mean, cases of one day taken together: 0.726832 (threshold: confirm: mean > 0 with day-clustered t >= 2 and larger-half minus smaller-half > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger minus smaller half of |forecast|: -0.00186107, passed: False
- Counts: cases: 694, days with cases: 379
- Decided by: the t lies between -2 and 2, which the plan calls inconclusive.
- Reading: a case is the first short bet (short size up >= 2 points from its lowest level since the last bet, reset at flat) in each 3-bar grid cell from each window's first row, with its 3-bar return inside the window; the larger half is |forecast| strictly above the median and the smaller half the rest; the day-clustered t uses the G/(G-1) correction; the profile is read from the recorded regime 'unknown'; fewer than 30 days with cases is reported as not observable.
- Size: unusual move +0.33 % (t 0.73, the cases of one day together: 379 days) per case over 3 bars, 0.039 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total -0.06 %; 694 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2_agitated-decline-one-day-rise-fades_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2_agitated-decline-one-day-rise-fades_1d`
Measure: `measure.py`
