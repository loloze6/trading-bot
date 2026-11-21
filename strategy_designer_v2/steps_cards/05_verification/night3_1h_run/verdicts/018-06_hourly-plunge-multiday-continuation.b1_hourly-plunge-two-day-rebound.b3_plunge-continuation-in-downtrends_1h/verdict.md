---
plan: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h
idea: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 96-bar short-direction move: 0.00305462; t of the mean: 1.55775 (threshold: confirm: mean > 0 with t >= 2 and depth slope < 0; reject: t <= -2, or confirm with depth slope > 0 and slope t >= 2; at least 30 cases)
- Supporting check: slope of unusual short move on 30-day return: 0.0360069, passed: False
- Counts: independent cases: 2329, cases with 30-day return: 1657, active bars: 112010
- Decided by: Inconclusive rule: the t of the mean unusual move lies between -2 and 2 (or the mean is not above 0).
- Reading: A case is the first bet bar (short forecast magnitude rising >= 2 above its lowest level since the last bet, reset on flat) in each 96-bar grid cell from each window's first row, kept only if its 96-bar forward return lies in the window; the 30-day return is close[t]/close[t-720]-1 within the window (cases without 720 prior bars are left out of the slope); the plan's fewer-than-30-cases rule is applied as the minimum count giving 'not observable'.
- Size: unusual move +0.31 % per case over 96 bars, 0.036 of the coin's usual move (8.92 %); normal drift in its direction -0.51 %, total -0.20 %; 2329 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.b3_plunge-continuation-in-downtrends_1h`
Measure: `measure.py`
