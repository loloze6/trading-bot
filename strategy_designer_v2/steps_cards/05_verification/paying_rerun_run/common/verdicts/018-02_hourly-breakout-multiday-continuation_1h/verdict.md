---
plan: 018-02_hourly-breakout-multiday-continuation_1h
idea: 018-02_hourly-breakout-multiday-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 120-bar move of long bets (one per 120-bar grid cell): 0.0251756; t of the mean: 5.25863 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2; at least 30 cases)
- Supporting check: mean unusual move, upper-break half minus lower-break half: 0.0203292, passed: True
- Counts: cases: 1483, upper half cases: 741, lower half cases: 742
- Decided by: Mean unusual move above 0 with t >= 2, and the larger-break half beats the smaller-break half.
- Reading: Cases are the first long bet (forecast rise >= 2 points from its lowest long level since the last bet) in each 120-bar grid cell counted from each window's first row, dropped if t+120 leaves the window; the upper half is raw break strictly above the median of the cases, the lower half at or below it.
- Size: unusual move +2.52 % (t 4.37, the cases of one day together: 857 days) per case over 120 bars, 0.199 of the coin's usual move (11.69 %); normal drift in its direction +1.04 %, total +3.56 %; 1483 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-02_hourly-breakout-multiday-continuation_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/018-02_hourly-breakout-multiday-continuation_1h`
Measure: `measure.py`
