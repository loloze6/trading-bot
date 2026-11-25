---
plan: 032-02.b2.g1_close-location-next-day-reversal_1d
idea: 032-02.b2.g1_close-location-next-day-reversal
fit: exact
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of next-day return minus coin mean on forecast: 0.000604317; OLS t of the slope: 4.75869 (threshold: confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2)
- Supporting check: mean daily timing gain (position gain minus drift): 0.000211799, passed: True
- Counts: bars with a non-zero forecast: 17380, bars in the regression: 17380
- Decided by: The slope is positive with t >= 2 and the timing gain is above 0 (confirm rule).
- Reading: The situation 'close lower in the range' is read as the raw location (high-close)/(high-low) above its mean over the last 60 recorded bars of the window (bar left out, at least 20; mid-range 0.5 before that), the expected side long there and short below; the slope is an OLS with intercept on every bar with a next-day return in its window (zero forecasts included), the minimum count is the non-zero-forecast bars of that sample, and the book's day is the mean over coins of each bar's position gain minus drift.
- Size: unusual move +0.22 % (t 2.46, the cases of one day together: 2539 days) per case over 1 bars, 0.049 of the coin's usual move (4.78 %); normal drift in its direction -0.00 %, total +0.22 %; 7862 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001024 on the check folds against +0.0006043 on every fold
Plan: `steps_cards/03_test_plan/night7c_panic_run/plans/032-02.b2.g1_close-location-next-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night7c_panic_run/backtests/032-02.b2.g1_close-location-next-day-reversal_1d`
Measure: `measure.py`
