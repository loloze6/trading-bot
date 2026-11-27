---
plan: 061-01.b1.b1.b1_high-close-location-fades-weekly_1d
idea: 061-01.b1.b1.b1_high-close-location-fades-weekly
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 5-bar move of the bets: 0.0170595; t of the mean, cases of one day pooled: 3.12776 (threshold: confirm: mean > 0 with day-pooled t >= 2 and check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move at close location >= 0.9 minus 0.8 to < 0.9: 0.0134473, passed: True
- Counts: cases: 349, distinct days: 248, cases at 0.9 or more: 164, cases from 0.8 to below 0.9: 185
- Decided by: The mean short-side unusual move is above 0 with a t of 2 or more, and the supporting check passes.
- Reading: A case is the first short bet (rise of the short forecast of >= 2 points from its lowest level since the last bet) in each 5-bar grid cell of a window, its return taken from that bar's close to 5 bars later inside the window; the normal drift is the coin's mean 5-bar return on the grid of all its windows; the day-pooled t uses summed deviations per UTC day with a D/(D-1) correction; the situation check uses close location >= 0.8 (recorded high_close value, else from prices) and a negative forecast, the profile not being recomputable.
- Size: unusual move +1.71 % (t 3.13, the cases of one day together: 248 days) per case over 5 bars, 0.156 of the coin's usual move (11.68 %); normal drift in its direction -0.66 %, total +1.04 %; 349 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01347 on the check folds against +0.01706 on every fold
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1_high-close-location-fades-weekly_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1_high-close-location-fades-weekly_1d`
Measure: `measure.py`
