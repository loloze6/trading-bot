---
plan: 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d
idea: 031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move after the cases (return minus the coin's normal 3-bar drift): 0.0104599; t of the mean, cases pooled by day: 2.8263 (threshold: confirm: mean > 0 with t >= 2 and upper half beats lower half; reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean unusual move (split at median forecast): 0.00672342, passed: True
- Counts: cases: 2037, distinct days: 919, upper half cases: 1018, lower half cases: 1019
- Decided by: The mean unusual move is above 0 with t >= 2 and the upper half beats the lower half.
- Reading: The situation is a bar whose high-low range is at least 1.5 times the mean range of the last 20 bars (today included) within the window, with the regime column used where 20 recorded bars are not yet available, and a positive raw 20-day rise where recorded, on the long side; a case is the first bet (forecast rise of at least 2 points from its lowest long level since the last bet, from 0 after a flat) in each 3-bar grid cell of a window, with a full 3-bar return inside the window; the drift is the mean non-overlapping 3-bar return of the coin over all its windows; the t sums the deviations per UTC day; the upper half is the cases with forecast above the median, the lower half the rest.
- Size: unusual move +1.05 % (t 2.83, the cases of one day together: 919 days) per case over 3 bars, 0.095 of the coin's usual move (9.14 %); normal drift in its direction +0.48 %, total +1.52 %; 2037 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1.b1.d1.g2_wide-day-after-strong-month_1d`
Measure: `measure.py`
