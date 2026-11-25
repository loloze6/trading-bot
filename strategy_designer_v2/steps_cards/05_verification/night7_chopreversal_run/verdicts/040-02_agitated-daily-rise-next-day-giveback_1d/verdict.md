---
plan: 040-02_agitated-daily-rise-next-day-giveback_1d
idea: 040-02_agitated-daily-rise-next-day-giveback
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess gain (position x next-day excess return) on short bars, summed per day: 0.00207194; t of the mean over days: 1.32864 (threshold: confirm: mean > 0 with t >= 2 and slope > 0; reject: mean < 0 with t <= -2)
- Supporting check: slope of next-day excess return on forecast: -9.28364e-05, passed: False
- Counts: distinct days with a short case: 1517, short cases: 3955
- Decided by: t between -2 and 2 (inconclusive rule).
- Reading: The agitated profile is read as the recorded regime not being 'chop' (the detector's veto), the rise as the recorded raw day change > 0 (recomputed from closes if missing), the 100 distinct days are days with a measurable short case, and the slope is pooled over all short cases (not day sums).
- Size: unusual move +0.38 % (t 2.26, the cases of one day together: 1138 days) per case over 1 bars, 0.085 of the coin's usual move (4.73 %); normal drift in its direction -0.13 %, total +0.25 %; 2566 cases
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/040-02_agitated-daily-rise-next-day-giveback_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/040-02_agitated-daily-rise-next-day-giveback_1d`
Measure: `measure.py`
