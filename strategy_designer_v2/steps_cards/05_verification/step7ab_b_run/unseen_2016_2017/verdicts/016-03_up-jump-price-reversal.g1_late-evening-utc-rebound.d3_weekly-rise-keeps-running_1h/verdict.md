---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean (72-bar forward excess return x forecast/10), non-overlapping grid, pooled: 0.0093877; ordinary t of the mean: 1.55279 (threshold: confirm t >= 2 with supporting check passing; reject t <= -2)
- Supporting check: mean excess 72-bar return of cells with forecast above median positive forecast minus that of zero-forecast cells: 0.0320114, passed: True
- Counts: grid cases with a positive forecast: 450, grid cases with a zero forecast: 279, grid cases in product: 729
- Decided by: The main measure's t lies between -2 and 2 (inconclusive rule).
- Reading: The drift is each coin's mean 72-bar return over the non-overlapping grid of all its windows; the median of positive forecasts is taken over all pooled grid cells with a positive forecast; the plan's 'fewer than 200 cases' rule is treated as a minimum count giving 'not observable'.
- Size: unusual move +0.10 % per case over 72 bars, -0.015 of the coin's usual move (15.26 %); normal drift in its direction +3.01 %, total +3.11 %; 564 cases
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h.md`
Record: `steps_cards/04_backtest/step7ab_b_run/unseen_2016_2017/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h`
Measure: `measure.py`
