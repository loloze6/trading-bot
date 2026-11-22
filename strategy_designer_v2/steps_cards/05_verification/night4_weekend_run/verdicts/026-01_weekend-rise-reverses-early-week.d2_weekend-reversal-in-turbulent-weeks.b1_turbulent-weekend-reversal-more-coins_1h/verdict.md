---
plan: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h
idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 48-bar unusual move in the short direction after Monday 00:00 short bets: 0.0116868; t of the mean: 3.65278 (threshold: mean unusual short move > 0 with t >= 2 (confirm); < 0 with t <= -2 (reject); at least 300 cases)
- Supporting check: correlation of abs(forecast) with the unusual move above 0: 0.0396555, passed: True
- Counts: cases over all coins and windows: 853
- Decided by: Mean unusual short move positive with t >= 2 and correlation of abs(forecast) with it above 0.
- Reading: A case is a bar whose close (timestamp + 1 h) is Monday 00:00 UTC with forecast <= -2 and a full 48-bar forward return in its window; the normal drift is each coin's mean 48-bar return on the non-overlapping grid of all its windows; the situation's volatility condition is read from the recorded regime since the 720/4320-bar ratio cannot be rebuilt inside a window, and the weekend rise from the component's raw 48-bar return (prices where missing).
- Size: unusual move +1.17 % per case over 48 bars, 0.154 of the coin's usual move (7.37 %); normal drift in its direction -0.32 %, total +0.84 %; 853 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b1_turbulent-weekend-reversal-more-coins_1h`
Measure: `measure.py`
