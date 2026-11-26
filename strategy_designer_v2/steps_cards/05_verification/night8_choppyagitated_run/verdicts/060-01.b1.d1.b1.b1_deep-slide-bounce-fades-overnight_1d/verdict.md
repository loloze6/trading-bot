---
plan: 060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight_1d
idea: 060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x next-day excess return, cases summed per day: 0.0190795; t of the mean of daily sums: 1.57805 (threshold: positive with t >= 2 confirms (with negative slope); negative with t <= -2 rejects)
- Supporting check: slope of next-day excess return on |forecast|: -0.000326275, passed: True
- Counts: cases: 1598, distinct days: 535
- Decided by: The main measure's t lies between -2 and 2 (neither confirm nor reject).
- Reading: Situation checked as a one-day close-to-close rise with the 5-day vol-scaled return at t-1 below 0 (recorded slide_depth raw value, recomputed from prices if missing) on the short side, over active bars where it can be computed (a window's first bar is left out), the code-added profile not being rechecked; cases are bars with forecast<0 and a next close in the same window, summed per UTC day before the mean and its t; the plan's minimum counts, when unmet, give 'not observable'.
- Size: unusual move +0.57 % (t 1.76, the cases of one day together: 382 days) per case over 1 bars, 0.118 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.43 %; 1069 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/backtests/060-01.b1.d1.b1.b1_deep-slide-bounce-fades-overnight_1d`
Measure: `measure.py`
