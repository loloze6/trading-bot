---
plan: 002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound_1d
idea: 002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar forward return on forecast (forecast > 0, non-overlapping grid): 5.25081e-05; OLS slope t: 0.200084 (threshold: confirm if slope t >= 2 and top-quintile mean excess > 0; reject if slope t <= -2)
- Supporting check: mean excess 3-bar return of top-quintile forecast cases: 0.00314259, passed: True
- Counts: cases with a positive forecast: 2718, cases in the top quintile: 544
- Decided by: The slope's t lies between -2 and 2.
- Reading: Cases are pooled over all coins and windows on the 0,3,6,... grid of each window; the coin's mean 3-bar return is the mean over all its grid bars in all windows; the top quintile is cases with forecast at or above the pooled 80th percentile; the plan's 'fewer cases -> inconclusive' minimums are reported as 'not observable' per the workflow; a fall is a negative raw component value (price 1-bar return where the raw value is missing).
Plan: `steps_cards/03_test_plan/plans/002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/backtests/002-03_price-cross-above-long-sma.g1_volatility-scaled-one-day-fall-rebound_1d`
Measure: `measure.py`
