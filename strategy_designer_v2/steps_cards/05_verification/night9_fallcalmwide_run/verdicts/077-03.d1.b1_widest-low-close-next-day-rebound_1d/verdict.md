---
plan: 077-03.d1.b1_widest-low-close-next-day-rebound_1d
idea: 077-03.d1.b1_widest-low-close-next-day-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess next-day return on long bars (minus coin's all-window mean daily return): 0.0043688; t of the mean over day sums: 0.771245 (threshold: confirm: mean > 0 with t >= 2 and upper-minus-lower > 0; reject: mean < 0 with t <= -2)
- Supporting check: upper-half minus lower-half mean excess return at the median forecast (Welch t n/a): None, passed: None
- Counts: cases: 96, independent days: 78
- Decided by: The t lies between -2 and 2 (or its sign disagrees with the mean), which the plan calls inconclusive.
- Reading: Cases are bars with postRebalance_current_allocation > 0 and a next close in the same window; the mean is over cases and the t over day sums of the excess; the median split puts forecasts above the median in the upper half and the rest in the lower; the profile is read from `regime` since its 365-bar inputs are not in the record, the low close and width are recomputed from prices.
- Size: unusual move +0.67 % (t 1.16, the cases of one day together: 80 days) per case over 1 bars, 0.133 of the coin's usual move (5.33 %); normal drift in its direction +0.13 %, total +0.80 %; 98 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03.d1.b1_widest-low-close-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03.d1.b1_widest-low-close-next-day-rebound_1d`
Measure: `measure.py`
