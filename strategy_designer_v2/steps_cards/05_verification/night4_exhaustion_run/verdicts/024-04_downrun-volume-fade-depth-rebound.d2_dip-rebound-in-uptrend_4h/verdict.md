---
plan: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
idea: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of long bets: 0.00357764; t of the mean: 2.33757 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: top-half minus bottom-half mean unusual move (median entry forecast split): 0.00462043, passed: True
- Counts: cases: 3168, top half cases: 1584, bottom half cases: 1584
- Decided by: The mean unusual move is positive with t >= 2 over at least 30 cases and the supporting check passes.
- Reading: Bets are long forecast rises of at least 2 points from the lowest positive forecast since the last bet (reset to 0 when the forecast is not positive), the first bet of each 18-bar grid cell counted from each window's first row is the case, the normal drift is the mean 18-bar return on each coin's non-overlapping grid over all its windows, the median split puts cases with entry forecast above the median in the top half and the rest in the bottom half, and the 180-bar regime is recomputed from closes where 180 bars exist in the window and taken from the recorded regime otherwise.
- Size: unusual move +0.36 % per case over 18 bars, 0.044 of the coin's usual move (8.17 %); normal drift in its direction +0.40 %, total +0.76 %; 3168 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h`
Measure: `measure.py`
