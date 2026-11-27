---
plan: 067-01.b1.g1.b1.g1_deep-month-slide-accelerates_1d
idea: 067-01.b1.g1.b1.g1_deep-month-slide-accelerates
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move in the short direction over 10 bars, top third of position size (fraction of price): 0.0265117; t of the mean, cases of one day taken together: 2.08486 (threshold: confirm: positive with day-clustered t >= 2; reject: negative with t <= -2; on >= 30 cases over >= 30 distinct days)
- Supporting check: top-third minus bottom-third mean unusual move > 0: 0.0178875, passed: True
- Counts: top-third cases: 212, top-third distinct days: 166, bottom-third cases: 212, all cases: 636
- Decided by: The top-third unusual move is positive with t >= 2 on enough cases and days, and top minus bottom > 0.
- Reading: Situation = 30-day return < 0 (recorded raw value, else rebuilt from closes, else regime 'trending') and 60-day return within [-10, 10] % (rebuilt from closes, else regime not 'chop'), short side; a case is the first bet bar (forecast rise on the short side of >= 2 from its lowest level since the last bet) in each 10-bar grid cell with a full 10-bar forward return in its window, position size is |postRebalance_current_allocation| on that bar, top/bottom thirds are cases at or above the 2/3 / at or below the 1/3 quantile of all cases pooled, drift is each coin's mean non-overlapping 10-bar return over all its windows, and t clusters cases by UTC date.
- Size: unusual move +1.82 % (t 2.41, the cases of one day together: 425 days) per case over 10 bars, 0.100 of the coin's usual move (16.82 %); normal drift in its direction -1.49 %, total +0.33 %; 636 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01106 on the check folds against +0.02651 on every fold
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.g1_deep-month-slide-accelerates_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.g1_deep-month-slide-accelerates_1d`
Measure: `measure.py`
