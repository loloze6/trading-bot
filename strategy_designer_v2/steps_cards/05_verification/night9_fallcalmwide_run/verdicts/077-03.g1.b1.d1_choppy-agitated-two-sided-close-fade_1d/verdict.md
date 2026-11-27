---
plan: 077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade_1d
idea: 077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the daily mean of forecast/10-weighted drift-adjusted next-day returns: 0.00817885; t of the mean over days: 2.62023 (threshold: confirm if t >= 2 with supporting check passing; reject if t <= -2)
- Supporting check: top-third minus bottom-third |forecast| mean drift-adjusted next-day return in forecast direction: 0.00772165, passed: True
- Counts: cases: 2278, distinct days: 1086
- Decided by: The main t is 2 or more and the top-third minus bottom-third difference is above 0.
- Reading: Profile bars are those whose recorded regime is the config's strategy regime 'unknown' (not 'chop'), the expected side is the opposite sign of the close's off-mid distance (raw value, prices where missing), cases are all active bars with a next bar in the window, days are UTC calendar days, and thirds are the lowest and highest n//3 cases ranked by |forecast| with unweighted means.
- Size: unusual move +0.54 % (t 3.26, the cases of one day together: 761 days) per case over 1 bars, 0.114 of the coin's usual move (5.33 %); normal drift in its direction -0.00 %, total +0.54 %; 1289 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003811 on the check folds against +0.008179 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.g1.b1.d1_choppy-agitated-two-sided-close-fade_1d`
Measure: `measure.py`
