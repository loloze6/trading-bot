---
plan: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d
idea: 022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 20-bar return over cases with abs(forecast) >= 2 (before costs): 0.0290847; t of the mean: 2.6293 (threshold: t >= 2 over at least 30 cases confirms (with supporting check > 0); t <= -2 over at least 30 cases rejects)
- Supporting check: mean signed excess return, larger-|forecast| half minus smaller half: 0.0412555, passed: True
- Counts: cases: 512
- Decided by: The main-measure t is 2 or more over at least 30 cases and the supporting check difference is above 0.
- Reading: The situation is taken as a non-zero raw term (the graded size), its side as the sign of the raw term, compared with the sign of a non-zero forecast; the median split puts cases with abs(forecast) above the median in the larger half and the rest in the smaller half; the drift is each coin's mean 20-bar return on the non-overlapping grid of all its windows; fewer than 30 cases is reported as not observable.
- Size: unusual move -0.66 % per case over 20 bars, -0.028 of the coin's usual move (22.51 %); normal drift in its direction +0.13 %, total -0.53 %; 1142 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-03_combined-extremes-larger-moves.b1_past-weighted-reversal-20-days_1d`
Measure: `measure.py`
