---
plan: 064-02_choppy-range-top-break-continuation_1d
idea: 064-02_choppy-range-top-break-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar unusual move per case (return from signal close minus coin's normal 5-bar drift): 0.0238568; t of the mean, cases of one day pooled: 1.26823 (threshold: mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: OLS slope of the 5-bar unusual move on the signal-bar forecast, t >= 2: 5.74181, passed: True
- Counts: cases: 245, distinct days: 187
- Decided by: The day-pooled t of the mean unusual move lies between -2 and 2.
- Reading: The situation check uses the recorded brk raw value (> 0, long) and the recomputed distance where it is missing, and leaves out the code-added choppy profile; a case is the first bet of each 5-bar grid cell from each window's first row, the day-pooled t uses the per-day sums of deviations with a G/(G-1) correction, and the supporting t is the ordinary OLS slope t.
- Size: unusual move +2.39 % (t 1.27, the cases of one day together: 187 days) per case over 5 bars, 0.088 of the coin's usual move (12.35 %); normal drift in its direction +0.81 %, total +3.20 %; 245 cases
Plan: `steps_cards/03_test_plan/night9_chopmonth_run/plans/064-02_choppy-range-top-break-continuation_1d.md`
Record: `steps_cards/04_backtest/night9_chopmonth_run/backtests/064-02_choppy-range-top-break-continuation_1d`
Measure: `measure.py`
