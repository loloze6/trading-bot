---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 72-bar return on forecast, trending grid bars: 0.000469128; OLS slope t: 1.90152 (threshold: confirm if t >= 2 with the supporting check passing; reject if t <= -2)
- Supporting check: mean excess return, top third of positive forecasts minus forecast 0: 0.00978564, passed: True
- Counts: pooled trending-regime grid cases: 2837, grid cases with a positive forecast: 1190, grid cases with forecast 0: 1647
- Decided by: The slope's t lies between -2 and 2.
- Reading: Trending-regime grid bars are those whose recorded regime is 'trending' at grid positions 0, 72, 144, ... of each window with a full 72-bar forward return inside the window, the coin's mean 72-bar return is the mean over all its grid bars of all windows, the top third of positive forecasts is the ceil(n/3) largest positive grid forecasts pooled over coins, and the situation check uses the 720-bar return from prices (the recorded regime where the window lacks 720 bars of history) with the recorded relvol raw value.
- Size: unusual move +0.61 % per case over 72 bars, 0.068 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +1.01 %; 2348 cases
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h`
Measure: `measure.py`
