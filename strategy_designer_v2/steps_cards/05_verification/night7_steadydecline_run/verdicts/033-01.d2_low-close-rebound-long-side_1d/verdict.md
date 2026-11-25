---
plan: 033-01.d2_low-close-rebound-long-side_1d
idea: 033-01.d2_low-close-rebound-long-side
fit: adapted
status: confirmed
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on forecast, regime bars: 0.00117971; t, standard errors clustered by day: 2.06946 (threshold: confirm: slope > 0 with t >= 2 (and check passes); reject: slope < 0 with t <= -2)
- Supporting check: mean excess next-day return on regime bars with forecast >= 2, above 0: 0.00246233, passed: True
- Counts: regime bars: 8067, distinct days: 2177, forecast >= 2 regime bars: 5199
- Decided by: The slope is positive with t >= 2 and the mean excess next-day return on forecast >= 2 bars is above 0.
- Reading: Situation computed from prices as (close-low)/(high-low) < 0.5 (zero-range bars count as outside it), long side; the slope is a pooled OLS with intercept of excess next-day return on forecast over regime bars of all coins and windows, with day-clustered (CR1) standard errors; the coin's mean daily return is the mean of all its next-bar returns over all windows; the t of the forecast>=2 excess return in the reject rule is the ordinary t of the mean; counts are regime bars with a next-day return.
- Size: unusual move +0.25 % (t 1.76, the cases of one day together: 1442 days) per case over 1 bars, 0.055 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.37 %; 3902 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001089 on the check folds against +0.00118 on every fold
Plan: `steps_cards/03_test_plan/night7_steadydecline_run/plans/033-01.d2_low-close-rebound-long-side_1d.md`
Record: `steps_cards/04_backtest/night7_steadydecline_run/backtests/033-01.d2_low-close-rebound-long-side_1d`
Measure: `measure.py`
