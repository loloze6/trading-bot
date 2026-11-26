---
plan: 058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days_1d
idea: 058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of short bets, in the short direction: 0.00350769; t clustered by day: 0.815745 (threshold: confirm: mean > 0 with day-clustered t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of larger-forecast half minus smaller half: 0.00699466, passed: True
- Counts: cases: 1115, distinct case days: 467
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: The falling-agitated profile cannot be rebuilt from the record (its detector components are not recorded and windows are shorter than its 365-bar lookback), so the situation check tests the 0-to-1.0 scaled-rise band (recorded raw value, else recomputed with a 30-bar std including the day) and the short side; a case is the first short bet (forecast magnitude up >= 2 points from its lowest level since the last bet) in each 3-bar grid cell of a window; the drift is the mean of each coin's non-overlapping 3-bar grid returns over all its windows; the clustered standard error uses day sums of deviations with a G/(G-1) correction; the larger half is forecast size above the median; fewer than 30 case days is reported as not observable.
- Size: unusual move +0.35 % (t 0.82, the cases of one day together: 467 days) per case over 3 bars, 0.039 of the coin's usual move (8.85 %); normal drift in its direction -0.44 %, total -0.09 %; 1115 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d1.d1_capped-rise-fade-three-days_1d`
Measure: `measure.py`
