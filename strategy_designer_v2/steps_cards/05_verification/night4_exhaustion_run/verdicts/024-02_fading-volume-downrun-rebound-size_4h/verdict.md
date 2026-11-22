---
plan: 024-02_fading-volume-downrun-rebound-size_4h
idea: 024-02_fading-volume-downrun-rebound-size
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar unusual move of long bets (return minus coin's normal 18-bar drift): 2.73067e-06; t of the mean: 0.0022302 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject))
- Supporting check: mean unusual move above-median forecast minus below-median forecast: 0.0107146, passed: True
- Counts: cases: 4537, active bars: 10507
- Decided by: t between -2 and 2 (inconclusive rule).
- Reading: Down-streak = consecutive bars with close below the previous close within the window, volume fade = least-squares volume slope over the streak's down bars below 0; a bet is a rise of a positive forecast of at least 2 from its lowest level since the last bet (from 0 after flat), the first bet in each 18-bar grid cell from the window's first row is the case, cases without 18 bars left in the window are dropped, and the supporting check compares cases strictly above vs strictly below the median signal-bar forecast.
- Size: unusual move +0.00 % per case over 18 bars, 0.000 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.41 %; 4537 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size_4h`
Measure: `measure.py`
