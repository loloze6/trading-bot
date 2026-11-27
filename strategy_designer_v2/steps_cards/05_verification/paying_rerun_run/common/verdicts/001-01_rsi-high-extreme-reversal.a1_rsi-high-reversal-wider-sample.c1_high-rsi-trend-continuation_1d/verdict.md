---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess return on forecast: 0.00300311; OLS slope t: 7.70294 (threshold: confirm if slope t >= 2 and positive-60d slope > other slope; reject if t <= -2)
- Supporting check: slope on positive-60d cases minus slope on other cases: 0.000932187, passed: True
- Counts: cases: 5423, cases with forecast > 0: 2438, cases with positive 60-day return: 1223, cases with non-positive 60-day return: 1428
- Decided by: The main slope's t is 2 or more and the slope on positive-60-day cases exceeds the slope on the other cases.
- Reading: Cases are grid bars 0,10,20,... of each window with close[t+10] inside the window, the coin's mean 10-bar return is the mean over that coin's grid cases in all windows, the slope t is the ordinary OLS t (with intercept), the 'other' group is cases with a 60-day return <= 0, the 30-case minimum is counted on all cases of each group, and minimum counts not reached give 'not observable'.
- Size: unusual move +1.01 % (t 1.42, the cases of one day together: 1162 days) per case over 10 bars, 0.052 of the coin's usual move (16.74 %); normal drift in its direction +1.47 %, total +2.48 %; 3129 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d`
Measure: `measure.py`
