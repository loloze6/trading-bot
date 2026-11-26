---
plan: 032-02.g1.e2.e1_new-closing-high-continuation_1d
idea: 032-02.g1.e2.e1_new-closing-high-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar return, new-high (prox=1) minus other in-regime grid cases: 0.0419109; Welch t: 0.745296 (threshold: Welch t >= 2 (with correlation > 0) confirms; Welch t <= -2 rejects; at least 30 grid cases per group)
- Supporting check: correlation of prox with excess 10-bar return across in-regime grid cases: 0.0606026, passed: True
- Counts: new-high grid cases: 47, other in-regime grid cases: 136, all in-regime grid cases: 183
- Decided by: Welch t lies between -2 and 2 (inconclusive rule).
- Reading: In-regime grid cases are grid bars (positions 0,10,20,... of each window) with a recorded prox value; new-high means prox equal to 1 within 1e-9; the coin's mean 10-bar return is taken over the same non-overlapping grid of all its windows; for bars with fewer than 28 in-window bars of history the situation check uses the recorded regime ('trending').
- Size: unusual move +5.02 % (t 1.85, the cases of one day together: 140 days) per case over 10 bars, 0.173 of the coin's usual move (30.80 %); normal drift in its direction +10.03 %, total +15.05 %; 192 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e1_new-closing-high-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/unseen_2016_2017/backtests/032-02.g1.e2.e1_new-closing-high-continuation_1d`
Measure: `measure.py`
