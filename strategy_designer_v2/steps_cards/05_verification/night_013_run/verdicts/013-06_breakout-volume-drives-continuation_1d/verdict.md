---
plan: 013-06_breakout-volume-drives-continuation_1d
idea: 013-06_breakout-volume-drives-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 30-bar excess return on breakout volume ratio: 0.0639746; OLS slope t: 4.71565 (threshold: t >= 2 with >= 30 cases (and top-third mean excess > 0) confirms; t <= -2 with >= 30 cases rejects)
- Supporting check: mean excess 30-bar return of top third by volume ratio > 0: 0.237378, passed: True
- Counts: non-overlapping breakout cases: 60, top-third cases: 20
- Decided by: The slope's t is 2 or more with at least 30 cases and the top-third mean excess return is above zero.
- Reading: Situation bars are bars whose close exceeds every prior in-window close (up to 365 back) and whose recorded regime is 'trending' (the 365-close high itself needs warm-up history not in the record), expected side long; breakout bars for cases are regime 'trending' with a recorded volratio, a selected bar without close[t+30] in its window is not a case; the coin's mean 30-bar return is pooled over the non-overlapping grid (positions 0, 30, 60, ...) of all its windows; the top third is the ceil(n/3) cases with the largest volume ratio; the OLS t uses the usual slope standard error with n-2 df; fewer than 30 cases is reported as 'not observable' per the workflow's minimum-count rule.
- Size: unusual move +8.61 % per case over 30 bars, 0.277 of the coin's usual move (25.51 %); normal drift in its direction +3.46 %, total +12.06 %; 70 cases
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-06_breakout-volume-drives-continuation_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-06_breakout-volume-drives-continuation_1d`
Measure: `measure.py`
