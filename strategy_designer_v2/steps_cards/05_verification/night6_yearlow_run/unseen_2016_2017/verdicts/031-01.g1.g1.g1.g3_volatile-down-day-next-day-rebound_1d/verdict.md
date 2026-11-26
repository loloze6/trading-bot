---
plan: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d
idea: 031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of next-day excess return on forecast: 0.00129846; OLS slope t, residuals summed per day: 1.15535 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects)
- Supporting check: top-third mean next-day excess return: 0.0149154, passed: True
- Counts: bars with forecast > 0: 236, days: 156, top third bars: 79
- Decided by: The slope's t is between -2 and 2 (inconclusive rule).
- Reading: The regime part of the situation is read from the recorded `regime` column (the volatility-rank detector is not recorded and 365 days of history are not in the windows), the down day from the fall component's raw value < 0 (the bar's close-to-close return when the raw value is missing); the coin's mean daily return is the mean of all its 1-bar returns over all windows; the slope's t uses day-clustered errors (x-deviation times residual summed per day, with G/(G-1) correction); the top third is the ceil(n/3) bars with the largest forecast; the 100-bar minimum counts bars with forecast > 0 and a next-day return in the same window.
- Size: unusual move +0.65 % (t 0.89, the cases of one day together: 107 days) per case over 1 bars, 0.143 of the coin's usual move (6.37 %); normal drift in its direction +0.73 %, total +1.38 %; 143 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/unseen_2016_2017/backtests/031-01.g1.g1.g1.g3_volatile-down-day-next-day-rebound_1d`
Measure: `measure.py`
