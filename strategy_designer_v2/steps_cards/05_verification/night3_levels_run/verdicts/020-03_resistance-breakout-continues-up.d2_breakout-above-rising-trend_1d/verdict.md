---
plan: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d
idea: 020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-day move over long bet cases (5-day return minus coin's normal 5-day drift): 0.0103742; one-sample t: 2.58145 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: OLS slope of 5-day excess return on case forecast > 0: -6.81539e-05, passed: False
- Counts: independent cases: 655
- Decided by: The t is confirming (>= 2) but the supporting slope is 0 or below (or not computable), so the result is inconclusive.
- Reading: The breakout and swing-high cluster conditions are taken from the recorded regime 'trending', since the detector's components are not recorded. Close above SMA50 comes from the ma_dist raw value, or from the SMA50 of in-window closes where that value is missing. A fresh upward cross is checked as a close above the previous close. A case is the first long bet in each 5-bar grid cell counted from each window's first row. A bet is a rise of >= 2 points over the lowest positive forecast since the last bet, starting from 0 after a flat bar, on a trending bar. A case without 5 bars left in its window is dropped. The drift is the mean of non-overlapping 5-bar returns on the same grid over all of the coin's windows. The slope is the OLS slope of excess return on the case-bar forecast.
- Size: unusual move +1.04 % per case over 5 bars, 0.086 of the coin's usual move (10.60 %); normal drift in its direction +0.57 %, total +1.61 %; 655 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.d2_breakout-above-rising-trend_1d`
Measure: `measure.py`
