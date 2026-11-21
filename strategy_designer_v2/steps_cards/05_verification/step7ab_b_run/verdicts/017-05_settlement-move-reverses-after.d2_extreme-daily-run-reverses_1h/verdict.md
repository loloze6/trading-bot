---
plan: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h
idea: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forecast-signed drift-adjusted 24-bar forward return on extreme grid bars: 0.00204307; t of the mean: 3.34513 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases (and supporting difference > 0); reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: extreme minus other non-zero grid bars, mean signed drift-adjusted 24-bar return: 0.00148239, passed: True
- Counts: extreme grid cases: 7079, other non-zero grid cases: 10121
- Decided by: Main mean above 0 with t >= 2 over at least 30 cases and supporting difference (extreme minus rest) above 0.
- Reading: The grid is positions 0, 24, 48, ... of each window with a full 24-bar forward return inside the window, the coin's mean 24-bar return is the mean of these grid returns over all its windows, and the situation check takes every non-zero volatility-scaled run as the situation with the expected side opposite to its sign.
- Size: unusual move +0.06 % per case over 24 bars, 0.013 of the coin's usual move (4.87 %); normal drift in its direction -0.00 %, total +0.06 %; 16146 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/backtests/017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h`
Measure: `measure.py`
