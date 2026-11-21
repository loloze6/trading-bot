---
plan: 018-02_hourly-breakout-multiday-continuation_1h
idea: 018-02_hourly-breakout-multiday-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move of long bets (one per 120-bar grid cell): 0.0160049; t of the mean: 3.21196 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: mean unusual move, upper-break half minus lower-break half: 0.012425, passed: True
- Counts: cases: 746, upper half cases: 373, lower half cases: 373
- Decided by: Mean unusual move above 0 with t >= 2, and the larger-break half beats the smaller-break half.
- Reading: Cases are the first long bet (forecast rise >= 2 points from its lowest long level since the last bet) in each 120-bar grid cell counted from each window's first row, dropped if t+120 leaves the window; the upper half is raw break strictly above the median of the cases, the lower half at or below it.
- Size: unusual move +1.60 % per case over 120 bars, 0.141 of the coin's usual move (10.37 %); normal drift in its direction +0.65 %, total +2.25 %; 746 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-02_hourly-breakout-multiday-continuation_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/backtests/018-02_hourly-breakout-multiday-continuation_1h`
Measure: `measure.py`
