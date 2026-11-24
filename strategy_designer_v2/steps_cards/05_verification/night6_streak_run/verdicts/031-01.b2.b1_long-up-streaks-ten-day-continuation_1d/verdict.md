---
plan: 031-01.b2.b1_long-up-streaks-ten-day-continuation_1d
idea: 031-01.b2.b1_long-up-streaks-ten-day-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 10-day excess return (over coin drift) on forecast, pooled non-overlapping grid: 0.00291212; OLS slope t: 3.10748 (threshold: confirm: slope t >= 2 with top-fifth difference > 0; reject: slope t <= -2; otherwise inconclusive)
- Supporting check: mean excess return of top fifth of positive-forecast cases minus rest of positive-forecast cases: 0.0439424, passed: True
- Counts: grid cases: 1646, grid cases with forecast above 0: 807, top fifth: 161
- Decided by: Slope t is 2 or more and the top-fifth minus rest difference is above 0 (confirm rule).
- Reading: Drift is each coin's mean 10-bar return over its grid cases in all windows, the slope comes from an OLS with intercept on all grid cases, and the top fifth is the round(n/5) highest-forecast positive cases (ties kept in time order).
- Size: unusual move -0.21 % (t -0.34, the cases of one day together: 596 days) per case over 10 bars, -0.017 of the coin's usual move (14.49 %); normal drift in its direction +1.33 %, total +1.13 %; 1627 cases
Plan: `steps_cards/03_test_plan/night6_streak_run/plans/031-01.b2.b1_long-up-streaks-ten-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night6_streak_run/backtests/031-01.b2.b1_long-up-streaks-ten-day-continuation_1d`
Measure: `measure.py`
