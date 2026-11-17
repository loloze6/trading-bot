---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope t of excess 7-bar return on forecast: 1.95549; OLS slope t: 1.95549 (threshold: confirm if t >= 2 with supporting check passing; reject if t <= -2)
- Supporting check: per-coin slope of excess 7-bar return on forecast positive in at least 4 of 6 coins: 4, passed: True
- Counts: non-overlapping 7-bar cases pooled across coins: 2443, coins with positive slope: 4
- Decided by: Pooled slope t = 1.96 lies between -2 and 2 over 2443 cases.
- Reading: Grid at positions 0, 7, 14, ... of each window keeping only points with a full 7-bar forward return inside the window, the coin's mean taken over its grid returns from all windows, OLS with intercept on all grid bars including zero forecasts, and the supporting check needs 4 positive per-coin slopes among the coins present.
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d`
Measure: `measure.py`
