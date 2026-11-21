---
plan: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d
idea: 020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar forward return minus normal drift on post_pipeline_value: 0.000732401; OLS slope t: 2.43663 (threshold: t >= 2 over at least 300 cases confirms (with timing gain > 0); t <= -2 over at least 300 cases rejects)
- Supporting check: timing gain before costs (mean daily book return minus position x coin mean daily return): 0.000389204, passed: True
- Counts: grid cases: 3419
- Decided by: The slope's t is 2 or more over at least 300 cases and the timing gain before costs is above 0.
- Reading: Slope is an OLS with intercept on grid bars 0,5,10,... of each window (pooled), normal drift is each coin's mean grid 5-bar return over all its windows, and the timing gain uses each bar as a day, the book's daily return being the mean over coins of position x next-bar return.
- Size: unusual move +0.60 % per case over 5 bars, 0.051 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +1.19 %; 1342 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d3_nearness-to-90-day-high_1d`
Measure: `measure.py`
