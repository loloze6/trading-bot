---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 18-bar move of forecast rises >= 2 (one per 18-bar grid cell): 0.00430502; ordinary t of the mean: 2.30906 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move above minus below median forecast: None, passed: None
- Counts: independent cases: 2398
- Decided by: t >= 2 but the supporting check (top minus bottom half above 0) fails, which the plan calls inconclusive.
- Reading: A case is the first bet (forecast rise >= 2 from its lowest level on its side since the last bet) in each 18-bar grid cell counted from each window's first row, cases without 18 bars ahead in their window are dropped, drift is the coin's mean non-overlapping 18-bar return over all windows, and the median split uses strictly above and strictly below the median forecast (cases at the median left out).
- Size: unusual move +0.43 % per case over 18 bars, 0.048 of the coin's usual move (8.17 %); normal drift in its direction +0.41 %, total +0.84 %; 2398 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h`
Measure: `measure.py`
