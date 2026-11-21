---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 36-bar move of long bets, before costs: 0.00509419; ordinary t of the mean: 1.67819 (threshold: confirm: mean > 0 with t >= 2 over >= 30 independent cases; reject: mean < 0 with t <= -2 over >= 30)
- Supporting check: mean unusual move above minus below forecast median: None, passed: False
- Counts: independent cases: 1743
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean's), so neither rule is met.
- Reading: Situation = recorded break raw value > 0 (or close above the prior 12-bar high from prices) and 42-bar close return > 0 from prices (the regime 'trending' where the window's first 42 bars leave it uncomputable), long side; a case is the first long bet (forecast rise >= 2 points from its lowest long level since the last bet, from 0 after flat) in each 36-bar grid cell from each window's first row, pooled over all coins, with the coin's drift the mean of its grid 36-bar returns over all windows; the median split excludes cases equal to the median.
- Size: unusual move +0.51 % per case over 36 bars, 0.039 of the coin's usual move (11.69 %); normal drift in its direction +0.79 %, total +1.30 %; 1743 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation_4h`
Measure: `measure.py`
