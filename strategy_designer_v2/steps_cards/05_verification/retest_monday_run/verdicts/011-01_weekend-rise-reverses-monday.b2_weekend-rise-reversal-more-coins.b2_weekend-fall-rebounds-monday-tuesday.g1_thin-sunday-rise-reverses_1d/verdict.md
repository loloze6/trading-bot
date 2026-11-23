---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 2-bar move in the short's direction (Sunday close to Tuesday close, minus coin drift, negated): 0.0107954; ordinary t of the mean: 6.95134 (threshold: confirm: mean > 0 with t >= 2 and supporting difference > 0; reject: mean < 0 with t <= -2; fewer than 200 cases: not observable)
- Supporting check: mean unusual move of larger-|forecast| half minus smaller half (> 0): 7.34891e-05, passed: True
- Counts: cases: 2541, larger half: 1270, smaller half: 1271, active bars: 2572
- Decided by: The mean unusual move is above 0 with t >= 2 and the larger-|forecast| half minus the smaller half is above 0.
- Reading: Sunday bars are those whose UTC start timestamp falls on a Sunday and a rise is the raw component value > 0 (close over previous row's close when raw is missing); the return is close at row t+2 over close at t inside the window; the coin's drift is the mean of non-overlapping 2-bar returns at positions 0,2,4,... of each window pooled over all its windows; the median split puts cases with |forecast| strictly above the pooled median in the larger half and the rest in the smaller half.
- Size: unusual move +1.18 % per case over 2 bars, 0.157 of the coin's usual move (7.48 %); normal drift in its direction -0.29 %, total +0.89 %; 2266 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.g1_thin-sunday-rise-reverses_1d`
Measure: `measure.py`
