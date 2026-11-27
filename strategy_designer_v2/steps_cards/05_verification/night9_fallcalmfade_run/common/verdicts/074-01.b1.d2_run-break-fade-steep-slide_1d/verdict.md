---
plan: 074-01.b1.d2_run-break-fade-steep-slide_1d
idea: 074-01.b1.d2_run-break-fade-steep-slide
fit: exact
status: confirmed
---
Situation check: 98 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess short return (return minus coin mean, sign flipped): 0.00436291; t of the mean, cases of the same day taken together: 2.13544 (threshold: confirm: mean > 0 with t >= 2 and check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean excess, larger-|forecast| half minus smaller half: 0.0015472, passed: True
- Counts: cases (bars with forecast < 0): 3191, days with cases: 843
- Decided by: The mean excess short return is above 0 with t >= 2 and the larger-minus-smaller forecast half difference is above 0.
- Reading: The situation is rebuilt from closes (60-day return = close[t]/close[t-60]-1 in %, below -10; an up close after two consecutive down closes) and checked only on active bars where 60 prior bars exist inside the window; the coin's mean daily return pools all its windows' next-day returns; cases are bars with forecast < 0 that have a next-day return in the same window; the day-clustered t sums deviations per UTC day with a G/(G-1) correction; the larger half is cases with absolute forecast above the median, the smaller half those at or below it.
- Size: unusual move +0.41 % (t 1.95, the cases of one day together: 813 days) per case over 1 bars, 0.078 of the coin's usual move (5.44 %); normal drift in its direction -0.13 %, total +0.28 %; 3088 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.d2_run-break-fade-steep-slide_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/common/backtests/074-01.b1.d2_run-break-fade-steep-slide_1d`
Measure: `measure.py`
