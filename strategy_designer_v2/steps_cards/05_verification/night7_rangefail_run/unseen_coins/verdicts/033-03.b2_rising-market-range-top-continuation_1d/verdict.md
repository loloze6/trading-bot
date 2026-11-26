---
plan: 033-03.b2_rising-market-range-top-continuation_1d
idea: 033-03.b2_rising-market-range-top-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the 5-bar forward return minus normal drift on the forecast: 0.198585; OLS t of the slope: 0.198585 (threshold: confirm: slope positive with t >= 2; reject: slope negative with t <= -2; otherwise inconclusive; at least 100 non-overlapping in-profile cases)
- Supporting check: none
- Counts: non-overlapping in-profile cases: 1496
- Decided by: A t between -2 and 2 is inconclusive (t = 0.20, 1496 cases).
- Reading: The rising profile is taken as the bars whose regime is 'unknown' (the only regime with a strategy, the chop veto not applied), the expected side is the sign of the range position (raw value, or recomputed from 20 closes when not recorded); the slope's t is the ordinary least-squares t of the pooled regression with intercept, the drift is each coin's mean 5-bar return on the non-overlapping grid of all its windows, and the plan's minimum of 100 cases is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.75 % (t 1.38, the cases of one day together: 800 days) per case over 5 bars, 0.052 of the coin's usual move (12.49 %); normal drift in its direction +0.21 %, total +0.96 %; 1559 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-03.b2_rising-market-range-top-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_coins/backtests/033-03.b2_rising-market-range-top-continuation_1d`
Measure: `measure.py`
