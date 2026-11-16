---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-bar excess return on forecast, pooled: 0.00014278; OLS slope t: 4.238 (threshold: slope t >= 2 (with positive timing gain) confirms; slope t <= -2 rejects)
- Supporting check: book timing gain before costs (mean daily): -0.000132072, passed: False
- Counts: bars with a non-zero forecast: 17363, bars in the regression: 17380
- Decided by: The slope t is 2 or more but the book's timing gain is zero or below.
- Reading: Situation bars are those with a non-zero recorded raw vsr value (the one-day move over the 20-day std, price return used where it is missing), with the expected side being the opposite sign of that move; the slope is plain OLS with an intercept on every in-window bar with a next close (horizon 1, so the non-overlapping grid is every bar), the count is bars with a non-zero forecast in that regression, and the timing gain uses per-coin daily returns of postRebalance_total_value averaged across coins by day.
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.g1_one-day-move-reversal_1d`
Measure: `measure.py`
