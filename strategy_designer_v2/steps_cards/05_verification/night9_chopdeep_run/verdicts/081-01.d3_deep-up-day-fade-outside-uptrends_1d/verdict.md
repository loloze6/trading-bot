---
plan: 081-01.d3_deep-up-day-fade-outside-uptrends_1d
idea: 081-01.d3_deep-up-day-fade-outside-uptrends
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction next-day return minus coin mean daily return, days pooled: 0.0027201; t of the mean (day-pooled): 2.37848 (threshold: t >= 2 over at least 100 days (with deeper-half check) to confirm; t <= -2 over at least 100 days to reject)
- Supporting check: deeper-half minus shallower-half mean unusual short return, Welch t > 0: 2.89519, passed: True
- Counts: days with cases: 1809, cases: 9189, active bars: 4502
- Decided by: The main measure's t is 2 or more over at least 100 days and the deeper half fades more (Welch t > 0).
- Reading: The 1-day and 60-day returns are recomputed from closes inside each window, and active bars without 60 prior bars in their window are left out of the agreement share; the 100-day minimum is treated as the plan's minimum count (not observable when unmet); cases of one day are pooled by summing their deviations per day (clustered standard error with G/(G-1) correction); the supporting check splits active bars with a next-day return into |forecast| above the median (deeper) versus at or below it (shallower).
- Size: unusual move +0.40 % (t 2.74, the cases of one day together: 1287 days) per case over 1 bars, 0.078 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.25 %; 5217 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001543 on the check folds against +0.00272 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/081-01.d3_deep-up-day-fade-outside-uptrends_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/081-01.d3_deep-up-day-fade-outside-uptrends_1d`
Measure: `measure.py`
