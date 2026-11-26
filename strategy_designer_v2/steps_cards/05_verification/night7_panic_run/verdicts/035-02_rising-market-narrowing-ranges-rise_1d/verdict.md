---
plan: 035-02_rising-market-narrowing-ranges-rise_1d
idea: 035-02_rising-market-narrowing-ranges-rise
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of excess 3-day return, top third minus bottom third of forecast: -0.000551736; Welch t: -0.108712 (threshold: confirm t >= 2 with top-third mean excess > 0; reject t <= -2; at least 100 grid cases per third)
- Supporting check: top-third mean excess 3-day return > 0: -4.82599e-05, passed: False
- Counts: grid cases: 2224, top-third cases: 741, bottom-third cases: 741
- Decided by: Welch t is between -2 and +2.
- Reading: The rising-market profile is read from the recorded regime (the detector's decision, 'unknown' = not vetoed to chop), the situation also needs a recorded positive range ratio, the side is long; the coin's mean 3-day return uses the non-overlapping grid of all its bars in all windows; thirds are the lowest and highest floor(n/3) cases of the forecast pooled over all coins and windows (ties broken by record order); fewer than 100 cases in a third is reported as not observable.
- Size: unusual move -0.02 % (t -0.05, the cases of one day together: 508 days) per case over 3 bars, 0.003 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.34 %; 691 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/035-02_rising-market-narrowing-ranges-rise_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/035-02_rising-market-narrowing-ranges-rise_1d`
Measure: `measure.py`
