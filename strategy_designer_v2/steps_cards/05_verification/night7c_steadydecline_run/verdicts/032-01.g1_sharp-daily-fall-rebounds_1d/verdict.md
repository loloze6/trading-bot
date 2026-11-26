---
plan: 032-01.g1_sharp-daily-fall-rebounds_1d
idea: 032-01.g1_sharp-daily-fall-rebounds
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 2-bar return of the cases over the coin's mean 2-bar return, before costs: 0.00224921; t of the mean, cases of one day taken together: 0.506815 (threshold: confirm: mean > 0 with t >= 2 (and slope > 0 with t >= 2); reject: mean < 0 with t <= -2 or slope < 0 with t <= -2)
- Supporting check: OLS slope of the case's excess 2-bar return on its forecast: 0.000344379, passed: False
- Counts: cases: 463, case-days: 191
- Decided by: Inconclusive rule: neither the confirm nor the reject rule is met, a t lies between -2 and 2 on a measure (t mean 0.51, t slope 0.33).
- Reading: Bets are read as in the holding-period rule (forecast rise >= 2 from its lowest level on its side since the last bet), one per 2-bar grid cell from each window's first row taking the cell's first bet bar and its return from that bar's close over 2 bars inside the window; the drift is the coin's mean of grid 2-bar returns over all its windows; the mean's t sums deviations per day (cluster SE with D/(D-1)); the slope is ordinary OLS on the case's forecast; the 30 minimum counts case-days.
- Size: unusual move +0.22 % (t 0.51, the cases of one day together: 191 days) per case over 2 bars, 0.037 of the coin's usual move (6.58 %); normal drift in its direction +0.23 %, total +0.46 %; 463 cases
Plan: `steps_cards/03_test_plan/night7c_steadydecline_run/plans/032-01.g1_sharp-daily-fall-rebounds_1d.md`
Record: `steps_cards/04_backtest/night7c_steadydecline_run/backtests/032-01.g1_sharp-daily-fall-rebounds_1d`
Measure: `measure.py`
