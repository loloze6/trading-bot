---
plan: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
idea: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move after bets (return minus coin's normal 18-bar drift), pooled: 0.0045599; t of the mean: 3.59429 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move, upper half minus lower half of 180-bar return at signal bar: 0.00716509, passed: True
- Counts: independent cases: 6339, cases with 180-bar return: 4779
- Decided by: The mean unusual move is above 0 with t >= 2 over at least 30 independent cases and the supporting check passes.
- Reading: A bet is the holding-period bet (long forecast rising >= 2 from its lowest level since the last bet, reset at flat), the first bet per 18-bar cell of each window is kept, cases without 18 bars ahead in the window are dropped, the supporting split puts cases with 180-bar return above the median in the upper half (others lower) and leaves out cases without 180 past bars in the window, and the situation's gate uses the regime column where the 180-bar return cannot be computed.
- Size: unusual move +0.46 % (t 2.01, the cases of one day together: 1786 days) per case over 18 bars, 0.049 of the coin's usual move (9.37 %); normal drift in its direction +0.71 %, total +1.17 %; 6339 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/common/backtests/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h`
Measure: `measure.py`
