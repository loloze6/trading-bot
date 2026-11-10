---
plan: 002-03_price-cross-above-sma-up_1h
idea: 002-03_price-cross-above-sma-up
fit: adapted
status: inconclusive
---
Situation check: 1 of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next 24-bar return minus window mean 24-bar return on forecast: -4.95899e-05; OLS slope t: -0.32363 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: share of positive 24-bar returns, forecast > 0 vs all sampled bars (two-proportion z): -2.28721, passed: False
- Counts: non-overlapping sampled cases with forecast > 0 pooled: 340, windows containing such cases: 6, sampled cases pooled: 724
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: The window's mean 24-bar return is the mean over that window's non-overlapping sampled bars (positions 0, 24, 48, ... with a full 24-bar return inside the window), the regression is pooled OLS with an intercept, and the supporting check counts as passed when its pooled two-proportion z is at least 1.96 since the plan names no threshold for it.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-03_price-cross-above-sma-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-03_price-cross-above-sma-up_1h`
Measure: `measure.py`
