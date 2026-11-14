---
plan: 002-05_up-cross-to-reverse-cross-gain_1d
idea: 002-05_up-cross-to-reverse-cross-gain
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return when forecast > 0 minus mean next-bar return over all bars, pooled: -1.57075e-05; Newey-West t (10 lags): -0.0427241 (threshold: excess > 0 with t >= 2 to confirm; excess < 0 with t <= -2 to reject)
- Supporting check: up-bar share when forecast > 0 minus coin-baseline up share (binomial z): 0.114022, passed: False
- Counts: distinct up-cross spans: 127, bars with a positive forecast: 8569, all bars: 17022
- Decided by: The Newey-West t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Spans are maximal runs of forecast > 0 inside each window; the t-statistic uses a Bartlett Newey-West variance of the influence function of (mean_in - mean_all), with autocovariances taken only within windows; an up bar is a positive next-bar return; the up-share z-test is required for confirmation.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-05_up-cross-to-reverse-cross-gain_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Measure: `measure.py`
