---
plan: 077-02_choppy-calm-swing-fall-carries_1d
idea: 077-02_choppy-calm-swing-fall-carries
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-signed 7-day unusual move after short signals: -0.0285648; t of the mean, cases of one day taken together: -5.70393 (threshold: confirm: mean > 0 with t >= 2 over >= 20 distinct case days and slope on |forecast| > 0; reject: mean < 0 with t <= -2 over >= 20 distinct case days)
- Supporting check: OLS slope of short-signed unusual move on |forecast|: None, passed: None
- Counts: distinct case days: 2, cases: 2, active bars: 3
- Decided by: Fewer than 20 distinct case days (2), the plan's minimum count, so the data cannot show the idea.
- Reading: Situation checked as raw 14-day swing-scaled return (recorded scaled_fall last_history_value, else recomputed from closes) <= -2 with a short forecast, the profile vetoes not being recomputed; cases are short bets (rise of |forecast| on the short side of >= 2 points from its lowest level since the last bet, reset at flat), first per 7-bar grid cell from each window's first row; normal drift is the coin's mean non-overlapping 7-bar return over all its windows; t uses day-clustered errors with D/(D-1) correction; fewer than 20 distinct case days is 'not observable'.
- Size: unusual move -2.86 % (t -8.07, the cases of one day together: 2 days) per case over 7 bars, -0.282 of the coin's usual move (12.44 %); normal drift in its direction -0.80 %, total -3.66 %; 2 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-02_choppy-calm-swing-fall-carries_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-02_choppy-calm-swing-fall-carries_1d`
Measure: `measure.py`
