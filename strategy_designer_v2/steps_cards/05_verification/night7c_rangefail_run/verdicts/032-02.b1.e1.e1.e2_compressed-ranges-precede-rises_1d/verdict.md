---
plan: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d
idea: 032-02.b1.e1.e1.e2_compressed-ranges-precede-rises
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 20-bar excess return on forecast (date-clustered SE): 0.000760675; date-clustered t of slope: 0.105468 (threshold: confirm: slope > 0 with t >= 2 and top-minus-bottom > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean excess 20-bar return, top fifth minus bottom fifth of forecast: 0.0138668, passed: True
- Counts: grid cases: 827, distinct dates: 147, top fifth cases: 166, bottom fifth cases: 166
- Decided by: Inconclusive: the slope has |t| < 2.
- Reading: Situation is every bar with the long side when the standardised compression exceeds its usual level (expected sign = sign of the rebuilt (compression + offset)/2, standardise rebuilt from last_history_value where 61 past in-window values exist, else the recorded post_pipeline_value); grid at positions 0,20,40,... of each window with the 20-bar return inside the window, coin mean = mean of that coin's grid returns over all windows, OLS with intercept and CR1 date-clustered SE, top/bottom fifth = forecast >= 80th / <= 20th percentile of pooled grid cases, and fewer than 300 cases or 100 dates gives 'not observable'.
- Size: unusual move +1.02 % (t 0.58, the cases of one day together: 173 days) per case over 20 bars, 0.033 of the coin's usual move (21.24 %); normal drift in its direction +0.88 %, total +1.89 %; 224 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e2_compressed-ranges-precede-rises_1d`
Measure: `measure.py`
