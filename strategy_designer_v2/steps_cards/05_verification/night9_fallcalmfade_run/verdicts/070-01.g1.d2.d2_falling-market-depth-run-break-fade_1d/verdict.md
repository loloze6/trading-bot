---
plan: 070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d
idea: 070-01.g1.d2.d2_falling-market-depth-run-break-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day return minus drift, short direction: 0.00553749; t of the mean, cases summed per day: 2.57795 (threshold: mean > 0 with t >= 2 to confirm; t <= -2 rejects)
- Supporting check: t of slope of next-day return on run loss: -7.61936, passed: True
- Counts: cases: 1414, distinct days: 637
- Decided by: Confirm rule: mean above 0 with t >= 2 and a negative slope with t <= -2.
- Reading: Cases are the short bets of the workflow (a rise of the forecast's size of at least 2 points from its lowest level since the last bet), the supporting regression uses the raw next-day return, the main t uses per-day sums of deviations, the situation's 60-day profile is computed from prices when 60 bars precede the bar in its window and read from the recorded regime otherwise, and the plan's minimum of 100 cases on 80 days yields 'not observable' when unmet.
- Size: unusual move +0.55 % (t 2.60, the cases of one day together: 637 days) per case over 1 bars, 0.118 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.43 %; 1414 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001252 on the check folds against +0.005537 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d2.d2_falling-market-depth-run-break-fade_1d`
Measure: `measure.py`
