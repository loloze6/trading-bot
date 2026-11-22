---
plan: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d
idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 5-day forward return minus coin mean 5-day return on recorded forecast, non-overlapping 5-bar grid: 0.000717243; OLS slope t: 2.3411 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; else inconclusive)
- Supporting check: none
- Counts: grid cases with forecast > 0: 1646, grid cases: 3419
- Decided by: The slope is positive with t = 2.34 >= 2 (confirm rule); no supporting check.
- Reading: Situation taken as raw component > 0 (close above the range middle with a nonzero flatness factor, 'far above' having no stated cut-off) on the long side; the coin's mean 5-day return is the mean of its non-overlapping grid returns over all windows; the slope is from OLS with an intercept; the plan's 'fewer than 200 grid cases with forecast > 0' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.34 % per case over 5 bars, 0.035 of the coin's usual move (10.60 %); normal drift in its direction +0.59 %, total +0.93 %; 1793 cases
Plan: `steps_cards/03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d.md`
Record: `steps_cards/04_backtest/night4_range_run/backtests/023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation.d1_flat-range-upside-breakout-continuation_1d`
Measure: `measure.py`
