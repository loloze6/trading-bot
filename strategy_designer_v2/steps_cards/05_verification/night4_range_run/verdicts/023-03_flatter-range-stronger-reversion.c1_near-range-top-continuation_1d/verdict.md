---
plan: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d
idea: 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of 10-bar forward return minus coin mean on forecast: 0.000737896; OLS slope t: 2.17207 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; over at least 200 grid cases)
- Supporting check: timing gain (book mean daily return minus market-rise gain) above 0: 0.000436302, passed: True
- Counts: grid cases: 1691
- Decided by: The slope is positive with t >= 2 over at least 200 grid cases and the timing gain is above 0.
- Reading: The situation is read as the graded range position: a bar is on the plan's side when the forecast's sign equals the sign of the raw 30-close range position (above the middle long, below short, as 'more the closer to the top' implies); the regression uses every grid bar including zero forecasts, the coin mean is the mean of its grid 10-bar returns over all windows, and the book's daily returns are bar-to-bar postRebalance_total_value changes averaged over coins per timestamp.
- Size: unusual move +0.33 % per case over 10 bars, 0.018 of the coin's usual move (14.49 %); normal drift in its direction -0.06 %, total +0.27 %; 1579 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation_1d`
Measure: `measure.py`
