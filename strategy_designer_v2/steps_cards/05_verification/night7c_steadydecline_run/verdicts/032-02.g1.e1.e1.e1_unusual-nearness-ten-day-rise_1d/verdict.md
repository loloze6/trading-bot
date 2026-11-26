---
plan: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d
idea: 032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean timing gain forecast/10 x excess 10-bar return: 0.00323519; t of the mean, cases of one day summed: 1.4326 (threshold: positive with t >= 2 to confirm, negative with t <= -2 to reject)
- Supporting check: excess 10-bar return, forecast >= +2 minus forecast <= -2, above 0: 0.0200937, passed: True
- Counts: grid cases: 1691, distinct days: 304, cells forecast >= +2: 624, cells forecast <= -2: 530
- Decided by: The t of the mean timing gain lies between -2 and 2.
- Reading: The situation is the close nearer its 28-day closing high than its mean absolute distance over the 60 prior raw values (long) and, by the graded forecast, farther than usual (short), rebuilt from last_history_value where 60 prior values are in the window and from post_pipeline_value otherwise; the grid is positions 0,10,20,... of each window with the 10-bar return inside the window, all grid cells (forecast 0 included, gain 0) are cases, the coin's mean 10-bar return is the mean of its grid returns over all windows, the t sums each day's deviations, and the plan's minimum counts not reached give 'not observable'.
- Size: unusual move +1.31 % (t 2.13, the cases of one day together: 688 days) per case over 10 bars, 0.086 of the coin's usual move (14.49 %); normal drift in its direction +0.23 %, total +1.54 %; 1105 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-02.g1.e1.e1.e1_unusual-nearness-ten-day-rise_1d`
Measure: `measure.py`
