---
plan: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d
idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 3-bar return of the top-20% forecast grid bars: 0.00896569; one-group t: 3.00445 (threshold: mean > 0 with t >= 2 (and supporting difference > 0) confirms; mean < 0 with t <= -2 rejects)
- Supporting check: top-group mean excess minus forecast-0 mean excess: 0.0122932, passed: True
- Counts: grid bars in the top group: 1030, grid bars with forecast > 0: 2922, grid bars with forecast 0: 2801
- Decided by: The top-group mean excess return is above 0 with t >= 2 and the supporting difference is above 0.
- Reading: The top group is the grid bars with forecast > 0 (and a valid 3-bar return) whose forecast is at or above the 80th percentile of those bars pooled over coins, ties at the cut-off included; the coin's mean 3-bar return is the mean over its non-overlapping grid returns across all windows; the plan's 'fewer than 100 top-group bars' case is reported as not observable.
Plan: `steps_cards/03_test_plan/night_006_run/plans/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d.md`
Record: `steps_cards/04_backtest/night_006_run/backtests/006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1d`
Measure: `measure.py`
