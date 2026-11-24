---
plan: 031-03.b1.a1_yearly-low-break-all-coins_1d
idea: 031-03.b1.a1_yearly-low-break-all-coins
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move of long cases (return minus coin's 10-bar drift), before costs: 0.0684144; t of the mean, cases of one day together: 1.7793 (threshold: confirm: mean > 0 with day-clustered t >= 2 on >= 30 distinct days and slope > 0; reject: mean < 0 with t <= -2 on >= 30 days)
- Supporting check: OLS slope of unusual move on signal-bar forecast: 0.000960617, passed: True
- Counts: distinct case days: 16, cases: 18
- Decided by: Fewer than 30 distinct case days over all coins and windows (16).
- Reading: The situation is read from the recorded break_depth raw value (same component and parameters as the detector's yl), with missing values counted as outside the situation; a case is the first bet (long forecast rise of at least 2 points from its lowest level since the last bet, from 0 after a flat) in each 10-bar grid cell of a window, cases without 10 bars ahead in the window are dropped, the drift is the mean of the coin's non-overlapping 10-bar grid returns over all its windows, the t clusters cases by UTC day with a D/(D-1) correction, and the slope is an OLS of the unusual move on the signal bar's forecast.
- Size: unusual move +6.84 % (t 1.84, the cases of one day together: 16 days) per case over 10 bars, 0.422 of the coin's usual move (15.55 %); normal drift in its direction +1.66 %, total +8.50 %; 18 cases
Plan: `steps_cards/03_test_plan/night6_yearlow_run/plans/031-03.b1.a1_yearly-low-break-all-coins_1d.md`
Record: `steps_cards/04_backtest/night6_yearlow_run/backtests/031-03.b1.a1_yearly-low-break-all-coins_1d`
Measure: `measure.py`
