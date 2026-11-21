---
plan: 018-02_hourly-breakout-multiday-continuation_1h
idea: 018-02_hourly-breakout-multiday-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move of long bets (one per 120-bar grid cell): 0.04681; t of the mean: 2.06971 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: mean unusual move, upper-break half minus lower-break half: 0.0467324, passed: True
- Counts: cases: 145, upper half cases: 72, lower half cases: 73
- Decided by: Mean unusual move above 0 with t >= 2, and the larger-break half beats the smaller-break half.
- Reading: Cases are the first long bet (forecast rise >= 2 points from its lowest long level since the last bet) in each 120-bar grid cell counted from each window's first row, dropped if t+120 leaves the window; the upper half is raw break strictly above the median of the cases, the lower half at or below it.
- Size: unusual move +4.68 % per case over 120 bars, 0.293 of the coin's usual move (19.38 %); normal drift in its direction +4.80 %, total +9.48 %; 145 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-02_hourly-breakout-multiday-continuation_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/unseen_2016_2017/backtests/018-02_hourly-breakout-multiday-continuation_1h`
Measure: `measure.py`
