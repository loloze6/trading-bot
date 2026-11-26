---
plan: 060-01.b1.g1_quiet-day-next-fade_1d
idea: 060-01.b1.g1_quiet-day-next-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean drift-adjusted next-day return of short cases: -0.00151843; t of the mean, cases pooled by day: -1.26191 (threshold: confirm: mean < 0 with t <= -2 (and check passes); reject: mean > 0 with t >= +2)
- Supporting check: mean adj. return, top half minus bottom half of |flatness|: -0.00270415, passed: True
- Counts: cases: 3689, days with cases: 1863
- Decided by: The t of the mean drift-adjusted next-day return lies between -2 and +2.
- Reading: Every bar with forecast < 0 is a case (the plan's own case definition), the drift is the coin's mean next-bar return over all its windows, the day-clustered t sums deviations per UTC day with a D/(D-1) correction, the halves are the n//2 cases with largest and smallest |post_pipeline_value| (middle case dropped if odd), and the plan's 'fewer than 200 cases' is treated as the minimum count giving 'not observable'.
- Size: unusual move +0.03 % (t 0.18, the cases of one day together: 1575 days) per case over 1 bars, 0.002 of the coin's usual move (5.56 %); normal drift in its direction -0.12 %, total -0.09 %; 2789 cases
Plan: `steps_cards/03_test_plan/a4_research_run/plans/060-01.b1.g1_quiet-day-next-fade_1d.md`
Record: `steps_cards/04_backtest/a4_research_run/backtests/060-01.b1.g1_quiet-day-next-fade_1d`
Measure: `measure.py`
