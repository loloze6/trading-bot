---
plan: 033-03.b2_rising-market-range-top-continuation_1d
idea: 033-03.b2_rising-market-range-top-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 5-bar forward return minus normal drift on the forecast: 3.34496; OLS t of the slope: 3.34496 (threshold: confirm: slope positive with t >= 2; reject: slope negative with t <= -2; otherwise inconclusive; at least 100 non-overlapping in-profile cases)
- Supporting check: none
- Counts: non-overlapping in-profile cases: 354
- Decided by: The slope is positive with t of 2 or more (t = 3.34, 354 cases).
- Reading: The rising profile is taken as the bars whose regime is 'unknown' (the only regime with a strategy, the chop veto not applied), the expected side is the sign of the range position (raw value, or recomputed from 20 closes when not recorded); the slope's t is the ordinary least-squares t of the pooled regression with intercept, the drift is each coin's mean 5-bar return on the non-overlapping grid of all its windows, and the plan's minimum of 100 cases is treated as the minimum count giving 'not observable'.
- Size: unusual move +2.78 % (t 2.19, the cases of one day together: 247 days) per case over 5 bars, 0.144 of the coin's usual move (18.32 %); normal drift in its direction +1.68 %, total +4.46 %; 336 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-03.b2_rising-market-range-top-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/033-03.b2_rising-market-range-top-continuation_1d`
Measure: `measure.py`
