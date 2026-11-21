---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high
fit: exact
status: confirmed
---
Situation check: 93 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward return minus coin drift on forecast, non-overlapping grid, pooled: 0.00137373; OLS t of slope: 2.31042 (threshold: t >= 2 confirms, t <= -2 rejects, over at least 1000 grid cases)
- Supporting check: timing gain before costs (mean daily position gain minus gain from coin mean drift): 0.00011245, passed: True
- Counts: independent grid cases: 3419
- Decided by: The slope's t is 2 or more over at least 1000 grid cases and the timing gain is positive.
- Reading: All grid bars (positions 0,5,10,... of each window with a full 5-bar return, flat forecasts included) enter an ordinary least-squares slope with intercept, the drift is the coin's mean grid 5-bar return over all windows, and the book before costs is the previous bar's allocation times the coin's daily return, averaged over coins per day.
- Size: unusual move +1.52 % per case over 5 bars, 0.130 of the coin's usual move (10.60 %); normal drift in its direction +0.10 %, total +1.63 %; 833 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d2_nearness-to-90-day-high_1d`
Measure: `measure.py`
