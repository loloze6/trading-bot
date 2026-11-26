---
plan: 060-01.g1_wide-day-high-close-fade_1d
idea: 060-01.g1_wide-day-high-close-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-direction unusual next-bar move on forecast<0 bars: 0.0203712; t of the mean, cases clustered by day: 2.5037 (threshold: confirm: mean > 0 with t >= 2 over >= 30 cases and slope >= 0; reject: mean < 0 with t <= -2 over >= 30 cases)
- Supporting check: OLS slope of short-direction unusual move on abs(forecast): 0.00107739, passed: True
- Counts: cases: 89, days: 56
- Decided by: Mean short-direction unusual move above 0 with t >= 2 over at least 30 cases, and the slope on abs(forecast) is >= 0.
- Reading: Every bar with forecast < 0 and a next bar in the same window is a case (1-bar grid = every bar), the drift is the coin's mean 1-bar return over all its windows, the day-clustered t sums the deviations per UTC day, and the slope is an ordinary least-squares fit.
- Size: unusual move +2.00 % (t 2.45, the cases of one day together: 55 days) per case over 1 bars, 0.451 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +1.87 %; 88 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (49 cases, 33 days)
Plan: `steps_cards/03_test_plan/night8_risingagitated_run/plans/060-01.g1_wide-day-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night8_risingagitated_run/backtests/060-01.g1_wide-day-high-close-fade_1d`
Measure: `measure.py`
