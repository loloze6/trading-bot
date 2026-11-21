---
plan: 017-05_settlement-move-reverses-after_1h
idea: 017-05_settlement-move-reverses-after
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x excess 2-bar forward return on settlement bars: 0.000434249; ordinary t of the mean: 5.09841 (threshold: confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: Welch t of forecast-signed excess 2-bar return, top third minus bottom third by |forecast|: 3.35171, passed: True
- Counts: settlement bars: 51746, top third: 17248, middle third: 17250, bottom third: 17248
- Decided by: The main mean is positive with t >= 2 and the top-minus-bottom third Welch t is >= 2.
- Reading: The coin's mean 2-bar return is taken on the non-overlapping grid (positions 0, 2, 4, ...) of each window pooled over its windows, settlement bars without a full 2-bar forward return in their window are left out, and the thirds are the pooled cases sorted by |forecast| split into floor(n/3) bottom and top with the remainder in the middle, all three needing 300.
- Size: unusual move +0.05 % per case over 2 bars, 0.032 of the coin's usual move (1.47 %); normal drift in its direction -0.00 %, total +0.05 %; 44171 cases
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-05_settlement-move-reverses-after_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-05_settlement-move-reverses-after_1h`
Measure: `measure.py`
