---
plan: 060-02.d1_volume-growth-fall-still-running_1d
idea: 060-02.d1_volume-growth-fall-still-running
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-day excess forward return on vol_growth post_pipeline_value: 0.00114721; OLS slope t: 3.84557 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 cases)
- Supporting check: none
- Counts: cases: 906
- Decided by: The slope is positive with t >= 2 over at least 100 cases.
- Reading: The grid is positions 0,5,10,... of each window keeping only cells with a full 5-bar forward return inside the window, the coin's mean 5-day return is taken over all those grid cells of all its windows, and the 20-day-return situation is recomputed from closes with the recorded regime standing in on each window's first 20 bars.
- Size: unusual move +1.24 % (t 2.90, the cases of one day together: 561 days) per case over 5 bars, 0.112 of the coin's usual move (10.60 %); normal drift in its direction -0.08 %, total +1.16 %; 782 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0003955 on the check folds against +0.001147 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02.d1_volume-growth-fall-still-running_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02.d1_volume-growth-fall-still-running_1d`
Measure: `measure.py`
