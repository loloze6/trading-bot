---
plan: 030-01_absorption-close-high-rises_1d
idea: 030-01_absorption-close-high-rises
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of unusual 5-bar move on forecast: -0.000160106; OLS slope t: -0.385677 (threshold: confirm: slope > 0 with t >= 2 on >= 30 cases; reject: slope < 0 with t <= -2 on >= 30 cases)
- Supporting check: none
- Counts: cases: 369
- Decided by: The t lies between -2 and 2 on at least 30 cases (inconclusive rule).
- Reading: Situation recomputed from prices (volume over the mean of the 20 prior bars of the window, body over range, side from the sign of the close location), falling back to the recorded regime on a window's first 20 bars; a case is the first bet (forecast rise of >= 2 on its side from its lowest level since the last bet, reset to 0 after flat or a side change) in each 5-bar grid cell of a window, with its 5-bar return inside the window, pooled over all coins in one OLS of the unusual move (not direction-flipped) on the signed forecast.
- Size: unusual move +0.03 % per case over 5 bars, -0.012 of the coin's usual move (10.60 %); normal drift in its direction +0.09 %, total +0.12 %; 369 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-01_absorption-close-high-rises_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-01_absorption-close-high-rises_1d`
Measure: `measure.py`
