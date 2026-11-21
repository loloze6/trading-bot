---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x (5-bar return minus coin mean 5-bar return): 0.0047185; ordinary t of the mean: 2.03556 (threshold: confirm t >= 2, reject t <= -2, with at least 300 non-zero cases)
- Supporting check: none
- Counts: non-overlapping cases where the forecast is not zero: 3018, non-overlapping cells: 3018
- Decided by: Confirm rule met: t >= 2 with at least 300 non-zero non-overlapping cases.
- Reading: The mean and its t are taken over all non-overlapping 5-bar cells (zero-forecast cells contribute zero), with the coin's mean 5-bar return taken on the same grid over all its windows, while the 300 minimum counts only cells with a non-zero forecast.
- Size: unusual move +0.29 % per case over 5 bars, 0.038 of the coin's usual move (10.47 %); normal drift in its direction +0.01 %, total +0.29 %; 1471 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d`
Measure: `measure.py`
