---
plan: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 24-bar return after bets, both coins: -0.000931123; t of the mean: -1.56223 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of excess 24-bar return on signal-bar forecast: 2.37223e-05, passed: True
- Counts: cases over both coins: 4990, cases BTCUSD: 2478, cases ETHUSD: 2512
- Decided by: t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A bet is the first bar in each 24-bar grid cell (from each window's first row) where the positive forecast rises at least 2 points above its lowest level since the last bet (reset to 0 when flat), the drift is each coin's own pooled grid mean, cases of both coins are pooled for the mean, t and slope, and the plan's count below 30 is reported as not observable.
- Size: unusual move -0.09 % per case over 24 bars, -0.022 of the coin's usual move (4.12 %); normal drift in its direction +0.15 %, total +0.05 %; 4990 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h`
Measure: `measure.py`
