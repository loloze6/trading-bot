---
plan: 067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days_1d
idea: 067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move per short case over 20 bars (short-signed, minus coin drift): 0.00751602; t of the mean, same-day cases pooled: 0.445208 (threshold: positive with t >= 2 to confirm; negative with t <= -2 to reject)
- Supporting check: mean unusual move of cases with forecast <= -10 minus that of forecast > -10: 0.0593942, passed: True
- Counts: independent case-days: 376, cases: 571, large cases: 113, smaller cases: 458
- Decided by: the t lies between -2 and 2, which the plan calls inconclusive
- Reading: the choppy regime is the 60-day close-to-close return in percent within [-10, +10] recomputed from the prices, using the recorded regime label on bars without 60 earlier bars in the window; the fall is the recorded fall30 raw value below 0; a case is the first short bet (forecast size up >= 2 from its lowest since the last bet) in each 20-bar grid cell of a window, its return taken from its own close, cases without 20 later bars in the window dropped, and a supporting check with an empty group counts as failed
- Size: unusual move +0.75 % (t 0.45, the cases of one day together: 376 days) per case over 20 bars, 0.009 of the coin's usual move (25.96 %); normal drift in its direction -3.20 %, total -2.45 %; 571 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d2_choppy-month-fall-twenty-days_1d`
Measure: `measure.py`
