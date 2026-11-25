---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess return on forecast: 0.00273402; OLS slope t: 3.95104 (threshold: confirm if slope t >= 2 and positive-60d slope > other slope; reject if t <= -2)
- Supporting check: slope on positive-60d cases minus slope on other cases: -0.00342354, passed: False
- Counts: cases: 1907, cases with forecast > 0: 890, cases with positive 60-day return: 484, cases with non-positive 60-day return: 451
- Decided by: The main slope's t is 2 or more but the supporting check failed (positive-60-day slope not larger), which the plan calls inconclusive.
- Reading: Cases are grid bars 0,10,20,... of each window with close[t+10] inside the window, the coin's mean 10-bar return is the mean over that coin's grid cases in all windows, the slope t is the ordinary OLS t (with intercept), the 'other' group is cases with a 60-day return <= 0, the 30-case minimum is counted on all cases of each group, and minimum counts not reached give 'not observable'.
- Size: unusual move +1.31 % (t 1.34, the cases of one day together: 555 days) per case over 10 bars, 0.067 of the coin's usual move (16.96 %); normal drift in its direction +1.80 %, total +3.11 %; 1118 cases
Plan: `steps_cards/03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/unseen_coins/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d`
Measure: `measure.py`
