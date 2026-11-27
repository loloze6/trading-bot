---
plan: 070-01.g1.d1_deep-slide-calm-run-break-fade_1d
idea: 070-01.g1.d1_deep-slide-calm-run-break-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side excess next-day return on case bars: 0.0103484; t of the mean, same-day cases summed: 1.82389 (threshold: confirm: mean > 0 with t >= 2.0 over >= 30 case-days; reject: mean < 0 with t <= -2.0 over >= 30 case-days)
- Supporting check: upper-half minus lower-half mean excess, split at median |forecast|: None, passed: None
- Counts: case-days: 82, cases: 117, active bars: 119
- Decided by: t between -2.0 and 2.0 (or sign and t disagree), meeting neither confirm nor reject
- Reading: cases are bars where the short forecast deepens by >= 2 points from its lowest short level since the last bet (reset at flat), the mean is over cases and the t over day-summed cases, the upper half is |forecast| strictly above the median, and fewer than 30 case-days is treated as not observable
- Size: unusual move +1.03 % (t 1.88, the cases of one day together: 82 days) per case over 1 bars, 0.225 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.91 %; 117 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/070-01.g1.d1_deep-slide-calm-run-break-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/070-01.g1.d1_deep-slide-calm-run-break-fade_1d`
Measure: `measure.py`
