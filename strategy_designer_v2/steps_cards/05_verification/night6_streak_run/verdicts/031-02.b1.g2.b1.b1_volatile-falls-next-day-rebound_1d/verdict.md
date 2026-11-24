---
plan: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound_1d
idea: 031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on forecast (forecast > 0, pooled): 0.000290295; day-clustered OLS t: 2.38358 (threshold: confirm: slope > 0 with day-clustered t >= 2 and supporting check passes; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: mean excess next-day return, top fifth minus bottom fifth of forecasts: 0.0047858, passed: True
- Counts: cases with forecast > 0: 18028, distinct days: 2405
- Decided by: The slope is positive with t >= 2 and the top fifth's mean excess return is above the bottom fifth's (confirm rule).
- Reading: The situation is a down day (close below the previous close in the same window, or a positive raw component value on a window's first bar) on the long side; the slope is an OLS fit with intercept whose t uses standard errors clustered by UTC day (with the usual G/(G-1)*(N-1)/(N-K) correction); the top and bottom fifths are the highest and lowest floor(n/5) cases by forecast, ties broken stably by record order.
- Size: unusual move +0.06 % (t 0.45, the cases of one day together: 2024 days) per case over 1 bars, 0.012 of the coin's usual move (5.31 %); normal drift in its direction +0.15 %, total +0.20 %; 12110 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b1.b1_volatile-falls-next-day-rebound_1d`
Measure: `measure.py`
