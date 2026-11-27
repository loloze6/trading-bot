---
plan: 067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues_1d
idea: 067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean signed excess 10-bar return, weighted by -forecast/10, short side: 0.00388165; t of the mean, cases of one day summed: 0.213153 (threshold: mean > 0 with t >= 2 (confirm), mean < 0 with t <= -2 (reject), on at least 30 distinct days)
- Supporting check: unweighted mean signed excess, largest-|forecast| half minus smallest half: -0.020866, passed: False
- Counts: distinct case days: 70, cases: 136
- Decided by: The main measure's t lies between -2 and 2 (or its sign disagrees with the mean's), meeting neither confirm nor reject.
- Reading: Situation bars are those with a negative 30-day return (recorded fall30 raw value, rebuilt from closes where missing) in the regime 'unknown' the profile leaves open, on the short side; grid bars are positions 0,10,20,... of each window with a close 10 bars later in the same window; the normal drift is the mean of all the coin's grid 10-bar returns over all its windows; the t sums the cases' deviations per UTC day (clustered standard error); the halves are the n//2 cases with the largest and smallest |forecast| (stable sort), the middle case left out when n is odd; the 30-distinct-day minimum gives 'not observable' when not reached.
- Size: unusual move +1.36 % (t 1.51, the cases of one day together: 227 days) per case over 10 bars, 0.055 of the coin's usual move (15.92 %); normal drift in its direction -1.30 %, total +0.07 %; 310 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-01.b1.g1.b1.d1.g1_agitated-chop-slide-continues_1d`
Measure: `measure.py`
