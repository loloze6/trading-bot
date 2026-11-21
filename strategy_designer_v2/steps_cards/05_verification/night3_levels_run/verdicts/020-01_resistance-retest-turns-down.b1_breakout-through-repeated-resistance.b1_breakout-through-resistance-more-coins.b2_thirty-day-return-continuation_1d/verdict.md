---
plan: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d
idea: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-excess 10-bar forward return on forecast (non-overlapping grid): 0.001012; OLS slope t: 3.81933 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: none
- Counts: grid cases with a recorded forecast: 3598
- Decided by: Confirm rule met: the slope is positive with t >= 2.
- Reading: Grid bars are positions 0, 10, 20, ... of each window with a 10-bar forward return inside the window; the coin's mean is the mean of these grid returns over all its windows; every grid bar with a non-missing forecast (zeros included) enters an OLS regression with an intercept; and the plan's 300-case minimum is applied as 'not observable'.
- Size: unusual move +1.52 % per case over 10 bars, 0.078 of the coin's usual move (16.82 %); normal drift in its direction -0.09 %, total +1.43 %; 3092 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b2_thirty-day-return-continuation_1d`
Measure: `measure.py`
