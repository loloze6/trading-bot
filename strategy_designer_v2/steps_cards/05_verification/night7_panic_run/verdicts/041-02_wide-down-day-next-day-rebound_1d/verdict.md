---
plan: 041-02_wide-down-day-next-day-rebound_1d
idea: 041-02_wide-down-day-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next-day excess return on the range_swing forecast: 5.82579; OLS slope t: 5.82579 (threshold: confirm if slope t >= +2 (with mean excess > 0); reject if slope t <= -2)
- Supporting check: mean next-day excess return over the cases: 0.00161435, passed: True
- Counts: cases: 8513
- Decided by: The slope's t is >= +2 and the mean next-day excess return over the cases is > 0.
- Reading: The first bar of each window has no recorded prior close, so its down close is read from the recorded regime; the coin's mean daily return is the mean of all its within-window 1-bar close-to-close returns over all windows; every forecast>0 bar with a next close in the same window is a case, pooled across coins in one OLS of next-day excess return on post_pipeline_value, slope t = slope / its standard error; fewer than 300 cases gives 'not observable' as the workflow requires for unmet minimum counts.
- Size: unusual move +0.17 % (t 1.43, the cases of one day together: 1819 days) per case over 1 bars, 0.036 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.29 %; 6170 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +3.381 on the check folds against +5.826 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/041-02_wide-down-day-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/041-02_wide-down-day-next-day-rebound_1d`
Measure: `measure.py`
