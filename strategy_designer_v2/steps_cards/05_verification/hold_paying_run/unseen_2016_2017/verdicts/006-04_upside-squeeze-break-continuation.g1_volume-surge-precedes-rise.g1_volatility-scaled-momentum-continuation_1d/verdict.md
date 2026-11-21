---
plan: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar return of the top-20% forecast grid bars: 0.0132423; one-group t: 1.28311 (threshold: mean > 0 with t >= 2 (and supporting difference > 0) confirms; mean < 0 with t <= -2 rejects)
- Supporting check: top-group mean excess minus forecast-0 mean excess: 0.0233458, passed: True
- Counts: grid bars in the top group: 253, grid bars with forecast > 0: 580, grid bars with forecast 0: 376
- Decided by: The t of the top-group mean excess return lies between -2 and 2, which the plan calls inconclusive.
- Reading: The top group is the grid bars with forecast > 0 (and a valid 3-bar return) whose forecast is at or above the 80th percentile of those bars pooled over coins, ties at the cut-off included; the coin's mean 3-bar return is the mean over its non-overlapping grid returns across all windows; the plan's 'fewer than 100 top-group bars' case is reported as not observable.
Plan: `steps_cards/03_test_plan/hold_paying_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/hold_paying_run/unseen_2016_2017/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d`
Measure: `measure.py`
