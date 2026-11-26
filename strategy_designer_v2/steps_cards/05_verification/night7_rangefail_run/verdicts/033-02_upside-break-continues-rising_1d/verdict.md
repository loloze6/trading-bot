---
plan: 033-02_upside-break-continues-rising_1d
idea: 033-02_upside-break-continues-rising
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move per long bet (return minus coin's normal 5-bar drift): 0.017468; t of the mean, cases pooled by day: 2.04949 (threshold: confirm: mean > 0 with day-pooled t >= 2 and graded-size check passes; reject: mean < 0 with t <= -2)
- Supporting check: graded size: mean unusual move of cases with forecast above the cases' median minus that at or below: 0.0390207, passed: True
- Counts: distinct case days: 284, cases: 387
- Decided by: The mean unusual move is above 0 with t >= 2 and the graded-size check passes.
- Reading: Bets are rises of the positive forecast of at least 2 points from its lowest level since the last bet (reset to 0 when flat), the first bet in each 5-bar cell counted from each window's first row; the normal drift is the mean of each coin's non-overlapping 5-bar returns on that grid over all windows; the t sums deviations per signal day (UTC date) with a D/(D-1) correction; the plan's 'fewer than 30 distinct case days' is applied as a minimum count, giving 'not observable'.
- Size: unusual move +1.75 % (t 2.05, the cases of one day together: 284 days) per case over 5 bars, 0.139 of the coin's usual move (10.60 %); normal drift in its direction +0.60 %, total +2.34 %; 387 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01427 on the check folds against +0.01747 on every fold
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-02_upside-break-continues-rising_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-02_upside-break-continues-rising_1d`
Measure: `measure.py`
