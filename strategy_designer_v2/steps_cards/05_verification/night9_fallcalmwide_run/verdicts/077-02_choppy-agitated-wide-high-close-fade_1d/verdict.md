---
plan: 077-02_choppy-agitated-wide-high-close-fade_1d
idea: 077-02_choppy-agitated-wide-high-close-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-bar unusual move of short bets (signed for the short): 0.0063816; t of the mean, cases of one day taken together: 1.54157 (threshold: confirm: mean > 0 with t >= 2 and supporting check passing; reject: t <= -2)
- Supporting check: upper minus lower half mean unusual move, split at median |forecast|: -0.00934424, passed: False
- Counts: distinct case days: 163, cases: 220
- Decided by: t lies between -2 and 2.
- Reading: Range is high minus low against the mean of the last 30 ranges including the current bar, with active bars in a window's first 29 rows left out of the agreement; the upper half is the cases strictly above the median |forecast| and ties go to the lower half; the day-clustered t uses a D/(D-1) correction; the plan's 100-day minimum gives 'not observable' when not reached.
- Size: unusual move +0.64 % (t 1.55, the cases of one day together: 163 days) per case over 1 bars, 0.145 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.51 %; 220 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-02_choppy-agitated-wide-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-02_choppy-agitated-wide-high-close-fade_1d`
Measure: `measure.py`
