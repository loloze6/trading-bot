---
plan: 018-04_hourly-surge-multiday-continuation_1h
idea: 018-04_hourly-surge-multiday-continuation
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move after long forecast rises of >= 2 points: -0.000115334; t of the mean: -0.0589495 (threshold: positive with t >= 2 over at least 30 cases to confirm; negative with t <= -2 over at least 30 cases to reject)
- Supporting check: OLS slope of unusual move on forecast at the case's bar: 0.000676035, passed: True
- Counts: cases: 3205
- Decided by: The t-statistic is between -2 and 2.
- Reading: The situation is read as 'the 24-bar return is above 0' on the long side; a case is a long-side rise of the forecast of at least 2 points from its lowest level since the last such rise (from 0 after flat), the first per 120-bar grid cell counted from each window's first row, with a full 120-bar forward return inside the window; the drift is the coin's mean 120-bar return on that grid over all windows; the slope is an OLS fit of unusual move on forecast, failed if not computable; fewer than 30 cases is reported as not observable.
- Size: unusual move -0.01 % per case over 120 bars, -0.002 of the coin's usual move (10.37 %); normal drift in its direction +0.64 %, total +0.63 %; 3205 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-04_hourly-surge-multiday-continuation_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-04_hourly-surge-multiday-continuation_1h`
Measure: `measure.py`
