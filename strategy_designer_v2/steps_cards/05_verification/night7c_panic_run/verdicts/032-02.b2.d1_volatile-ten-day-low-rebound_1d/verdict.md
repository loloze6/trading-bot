---
plan: 032-02.b2.d1_volatile-ten-day-low-rebound_1d
idea: 032-02.b2.d1_volatile-ten-day-low-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 1-day move after a long bet (close to next close minus coin's mean daily return): 0.0203643; t of the mean, cases of one day taken together: 2.48079 (threshold: positive with t >= 2 over at least 30 distinct case days to confirm; negative with t <= -2 to reject)
- Supporting check: mean unusual move of deeper half minus shallower half (split at median post_pipeline_value of depth_below_low): None, passed: None
- Counts: cases: 195, distinct case days: 124
- Decided by: t >= 2 but the deeper half does not beat the shallower half, which the plan calls inconclusive.
- Reading: Bets are taken on every bar (1-bar grid) as long rises of the forecast of >= 2 points from its lowest long level since the last bet; the regime part of the situation is read from the recorded `regime` column; the day-clustered t uses per-day summed deviations with a G/(G-1) correction; the deeper half is the cases strictly above the median depth and the shallower half those at or below it; a count below 30 days is reported as not observable.
- Size: unusual move +2.04 % (t 2.49, the cases of one day together: 124 days) per case over 1 bars, 0.429 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +2.16 %; 195 cases
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.d1_volatile-ten-day-low-rebound_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.d1_volatile-ten-day-low-rebound_1d`
Measure: `measure.py`
