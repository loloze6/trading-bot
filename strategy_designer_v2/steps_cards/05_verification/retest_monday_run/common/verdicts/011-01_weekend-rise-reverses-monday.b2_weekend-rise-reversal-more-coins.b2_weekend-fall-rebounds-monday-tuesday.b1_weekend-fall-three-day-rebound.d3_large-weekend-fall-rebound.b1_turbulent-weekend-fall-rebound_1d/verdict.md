---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move of Sunday-close bets (forecast >= 2): 0.0189427; ordinary t of the mean: 5.55864 (threshold: positive with t >= 2 (and supporting check passes) to confirm; negative with t <= -2 to reject)
- Supporting check: mean unusual move, upper minus lower half at median forecast: 0.0116602, passed: True
- Counts: cases in total: 769, upper half cases: 384, lower half cases: 385
- Decided by: The mean unusual move is positive with t >= 2 and the upper-minus-lower half difference is above 0.
- Reading: The vol-ratio >= 1 condition is read from the recorded regime 'mean_reversion' because the detector's component is not recorded and its 365-day lookback cannot be rebuilt inside a window; the Sunday bar is the bar starting on a Sunday (UTC); cases are all Sunday-close bars with forecast >= 2 having a bar t+3 in the same window (Sundays are 7 bars apart, so none overlap); the coin's normal 3-day drift is the mean of non-overlapping 3-bar returns at positions 0,3,6,... of each of its windows pooled; the median split puts forecasts above the median in the upper half and those at or below it in the lower half.
- Size: unusual move +1.89 % (t 2.78, the cases of one day together: 205 days) per case over 3 bars, 0.232 of the coin's usual move (8.57 %); normal drift in its direction +0.36 %, total +2.25 %; 770 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/common/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound.b1_turbulent-weekend-fall-rebound_1d`
Measure: `measure.py`
