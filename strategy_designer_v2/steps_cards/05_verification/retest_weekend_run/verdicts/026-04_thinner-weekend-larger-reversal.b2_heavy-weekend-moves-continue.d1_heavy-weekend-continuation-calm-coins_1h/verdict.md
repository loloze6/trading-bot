---
plan: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h
idea: 026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (48h return minus normal 48h drift) over weekend bets, before costs: 0.0149193; t of the mean: 2.63289 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 100 cases)
- Supporting check: none
- Counts: cases: 463
- Decided by: The mean position-weighted unusual 48h move is positive with t >= 2 over at least 100 cases.
- Reading: The situation bar is read literally as the bar whose start + 1h is Monday 00:00 UTC (Sunday 23:00 start) with mean volume of its last 48 rows over the mean of the 120 rows before them > 1 and the forecast signed like the 48h close-to-close move; active bars without 168 prior rows in their window cannot be checked and are left out of the agreement; cases are active bars (one per coin and weekend) whose 48-bar return lies inside the window, with drift the mean of non-overlapping 48h returns over all windows of the coin.
- Size: unusual move +1.37 % per case over 48 bars, 0.193 of the coin's usual move (6.56 %); normal drift in its direction +0.07 %, total +1.43 %; 405 cases
Plan: `steps_cards/03_test_plan/retest_weekend_run/plans/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h.md`
Record: `steps_cards/04_backtest/retest_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.b2_heavy-weekend-moves-continue.d1_heavy-weekend-continuation-calm-coins_1h`
Measure: `measure.py`
