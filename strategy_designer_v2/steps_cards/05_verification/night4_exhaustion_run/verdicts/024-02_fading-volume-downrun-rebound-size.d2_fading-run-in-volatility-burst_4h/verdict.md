---
plan: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return of long bets over the coin's normal drift: -0.000147301; t of the mean: -0.120866 (threshold: confirm: positive with t >= 2 and supporting check passes; reject: negative with t <= -2; at least 30 cases)
- Supporting check: mean excess return of upper forecast half minus lower half: 0.00993952, passed: True
- Counts: cases: 4559, upper half cases: 2279, lower half cases: 2280
- Decided by: t lies between -2 and 2 (or is undefined), which the plan calls inconclusive.
- Reading: cases pooled over all coins, the first bet in each non-overlapping 18-bar cell per window, dropping cells whose 18-bar return leaves the window; the median split puts forecasts above the median in the upper half and the rest in the lower half; the situation's streak is consecutive lower closes ending on the bar with the volume least-squares slope over those bars below 0.
- Size: unusual move -0.01 % per case over 18 bars, -0.001 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.39 %; 4559 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h`
Measure: `measure.py`
