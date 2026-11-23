---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (5-bar forward return minus coin's mean 5-bar return), before costs: 0.00370715; t of the mean: 2.04648 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 non-zero-forecast cases)
- Supporting check: none
- Counts: cases with a non-zero forecast: 4732, grid cases: 4732
- Decided by: The mean is above 0 with t >= 2 on at least 300 non-zero-forecast cases (confirm rule).
- Reading: The mean and t are taken over all grid cases at positions 0, 5, 10, ... of each window with a full 5-bar forward return (zero-forecast cases contribute 0), the coin's mean 5-bar return is the mean of its grid returns over all its windows, and the 300-case minimum counts the non-zero-forecast cases.
- Size: unusual move +0.15 % per case over 5 bars, 0.015 of the coin's usual move (11.11 %); normal drift in its direction -0.01 %, total +0.14 %; 2306 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins_1d`
Measure: `measure.py`
