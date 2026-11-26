---
plan: 061-01.g1.d1.d2_calm-big-rise-near-highs_1d
idea: 061-01.g1.d1.d2_calm-big-rise-near-highs
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of coin-excess 5-bar forward return on forecast, grid bars with forecast > 0: 0.00258539; slope t, errors clustered by date: 2.48722 (threshold: slope > 0 with t >= 2 confirms (with mean excess > 0); slope < 0 with t <= -2 rejects)
- Supporting check: mean excess 5-bar return on the same grid bars > 0: 0.00281912, passed: True
- Counts: grid bars with forecast > 0: 285, distinct dates: 168
- Decided by: The slope is positive with t >= 2 and the mean excess 5-bar return is above 0 (confirm rule).
- Reading: The situation is a rise day (raw rise_vol_units > 0, or the 1-day close return when not recorded) on a bar of the choppy-calm profile (regime 'unknown', the only non-vetoed regime), long side; the coin's mean 5-bar return is the mean of its non-overlapping grid 5-bar returns over all windows; the regression has an intercept and cluster-robust (by UTC date) errors with the usual small-sample correction; the plan's minimum of 40 grid bars over 20 dates, if not reached, gives 'not observable'.
- Size: unusual move -0.43 % (t -1.15, the cases of one day together: 457 days) per case over 5 bars, -0.055 of the coin's usual move (10.60 %); normal drift in its direction +0.62 %, total +0.19 %; 651 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001239 on the check folds against +0.002585 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2_calm-big-rise-near-highs_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2_calm-big-rise-near-highs_1d`
Measure: `measure.py`
