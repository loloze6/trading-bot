---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of coin-demeaned 5-bar forward return on forecast (trending, non-overlapping grid): 0.00147698; OLS slope t: 3.31556 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 100 grid cases with regime trending and forecast > 0)
- Supporting check: none
- Counts: grid cases with regime trending and forecast > 0: 1032, grid cases with regime trending: 1674
- Decided by: The pooled slope is positive with t >= 2 (confirm rule).
- Reading: The coin's mean 5-bar return is taken over all grid bars of all its windows (every regime), the pooled regression is an OLS with intercept over all coins' trending grid bars, and the 200-day gate is read from the regime column since the detector's component is not recorded.
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e2_short-drift-after-strong-highs_1d`
Measure: `measure.py`
