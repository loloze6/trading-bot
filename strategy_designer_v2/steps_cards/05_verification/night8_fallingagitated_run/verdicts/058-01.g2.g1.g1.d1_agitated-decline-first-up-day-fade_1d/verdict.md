---
plan: 058-01.g2.g1.g1.d1_agitated-decline-first-up-day-fade_1d
idea: 058-01.g2.g1.g1.d1_agitated-decline-first-up-day-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day short-signed return beyond the coin's mean daily return: 0.00943373; t of the mean, cases of one day taken together: 3.25308 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: top-half minus bottom-half |forecast| short-signed excess return: 0.00667862, passed: True
- Counts: cases: 759, days: 387
- Decided by: the main mean is positive with t >= 2 and the top-minus-bottom difference is positive (confirm rule)
- Reading: situation recomputed from closes within each window as close[t]>close[t-1] and close[t-1]<=close[t-2] with a short forecast; active bars on a window's first two rows (streak not computable) are left out; the falling-agitated profile (365-day volatility percentile) cannot be rebuilt from the record's windows and is not re-checked; the t clusters cases by UTC day (deviations from the mean summed per day, with a D/(D-1) correction); the top and bottom halves split the cases sorted by |forecast| (ties ordered by time then coin), the bottom half taking the extra case when the count is odd; fewer than 100 cases is reported as not observable
- Size: unusual move +0.93 % (t 3.20, the cases of one day together: 384 days) per case over 1 bars, 0.202 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.81 %; 753 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.004877 on the check folds against +0.009434 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.g1.d1_agitated-decline-first-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.g1.d1_agitated-decline-first-up-day-fade_1d`
Measure: `measure.py`
