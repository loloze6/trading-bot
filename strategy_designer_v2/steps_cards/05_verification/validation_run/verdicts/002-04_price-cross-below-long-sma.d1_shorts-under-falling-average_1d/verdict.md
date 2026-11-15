---
plan: 002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d
idea: 002-04_price-cross-below-long-sma.d1_shorts-under-falling-average
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: ordinary t of mean allocation x (20-bar return minus coin mean 20-bar return), shorts only: -0.00296516; ordinary t of the mean: -0.371636 (threshold: confirm if t >= 2 and supporting slope < 0; reject if t <= -2; inconclusive otherwise or if fewer than 30 active cases)
- Supporting check: OLS slope of excess 20-bar return on |forecast|, must be below 0: 0.00197786, passed: False
- Counts: active cases: 300
- Decided by: The main t lies between -2 and 2.
- Reading: Situation checked as regime == 'trending' (detector's close below SMA200) and raw 20-bar SMA200 slope (last_history_value) below 0 with forecast below 0; allocation x is the postRebalance_current_allocation held after the case bar's trade, the coin's mean 20-bar return is taken over all non-overlapping grid bars of all its windows, and a case requires forecast < 0 at the grid bar and a close 20 bars later in the same window.
Plan: `steps_cards/03_test_plan/plans/002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d.md`
Record: `steps_cards/04_backtest/backtests/002-04_price-cross-below-long-sma.d1_shorts-under-falling-average_1d`
Measure: `measure.py`
