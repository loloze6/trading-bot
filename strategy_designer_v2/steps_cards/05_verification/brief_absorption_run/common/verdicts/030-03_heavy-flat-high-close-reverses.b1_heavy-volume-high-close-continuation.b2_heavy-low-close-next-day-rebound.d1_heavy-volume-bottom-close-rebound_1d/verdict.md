---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, heavy-volume days: 0.00079908; OLS t of slope: 4.62263 (threshold: confirm: slope positive with t >= 2; reject: slope negative with t <= -2)
- Supporting check: mean next-day excess return, lowest-quarter minus other heavy days (Welch t >= 2): 0.00917786, passed: True
- Counts: heavy-volume days: 5690, lowest-quarter days: 1302, other heavy-volume days: 4388
- Decided by: Confirm: the slope is positive with t >= 2 and lowest-quarter days beat the other heavy days with Welch t >= 2.
- Reading: The volume ratio is recomputed inside each window as volume over the mean of the 20 prior bars, so active bars with fewer than 20 prior bars in their window are left out of the agreement; heavy-volume days are the bars with regime mean_reversion and a next-day return in the same window; the coin's mean daily return is over all its 1-day returns in all windows; the slope's t is the OLS slope over its standard error; the 'other heavy-volume days' are heavy days with loc_low post_pipeline_value below 8.4; the minimum counts make the result 'not observable' when not reached. Welch t = 4.164.
- Size: unusual move +0.70 % (t 2.31, the cases of one day together: 1120 days) per case over 1 bars, 0.131 of the coin's usual move (5.44 %); normal drift in its direction +0.14 %, total +0.84 %; 2649 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/common/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Measure: `measure.py`
