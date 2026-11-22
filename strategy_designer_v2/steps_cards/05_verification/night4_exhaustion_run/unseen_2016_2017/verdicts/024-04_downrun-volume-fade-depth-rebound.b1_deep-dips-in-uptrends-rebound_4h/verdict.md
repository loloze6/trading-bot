---
plan: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
idea: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move after bets (return minus coin's normal 18-bar drift), pooled: 0.00258639; t of the mean: 0.478767 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move, upper half minus lower half of 180-bar return at signal bar: 0.0278953, passed: True
- Counts: independent cases: 677, cases with 180-bar return: 495
- Decided by: The t of the mean unusual move is between -2 and 2.
- Reading: A bet is the holding-period bet (long forecast rising >= 2 from its lowest level since the last bet, reset at flat), the first bet per 18-bar cell of each window is kept, cases without 18 bars ahead in the window are dropped, the supporting split puts cases with 180-bar return above the median in the upper half (others lower) and leaves out cases without 180 past bars in the window, and the situation's gate uses the regime column where the 180-bar return cannot be computed.
- Size: unusual move +0.26 % per case over 18 bars, 0.033 of the coin's usual move (13.56 %); normal drift in its direction +3.09 %, total +3.35 %; 677 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/unseen_2016_2017/backtests/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h`
Measure: `measure.py`
