---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (7-bar forward return minus coin mean 7-bar return): 0.0136618; t of the mean: 3.76544 (threshold: t >= 2 (with check > 0) confirms, t <= -2 rejects, with at least 100 cases)
- Supporting check: top-half minus bottom-half forecast mean excess 7-bar return: 0.0228478, passed: True
- Counts: non-overlapping cases with forecast above 0: 2157
- Decided by: Main t is 2 or more with at least 100 cases and the top-minus-bottom half excess return is above 0.
- Reading: Situation taken as the regime gate (30-day return above 0, read from the recorded mom30 raw value, else recomputed from closes in the window, else the recorded regime) with a long forecast, not requiring the range part to be positive since the forecast averages both parts; the coin's mean 7-bar return is the mean over all non-overlapping grid bars of all its windows; the supporting check splits the cases at the median forecast (above median = top half, at or below = bottom half), using excess returns.
Plan: `steps_cards/03_test_plan/hold2_rerun_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d.md`
Record: `steps_cards/04_backtest/hold2_rerun_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1d`
Measure: `measure.py`
