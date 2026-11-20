---
plan: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d
idea: 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of 10-bar excess return on forecast: 0.00197932; OLS slope t: 3.4778 (threshold: confirm if slope t >= 2 and positive-60d slope > other slope; reject if t <= -2)
- Supporting check: slope on positive-60d cases minus slope on other cases: 0.000800793, passed: True
- Counts: cases: 1691, cases with forecast > 0: 808, cases with positive 60-day return: 423, cases with non-positive 60-day return: 404
- Decided by: The main slope's t is 2 or more and the slope on positive-60-day cases exceeds the slope on the other cases.
- Reading: Cases are grid bars 0,10,20,... of each window with close[t+10] inside the window, the coin's mean 10-bar return is the mean over that coin's grid cases in all windows, the slope t is the ordinary OLS t (with intercept), the 'other' group is cases with a 60-day return <= 0, the 30-case minimum is counted on all cases of each group, and minimum counts not reached give 'not observable'.
- Size: unusual move +0.54 % per case over 10 bars, 0.027 of the coin's usual move (14.49 %); normal drift in its direction +1.17 %, total +1.70 %; 1011 cases
Plan: `steps_cards/03_test_plan/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d.md`
Record: `steps_cards/04_backtest/backtests/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d`
Measure: `measure.py`
