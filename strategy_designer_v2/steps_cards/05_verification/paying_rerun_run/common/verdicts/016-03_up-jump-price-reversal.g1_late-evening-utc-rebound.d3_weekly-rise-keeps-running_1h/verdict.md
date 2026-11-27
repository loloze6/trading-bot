---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean (72-bar forward excess return x forecast/10), non-overlapping grid, pooled: 0.00325514; ordinary t of the mean: 3.41597 (threshold: confirm t >= 2 with supporting check passing; reject t <= -2)
- Supporting check: mean excess 72-bar return of cells with forecast above median positive forecast minus that of zero-forecast cells: 0.0101253, passed: True
- Counts: grid cases with a positive forecast: 5750, grid cases with a zero forecast: 5624, grid cases in product: 11374
- Decided by: The main measure has t >= 2 and the top-half minus zero-forecast excess return is > 0 (confirm rule).
- Reading: The drift is each coin's mean 72-bar return over the non-overlapping grid of all its windows; the median of positive forecasts is taken over all pooled grid cells with a positive forecast; the plan's 'fewer than 200 cases' rule is treated as a minimum count giving 'not observable'.
- Size: unusual move +0.05 % (t 0.27, the cases of one day together: 2313 days) per case over 72 bars, 0.003 of the coin's usual move (9.32 %); normal drift in its direction +0.65 %, total +0.70 %; 7978 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/step7ab_b_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_weekly-rise-keeps-running_1h`
Measure: `measure.py`
