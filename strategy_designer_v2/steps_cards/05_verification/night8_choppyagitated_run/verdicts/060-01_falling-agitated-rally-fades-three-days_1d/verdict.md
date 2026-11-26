---
plan: 060-01_falling-agitated-rally-fades-three-days_1d
idea: 060-01_falling-agitated-rally-fades-three-days
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed unusual 3-bar move of the cases (vs coin's normal 3-bar drift): 0.0043441; day-clustered t: 1.00916 (threshold: day-clustered t >= 2 to confirm (with slope t >= 2); t <= -2 or slope t <= -2 to reject)
- Supporting check: OLS slope of short-signed unusual move on |forecast|: 0.000766046, passed: False
- Counts: distinct case days: 488, cases: 1357
- Decided by: Neither rule met: the main t is between -2 and 2, or it is >= 2 with a slope t below 2 (or a statistic could not be computed).
- Reading: A case is the first short bet (rise of |forecast| >= 2 from its lowest level since the last bet) in each 3-bar cell counted from each window's first row; the day-clustered t sums deviations per UTC day with no small-sample correction; the slope t is the ordinary OLS t; the plan's 30-day minimum is applied as 'not observable'; the situation is read from the regime 'unknown' and raw value > 0.
- Size: unusual move +0.43 % (t 1.01, the cases of one day together: 488 days) per case over 3 bars, 0.048 of the coin's usual move (8.85 %); normal drift in its direction -0.43 %, total -0.00 %; 1357 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-01_falling-agitated-rally-fades-three-days_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-01_falling-agitated-rally-fades-three-days_1d`
Measure: `measure.py`
