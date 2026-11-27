---
plan: 076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d
idea: 076-01.b1.b1.b1_falling-agitated-wide-close-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move in the short direction (return minus coin drift): 0.00792584; t of the mean, same-day cases clustered: 1.75776 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move of cases above median forecast size minus at/below median: 0.00884057, passed: True
- Counts: cases: 660, distinct days: 282
- Decided by: t between -2 and 2, which the plan calls inconclusive.
- Reading: cases are short bets (forecast fall of >= 2 points from its lowest short level since the last bet, reset at 0) on every bar (1-bar grid) with a next bar in the window; larger cases are those with size strictly above the median, smaller those at or below it; the t clusters cases by UTC day; the plan's minimum counts give 'not observable'.
- Size: unusual move +0.79 % (t 1.76, the cases of one day together: 282 days) per case over 1 bars, 0.165 of the coin's usual move (5.33 %); normal drift in its direction -0.13 %, total +0.66 %; 660 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/076-01.b1.b1.b1_falling-agitated-wide-close-fade_1d`
Measure: `measure.py`
