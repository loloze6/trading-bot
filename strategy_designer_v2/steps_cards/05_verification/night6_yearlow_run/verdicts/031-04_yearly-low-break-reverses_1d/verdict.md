---
plan: 031-04_yearly-low-break-reverses_1d
idea: 031-04_yearly-low-break-reverses
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move after long bets in the mean_reversion regime: 0.0714982; t of the mean, same-day cases summed: 1.41036 (threshold: confirm: mean > 0 with t >= 2 and deeper half beats shallower; reject: mean < 0 with t <= -2)
- Supporting check: deeper-break half minus shallower half mean unusual move (split at median forecast): 0.0200137, passed: True
- Counts: cases: 13, distinct days: 12
- Decided by: Minimum not reached: 13 cases (need 20) on 12 distinct days (need 15).
- Reading: Cases are the first long bet (forecast rise >= 2 from its lowest level since the last bet, reset at 0) in the mean_reversion regime in each 10-bar grid cell from each window's first row, dropped when the 10-bar return leaves the window; the drift is the coin's mean grid 10-bar return over all windows; the t sums deviations per UTC day with a D/(D-1) correction; the deeper half is forecast above the median and the shallower half forecast at or below it; the plan's 'fewer than 20 cases or 15 days' minimum is reported as not observable.
- Size: unusual move +7.15 % (t 1.47, the cases of one day together: 12 days) per case over 10 bars, 0.450 of the coin's usual move (14.49 %); normal drift in its direction +1.85 %, total +9.00 %; 13 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-04_yearly-low-break-reverses_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-04_yearly-low-break-reverses_1d`
Measure: `measure.py`
