---
plan: 002-05_up-cross-to-reverse-cross-gain_1d
idea: 002-05_up-cross-to-reverse-cross-gain
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar return while forecast > 0 minus mean next-bar return over all bars (pooled): -1.57075e-05; Newey-West t (10 lags): -0.0272464 (threshold: confirm: excess > 0 with Newey-West(10) t >= 2; reject: excess < 0 with t <= -2)
- Supporting check: up-bar share while forecast > 0 vs coin's own up-bar share (binomial z): 0.114022, passed: False
- Counts: distinct up-cross spans pooled across coins: 92, bars with a positive forecast: 8569, all bars (next-bar returns): 17022
- Decided by: The Newey-West t of the excess mean return lies between -2 and 2.
- Reading: Situation is sma_cross raw value > 0 with a positive forecast; next-bar returns stay inside each window and the all-bars baseline pools every coin and window; Newey-West autocovariances use only pairs of positive-forecast bars in the same window; an up-cross span is a run of positive forecast, merged across time-contiguous windows; the binomial z sums each coin's expected up count from its own pooled up share; unmet minimum counts give 'not observable' as the workflow requires.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-05_up-cross-to-reverse-cross-gain_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Measure: `measure.py`
