---
plan: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h
idea: 026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of drift-removed 48-bar return on forecast, Thursday-23:00 cases: 0.000564264; OLS slope t: 4.71365 (threshold: confirm: slope > 0 with t >= 2 and supporting mean > 0; reject: slope < 0 with t <= -2; at least 300 cases)
- Supporting check: mean drift-removed 48-bar return in the forecast's direction: 0.00646597, passed: True
- Counts: cases: 2724, active bars: 2767, situation bars with non-zero forecast: 2754
- Decided by: The slope is positive with t >= 2 and the supporting mean is above 0.
- Reading: Cases are bars starting Thursday 23:00 UTC with a non-zero forecast and a full 48-bar forward return inside their window; the normal drift is the coin's mean 48-bar return on the non-overlapping grid of all its windows; the fit has an intercept; fewer than 300 cases is reported as not observable.
- Size: unusual move +0.72 % (t 2.45, the cases of one day together: 343 days) per case over 48 bars, 0.091 of the coin's usual move (7.76 %); normal drift in its direction -0.01 %, total +0.71 %; 2409 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005924 on the check folds against +0.0005643 on every fold
Plan: `steps_cards/03_test_plan/night4_weekend_run/plans/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h.md`
Record: `steps_cards/04_backtest/night4_weekend_run/unseen_coins/backtests/026-03_weekend-reversal-exceeds-weekday.b1_midweek-moves-continue-into-weekend_1h`
Measure: `measure.py`
