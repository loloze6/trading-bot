---
plan: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d
idea: 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move after a short bet: 0.0283168; t of the mean: 2.73124 (threshold: t >= 2 over at least 30 cases (confirm, with Spearman > 0); t <= -2 over at least 30 cases (reject))
- Supporting check: Spearman of |forecast| vs short-side unusual move: 0.240839, passed: True
- Counts: cases: 50
- Decided by: The mean short-side unusual move has t >= 2 over at least 30 cases and the Spearman correlation is above 0.
- Reading: A short bet is a fall of the forecast of at least 2 points below its least negative level on the short side since the last bet (reset to 0 after a flat or a long), taking the first such bar in each 5-bar grid cell counted from each window's first row; the drift is the mean of each coin's non-overlapping 5-bar returns at grid positions 0, 5, 10, ... of all its windows; the situation holds where the raw component value is positive or a close lies below the low of the most recent of the last bars that closed above the prior 20-bar high.
- Size: unusual move +2.83 % per case over 5 bars, 0.254 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +2.24 %; 50 cases
Plan: `steps_cards/03_test_plan/short_1d_run/plans/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d.md`
Record: `steps_cards/04_backtest/short_1d_run/backtests/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d`
Measure: `measure.py`
