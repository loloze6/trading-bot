---
plan: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
idea: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
fit: adapted
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move after a short bet: -0.0017709; t of the mean: -0.0425582 (threshold: t >= 2 over at least 30 cases (confirm, with Spearman > 0); t <= -2 over at least 30 cases (reject))
- Supporting check: Spearman of |forecast| vs short-side unusual move: -0.0128973, passed: False
- Counts: cases: 17
- Decided by: Only 17 cases across all coins and windows, below the plan's minimum of 30.
- Reading: A short bet is a fall of the forecast of at least 2 points below its least negative level on the short side since the last bet (reset to 0 after a flat or a long), taking the first such bar in each 5-bar grid cell counted from each window's first row; the drift is the mean of each coin's non-overlapping 5-bar returns at grid positions 0, 5, 10, ... of all its windows; the situation holds where the raw component value is positive or a close lies below the low of the most recent of the last bars that closed above the prior 20-bar high.
- Size: unusual move -0.18 % (t -0.04, the cases of one day together: 15 days) per case over 5 bars, -0.024 of the coin's usual move (18.32 %); normal drift in its direction -4.66 %, total -4.84 %; 17 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/unseen_2016_2017/backtests/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d`
Measure: `measure.py`
