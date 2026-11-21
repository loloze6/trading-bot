---
plan: 020-01_resistance-retest-turns-down_1d
idea: 020-01_resistance-retest-turns-down
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of drift-adjusted 5-bar return on forecast (forecast < 0, grid bars): -4.39712e-05; OLS slope t: -0.171628 (threshold: confirm if t >= 2 with the supporting check passing; reject if t <= -2)
- Supporting check: mean unusual 5-bar move in short direction of cases (forecast <= -5): -0.000370423, passed: False
- Counts: cases with forecast at -5 or below: 1720, grid bars with a non-zero forecast: 3226
- Decided by: The slope's t is between -2 and +2.
- Reading: Cases are short-side bets (a rise of |forecast| of at least 2 points from its lowest since the last bet) with forecast <= -5, the first one per 5-bar grid cell, measured from that bar's close over 5 bars within the window; the regression uses grid bars (positions 0,5,10,...) with forecast < 0 and an OLS fit with intercept; drift is each coin's mean non-overlapping 5-bar return over all its windows.
- Size: unusual move -0.05 % per case over 5 bars, 0.002 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total -0.64 %; 1967 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down_1d`
Measure: `measure.py`
