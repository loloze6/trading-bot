---
plan: 058-01.g2.g1.g1_agitated-decline-wide-up-day-fade_1d
idea: 058-01.g2.g1.g1_agitated-decline-wide-up-day-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day move of short cases (day-clustered t): 0.0055899; day-clustered t of the mean: 2.50447 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, upper minus lower half of |forecast|: 0.00667642, passed: True
- Counts: cases across coins: 1326, distinct days: 633
- Decided by: The mean unusual move is positive with t >= 2 and wider up days fall more than narrow ones.
- Reading: Cases are bars with forecast < 0 and a next close in the same window; the coin's mean daily return is over all its 1-bar returns in all windows; the day-clustered t sums each day's deviations from the mean (SE = sqrt(D/(D-1) * sum of squared day sums) / N); the upper half is |forecast| strictly above the median, the lower half the rest; the profile in the situation check is read as regime not 'chop' and each window's first bar is left out of that check.
- Size: unusual move +0.82 % (t 3.08, the cases of one day together: 473 days) per case over 1 bars, 0.179 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.69 %; 922 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.002405 on the check folds against +0.00559 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1_agitated-decline-wide-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.g1_agitated-decline-wide-up-day-fade_1d`
Measure: `measure.py`
