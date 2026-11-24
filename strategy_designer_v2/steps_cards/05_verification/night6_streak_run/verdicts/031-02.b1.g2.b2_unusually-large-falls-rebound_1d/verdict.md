---
plan: 031-02.b1.g2.b2_unusually-large-falls-rebound_1d
idea: 031-02.b1.g2.b2_unusually-large-falls-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 2-day return minus normal drift on the forecast (pooled, non-overlapping grid): 0.0003902; slope t, cases summed per day (day-clustered): 1.80899 (threshold: t >= 2 with the supporting check passing confirms; t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean 2-day return minus normal drift on grid bars in the top fifth of positive forecasts, above 0: 0.00729167, passed: True
- Counts: grid bars with a positive forecast: 4217, distinct days of those grid bars: 1125, grid bars (all): 8650, distinct days (all grid bars): 1509
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Grid at positions 0,2,4,... of each window with all grid bars (forecast 0 included) in the regression; normal drift is the coin's mean 2-day grid return over all its windows; the slope's t uses day-summed score contributions (cluster-robust, G/(G-1) correction); the top fifth is forecasts at or above the 80th percentile of positive grid forecasts pooled over coins; the minimum counts count positive-forecast grid bars with a valid 2-day return, and failing them gives 'not observable'.
- Size: unusual move +0.15 % (t 0.86, the cases of one day together: 1623 days) per case over 2 bars, 0.021 of the coin's usual move (6.58 %); normal drift in its direction +0.24 %, total +0.38 %; 5183 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.g2.b2_unusually-large-falls-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b2_unusually-large-falls-rebound_1d`
Measure: `measure.py`
