---
plan: 067-02.b1_choppy-plain-month-fall-continues_1d
idea: 067-02.b1_choppy-plain-month-fall-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of -(forecast/10) x (7-bar return minus normal 7-bar drift), non-overlapping grid, forecast < 0: -0.0120588; t of the mean, cases of one day taken together: -1.5538 (threshold: confirm: mean > 0 with day-clustered t >= 2 on >= 30 case-days and check passing; reject: mean < 0 with t <= -2 on >= 30 case-days)
- Supporting check: deeper-fall half minus shallower half, mean short-direction excess move: 0.0242012, passed: True
- Counts: case-days: 211, cells: 633
- Decided by: The t lies between -2 and 2 on at least 30 case-days, meeting neither the confirm nor the reject rule.
- Reading: Choppy is recomputed as the 60-day close return in percent within [-10, +10] inside each window, falling back to the recorded regime 'mean_reversion' on bars without 60 prior bars in the window; the 30-day fall uses the recorded raw fall30 value (prices where missing); the coin's normal drift is the mean of all its non-overlapping 7-bar grid returns over all windows; the t clusters cases by UTC day (deviations summed per day, D/(D-1) correction); the deeper half is |forecast| above the median, the shallower half at or below it, compared on the unweighted short-direction excess move.
- Size: unusual move +1.13 % (t 2.08, the cases of one day together: 624 days) per case over 7 bars, 0.071 of the coin's usual move (14.34 %); normal drift in its direction -1.13 %, total -0.01 %; 1024 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/067-02.b1_choppy-plain-month-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/067-02.b1_choppy-plain-month-fall-continues_1d`
Measure: `measure.py`
