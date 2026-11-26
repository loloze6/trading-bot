---
plan: 032-01.g1.b1_sharp-fall-rebound-more-coins_1d
idea: 032-01.g1.b1_sharp-fall-rebound-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move per case (long), day-pooled: 0.00105236; t of the mean, cases of one day pooled: 0.21145 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on fall post_pipeline_value: -1.47021e-05, passed: False
- Counts: cases: 922, distinct case days: 253
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: Cases are long-side bets (forecast rise >= 2 points from its lowest level on that side since the last bet, from 0 after a flat), the first bet in each 2-bar grid cell from each window's first row; the normal drift is the mean of the coin's non-overlapping 2-bar returns on that grid over all its windows; the t pools cases of the same UTC date by summing their deviations; the slope is OLS of the unusual move on post_pipeline_value of fall; the plan's 30-distinct-case-day minimum is treated as a minimum count (not observable).
- Size: unusual move +0.11 % (t 0.21, the cases of one day together: 253 days) per case over 2 bars, 0.019 of the coin's usual move (7.48 %); normal drift in its direction +0.31 %, total +0.41 %; 922 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-01.g1.b1_sharp-fall-rebound-more-coins_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-01.g1.b1_sharp-fall-rebound-more-coins_1d`
Measure: `measure.py`
