---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 3-bar return after a weekend fall: 0.0110693; t of the weighted mean: 3.65209 (threshold: above 0 with t >= 2 confirms (with the top-quartile check); t <= -2 rejects)
- Supporting check: top-quartile minus other cases mean excess return, Welch t > 0: -1.7997, passed: False
- Counts: cases: 1477
- Decided by: The main measure reaches t >= 2 but the top-quartile check fails, which the plan calls inconclusive.
- Reading: Cases are Sunday bars (UTC weekday 6) with forecast >= 2 whose 3-bar return lies inside the window; the coin's mean 3-bar return is taken on the non-overlapping grid of all its windows; the t of the forecast-weighted mean is that mean over its weighted standard error sqrt(sum(w^2 (x - m)^2)) / sum(w) (sandwich form); the top quartile is the ceil(n/4) cases with the largest forecast (stable sort), compared with the rest by Welch t.
- Size: unusual move +1.20 % per case over 3 bars, 0.146 of the coin's usual move (9.14 %); normal drift in its direction +0.49 %, total +1.69 %; 1478 cases
Plan: `steps_cards/03_test_plan/retest_monday_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/retest_monday_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b2_weekend-fall-rebounds-monday-tuesday.b1_weekend-fall-three-day-rebound.d3_large-weekend-fall-rebound_1d`
Measure: `measure.py`
