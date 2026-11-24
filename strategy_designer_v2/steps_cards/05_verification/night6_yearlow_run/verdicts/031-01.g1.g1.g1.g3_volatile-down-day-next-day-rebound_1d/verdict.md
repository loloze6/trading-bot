---
plan: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d
idea: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of next-day excess return on forecast: 0.00115227; OLS slope t, residuals summed per day: 2.48215 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects)
- Supporting check: top-third mean next-day excess return: 0.0161028, passed: True
- Counts: bars with forecast > 0: 1576, days: 766, top third bars: 526
- Decided by: The slope is positive with t >= 2 and the top-third mean excess return is above 0 (confirm rule).
- Reading: The regime part of the situation is read from the recorded `regime` column (the volatility-rank detector is not recorded and 365 days of history are not in the windows), the down day from the fall component's raw value < 0 (the bar's close-to-close return when the raw value is missing); the coin's mean daily return is the mean of all its 1-bar returns over all windows; the slope's t uses day-clustered errors (x-deviation times residual summed per day, with G/(G-1) correction); the top third is the ceil(n/3) bars with the largest forecast; the 100-bar minimum counts bars with forecast > 0 and a next-day return in the same window.
- Size: unusual move +0.69 % (t 2.00, the cases of one day together: 538 days) per case over 1 bars, 0.153 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +0.82 %; 1031 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d`
Measure: `measure.py`
