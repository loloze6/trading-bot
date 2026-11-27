---
plan: 074-01.b1.d2_run-break-fade-steep-slide_1d
idea: 074-01.b1.d2_run-break-fade-steep-slide
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess short return (return minus coin mean, sign flipped): 0.00850753; t of the mean, cases of the same day taken together: 1.93657 (threshold: confirm: mean > 0 with t >= 2 and check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess, larger-|forecast| half minus smaller half: -0.00375015, passed: False
- Counts: cases (bars with forecast < 0): 58, days with cases: 48
- Decided by: Only 58 cases (bars with forecast < 0) across the coins, below the plan's minimum of 100.
- Reading: The situation is rebuilt from closes (60-day return = close[t]/close[t-60]-1 in %, below -10; an up close after two consecutive down closes) and checked only on active bars where 60 prior bars exist inside the window; the coin's mean daily return pools all its windows' next-day returns; cases are bars with forecast < 0 that have a next-day return in the same window; the day-clustered t sums deviations per UTC day with a G/(G-1) correction; the larger half is cases with absolute forecast above the median, the smaller half those at or below it.
- Size: unusual move +0.71 % (t 1.61, the cases of one day together: 45 days) per case over 1 bars, 0.084 of the coin's usual move (7.55 %); normal drift in its direction -1.03 %, total -0.32 %; 54 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d2_run-break-fade-steep-slide_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/unseen_2016_2017/backtests/074-01.b1.d2_run-break-fade-steep-slide_1d`
Measure: `measure.py`
