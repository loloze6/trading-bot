---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean signed 48-bar return minus coin's mean 48-bar return, Sunday 23:00 cases: 0.010981; t of the mean: 2.51337 (threshold: t >= 2 over at least 100 cases confirms (with supporting check); t <= -2 over at least 100 cases rejects)
- Supporting check: mean signed unusual move, top half of |forecast| minus bottom half: 0.00229518, passed: True
- Counts: cases: 463
- Decided by: The main t is 2 or more over at least 100 cases and the top-minus-bottom difference is above 0.
- Reading: Situation bars are bars starting Sunday 23:00 UTC with the mean volume of the last 48 bars above that of the 120 bars before them and the side taken as the sign of the 48-bar close-to-close move (by row position within the window, falling back to the recorded regime and the move component's raw sign where the window's history is too short); cases are all Sunday 23:00 bars with a non-zero forecast and a close 48 rows later in the same window; the coin's mean 48-bar return is taken on the non-overlapping grid 0, 48, 96... of all its windows pooled; the top and bottom halves of |forecast| are the n//2 largest and n//2 smallest cases pooled over all coins (stable sort, middle case dropped when n is odd).
- Size: unusual move +1.47 % per case over 48 bars, 0.206 of the coin's usual move (6.56 %); normal drift in its direction +0.06 %, total +1.54 %; 418 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue_1h`
Measure: `measure.py`
