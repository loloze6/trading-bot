---
plan: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h
idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 36-bar unusual move of the bets (return minus coin's normal drift): 0.00766163; ordinary t of the mean: 2.84977 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-forecast half minus smaller-forecast half: None, passed: None
- Counts: independent cases: 3662, larger-forecast half: 0, smaller-forecast half: 3662
- Decided by: t >= 2 but the supporting check is at or below 0, which the plan calls inconclusive.
- Reading: The break is read from the component's raw value > 0 (recomputed as close above the prior 12 highs where not recorded) and the 7-day gate from close/close[-42]-1 > 0, falling back to the recorded regime on a window's first 42 bars; a case is the first bet (forecast rise of >= 2 points from its lowest positive level since the last bet, from 0 after flat) in each 36-bar grid cell counted from the window's first row, with a full 36-bar return inside the window; the median split puts forecasts above the median in the larger half and the rest in the smaller half; fewer than 30 cases is reported as not observable.
- Size: unusual move +0.77 % per case over 36 bars, 0.047 of the coin's usual move (13.81 %); normal drift in its direction +1.03 %, total +1.79 %; 3662 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/backtests/019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h`
Measure: `measure.py`
