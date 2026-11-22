---
plan: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h
idea: 024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move after bets (return minus coin's normal 18-bar drift), pooled: 0.00402503; t of the mean: 2.60508 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases and supporting check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: mean unusual move, upper half minus lower half of 180-bar return at signal bar: 0.000948955, passed: True
- Counts: independent cases: 3245, cases with 180-bar return: 2478
- Decided by: The mean unusual move is above 0 with t >= 2 over at least 30 independent cases and the supporting check passes.
- Reading: A bet is the holding-period bet (long forecast rising >= 2 from its lowest level since the last bet, reset at flat), the first bet per 18-bar cell of each window is kept, cases without 18 bars ahead in the window are dropped, the supporting split puts cases with 180-bar return above the median in the upper half (others lower) and leaves out cases without 180 past bars in the window, and the situation's gate uses the regime column where the 180-bar return cannot be computed.
- Size: unusual move +0.40 % per case over 18 bars, 0.049 of the coin's usual move (8.17 %); normal drift in its direction +0.40 %, total +0.81 %; 3245 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-04_downrun-volume-fade-depth-rebound.b1_deep-dips-in-uptrends-rebound_4h`
Measure: `measure.py`
