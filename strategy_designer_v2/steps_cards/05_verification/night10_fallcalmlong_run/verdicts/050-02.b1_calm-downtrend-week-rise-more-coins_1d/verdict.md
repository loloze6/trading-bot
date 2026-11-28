---
plan: 050-02.b1_calm-downtrend-week-rise-more-coins_1d
idea: 050-02.b1_calm-downtrend-week-rise-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-day move on forecast > 0 cases (non-overlapping grid): 0.00878316; t of the mean, cases of one day taken together: 2.14976 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: upper-minus-lower half (by coin's median forecast) mean unusual 3-day move: 0.00423143, passed: True
- Counts: distinct case days: 239, cases: 456
- Decided by: mean unusual 3-day move > 0 with t >= 2 and upper-minus-lower difference > 0.
- Reading: cases are grid bars (positions 0,3,6,... of each window) with forecast > 0 and a 3-bar return inside the window, the drift is the coin's mean grid 3-bar return over all its windows, the halves split each coin's case forecasts at their median with ties at the median put in the lower half, and the 30-day minimum is treated as 'not observable'.
- Size: unusual move +0.64 % (t 1.89, the cases of one day together: 341 days) per case over 3 bars, 0.077 of the coin's usual move (8.43 %); normal drift in its direction +0.34 %, total +0.99 %; 503 cases
- Direction check on the check half (2022 onward) (the years step 7 does not explore): agrees: main measure +0.007486 on the check half (2022 onward) against +0.008783 on every window
Plan: `steps_cards/03_test_plan/night10_fallcalmlong_run/plans/050-02.b1_calm-downtrend-week-rise-more-coins_1d.md`
Record: `steps_cards/04_backtest/night10_fallcalmlong_run/backtests/050-02.b1_calm-downtrend-week-rise-more-coins_1d`
Measure: `measure.py`
