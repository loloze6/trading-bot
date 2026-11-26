---
plan: 059-01.b1.b1_choppy-calm-rise-two-weeks_1d
idea: 059-01.b1.b1_choppy-calm-rise-two-weeks
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 14-bar excess forward return on forecast (forecast > 0 grid cells, pooled): 0.00878422; OLS slope t, clustered by day: 2.75751 (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2; at least 100 cells)
- Supporting check: mean excess 14-bar return over the same cells > 0: 0.0098917, passed: True
- Counts: grid cells with forecast > 0: 180, days of those cells: 79
- Decided by: Confirm rule met: the slope's t is 2 or more and the mean excess return is above 0.
- Reading: The choppy calm profile is read from the recorded regime (the detector's default 'unknown', i.e. no veto) since the detector's components are not recorded and its 365-bar lookback cannot be rebuilt in a window, the rise from the raw weekly_rise value (or its price rebuild where missing); the coin's mean 14-bar return is taken over all its grid cells in all windows, and both t's cluster cases by UTC day with a G/(G-1) correction.
- Size: unusual move -0.04 % (t -0.04, the cases of one day together: 377 days) per case over 14 bars, -0.017 of the coin's usual move (18.92 %); normal drift in its direction +2.21 %, total +2.17 %; 589 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (58 cases, 58 days)
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/059-01.b1.b1_choppy-calm-rise-two-weeks_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/059-01.b1.b1_choppy-calm-rise-two-weeks_1d`
Measure: `measure.py`
