---
plan: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h
idea: 024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of long bets: 0.00496096; t of the mean: 3.57546 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: top-half minus bottom-half mean unusual move (median entry forecast split): 0.00512772, passed: True
- Counts: cases: 6191, top half cases: 3095, bottom half cases: 3096
- Decided by: The mean unusual move is positive with t >= 2 over at least 30 cases and the supporting check passes.
- Reading: Bets are long forecast rises of at least 2 points from the lowest positive forecast since the last bet (reset to 0 when the forecast is not positive), the first bet of each 18-bar grid cell counted from each window's first row is the case, the normal drift is the mean 18-bar return on each coin's non-overlapping grid over all its windows, the median split puts cases with entry forecast above the median in the top half and the rest in the bottom half, and the 180-bar regime is recomputed from closes where 180 bars exist in the window and taken from the recorded regime otherwise.
- Size: unusual move +0.50 % (t 2.14, the cases of one day together: 1821 days) per case over 18 bars, 0.051 of the coin's usual move (9.37 %); normal drift in its direction +0.71 %, total +1.21 %; 6191 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-04_downrun-volume-fade-depth-rebound.d2_dip-rebound-in-uptrend_4h`
Measure: `measure.py`
