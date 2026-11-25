---
plan: 032-02.g1.e1.e1_raw-nearness-to-28-day-high_1d
idea: 032-02.g1.e1.e1_raw-nearness-to-28-day-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on the high_prox forecast (pooled OLS): 0.00077628; OLS slope t, day-clustered: 1.56557 (threshold: slope t >= 2 confirms (with top-minus-bottom third > 0); t <= -2 rejects)
- Supporting check: mean excess 5-bar return, top third of forecasts minus bottom third: 0.0120335, passed: True
- Counts: grid cases across coins and windows: 3419, days: 617
- Decided by: The slope's t lies between -2 and 2.
- Reading: The slope's t uses a day-clustered standard error (cases summed per calendar day, with a G/(G-1) correction), the coin's mean 5-bar return is the mean of its grid returns over all windows, and the thirds are the n//3 lowest and highest cases by post_pipeline_value (stable sort).
- Size: unusual move +0.47 % (t 1.29, the cases of one day together: 960 days) per case over 5 bars, 0.039 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +1.06 %; 1762 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e1.e1_raw-nearness-to-28-day-high_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e1_raw-nearness-to-28-day-high_1d`
Measure: `measure.py`
