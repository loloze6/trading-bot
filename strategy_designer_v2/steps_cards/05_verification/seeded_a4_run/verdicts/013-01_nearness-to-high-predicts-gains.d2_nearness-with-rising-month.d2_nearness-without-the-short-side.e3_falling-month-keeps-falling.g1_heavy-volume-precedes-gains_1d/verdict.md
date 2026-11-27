---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of coin-demeaned 3-bar forward return on forecast (non-overlapping grid, pooled): 0.00243206; OLS slope t: 5.19886 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; otherwise inconclusive; at least 300 non-overlapping cases)
- Supporting check: none
- Counts: non-overlapping cases: 5920, active bars: 18138
- Decided by: The slope is positive with t = 5.20 >= 2 over 5920 cases (confirm rule).
- Reading: The coin's mean 3-bar return is taken over that coin's non-overlapping grid samples pooled over all its windows, the regression is OLS with an intercept, the 300-case minimum counts the pooled grid cases with a forecast and a return, and the situation check rebuilds standardise from raw values where the full 60-bar history is inside the window and uses the recorded post-pipeline values before that.
- Size: unusual move +0.66 % (t 3.46, the cases of one day together: 2094 days) per case over 3 bars, 0.066 of the coin's usual move (9.93 %); normal drift in its direction -0.03 %, total +0.63 %; 3694 cases
- Direction check on the check half (2022 onward) (the years step 7 does not explore): agrees: main measure +0.002076 on the check half (2022 onward) against +0.002432 on every window
Plan: `steps_cards/03_test_plan/seeded_a4_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d.md`
Record: `steps_cards/04_backtest/seeded_a4_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.g1_heavy-volume-precedes-gains_1d`
Measure: `measure.py`
