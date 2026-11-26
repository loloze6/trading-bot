---
plan: 035-02_swing-wide-low-close-rebounds_1d
idea: 035-02_swing-wide-low-close-rebounds
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day excess return on forecast (all coins, windows): 0.00035356; OLS t, day-clustered: 3.20275 (threshold: confirm: slope > 0 with t >= 2 and top-minus-bottom fifth > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return, top fifth minus bottom fifth of forecasts (per coin): 0.00632807, passed: True
- Counts: independent days: 2898, bars with forecast >= 2: 15131, bars: 17380
- Decided by: The slope is positive with t >= 2 and the top-minus-bottom fifth difference is above 0.
- Reading: Every recorded bar enters the regression (forecast 0 included), the coin mean is over all its next-day returns in all windows, t is OLS with day-clustered errors, the fifths are cut per coin by forecast rank (ties broken by time order), and a minimum count not reached is reported as 'not observable'.
- Size: unusual move +0.10 % (t 0.94, the cases of one day together: 2073 days) per case over 1 bars, 0.023 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.22 %; 7094 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001213 on the check folds against +0.0003536 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/035-02_swing-wide-low-close-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/035-02_swing-wide-low-close-rebounds_1d`
Measure: `measure.py`
