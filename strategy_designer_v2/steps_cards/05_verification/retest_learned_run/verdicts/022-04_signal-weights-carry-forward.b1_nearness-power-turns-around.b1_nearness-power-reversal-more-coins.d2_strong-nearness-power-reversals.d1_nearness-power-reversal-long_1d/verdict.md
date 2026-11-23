---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next 5-bar return minus coin drift on forecast: 0.000583273; OLS slope t: 2.4769 (threshold: confirm if slope > 0 with t >= 2 (and supporting check passes); reject if slope < 0 with t <= -2)
- Supporting check: mean next 5-bar return minus coin drift on grid bars with forecast > 0, above 0: 0.00372994, passed: True
- Counts: grid bars with forecast > 0: 2457, grid bars in regression: 4732
- Decided by: Confirm: the slope is positive with t >= 2 and the mean excess 5-bar return on forecast > 0 grid bars is above 0.
- Reading: The coin's normal drift is its mean next 5-bar return over all its grid bars (positions 0, 5, 10, ... of each window) pooled across windows, the slope is an OLS with intercept over all grid bars with a forecast, and the plan's 'at least 100 grid bars with forecast > 0' minimum is applied as a minimum count giving 'not observable'.
- Size: unusual move -0.07 % per case over 5 bars, -0.004 of the coin's usual move (11.11 %); normal drift in its direction +0.72 %, total +0.64 %; 1224 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d2_strong-nearness-power-reversals.d1_nearness-power-reversal-long_1d`
Measure: `measure.py`
