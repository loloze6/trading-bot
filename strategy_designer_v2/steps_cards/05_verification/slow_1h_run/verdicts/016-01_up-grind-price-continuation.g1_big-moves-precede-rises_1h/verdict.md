---
plan: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
idea: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope t of 72-bar forward excess return on forecast (pooled, sampled bars 0,72,...): 0.0012984; OLS slope t: 3.66688 (threshold: confirm: slope > 0 with t >= 2 and timing part > 0; reject: slope < 0 with t <= -2; else inconclusive; at least 500 sampled cases)
- Supporting check: book mean daily return minus gain from the market's own rise (timing part) > 0: -0.000497599, passed: False
- Counts: independent sampled cases: 5683
- Decided by: t >= 2 but the timing part of the book is at or below 0 (or not measurable).
- Reading: situation = non-zero 72-bar move (raw component value, prices as fallback) on the long side; the coin's mean 72-bar return is the mean of its sampled forward returns over all windows; the position behind each day's market gain is the mean hourly allocation held over that day, and the coin's mean daily return comes from its day-end closes over all windows.
Plan: `steps_cards/03_test_plan/slow_1h_run/plans/016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h.md`
Record: `steps_cards/04_backtest/slow_1h_run/backtests/016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h`
Measure: `measure.py`
