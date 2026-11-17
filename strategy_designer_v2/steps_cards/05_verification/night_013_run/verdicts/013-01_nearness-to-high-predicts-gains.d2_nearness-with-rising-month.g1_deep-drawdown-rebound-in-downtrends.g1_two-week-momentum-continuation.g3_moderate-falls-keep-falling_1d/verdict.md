---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 7-bar return on forecast (non-overlapping grid, forecast != 0, pooled): 0.00225661; OLS slope t: 1.81335 (threshold: t >= +2 confirms (with positive supporting difference); t <= -2 rejects; between is inconclusive)
- Supporting check: mean excess 7-bar return at forecast > 0 minus at forecast < 0: 0.016547, passed: True
- Counts: non-zero grid points: 1253, grid points with forecast > 0: 153, grid points with forecast < 0: 1100
- Decided by: The slope t lies between -2 and +2 (inconclusive rule).
- Reading: Grid points at positions 0,7,14,... of each window with t+7 inside the window; the coin's mean 7-bar return is the mean over all its grid points in all windows; the minimum counts of the plan's inconclusive rule are applied as minimums (not observable).
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g3_moderate-falls-keep-falling_1d`
Measure: `measure.py`
