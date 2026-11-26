---
plan: 058-02.b1_quiet-calm-fall-more-coins_1d
idea: 058-02.b1_quiet-calm-fall-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of short-direction 5-bar unusual move x |forecast|/10, per case: 0.00461103; t of the mean, cases of one day summed: 0.674402 (threshold: confirm: mean > 0 with day-clustered t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: larger-|forecast| half minus smaller half, mean short-direction unusual move: -3.45941e-05, passed: False
- Counts: cases: 907, distinct days: 263
- Decided by: The t lies between -2 and 2: inconclusive by the plan's rule
- Reading: Profile membership is the recorded regime 'unknown' (the only regime with a strategy, i.e. neither veto fired) and a fall is a negative raw quiet_fall value; the case value is (drift - forward return) x (-forecast/10), i.e. the unusual move taken in the short direction as the plan's confirm rule describes; t uses per-day summed deviations; the larger |forecast| half is the top floor(n/2) cases by |forecast| (ties broken by coin then time).
- Size: unusual move +0.74 % (t 1.54, the cases of one day together: 500 days) per case over 5 bars, 0.069 of the coin's usual move (11.38 %); normal drift in its direction -0.67 %, total +0.07 %; 929 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-02.b1_quiet-calm-fall-more-coins_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-02.b1_quiet-calm-fall-more-coins_1d`
Measure: `measure.py`
