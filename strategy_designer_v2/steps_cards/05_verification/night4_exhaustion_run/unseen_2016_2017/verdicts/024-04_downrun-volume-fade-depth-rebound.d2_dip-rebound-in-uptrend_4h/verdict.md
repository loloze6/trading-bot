---
plan: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
idea: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of long bets: 0.000278472; t of the mean: 0.0520093 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: top-half minus bottom-half mean unusual move (median entry forecast split): 0.00753073, passed: True
- Counts: cases: 664, top half cases: 332, bottom half cases: 332
- Decided by: The t lies between -2 and 2 over at least 30 cases.
- Reading: Bets are long forecast rises of at least 2 points from the lowest positive forecast since the last bet (reset to 0 when the forecast is not positive), the first bet of each 18-bar grid cell counted from each window's first row is the case, the normal drift is the mean 18-bar return on each coin's non-overlapping grid over all its windows, the median split puts cases with entry forecast above the median in the top half and the rest in the bottom half, and the 180-bar regime is recomputed from closes where 180 bars exist in the window and taken from the recorded regime otherwise.
- Size: unusual move +0.03 % per case over 18 bars, 0.009 of the coin's usual move (13.56 %); normal drift in its direction +3.09 %, total +3.12 %; 664 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h`
Measure: `measure.py`
