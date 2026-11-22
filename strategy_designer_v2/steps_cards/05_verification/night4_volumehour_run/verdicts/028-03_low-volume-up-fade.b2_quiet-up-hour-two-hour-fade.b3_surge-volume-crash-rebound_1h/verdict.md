---
plan: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h
idea: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 2-bar unusual move (return minus coin's normal 2-bar drift) over long bets: 0.00028103; t of the mean: 2.37574 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on signal-bar forecast: -4.94978e-06, passed: False
- Counts: independent cases across both coins: 14913, cases BTCUSD: 7318, cases ETHUSD: 7595
- Decided by: The mean unusual move is positive with t >= 2 but the slope on the forecast is zero or negative.
- Reading: Bets are rises of the long forecast of at least 2 points from its lowest long level since the last bet (from 0 after a flat), one case per 2-bar grid cell of each window (the cell's first bet); the drift is each coin's mean non-overlapping 2-bar return over all its windows; the slope is ordinary least squares of the unusual move on the signal bar's forecast; the plan's 30-case minimum, when missed, gives 'not observable' as the workflow requires.
- Size: unusual move +0.03 % per case over 2 bars, 0.025 of the coin's usual move (1.16 %); normal drift in its direction +0.01 %, total +0.04 %; 14913 cases
Plan: `steps_cards/03_test_plan/night4_volumehour_run/plans/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h.md`
Record: `steps_cards/04_backtest/night4_volumehour_run/backtests/028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b3_surge-volume-crash-rebound_1h`
Measure: `measure.py`
