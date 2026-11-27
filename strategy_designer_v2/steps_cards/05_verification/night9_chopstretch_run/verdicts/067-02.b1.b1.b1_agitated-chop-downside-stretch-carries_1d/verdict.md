---
plan: 067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d
idea: 067-02.b1.b1.b1_agitated-chop-downside-stretch-carries
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: abs(forecast)-weighted mean short-direction 5-day excess return over the coin's mean: 0.0119778; t of the weighted mean, clustered by day: 0.64556 (threshold: confirm: > 0 with day-clustered t >= 2; reject: < 0 with t <= -2)
- Supporting check: size order: mean excess of larger half minus smaller half of abs(forecast): -0.00427398, passed: False
- Counts: cases: 133, distinct days: 93
- Decided by: The day-clustered t lies between -2 and 2.
- Reading: The profile is the regime 'unknown' and below-average a negative raw stretch; the coin's mean 5-day return is over its pooled non-overlapping grid of all windows; the larger half is abs(forecast) above the median (ties go to the smaller half), compared by unweighted means; the clustered t uses summed weighted deviations per UTC day with a G/(G-1) correction.
- Size: unusual move -0.13 % (t -0.19, the cases of one day together: 185 days) per case over 5 bars, -0.002 of the coin's usual move (10.60 %); normal drift in its direction -0.64 %, total -0.77 %; 225 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/067-02.b1.b1.b1_agitated-chop-downside-stretch-carries_1d`
Measure: `measure.py`
