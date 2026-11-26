---
plan: 032-02.g1.e2.e1_new-closing-high-continuation_1d
idea: 032-02.g1.e2.e1_new-closing-high-continuation
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 10-bar return, new-high (prox=1) minus other in-regime grid cases: 0.0478324; Welch t: 1.27898 (threshold: Welch t >= 2 (with correlation > 0) confirms; Welch t <= -2 rejects; at least 30 grid cases per group)
- Supporting check: correlation of prox with excess 10-bar return across in-regime grid cases: 0.142142, passed: True
- Counts: new-high grid cases: 19, other in-regime grid cases: 75, all in-regime grid cases: 94
- Decided by: The plan's minimum of 30 grid cases in each group is not reached (new-high 19, other 75).
- Reading: In-regime grid cases are grid bars (positions 0,10,20,... of each window) with a recorded prox value; new-high means prox equal to 1 within 1e-9; the coin's mean 10-bar return is taken over the same non-overlapping grid of all its windows; for bars with fewer than 28 in-window bars of history the situation check uses the recorded regime ('trending').
- Size: unusual move +1.07 % (t 0.66, the cases of one day together: 64 days) per case over 10 bars, 0.076 of the coin's usual move (9.14 %); normal drift in its direction +0.32 %, total +1.39 %; 111 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-02.g1.e2.e1_new-closing-high-continuation_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/unseen_2026/backtests/032-02.g1.e2.e1_new-closing-high-continuation_1d`
Measure: `measure.py`
