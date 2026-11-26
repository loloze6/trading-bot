---
plan: 032-02.g1.e1.e3_flat-base-high-breakout_1d
idea: 032-02.g1.e1.e3_flat-base-high-breakout
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 5-day return on forecast: 0.00089248; OLS slope t: 0.787421 (threshold: confirm if slope t >= 2 (with supporting check); reject if slope t <= -2)
- Supporting check: forecast-weighted mean excess 5-day return > 0: 0.0232684, passed: True
- Counts: cases: 327
- Decided by: The slope t is between -2 and 2 (or undefined), which the plan calls inconclusive.
- Reading: The situation is recomputed as close >= max of the last 28 closes including the bar, checked only on bars with 28 bars of history inside their window, side long; cases are 'trending' bars at grid positions 0,5,10,... of each window with a 5-bar return inside the window, the coin's mean 5-day return is the mean over all its windows' grid samples, the slope t is the OLS slope over its standard error, and the plan's minimum of 100 cases gives 'not observable' when unmet.
- Size: unusual move +1.51 % (t 2.53, the cases of one day together: 370 days) per case over 5 bars, 0.137 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +2.10 %; 497 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e1.e3_flat-base-high-breakout_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e3_flat-base-high-breakout_1d`
Measure: `measure.py`
