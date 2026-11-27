---
plan: 076-01.b1.b1_agitated-wide-upper-close-fade_1d
idea: 076-01.b1.b1_agitated-wide-upper-close-fade
fit: exact
status: inconclusive
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side unusual 1-day move: 0.00116892; t of the mean, cases of one day clustered: 0.457132 (threshold: confirm: mean > 0 with t >= 2 over >= 30 case-days and supporting check > 0; reject: mean < 0 with t <= -2 over >= 30 case-days)
- Supporting check: mean unusual move, larger minus smaller |forecast| half: None, passed: None
- Counts: case-days: 927, cases: 2245
- Decided by: The t lies between -2 and 2 over at least 30 case-days.
- Reading: Profile taken from the recorded regime (not 'chop', the veto's result) since the 365-bar volatility percentile cannot be rebuilt inside a window; range multiple against the prior 20 bars' mean range (from prices, or from the recorded component when the window lacks 20 prior bars); cases are short bets (rise of |forecast| >= 2) on every bar (1-bar grid); day-clustered t with deviations summed per UTC day; median split: larger half = |forecast| above the median, smaller half = at or below; fewer than 30 case-days gives 'not observable' per the workflow rule.
- Size: unusual move +0.12 % (t 0.46, the cases of one day together: 927 days) per case over 1 bars, 0.028 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total -0.02 %; 2245 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/076-01.b1.b1_agitated-wide-upper-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/076-01.b1.b1_agitated-wide-upper-close-fade_1d`
Measure: `measure.py`
