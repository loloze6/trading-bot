---
plan: 031-02.b1.b1.b1_wide-flat-uprun-three-day_1d
idea: 031-02.b1.b1.b1_wide-flat-uprun-three-day
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move per case (long), before costs: 0.0299187; t of the mean, cases clustered by day: 3.02788 (threshold: confirm: mean > 0 with t >= 2 and positive slope; reject: mean < 0 with t <= -2)
- Supporting check: OLS slope of unusual move on entry forecast: 0.000826574, passed: True
- Counts: cases: 201, distinct days: 147
- Decided by: Mean unusual move above 0 with t >= 2 and a positive slope on the entry forecast (confirm rule).
- Reading: active bars whose 20-day mean range cannot be rebuilt from the window's own prices (the first 19 bars of a window) are left out of the agreement share; a case is the first bet (forecast rise of >= 2 points from its low since the last bet, from 0 after flat) in each 3-bar grid cell of its window, its return taken from the signal bar's close, the t clusters cases by calendar day (deviations summed per day, D/(D-1) correction), and the plan's 'fewer than 30 cases or days' rule is applied as the minimum count giving 'not observable'.
- Size: unusual move +2.99 % (t 3.04, the cases of one day together: 147 days) per case over 3 bars, 0.323 of the coin's usual move (9.14 %); normal drift in its direction +0.51 %, total +3.50 %; 201 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1_wide-flat-uprun-three-day_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1_wide-flat-uprun-three-day_1d`
Measure: `measure.py`
