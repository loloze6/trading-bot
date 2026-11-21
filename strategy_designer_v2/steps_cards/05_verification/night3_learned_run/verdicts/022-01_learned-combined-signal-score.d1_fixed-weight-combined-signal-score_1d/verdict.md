---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast x (5-day return - coin mean 5-day return), grid cases pooled: 0.00647965; t of the mean: 1.20898 (threshold: t >= 2 (positive) confirms, t <= -2 (negative) rejects, over at least 500 grid cases)
- Supporting check: none
- Counts: grid cases: 3419
- Decided by: The t lies between -2 and 2 over at least 500 cases.
- Reading: All grid bars (positions 0, 5, 10, ... of each window with a 5-bar return inside it) are cases, flat-forecast ones included, and the coin's mean 5-day return is the mean of its grid returns over all its windows.
- Size: unusual move +0.96 % per case over 5 bars, 0.082 of the coin's usual move (10.60 %); normal drift in its direction +0.00 %, total +0.96 %; 2657 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score_1d`
Measure: `measure.py`
