---
plan: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d
idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of position x next-bar excess return, pooled, before costs: 0.000365649; t of the mean: 3.33524 (threshold: confirm if t >= 2 with supporting check passed; reject if t <= -2; otherwise inconclusive)
- Supporting check: mean next-bar excess return on top 10% of positive forecasts > 0: 0.00427275, passed: True
- Counts: bars with a non-zero position: 6725, bars in the top-10% group: 1059, bars in the main measure: 17380
- Decided by: Main t >= 2 and the top-10% group's mean next-bar excess return is above 0.
- Reading: Situation bars are bars whose volatility-scaled 1-day return (recorded raw value, or the 1-day price return where missing) is below zero, with a long forecast expected; the coin's mean daily return is pooled over all its windows; the main t uses every bar with a next-bar return (horizon 1, so every bar is its own non-overlapping case); the top-10% group is the pooled positive-forecast bars at or above the 90th percentile of positive forecasts across all coins; a minimum count not reached gives 'not observable'.
- Size: unusual move +0.35 % per case over 1 bars, 0.068 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.47 %; 3056 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d`
Measure: `measure.py`
