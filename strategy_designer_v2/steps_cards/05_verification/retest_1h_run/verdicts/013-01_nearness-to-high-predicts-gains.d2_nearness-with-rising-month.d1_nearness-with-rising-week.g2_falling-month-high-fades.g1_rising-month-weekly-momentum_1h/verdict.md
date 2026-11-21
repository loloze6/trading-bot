---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess forward 168-bar return on raw 7-day return, trending grid bars: 0.000526811; OLS slope t: 3.6453 (threshold: confirm if slope t >= 2 (and supporting difference > 0); reject if t <= -2)
- Supporting check: mean excess forward return, forecast > 0 minus forecast = 0: 0.0197436, passed: True
- Counts: trending grid cases: 1196, forecast > 0 cases: 776, forecast = 0 cases: 420
- Decided by: The slope's t is 2 or more and the supporting difference is above 0.
- Reading: The 720-bar return is recomputed from closes inside each window (bars without 720 prior bars in the window are left out of the agreement); trending = regime column 'trending'; a coin's mean 168-bar return is the mean of its non-overlapping grid forward returns over all windows and all bars; the minimum counts are applied to grid cases with a forward return and a raw week value.
- Size: unusual move +0.66 % per case over 168 bars, 0.052 of the coin's usual move (12.47 %); normal drift in its direction +0.98 %, total +1.64 %; 1471 cases
Plan: `steps_cards/03_test_plan/retest_1h_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h.md`
Record: `steps_cards/04_backtest/retest_1h_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1h`
Measure: `measure.py`
