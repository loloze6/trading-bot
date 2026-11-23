---
plan: 030-02_absorption-close-low-falls_1d
idea: 030-02_absorption-close-low-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day excess fall after short bets (minus coin drift, fall positive): -0.00503571; t of the mean: -0.65964 (threshold: confirm t >= 2 with the slope check passing; reject t <= -2; at least 30 cases)
- Supporting check: slope of excess fall on abs(forecast) above 0: -3.55477e-05, passed: False
- Counts: cases: 151
- Decided by: The t of the mean excess fall lies between -2 and 2 (or cannot be computed), which the plan calls inconclusive.
- Reading: The situation is recomputed per window from prices: volume over the mean of the 20 prior bars' volume (rows of the same window, current bar excluded) at least 2 and |close-open|/open at most 1 percent, the expected side short; active bars of a window's first 20 rows, where the ratio cannot be computed, are left out of the agreement; a case is a short bet (a rise of the short forecast's size of at least 2 points from its lowest level on that side since the last bet, reset to 0 after flat or long), the first such bet in each 5-row grid cell of a window, pooled over all coins, its 5-bar return taken from that bet's close and dropped if it runs past the window's end; the drift is the coin's mean non-overlapping 5-bar grid return over all its windows; the slope is ordinary least squares, judged above 0 by sign alone.
- Size: unusual move -0.50 % per case over 5 bars, -0.046 of the coin's usual move (10.60 %); normal drift in its direction -0.61 %, total -1.11 %; 151 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-02_absorption-close-low-falls_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-02_absorption-close-low-falls_1d`
Measure: `measure.py`
