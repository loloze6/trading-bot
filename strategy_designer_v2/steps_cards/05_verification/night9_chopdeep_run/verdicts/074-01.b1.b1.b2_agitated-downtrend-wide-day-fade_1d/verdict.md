---
plan: 074-01.b1.b1.b2_agitated-downtrend-wide-day-fade_1d
idea: 074-01.b1.b1.b2_agitated-downtrend-wide-day-fade
fit: adapted
status: inconclusive
---
Situation check: 94 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return in the short direction (vs coin's mean daily return): 0.0147446; t of the mean, deviations summed per day: 1.97422 (threshold: confirm: mean > 0 with t >= 2 (and |forecast|-weighted mean > unweighted mean); reject: mean < 0 with t <= -2)
- Supporting check: |forecast|-weighted mean minus unweighted mean of the excess fall: 0.000446089, passed: True
- Counts: distinct days with cases: 160, cases: 313
- Decided by: t lies between -2 and 2, meeting neither the confirm nor the reject rule.
- Reading: Situation checked as up day (close above the previous close in the same window) with high-low range over its 20-bar mean range (recorded width where present, else recomputed from prices; first bar of a window counted as not in the situation), side short, the profile not rechecked; cases are short bets on the 1-bar grid, the per-day t uses the sums of each day's deviations from the mean with a D/(D-1) correction, and the plan's 'fewer than 30 distinct days' minimum gives 'not observable'.
- Size: unusual move +1.47 % (t 1.98, the cases of one day together: 160 days) per case over 1 bars, 0.304 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +1.34 %; 313 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/074-01.b1.b1.b2_agitated-downtrend-wide-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/074-01.b1.b1.b2_agitated-downtrend-wide-day-fade_1d`
Measure: `measure.py`
