---
plan: 058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins_1d
idea: 058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next 5-bar return minus coin mean 5-bar return on forecast/10 (grid, forecast != 0): 0.00425997; t of slope, day-clustered: 0.904498 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive; needs >= 100 grid cases and >= 60 distinct days)
- Supporting check: none
- Counts: grid cases: 1274, distinct days: 309
- Decided by: inconclusive rule: the slope's t lies between -2 and 2.
- Reading: Profile read from the recorded regime ('unknown' = not vetoed) and side from the sign of ret5; the slope is ordinary least squares with an intercept, the coin's mean 5-bar return is taken over all grid bars of all its windows, and the t uses a day-clustered standard error (per-day sums of score, G/(G-1) correction).
- Size: unusual move +0.80 % (t 2.13, the cases of one day together: 746 days) per case over 5 bars, 0.071 of the coin's usual move (11.68 %); normal drift in its direction -0.10 %, total +0.70 %; 1567 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-03.g1.b1_calm-downtrend-weekly-continuation-more-coins_1d`
Measure: `measure.py`
