---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move of Sunday-close bets (forecast >= 2): 0.0214985; ordinary t of the mean: 4.83212 (threshold: positive with t >= 2 (and supporting check passes) to confirm; negative with t <= -2 to reject)
- Supporting check: mean unusual move, upper minus lower half at median forecast: 0.0217106, passed: True
- Counts: cases in total: 520, upper half cases: 260, lower half cases: 260
- Decided by: The mean unusual move is positive with t >= 2 and the upper-minus-lower half difference is above 0.
- Reading: The vol-ratio >= 1 condition is read from the recorded regime 'mean_reversion' because the detector's component is not recorded and its 365-day lookback cannot be rebuilt inside a window; the Sunday bar is the bar starting on a Sunday (UTC); cases are all Sunday-close bars with forecast >= 2 having a bar t+3 in the same window (Sundays are 7 bars apart, so none overlap); the coin's normal 3-day drift is the mean of non-overlapping 3-bar returns at positions 0,3,6,... of each of its windows pooled; the median split puts forecasts above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +2.14 % per case over 3 bars, 0.261 of the coin's usual move (8.82 %); normal drift in its direction +0.43 %, total +2.58 %; 521 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d`
Measure: `measure.py`
