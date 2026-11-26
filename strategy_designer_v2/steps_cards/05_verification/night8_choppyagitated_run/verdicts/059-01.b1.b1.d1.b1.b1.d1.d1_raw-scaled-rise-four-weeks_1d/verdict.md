---
plan: 059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d
idea: 059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of the coin-demeaned 28-bar forward return on the forecast, pooled over coins, non-overlapping grid, non-zero forecast bars: -0.0421221; OLS slope t: -0.0421221 (threshold: t >= 2 with at least 50 grid cases (and timing gain > 0) confirms; t <= -2 with at least 50 grid cases rejects)
- Supporting check: timing gain: book mean daily return minus position held x coin's mean daily return: 3.71646e-05, passed: True
- Counts: grid cases with a non-zero forecast: 188
- Decided by: The slope's t is between -2 and 2 with at least 50 grid cases.
- Reading: Profile bars are those whose recorded regime is 'unknown' (the only regime with a strategy) and the expected side is the sign of the raw centred multiple; the coin's mean 28-bar return is taken on all its windows' non-overlapping grid bars, the regression has an intercept, and the timing gain uses daily returns of postRebalance_total_value with the previous day's postRebalance_current_allocation for the market part.
- Size: unusual move +0.13 % (t 0.08, the cases of one day together: 321 days) per case over 28 bars, 0.023 of the coin's usual move (28.73 %); normal drift in its direction -1.99 %, total -1.86 %; 496 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d`
Measure: `measure.py`
