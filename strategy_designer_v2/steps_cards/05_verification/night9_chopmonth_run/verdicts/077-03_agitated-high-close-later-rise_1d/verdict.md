---
plan: 077-03_agitated-high-close-later-rise_1d
idea: 077-03_agitated-high-close-later-rise
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 6-bar move per case, long, from the signal bar's close: 0.00606355; t of the mean, cases of one day taken together: 1.27241 (threshold: above 0 with t >= 2 to confirm; below 0 with t <= -2 to reject)
- Supporting check: mean unusual move (close location >= 0.9) minus (0.8 to 0.9), above 0: 0.00290339, passed: True
- Counts: cases: 1899, distinct days: 751, cases with close location >= 0.9: 924, cases with close location 0.8 to 0.9: 975
- Decided by: The t lies between -2 and 2 (or is undefined), meeting neither the confirm nor the reject rule.
- Reading: The situation is the lagged close location >= 0.8 (recorded raw value, else from prices) on the long side, the agitated profile being the config's veto; a case is the first long-forecast rise of at least 2 points in each 6-bar grid cell of a window, its day the signal bar's UTC date, the day-clustered standard error is sqrt(sum over days of squared summed deviations)/n without small-sample correction, and an empty close-location group makes the supporting check fail.
- Size: unusual move +0.61 % (t 1.27, the cases of one day together: 751 days) per case over 6 bars, 0.052 of the coin's usual move (12.40 %); normal drift in its direction +0.86 %, total +1.46 %; 1899 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/077-03_agitated-high-close-later-rise_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/077-03_agitated-high-close-later-rise_1d`
Measure: `measure.py`
