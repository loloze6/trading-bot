---
plan: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d
idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed 5-bar return on forecast, non-overlapping grid, coins pooled: 0.000544755; OLS slope t: 3.22385 (threshold: confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2)
- Supporting check: timing gain: book mean daily return before costs minus gain from market's rise: 0.000388146, passed: True
- Counts: grid cases: 3419
- Decided by: The slope is positive with t >= 2 and the timing gain is above zero.
- Reading: All grid bars count as cases, including bars with forecast 0. The regression has an intercept. The drift is each coin's mean grid 5-bar return over all windows. The timing gain uses per-bar position x next-bar return, averaged over coins per UTC day, minus position x the coin's mean daily return.
- Size: unusual move +0.40 % per case over 5 bars, 0.039 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.39 %; 2912 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d`
Measure: `measure.py`
