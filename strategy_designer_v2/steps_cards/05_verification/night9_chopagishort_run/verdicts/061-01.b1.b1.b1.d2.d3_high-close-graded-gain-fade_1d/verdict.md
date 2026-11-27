---
plan: 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade_1d
idea: 061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short bets (short direction), day-pooled t: 0.0190216; t of the mean, cases pooled by day: 2.45323 (threshold: confirm: mean > 0 with t >= 2 and supporting check > 0; reject: mean < 0 with t <= -2)
- Supporting check: mean unusual move, larger-short half minus smaller-short half: 0.0150785, passed: True
- Counts: cases on distinct days: 105, cases: 120
- Decided by: Mean unusual move positive with t >= 2 and the supporting check above 0 (confirm rule).
- Reading: Profile read as the recorded regime not being 'chop'; a case is the first short bet in each 5-bar grid cell of a window; the day-pooled t sums deviations per signal day with a G/(G-1) correction; the larger-short half is |forecast| above the median, the smaller half at or below it; the plan's 'fewer than 30 cases on distinct days' is applied as the minimum count.
- Size: unusual move +1.90 % (t 2.46, the cases of one day together: 105 days) per case over 5 bars, 0.168 of the coin's usual move (11.68 %); normal drift in its direction -0.67 %, total +1.23 %; 120 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (79 cases, 79 days)
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d3_high-close-graded-gain-fade_1d`
Measure: `measure.py`
