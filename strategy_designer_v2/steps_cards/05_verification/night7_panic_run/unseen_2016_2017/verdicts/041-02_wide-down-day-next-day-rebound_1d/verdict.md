---
plan: 041-02_wide-down-day-next-day-rebound_1d
idea: 041-02_wide-down-day-next-day-rebound
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on the range_swing forecast: 3.0599; OLS slope t: 3.0599 (threshold: confirm if slope t >= +2 (with mean excess > 0); reject if slope t <= -2)
- Supporting check: mean next-day excess return over the cases: -0.00211982, passed: False
- Counts: cases: 1377
- Decided by: The slope's t is >= +2 but the mean next-day excess return is <= 0, which the plan calls inconclusive.
- Reading: The first bar of each window has no recorded prior close, so its down close is read from the recorded regime; the coin's mean daily return is the mean of all its within-window 1-bar close-to-close returns over all windows; every forecast>0 bar with a next close in the same window is a case, pooled across coins in one OLS of next-day excess return on post_pipeline_value, slope t = slope / its standard error; fewer than 300 cases gives 'not observable' as the workflow requires for unmet minimum counts.
- Size: unusual move -0.18 % (t -0.62, the cases of one day together: 497 days) per case over 1 bars, -0.020 of the coin's usual move (7.55 %); normal drift in its direction +0.96 %, total +0.78 %; 971 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/041-02_wide-down-day-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/unseen_2016_2017/backtests/041-02_wide-down-day-next-day-rebound_1d`
Measure: `measure.py`
