---
plan: 031-02_down-streak-length-reversal_1d
idea: 031-02_down-streak-length-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast (grid, pooled): -0.000432003; slope t, day-clustered (same-day cases summed): -1.26529 (threshold: confirm: slope > 0 with t >= 2 and supporting check passes; reject: slope < 0 with t <= -2)
- Supporting check: mean unusual 5-bar move over long cases (forecast rises >= 2): 0.000642065, passed: True
- Counts: grid bars with a forecast above 0: 1759, distinct days of those grid bars: 485, grid bars in regression: 3419, supporting cases: 3232
- Decided by: The slope's t lies between -2 and 2.
- Reading: The regression is OLS with intercept of every grid bar's (positions 0,5,10,... per window) excess 5-bar return (minus the coin's mean grid 5-bar return over all windows) on its forecast, with standard errors from scores summed per UTC day (G/(G-1) correction); cases are the first long-side forecast rise of >= 2 from its lowest level since the last bet in each grid cell, measured from that bar's close; the minimum counts use grid bars with forecast > 0 and a valid forward return, and a shortfall is reported as 'not observable'.
- Size: unusual move +0.06 % (t 0.20, the cases of one day together: 1207 days) per case over 5 bars, 0.006 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.65 %; 3232 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02_down-streak-length-reversal_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02_down-streak-length-reversal_1d`
Measure: `measure.py`
