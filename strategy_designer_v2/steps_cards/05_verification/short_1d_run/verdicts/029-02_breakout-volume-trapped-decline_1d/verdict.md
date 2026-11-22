---
plan: 029-02_breakout-volume-trapped-decline_1d
idea: 029-02_breakout-volume-trapped-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar short move (return minus coin drift, short direction): -0.00773538; t of the mean: -1.0325 (threshold: confirm if mean > 0 with t >= 2 (and slope > 0); reject if mean < 0 with t <= -2; at least 30 cases)
- Supporting check: slope of unusual short move on abs post_pipeline_value of fb_vol: -0.00151385, passed: False
- Counts: cases across all coins and windows: 335
- Decided by: The t of the mean unusual short move lies between -2 and 2.
- Reading: A short bet is a fall of the forecast of at least 2 points from its least negative level since the last bet (reset to 0 after a flat or long bar), the first bet in each 5-bar grid cell from the window's first row is the case, cases without 5 bars left in the window are dropped, and the plan's 'fewer than 30 cases' rule is reported as not observable.
- Size: unusual move -0.77 % per case over 5 bars, -0.062 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total -1.36 %; 335 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-02_breakout-volume-trapped-decline_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-02_breakout-volume-trapped-decline_1d`
Measure: `measure.py`
