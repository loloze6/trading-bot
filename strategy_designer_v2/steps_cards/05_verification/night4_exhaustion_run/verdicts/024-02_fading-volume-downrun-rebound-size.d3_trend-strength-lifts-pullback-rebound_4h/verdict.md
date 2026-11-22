---
plan: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound_4h
idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of the cases (return minus coin's normal 18-bar drift, signal direction): 0.00317177; t of the mean: 1.64855 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject))
- Supporting check: mean unusual move, upper minus lower forecast half: 0.0124094, passed: True
- Counts: cases: 2115, upper half cases: 1057, lower half cases: 1058, active bars: 5005
- Decided by: The t of the mean unusual move lies between -2 and 2 (or is undefined).
- Reading: The down streak is recomputed from prices as consecutive bars closing below the previous close (capped at 180 bars), volume fading means a negative least-squares slope of volume over those down bars, rise30 uses the recorded raw value (recomputed from closes where missing); in the supporting check the upper half is cases with forecast above the median and the lower half those at or below it; cases are the first bet in each 18-bar grid cell, pooled over coins, each against its own coin's drift.
- Size: unusual move +0.32 % per case over 18 bars, 0.037 of the coin's usual move (8.17 %); normal drift in its direction +0.40 %, total +0.72 %; 2115 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound_4h`
Measure: `measure.py`
