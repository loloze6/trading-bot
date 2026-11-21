---
plan: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
idea: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the mean unusual 240-bar move after a long bet, pooled over coins: 0.0107695; t of the mean: 2.08111 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and slope check passes; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: t of the OLS slope of unusual move on signal forecast (positive, t >= 1): 0.709087, passed: False
- Counts: cases: 1090
- Decided by: t >= 2 but the slope check fails.
- Reading: Situation = raw component > 0 and, where the window's prices allow, a negative 24-bar and positive 720-bar return; a bet is a rise of the positive forecast of >= 2 points from its lowest positive level since the last bet (from 0 at a window start or after a flat), the first bet of each 240-bar grid cell (counted from each window's first row) is the case; drift is the coin's mean non-overlapping 240-bar return over all its windows; the slope is an OLS of the unusual move on the signal bar's forecast; fewer than 30 cases is reported as not observable.
- Size: unusual move +1.08 % per case over 240 bars, 0.067 of the coin's usual move (14.43 %); normal drift in its direction +1.36 %, total +2.44 %; 1090 cases
Plan: `steps_cards/03_test_plan/night3_1h_run/plans/018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h.md`
Record: `steps_cards/04_backtest/night3_1h_run/backtests/018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h`
Measure: `measure.py`
