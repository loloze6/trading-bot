---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (3-bar return minus coin mean 3-bar return) on Sunday cases: 0.0105047; ordinary t of the mean: 6.58056 (threshold: t >= 2 confirms (with the supporting check), t <= -2 rejects, over at least 200 cases)
- Supporting check: thin minus heavy weekend-volume half, strength (fade-direction unusual 3-bar move / usual 3-bar move), Welch t >= 1: 0.33726, passed: False
- Counts: cases: 5176, thin_half: 2129, heavy_half: 2129
- Decided by: The main t is 2 or more but the thin-minus-heavy Welch t is below 1 (or could not be computed), which the plan calls inconclusive.
- Reading: Cases are bars starting on a UTC Sunday with a non-zero forecast and a full 3-bar return inside the window; the coin's mean and usual 3-bar move come from the non-overlapping grid 0,3,6,... of each window pooled over its windows; the volume factor is the mean volume of bars t-21..t-2 over the mean of bars t-1 and t, thin half above the pooled median and heavy half at or below it; the fade direction is the forecast's sign.
- Size: unusual move +0.83 % per case over 3 bars, 0.094 of the coin's usual move (9.14 %); normal drift in its direction +0.01 %, total +0.84 %; 4632 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d1_weekend-fall-rebound-volatile.g1_thin-weekend-sunday-move-reverses_1d`
Measure: `measure.py`
