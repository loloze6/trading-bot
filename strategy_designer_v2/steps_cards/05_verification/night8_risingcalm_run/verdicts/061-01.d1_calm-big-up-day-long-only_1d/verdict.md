---
plan: 061-01.d1_calm-big-up-day-long-only_1d
idea: 061-01.d1_calm-big-up-day-long-only
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast (calm grid bars), t clustered by date: 0.00175408; date-clustered OLS slope t: 3.50884 (threshold: t >= 2 confirms (with check mean > 0); t <= -2 rejects; between is inconclusive)
- Supporting check: mean 5-bar excess return over grid bars with forecast > 0: 0.0100184, passed: True
- Counts: grid bars with forecast > 0: 897, calm grid bars: 1829, dates (clusters): 483
- Decided by: The slope's t is 2 or more and the mean excess return over forecast > 0 grid bars is above 0.
- Reading: Calm = regime 'unknown' (not the 'chop' veto) at bar t; the normal 5-bar drift is each coin's mean 5-bar return over all its non-overlapping grid bars in all windows (all regimes); the regression pools all coins with an intercept and CR1 date-clustered errors; the 100 minimum counts calm grid bars with forecast > 0 and, unmet, gives 'not observable'.
- Size: unusual move +0.01 % (t 0.02, the cases of one day together: 822 days) per case over 5 bars, -0.003 of the coin's usual move (10.60 %); normal drift in its direction +0.64 %, total +0.64 %; 1765 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001325 on the check folds against +0.001754 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.d1_calm-big-up-day-long-only_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.d1_calm-big-up-day-long-only_1d`
Measure: `measure.py`
