---
plan: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t-statistic of the pooled OLS slope of excess 10-bar forward return on forecast (trending, 10-bar grid): 3.07623; OLS slope t: 3.07623 (threshold: confirm: slope > 0 with t >= 2 and top-minus-bottom-third > 0; reject: slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: mean excess 10-bar return, top third of forecasts minus bottom third: 0.0440079, passed: True
- Counts: independent grid cases in regime trending: 833
- Decided by: Slope positive with t = 3.08 >= 2 and top-minus-bottom-third difference 0.0440 > 0: confirm rule met.
- Reading: Coin mean 10-bar return taken over all grid samples of all its windows (all regimes), cases are grid bars whose `regime` is trending, and thirds are the n//3 lowest and n//3 highest forecasts by sorted rank.
Plan: `steps_cards/03_test_plan/demo_run/plans/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d.md`
Record: `steps_cards/04_backtest/demo_run/backtests/002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d`
Measure: `measure.py`
