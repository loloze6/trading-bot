---
plan: 038-02_rising-market-range-scaled-continuation_1d
idea: 038-02_rising-market-range-scaled-continuation
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess 3-bar forward return on forecast (in-profile grid bars): 0.00112665; OLS t, standard errors clustered by day: 2.69776 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2 (t clustered by day))
- Supporting check: mean excess 3-bar return on grid bars with forecast > 0 is above 0: 0.00473694, passed: True
- Counts: grid bars with forecast > 0: 1273, in-profile grid bars: 2224, days of grid bars with forecast > 0: 487
- Decided by: The slope is positive with t >= 2, the mean excess return on forecast > 0 bars is above 0, with at least 100 such bars.
- Reading: In-profile bars are grid bars where the scaled_rise raw value is recorded, the regression has an intercept with CR1 day-clustered errors, the coin's mean 3-bar return is taken over all grid bars of all its windows, and the supporting check needs only a mean above 0 (no t), as written.
- Size: unusual move +0.35 % (t 1.01, the cases of one day together: 751 days) per case over 3 bars, 0.040 of the coin's usual move (7.96 %); normal drift in its direction +0.36 %, total +0.71 %; 1407 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0004698 on the check folds against +0.001127 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/038-02_rising-market-range-scaled-continuation_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/038-02_rising-market-range-scaled-continuation_1d`
Measure: `measure.py`
