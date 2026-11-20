---
plan: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h
idea: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of (forecast/10) x excess 4-bar return after settlement: 0.000849507; t of the mean: 4.84689 (threshold: confirm: mean product > 0 with t >= 2 and supporting check passes; reject: mean product < 0 with t <= -2; at least 300 episodes)
- Supporting check: excess 4-bar return, largest-|forecast| third minus smallest third: -0.000559692, passed: True
- Counts: episodes with a negative forecast: 24787, episodes per third: 8262
- Decided by: the mean product is above 0 with t >= 2 and the top-minus-bottom third difference is below 0
- Reading: Entry bars are those stamped 23:00, 07:00 or 15:00 with forecast < 0 whose bar 4 rows later is exactly 4 h later in the same window; the coin's mean 4-bar return uses the non-overlapping grid of each window pooled over all windows; thirds are n//3 episodes by |forecast| pooled over coins and windows.
- Size: unusual move +0.05 % per case over 4 bars, 0.024 of the coin's usual move (2.03 %); normal drift in its direction -0.02 %, total +0.03 %; 32711 cases
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h`
Measure: `measure.py`
