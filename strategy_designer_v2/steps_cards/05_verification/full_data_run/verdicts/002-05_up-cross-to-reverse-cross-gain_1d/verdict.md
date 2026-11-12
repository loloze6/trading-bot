---
plan: 002-05_up-cross-to-reverse-cross-gain_1d
idea: 002-05_up-cross-to-reverse-cross-gain
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: excess mean next-bar return while forecast > 0 vs all bars (pooled): -1.57075e-05; Newey-West t (10 lags): -0.0427241 (threshold: excess > 0 with t >= 2 confirms; excess < 0 with t <= -2 rejects)
- Supporting check: binomial z of up-bar share while forecast > 0 vs per-coin baseline: 0.114022, passed: False
- Counts: distinct up-cross spans: 127, bars with a positive forecast: 8569
- Decided by: The t-statistic lies between -2 and 2, which the plan calls inconclusive.
- Reading: The situation is the raw SMA spread above 0 on the long side; the Newey-West t is the t of the slope in a regression of next-bar return on a forecast>0 indicator with lag sums kept within each coin-window; an up bar is a positive next-bar return; a span is a run of consecutive positive-forecast bars within one window; and confirmation requires both t >= 2 and z >= 2.
Plan: `steps_cards/03_test_plan/full_data_run/plans/002-05_up-cross-to-reverse-cross-gain_1d.md`
Record: `steps_cards/04_backtest/full_data_run/backtests/002-05_up-cross-to-reverse-cross-gain_1d`
Measure: `measure.py`
