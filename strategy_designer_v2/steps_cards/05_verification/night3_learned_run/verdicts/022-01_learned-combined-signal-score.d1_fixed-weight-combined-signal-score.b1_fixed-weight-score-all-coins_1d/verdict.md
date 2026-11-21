---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x excess 5-day return, before costs: 0.0011572; t of the mean: 2.81733 (threshold: t >= 2 confirms (with supporting difference > 0); t <= -2 rejects)
- Supporting check: mean excess 5-day return, forecast > 0 minus forecast < 0 (Welch): 0.00787719, passed: True
- Counts: non-overlapping cases with a non-zero forecast: 7123, non-overlapping cases: 7128, cases with forecast > 0: 3600, cases with forecast < 0: 3523
- Decided by: The main measure's t is 2 or more and the supporting difference is above 0.
- Reading: The main mean pools every grid bar (positions 0, 5, 10, ... of each window) with a valid 5-bar return, a zero forecast giving a zero product, the drift is each coin's mean non-overlapping 5-bar return over all its windows, and the supporting check passes on the sign of the difference alone, as the plan states.
- Size: unusual move +0.93 % per case over 5 bars, 0.072 of the coin's usual move (12.24 %); normal drift in its direction -0.00 %, total +0.92 %; 5578 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.b1_fixed-weight-score-all-coins_1d`
Measure: `measure.py`
