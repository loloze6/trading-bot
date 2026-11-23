---
plan: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d
idea: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of slope of 3-bar excess return on forecast, down-day grid bars: 0.00130253; OLS slope t: 3.06559 (threshold: confirm if t >= 2 (with timing gain > 0); reject if t <= -2; else inconclusive)
- Supporting check: book timing gain (mean daily return minus position x coin mean daily return): -7.88094e-05, passed: False
- Counts: down-day grid cases: 2718, active bars: 8453
- Decided by: The slope's t is 2 or more but the timing gain is at or below 0 (the plan's inconclusive rule).
- Reading: The situation is checked from prices as close below the previous close inside the same window, with the first bar of each window left out of the check since its prior close is not recorded; the coin's mean 3-bar return is taken on the same non-overlapping grid of all bars of all its windows; the timing gain is read on daily book returns (postRebalance_total_value, inside windows, mean over coins per day) minus the position held into the day times the coin's mean daily return over all windows, averaged the same way; a count under the plan's 200 cases is reported as not observable, as the workflow requires.
- Size: unusual move +0.08 % per case over 3 bars, 0.009 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.44 %; 4353 cases
Plan: `steps_cards/03_test_plan/retest_learned_run/plans/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d.md`
Record: `steps_cards/04_backtest/retest_learned_run/backtests/022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises.b1_range-versus-norm-both-sides.g1_wide-falling-days-rebound.g2_down-day-close-near-high_1d`
Measure: `measure.py`
