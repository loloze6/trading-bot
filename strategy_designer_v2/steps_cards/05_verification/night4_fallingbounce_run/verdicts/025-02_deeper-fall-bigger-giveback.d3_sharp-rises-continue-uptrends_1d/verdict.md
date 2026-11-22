---
plan: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d
idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move over cases: -0.00304833; t of the mean: -0.538177 (threshold: confirm: mean > 0 with t >= 2 (and positive slope); reject: mean < 0 with t <= -2)
- Supporting check: slope of unusual move on case forecast: 0.0020786, passed: True
- Counts: cases: 996
- Decided by: t lies between -2 and 2.
- Reading: A case is the first bet (forecast rise of >= 2 points from its lowest level on its side since the last bet) in each 10-bar grid cell of a window, its size in the regression is the forecast on the signal bar, the drift is the mean of the coin's non-overlapping 10-bar grid returns over all windows, and the 90-day return is recomputed from closes where 90 prior bars exist in the window, else read from the recorded regime.
- Size: unusual move -0.30 % per case over 10 bars, -0.025 of the coin's usual move (14.49 %); normal drift in its direction +1.17 %, total +0.87 %; 996 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends_1d`
Measure: `measure.py`
