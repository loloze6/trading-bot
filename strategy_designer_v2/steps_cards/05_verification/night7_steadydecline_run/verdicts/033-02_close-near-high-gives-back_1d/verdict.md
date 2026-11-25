---
plan: 033-02_close-near-high-gives-back_1d
idea: 033-02_close-near-high-gives-back
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day return minus coin mean on close location: -0.00625462; t clustered by day: -2.60742 (threshold: confirm: slope < 0 with t <= -2 (and top-fifth mean < 0); reject: slope > 0 with t >= +2)
- Supporting check: mean next-day return minus coin mean, close location >= 0.8: -0.0021413, passed: True
- Counts: distinct days of cases: 2898, bars in the top fifth: 3739, cases: 17380
- Decided by: The slope is negative with t <= -2 and the top-fifth mean is below 0 (confirm rule).
- Reading: Every bar is a case (1-bar horizon, so non-overlapping); the slope's t uses standard errors clustered by UTC day (residual x centred location summed per day, G/(G-1) correction); the situation holds where close location > 0, on the short side.
- Size: unusual move +0.16 % (t 1.57, the cases of one day together: 2032 days) per case over 1 bars, 0.034 of the coin's usual move (4.78 %); normal drift in its direction -0.12 %, total +0.04 %; 7119 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure -0.001101 on the check folds against -0.006255 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/033-02_close-near-high-gives-back_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-02_close-near-high-gives-back_1d`
Measure: `measure.py`
