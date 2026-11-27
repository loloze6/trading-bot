---
plan: 032-02.g1.e2.e1_new-closing-high-continuation_1d
idea: 032-02.g1.e2.e1_new-closing-high-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar return, new-high (prox=1) minus other in-regime grid cases: 0.0347954; Welch t: 2.75501 (threshold: Welch t >= 2 (with correlation > 0) confirms; Welch t <= -2 rejects; at least 30 grid cases per group)
- Supporting check: correlation of prox with excess 10-bar return across in-regime grid cases: 0.0583809, passed: True
- Counts: new-high grid cases: 524, other in-regime grid cases: 1982, all in-regime grid cases: 2506
- Decided by: Welch t >= 2 and the correlation of prox with the excess return is above 0 (confirm rule).
- Reading: In-regime grid cases are grid bars (positions 0,10,20,... of each window) with a recorded prox value; new-high means prox equal to 1 within 1e-9; the coin's mean 10-bar return is taken over the same non-overlapping grid of all its windows; for bars with fewer than 28 in-window bars of history the situation check uses the recorded regime ('trending').
- Size: unusual move +1.58 % (t 2.30, the cases of one day together: 1171 days) per case over 10 bars, 0.080 of the coin's usual move (16.74 %); normal drift in its direction +1.46 %, total +3.04 %; 2964 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e1_new-closing-high-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/common/backtests/032-02.g1.e2.e1_new-closing-high-continuation_1d`
Measure: `measure.py`
