---
plan: 002-03_price-cross-above-sma-up_1h
idea: 002-03_price-cross-above-sma-up
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of forward 24-bar return minus window mean, on forecast: -4.95899e-05; OLS slope t: -0.32363 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: two-proportion z: share of positive 24-bar returns, forecast > 0 vs all sampled bars: -2.28721, passed: False
- Counts: non-overlapping sampled cases with forecast > 0 pooled: 340, windows containing such cases: 6, sampled bars: 724
- Decided by: Inconclusive: the slope's t lies between -2 and 2.
- Reading: The window's mean 24-bar return is taken as the mean forward 24-bar return over that window's non-overlapping sampled bars (grid 0, 24, 48, ... with a full forward window), the slope's t is the OLS t on the pooled samples, and the supporting check, which has no threshold in the plan, counts as passed when z >= 1.96.
Plan: `steps_cards/03_test_plan/hourly_run/plans/002-03_price-cross-above-sma-up_1h.md`
Record: `steps_cards/04_backtest/hourly_run/backtests/002-03_price-cross-above-sma-up_1h`
Measure: `measure.py`
