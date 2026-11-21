---
plan: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h
idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean unusual 18-bar move of cases: 0.00185279; t of the weighted mean: 1.38886 (threshold: confirm: positive with t >= 2 (and top-minus-bottom third > 0); reject: negative with t <= -2)
- Supporting check: mean unusual move of top third by forecast minus bottom third: 0.0029514, passed: True
- Counts: cases: 6617, cases per third: 2205
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is the first bet bar (a forecast rise of >= 2 points above its lowest long level since the last bet, from 0 after a flat) in each 18-bar grid cell of a window, with its full 18-bar return inside the window; the t of the forecast-weighted mean uses its weighted standard error sqrt(n/(n-1) * sum(w^2 (x - mean)^2)) / sum(w); thirds are floor(n/3) cases by forecast, unweighted means; the plan's 'at least 100 cases' minimum gives 'not observable' when not reached.
- Size: unusual move +0.15 % per case over 18 bars, 0.015 of the coin's usual move (9.29 %); normal drift in its direction +0.51 %, total +0.66 %; 6617 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.b1_quiet-breakout-more-coins_4h`
Measure: `measure.py`
