---
plan: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h
idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean unusual 48-bar fall (short side): 0.0114712; t of the weighted mean: 2.80229 (threshold: t >= 2 over at least 100 cases to confirm; t <= -2 over at least 100 cases to reject)
- Supporting check: mean unusual fall, larger half minus smaller half of abs(forecast): -0.000806502, passed: False
- Counts: cases: 557
- Decided by: Inconclusive: t >= 2 but the size check (larger half minus smaller half) is at 0 or below.
- Reading: The Monday bar is taken as the bar whose start or close time is Monday 00:00 UTC (the engine's clock may read either), the volatility-rank condition is read from the recorded regime 'mean_reversion' since the detector's components are not recorded and cannot be rebuilt inside a window, the weekend rise from last_history_value (or the 48-bar price return); the t of the weighted mean uses the weighted standard error sqrt(n/(n-1) * sum(w^2 (x-m)^2)) / sum(w); the normal drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; the median split puts abs(forecast) above the median in the larger half and the rest in the smaller half, with unweighted half means.
- Size: unusual move +0.84 % per case over 48 bars, 0.118 of the coin's usual move (6.56 %); normal drift in its direction -0.27 %, total +0.57 %; 486 cases
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/backtests/026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks_1h`
Measure: `measure.py`
