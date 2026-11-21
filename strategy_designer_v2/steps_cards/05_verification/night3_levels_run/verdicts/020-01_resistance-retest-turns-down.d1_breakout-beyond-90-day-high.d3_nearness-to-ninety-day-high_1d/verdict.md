---
plan: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d
idea: 020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of 20-bar excess return on forecast, grid cases pooled: 0.00209297; OLS slope t: 0.73351 (threshold: confirm if slope t >= 2 with top-minus-bottom quintile > 0; reject if slope t <= -2)
- Supporting check: top minus bottom quintile mean excess 20-bar return: 0.0293522, passed: True
- Counts: grid cases: 827, top quintile cases: 166, bottom quintile cases: 166
- Decided by: The slope t is between -2 and 2.
- Reading: Expected side rebuilt as sign(standardised distance + 10) from dist_high's post-pipeline value (rebuilt from raw values where missing); grid cases include every grid bar with a full 20-bar forward return inside its window, including zero forecasts; the coin's mean 20-bar return is the mean of its grid returns over all windows; quintiles are the bars at or above the 80th and at or below the 20th percentile of the pooled grid forecasts.
- Size: unusual move +2.74 % per case over 20 bars, 0.092 of the coin's usual move (21.24 %); normal drift in its direction +0.65 %, total +3.39 %; 487 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d1_breakout-beyond-90-day-high.d3_nearness-to-ninety-day-high_1d`
Measure: `measure.py`
