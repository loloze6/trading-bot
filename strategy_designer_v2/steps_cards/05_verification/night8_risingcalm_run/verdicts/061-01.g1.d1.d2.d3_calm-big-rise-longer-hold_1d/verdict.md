---
plan: 061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d
idea: 061-01.g1.d1.d2.d3_calm-big-rise-longer-hold
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move after long bets (forecast rise >= 2), once per 10-bar grid cell: -0.00870363; t of the mean, cases of one day taken together: -1.27049 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above median forecast minus below median: 0.0191033, passed: True
- Counts: distinct case days: 346, cases: 473
- Decided by: The t is between -2 and 2, which is inconclusive.
- Reading: Bets are tracked per window from 0 at its first bar, the first bet in each 10-bar grid cell (counted from the window's first row) is the case and cases without 10 bars ahead in the window are dropped, cases equal to the median forecast are left out of both halves, and the day-clustered t uses the D/(D-1) correction so it equals the ordinary t with one case per day.
- Size: unusual move -0.87 % (t -1.27, the cases of one day together: 346 days) per case over 10 bars, -0.076 of the coin's usual move (14.49 %); normal drift in its direction +1.25 %, total +0.38 %; 473 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.d3_calm-big-rise-longer-hold_1d`
Measure: `measure.py`
