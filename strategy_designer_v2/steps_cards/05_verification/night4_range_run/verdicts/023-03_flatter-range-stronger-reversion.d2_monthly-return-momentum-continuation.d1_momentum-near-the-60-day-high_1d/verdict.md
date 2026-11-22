---
plan: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d
idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of 5-bar excess forward return on post_pipeline_value, pooled: 0.000272521; OLS slope t: 1.30444 (threshold: confirm: t >= +2.0 with timing gain > 0; reject: t <= -2.0; at least 300 grid cases with non-zero forecast)
- Supporting check: mean daily timing gain of the book: 0.000562759, passed: True
- Counts: grid cases with a non-zero forecast: 3418, grid cases in regression: 3419, book days: 2898
- Decided by: Slope t is between -2.0 and +2.0.
- Reading: Expected side = sign of the 30-day return (raw component sign); the regression uses all grid bars (zero forecasts included) with the coin's drift as the mean 5-bar grid return over all its windows; 'non-zero forecast' counted on post_pipeline_value; book daily returns from postRebalance_total_value with the previous day's position for the market part; a minimum count not reached is reported as 'not observable'.
- Size: unusual move +0.95 % per case over 5 bars, 0.087 of the coin's usual move (10.60 %); normal drift in its direction +0.17 %, total +1.13 %; 1548 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high_1d`
Measure: `measure.py`
