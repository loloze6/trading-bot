---
plan: 058-03.g1_calm-downtrend-weekly-continuation_1d
idea: 058-03.g1_calm-downtrend-weekly-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (next 5-bar return - coin drift), day-clustered: 0.00659382; t of the mean, cases of one day together: 1.03243 (threshold: confirm: mean > 0 with t >= 2 over >= 50 distinct days; reject: mean < 0 with t <= -2 over >= 50 distinct days)
- Supporting check: none
- Counts: distinct days: 255, cases: 654
- Decided by: The t lies between -2 and 2, which the plan rules inconclusive.
- Reading: Profile taken from the recorded regime ('unknown' = falling calm, both vetoes off), side = sign of the 5-day return (ret5 raw value, else recomputed from closes); drift = coin's mean next-5-bar return over all windows' grid bars; day-clustered t uses per-day summed deviations with a G/(G-1) correction; fewer than 50 distinct days is reported as not observable.
- Size: unusual move +1.08 % (t 2.44, the cases of one day together: 494 days) per case over 5 bars, 0.097 of the coin's usual move (10.60 %); normal drift in its direction -0.11 %, total +0.97 %; 779 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-03.g1_calm-downtrend-weekly-continuation_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-03.g1_calm-downtrend-weekly-continuation_1d`
Measure: `measure.py`
