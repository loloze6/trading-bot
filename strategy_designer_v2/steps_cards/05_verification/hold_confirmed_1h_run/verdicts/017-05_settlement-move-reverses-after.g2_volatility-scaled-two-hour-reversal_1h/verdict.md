---
plan: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next 2-bar excess return on forecast: 4.19835e-05; OLS slope t: 13.7889 (threshold: slope t >= 2 to confirm (t <= -2 to reject) on at least 5000 independent cases)
- Supporting check: top minus bottom |forecast| quintile mean of sign(forecast) x excess 2-bar return, Welch t >= 2: 7.2124, passed: True
- Counts: pooled cases: 208278, top quintile cases: 41656, bottom quintile cases: 41656
- Decided by: The slope is positive with t >= 2 on at least 5000 independent cases, and the supporting check passes.
- Reading: Each coin's mean 2-bar return is taken over its non-overlapping grid in all windows; the regression is OLS with an intercept on all grid bars, zero forecasts included; the quintiles are pooled over coins (|f| >= 80th percentile and |f| <= 20th percentile, ties included); the check passes when top minus bottom is positive with Welch t >= 2.
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h`
Measure: `measure.py`
