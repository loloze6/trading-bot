---
plan: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d
idea: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: day-clustered t of the slope of 2-day forward return minus normal drift on forecast (forecast > 0, non-overlapping 2-bar grid): 1.27878; day-clustered t of the OLS slope: 1.27878 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 cases over at least 50 days)
- Supporting check: none
- Counts: cases with forecast > 0: 8995, distinct days: 1230
- Decided by: The slope's day-clustered t lies between -2 and 2 (inconclusive rule).
- Reading: OLS with intercept of excess 2-day return on forecast over grid bars (positions 0, 2, 4, ... of each window with a forward close in the window) with forecast > 0, the normal drift being the coin's mean 2-day return over all its windows' grid bars, day-clustered standard errors with the usual CR1 small-sample correction, and the plan's too-few-cases case reported as 'not observable' as the workflow requires.
- Size: unusual move +0.08 % (t 0.42, the cases of one day together: 1909 days) per case over 2 bars, 0.010 of the coin's usual move (7.48 %); normal drift in its direction +0.30 %, total +0.37 %; 10820 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d`
Measure: `measure.py`
