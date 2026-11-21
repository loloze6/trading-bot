---
plan: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h
idea: 019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 18-bar excess return of bets over the coin's normal 18-bar drift: 0.022297; ordinary t of the mean: 2.03106 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2; fewer than 30 cases: not observable)
- Supporting check: mean excess of cases above median forecast minus at or below: 0.0247573, passed: True
- Counts: cases: 328, upper half cases: 164, lower half cases: 164
- Decided by: The mean excess return is positive with t >= 2 and the upper-minus-lower half difference is above 0.
- Reading: The 30-day return is recomputed from closes inside each window and, on bars too early in a window to compute it, the recorded regime stands in for it; a bet is a long-side forecast rise of at least 2 points from its lowest level since the last bet (from 0 after a flat); each 18-bar grid cell (positions 0,18,36,... of each window) keeps its first bet, dropped if its 18-bar return leaves the window; the drift is the coin's mean 18-bar return on the same grid over all its windows; the median split puts cases above the median forecast in the upper half and the rest in the lower half; the plan's fewer-than-30-cases rule is applied as the minimum count (not observable).
- Size: unusual move +2.23 % per case over 18 bars, 0.159 of the coin's usual move (13.56 %); normal drift in its direction +2.93 %, total +5.16 %; 328 cases
Plan: `steps_cards/03_test_plan/night3_4h_run/plans/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h.md`
Record: `steps_cards/04_backtest/night3_4h_run/unseen_2016_2017/backtests/019-03_upward-breakout-quiet-continuation.b1_upward-breakout-on-more-coins.b1_large-breakouts-in-rising-coins_4h`
Measure: `measure.py`
