---
plan: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h
idea: 026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 48-bar drift-removed return on Sunday-close forecast: 4.99415e-05; OLS slope t: 0.447051 (threshold: slope > 0 with t >= 2 confirms (with supporting check); slope < 0 with t <= -2 rejects)
- Supporting check: mean signed unusual move of top 20 % |forecast| cases: 0.00464782, passed: True
- Counts: cases with a non-zero forecast: 2409, top 20 % cases: 482
- Decided by: The slope's t lies between -2 and 2, which the plan counts as inconclusive.
- Reading: The Sunday-close bar is the 1h bar whose end (start + 1 h) is Monday 00:00 UTC and its expected side is opposite to the sign of the raw component (the weekend's 48-bar move); cases are those bars with a non-zero forecast and a full 48-bar forward return in the same window, pooled across coins in one OLS of unusual return on forecast; the top 20 % by |forecast| is the ceiling of 0.2 x cases; the plan's 'fewer than 300 cases' is reported as not observable.
- Size: unusual move -0.03 % per case over 48 bars, -0.001 of the coin's usual move (6.56 %); normal drift in its direction -0.02 %, total -0.05 %; 1669 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-04_thinner-weekend-larger-reversal.d1_large-thin-weekend-moves-reverse_1h`
Measure: `measure.py`
