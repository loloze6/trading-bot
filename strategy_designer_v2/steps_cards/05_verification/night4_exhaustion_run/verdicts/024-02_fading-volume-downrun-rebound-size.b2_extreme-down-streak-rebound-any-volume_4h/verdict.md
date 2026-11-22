---
plan: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h
idea: 024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move after long bets (return minus coin's normal 18-bar drift): 0.000531378; t of the mean: 0.480412 (threshold: confirm: positive with t >= 2 over at least 30 cases; reject: negative with t <= -2 over at least 30 cases)
- Supporting check: mean unusual move above median forecast minus below median: 0.00770129, passed: True
- Counts: cases: 5674, cases_above_median: 2837, cases_below_median: 2837
- Decided by: t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first bet (long forecast rise >= 2 from its low since the last bet) in each 18-bar grid cell counted from each window's first row, cases whose 18-bar return leaves the window are dropped, and cases exactly at the median forecast belong to neither half.
- Size: unusual move +0.05 % per case over 18 bars, 0.007 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.46 %; 5674 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.b2_extreme-down-streak-rebound-any-volume_4h`
Measure: `measure.py`
