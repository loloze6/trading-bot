---
plan: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h
idea: 017-02_presettle-rise-after-downtrend.g3_daily-move-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of the slope of next-24-bar excess return on forecast (non-overlapping grid, pooled): 3.90177; OLS slope t: 3.90177 (threshold: confirm if slope t >= 2 with timing gain > 0; reject if slope t <= -2; at least 500 independent 24-bar cases)
- Supporting check: book's mean daily timing gain (before costs) above 0: 0.000542295, passed: True
- Counts: independent 24-bar cases: 17246, days in timing check: 2898
- Decided by: The slope's t-statistic is 2 or more and the mean daily timing gain is above 0.
- Reading: Coin mean 24-bar return taken as the mean of that coin's grid 24-bar returns pooled over all its windows; OLS with intercept; the book's daily return before costs is the sum of each bar's position x next-bar return over the day, the market gain uses the day's mean position x the coin's pooled mean daily return, and days are averaged across coins by date.
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-02_presettle-rise-after-downtrend.g3_daily-move-reversal_1h`
Measure: `measure.py`
