---
plan: 058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d
idea: 058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual next-day fall after the bounce (sign flipped, coin mean removed): 0.00509087; t of the mean, cases summed per day: 1.64812 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects)
- Supporting check: deeper minus shallower half mean unusual fall (split at median |forecast|): 0.00511963, passed: True
- Counts: cases: 804, distinct days: 412
- Decided by: Main t lies between -2 and 2.
- Reading: Cases are bars with forecast < 0 and a next close in the same window; the t is that of the per-day sums of deviations; the deeper half is |forecast| strictly above the median, ties going to the shallower half; the up day and prior fall come from prices or the recorded raw value, with the recorded regime used only where they cannot be computed (a window's first bars).
- Size: unusual move +0.72 % (t 2.05, the cases of one day together: 300 days) per case over 1 bars, 0.152 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.59 %; 570 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.g1.d1.d1_bounce-after-deep-3-day-fall_1d`
Measure: `measure.py`
