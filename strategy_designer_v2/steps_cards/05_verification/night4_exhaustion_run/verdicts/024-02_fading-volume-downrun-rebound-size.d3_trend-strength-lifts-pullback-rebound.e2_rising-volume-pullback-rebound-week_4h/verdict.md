---
plan: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h
idea: 024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 42-bar unusual move (return minus coin's normal 42-bar drift) over bets: 0.004639; t of the mean: 1.23152 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of cases with forecast above median minus at or below: None, passed: None
- Counts: independent cases: 1360, active bars: 5683
- Decided by: The t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: Situation computed from prices: regime 'trending' (the detector's recorded decision for 180-bar return > 0), bar t closed below the prior close, a down-close streak of at least 2 bars inside the window, and a positive least-squares slope of volume over that streak, with a long (positive) forecast; a case is the first bet (forecast rise >= 2 points from its lowest long level since the last bet, from 0 after flat) in each 42-bar grid cell counted from each window's first row, cases whose 42-bar return leaves the window are dropped, and the drift is the coin's mean 42-bar return on the same grid over all its windows.
- Size: unusual move +0.46 % per case over 42 bars, 0.036 of the coin's usual move (12.42 %); normal drift in its direction +1.00 %, total +1.47 %; 1360 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.d3_trend-strength-lifts-pullback-rebound.e2_rising-volume-pullback-rebound-week_4h`
Measure: `measure.py`
