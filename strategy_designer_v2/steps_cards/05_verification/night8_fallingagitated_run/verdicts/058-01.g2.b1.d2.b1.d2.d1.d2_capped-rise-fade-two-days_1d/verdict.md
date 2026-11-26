---
plan: 058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days_1d
idea: 058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move of short cases (short direction): 0.00146627; t of the mean, cases of one day taken together: 0.391841 (threshold: confirm: mean > 0 with day-clustered t >= 2 and check > 0; reject: t <= -2 or upper-minus-lower Welch t <= -2)
- Supporting check: mean unusual move, upper minus lower half of |forecast|: 0.00494168, passed: True
- Counts: distinct days with cases: 501, cases: 1223
- Decided by: Inconclusive: the main measure's t is between -2 and 2 and no reject rule is met.
- Reading: A case is the first short bet (forecast rising >= 2 points on the short side from its lowest level since the last bet, reset at flat or side change) in each 2-bar grid cell of a window, measured from its own bar's close; the profile is read from the recorded regime; halves split as |forecast| > median vs <= median; the plan's 'fewer than 30 distinct days' minimum is treated as not observable.
- Size: unusual move +0.15 % (t 0.39, the cases of one day together: 501 days) per case over 2 bars, 0.023 of the coin's usual move (7.35 %); normal drift in its direction -0.28 %, total -0.13 %; 1223 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d1.d2_capped-rise-fade-two-days_1d`
Measure: `measure.py`
