---
plan: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h
idea: 024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 18-bar return of bets over the coin's normal 18-bar drift: 0.000182382; t of the mean: 0.144784 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and slope > 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: slope of excess 18-bar return on bet-bar forecast: 0.000594523, passed: True
- Counts: cases: 4334
- Decided by: The t lies between -2 and 2 (or is not computable): inconclusive.
- Reading: Situation read as: the bar closed below the previous close, within a down-streak of at least 2 down closes inside the window, whose down bars' volume has a negative least-squares slope (declining volume), on the long side; a case is the first bet (forecast rise of >= 2 points from its lowest positive level since the last bet, from 0 after flat) in each 18-bar grid cell counted from each window's first row, with a full 18-bar return in the window; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.02 % per case over 18 bars, 0.003 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.43 %; 4334 cases
Plan: `steps_cards/03_test_plan/night4_exhaustion_run/plans/024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h.md`
Record: `steps_cards/04_backtest/night4_exhaustion_run/backtests/024-02_fading-volume-downrun-rebound-size.b1_extreme-down-streak-rebound-only_4h`
Measure: `measure.py`
