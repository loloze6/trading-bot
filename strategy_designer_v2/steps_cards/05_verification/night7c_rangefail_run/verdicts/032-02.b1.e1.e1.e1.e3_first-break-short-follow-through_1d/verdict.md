---
plan: 032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d
idea: 032-02.b1.e1.e1.e1.e3_first-break-short-follow-through
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of excess 3-bar return on raw proximity (day-clustered): -0.0370431; OLS slope t, day-clustered SE: -1.84882 (threshold: confirm: t >= 2 with weighted mean excess > 0; reject: t <= -2; over at least 100 cases)
- Supporting check: proximity-weighted mean excess 3-bar return > 0: 0.00970847, passed: True
- Counts: cases: 511, days: 370
- Decided by: The slope's t lies between -2 and 2.
- Reading: A case is a 'trending' bar with no kept case 1 to 3 bars before it in its window, dropped if its 3-bar return or raw proximity is missing; the coin's mean 3-bar return uses the non-overlapping grid 0,3,6,... of every window pooled; same-day cases are summed into one deviation by clustering the OLS slope's standard error by UTC day; fewer than 100 cases is reported as not observable.
- Size: unusual move +1.15 % (t 2.15, the cases of one day together: 381 days) per case over 3 bars, 0.134 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +1.51 %; 528 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1.e1.e1.e3_first-break-short-follow-through_1d`
Measure: `measure.py`
