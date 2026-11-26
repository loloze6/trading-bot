---
plan: 060-01.d3_dry-up-without-bounce_1d
idea: 060-01.d3_dry-up-without-bounce
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean short-side excess 5-bar return on non-overlapping grid bars with forecast < 0: 0.00902821; t of the mean, cases summed per day: 1.11348 (threshold: confirm: mean > 0 with t >= 2 (and supporting check > 0); reject: mean < 0 with t <= -2)
- Supporting check: mean short-side excess return, |forecast| above median minus at/below median: 0.0177903, passed: True
- Counts: distinct days with cases: 191, short cases: 445
- Decided by: t lies between -2 and 2 (inconclusive rule).
- Reading: Cases are the bars at positions 0, 5, 10, ... of each window with forecast < 0 and a full 5-bar return inside the window; the coin's mean 5-day return is taken over the same grid of all its windows; t is the mean over its standard error with case deviations summed per UTC day; the 'larger half' is |forecast| strictly above the median and the 'smaller half' at or below it; the plan's 30-day minimum is applied as 'not observable' per the workflow rules.
- Size: unusual move +0.62 % (t 1.16, the cases of one day together: 419 days) per case over 5 bars, 0.057 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.03 %; 636 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-01.d3_dry-up-without-bounce_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-01.d3_dry-up-without-bounce_1d`
Measure: `measure.py`
