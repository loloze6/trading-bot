---
plan: 026-03_weekend-reversal-exceeds-weekday_1h
idea: 026-03_weekend-reversal-exceeds-weekday
fit: exact
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean reversal score, weekend (Mon 00:00) minus weekday (Wed/Fri 00:00) cases: 0.0310382; Welch t: 0.844284 (threshold: Welch t >= 2 to confirm (with supporting check t >= 2); t <= -2 rejects)
- Supporting check: weekend unusual 48-bar move in forecast direction, |forecast|-weighted mean: -0.00095384, passed: False
- Counts: weekend cases: 2387, weekday cases: 4784, weekend cases with a forecast: 2369
- Decided by: Neither the confirm rule (difference t >= 2 with the weekend check passing) nor the reject rule (a t <= -2) is met.
- Reading: Cases are bars whose close (timestamp + 1h) is Monday, Wednesday or Friday 00:00 UTC with 48 bars before and after inside the window (positional close[t±48]); the usual move and drift are the std and mean of the coin's 48-bar returns on a non-overlapping grid of all its windows; the supporting check uses the weekend cases with a non-zero forecast, and its t is the ordinary t of the |forecast|-weighted values; the plan's minimum of 300 cases per group is applied as 'not observable'.
- Size: unusual move -0.24 % per case over 48 bars, -0.032 of the coin's usual move (6.56 %); normal drift in its direction -0.02 %, total -0.26 %; 2059 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-03_weekend-reversal-exceeds-weekday_1h`
Measure: `measure.py`
